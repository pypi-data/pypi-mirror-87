__all__ = ["Plumber"]

import logging
import string
import random
from copy import deepcopy
from functools import partial
from threading import Thread, Lock, Timer
import networkx as nx
from pyplumber.Sink import Sink
from pyplumber.Task import Task
from pyplumber.log import PlumberLogger
from pyplumber.exceptions import FatalError


class Plumber:

    """
    Plumber define how Daemons and Tasks
    interact with each other, handling
    dependencies, the execution flow and
    monitoring for timeouts.
    """

    # pylint: disable=too-many-instance-attributes

    ALLOWED_WDT_ACTIONS = ["terminate", "restart", "warn"]

    def __init__(
        self,
        level: int = logging.INFO,
        name: str = "",
        use_linux_watchdog: bool = False,
        maxAttempts: int = 5,
    ) -> None:

        """Inits Plumber.

        Args:
            level: the Logger level, default is logging.INFO.
            name: name of this Plumber object. If not specified,
                a random one shall be generated.
            use_linux_watchdog: boolean that enables integration
                with Linux watchdog on "/dev/watchdog" file.
            maxAttempts: sets max attempts on writing on watchdog
                file before it reboots the system.
        """
        self.__G = nx.DiGraph()
        self.__graphLock = Lock()
        self.__outputs = []
        self.__level = level
        self.__plumber = None
        self.__name = name if name != "" else "Plumber-{}".format(self._generateId())
        self.__running = True
        self.__out = {}
        self.__sink = Sink()
        self.__maxAttempts = maxAttempts
        self.__useLinuxWatchdog = use_linux_watchdog
        self.__sendKeepAlives = True
        self.__logger = PlumberLogger(level=level)

    def __repr__(self) -> str:

        """
        Representation of the Plumber object
        """

        return "<PyPlumber Plumber (name={})>".format(self.name)

    def __str__(self) -> str:

        """
        Representation of the Plumber object
        """

        return self.__repr__()

    @classmethod
    def _generateId(cls) -> str:
        return "".join(random.choice(string.ascii_letters) for x in range(10))

    @property
    def name(self) -> str:
        return self.__name

    @property
    def logger(self) -> PlumberLogger:
        return self.__logger

    def add(
        self,
        cls,
        args: tuple = None,
        kwargs: dict = None,
        dependencies: list = None,
        output: bool = False,
        wdt_enabled: bool = False,
        wdt_action: str = "terminate",
        wdt_timeout: float = 24 * 3600,
    ):
        args = args or ()
        kwargs = kwargs or {}
        dependencies = dependencies or []
        if wdt_action not in self.ALLOWED_WDT_ACTIONS:
            raise FatalError(
                "Watchdog action {} not in the following allowed actions: {}".format(
                    wdt_action, self.ALLOWED_WDT_ACTIONS
                )
            )
        obj = cls(*args, **kwargs)
        if not issubclass(type(obj), Task):
            self.logger.fatal("Accepted objects must inherit from Task")
        self.__graphLock.acquire()
        if obj.name not in self.__G:
            kw = deepcopy(kwargs)
            kw["name"] = obj.name
            self.__G.add_node(
                obj.name,
                cls=cls,
                args=args,
                kwargs=kw,
                obj=obj,
                wdt_enabled=wdt_enabled,
                wdt_action=wdt_action,
                wdt_timeout=wdt_timeout,
                timer=None,
                timer_started=False,
                executed=False,
            )
        if len(dependencies) > 0:
            for dep in dependencies:
                try:
                    if dep.name not in self.__G:
                        raise FatalError(
                            "Dependencies for a Task must be added to the Plumber before the task itself"
                        )
                except AttributeError:
                    raise FatalError("Dependencies must be already built objects")
                self.__G.add_edge(dep.name, obj.name)
        if output:
            self.__outputs.append(obj.name)
        self.__graphLock.release()
        return obj

    def setup(self) -> None:
        if self.__useLinuxWatchdog:
            thread = Thread(target=self.__wdt_thread, daemon=True)
            thread.start()
        self.__graphLock.acquire()
        for node in self.__G.nodes():
            self.__G.nodes[node]["obj"].setSink(self.__sink)
            self.__G.nodes[node]["obj"].setPlumber(self)
            self.__G.nodes[node]["obj"].setup()
        self.__graphLock.release()

    def stop_watchdog(self) -> None:
        from time import sleep

        self.__useLinuxWatchdog = False
        sleep(0.5)
        self.__wdt_stop()

    def start(self) -> None:
        self.__graphLock.acquire()
        for node in self.__G.nodes():
            self.__G.nodes[node]["obj"].start()
        self.__graphLock.release()

    def __wdtHandler(self, name: str) -> None:
        action = self.__G.nodes[name]["wdt_action"]
        if action == "restart":
            self.__graphLock.acquire()
            self.logger.warning(
                "Node {} has triggered the watchdog, restarting node...".format(name)
            )
            self.__G.nodes[name]["obj"].kill()
            self.__G.nodes[name]["obj"] = self.__G.nodes[name]["cls"](
                *self.__G.nodes[name]["args"], **self.__G.nodes[name]["kwargs"]
            )
            self.__G.nodes[name]["obj"].setup()
            self.__G.nodes[name]["obj"].start()
            self.__graphLock.release()
        elif action == "terminate":
            self.logger.fatal(
                "Node {} has triggered the watchdog, will terminate everything soon".format(
                    name
                )
            )
            self.__sendKeepAlives = False
            self.stop()
        elif action == "warn":
            self.logger.warning(
                "Node {} has triggered the watchdog! This is just a warning.".format(
                    name
                )
            )

    def startTimer(self, name: str) -> None:
        self.__graphLock.acquire()
        if not self.__G.nodes[name]["timer_started"]:
            self.__G.nodes[name]["timer"] = Timer(
                interval=self.__G.nodes[name]["wdt_timeout"],
                function=self.__wdtHandler,
                args=(name,),
            )
            self.__G.nodes[name]["timer"].daemon = True
            self.__G.nodes[name]["timer"].start()
            self.__G.nodes[name]["timer_started"] = True
        self.__graphLock.release()

    def cancelTimer(self, name: str) -> None:
        self.__graphLock.acquire()
        try:
            self.__G.nodes[name]["timer"].cancel()
            self.__G.nodes[name]["timer_started"] = False
        except AttributeError:
            self.logger.warning("Failed to cancel timer for node {}".format(name))
        self.__graphLock.release()

    def _appendToResult(self, node, result):
        self.__out[node] = result

    def clear(self):
        self.__graphLock.acquire()
        del self.__out
        self.__out = {}
        for node in self.__G.nodes:
            self.__G.nodes[node]["executed"] = False
        self.__graphLock.release()

    def forward(self, wait: bool = False) -> list:
        self.clear()
        for node in self.__outputs:
            self.logger.debug("--> Getting result from output node {}".format(node))
            thread = Thread(
                target=self.nodeResult,
                args=(node, True, partial(self._appendToResult, node)),
                daemon=True,
            )
            thread.start()
        while (
            wait
            and len(list(self.__out.keys())) < len(self.__outputs)
            and self.__running
        ):
            pass
        return self.__out

    def loop(self) -> None:
        while self.__running:
            yield self.forward(wait=True)

    def stop(self) -> None:
        self.__running = False
        for key in self.__G.nodes():
            self.__G.nodes[key]["obj"].kill()
        # raise SystemExit

    def nodeResult(
        self, node: str, output: bool = False, callback: callable = None
    ) -> None:
        # Check if it's been executed this time
        self.__graphLock.acquire()
        if self.__G.nodes[node]["executed"]:
            return
        self.__graphLock.release()
        # Get predecessors
        preds = list(self.__G.predecessors(node))
        self.logger.debug("--> Node {} predecessors: {}".format(node, preds))
        # No predecessors means root
        if len(preds) > 0:
            # Iterate over predecessors
            self.logger.debug("--> Will iterate over predecessors now")
            for pred in preds:
                self.logger.debug(
                    "--> Predecessor {} has no data, will call for nodeResult".format(
                        pred
                    )
                )
                self.nodeResult(pred)
            self.logger.debug(
                "--> Successfully executed dependencies for node {}".format(node)
            )
        # Get data from node
        self.logger.debug("--> Starting timer for node {}".format(node))
        self.startTimer(node)
        success = False
        while not success and self.__running:
            try:
                data = self.__G.nodes[node]["obj"].execute()
                success = True
            except:
                self.__wdtHandler(node)
        self.logger.debug("--> Canceling timer for node {}".format(node))
        self.cancelTimer(node)
        self.logger.debug("--> No predecessors, data is {}".format(data))
        if output and callback:
            callback(data)
        self.__graphLock.acquire()
        self.__G.nodes[node]["executed"] = True
        self.__graphLock.release()
        return

    def print(self, file=None) -> None:
        try:
            import matplotlib.pyplot as plt

            nx.draw_networkx(self.__G, with_labels=True)
            if not file:
                plt.show()
            else:
                plt.savefig(file)
        except ImportError:
            self.logger.error(
                'Plotting dependencies for pyPlumber are not installed on this environment. If you want to plot the dependency chart please install them with "pip install pyplumber[plot]"'
            )

    def __wdt_write(self, value, count=0):
        import os
        from time import sleep

        if count > 0:
            self.logger.warning(
                "This is attempt #{} to write on the WDT file".format(count)
            )

        if count >= self.__maxAttempts:
            self.logger.fatal(
                "Tried to write on WDT file too many times, rebooting in few seconds..."
            )
            sleep(5)
            os.system("reboot")
        # Default operation
        try:
            fd = os.open("/dev/watchdog", os.O_WRONLY | os.O_NOCTTY)
            f = open(fd, "wb+", buffering=0)
            f.write(value)
            f.close()
        except FileNotFoundError:
            self.logger.error(
                'WDT file "/dev/watchdog" does not exist. Will disable watchdog...'
            )
            self.__useLinuxWatchdog = False
        except OSError:
            self.logger.warning(
                "WDT file could not be opened, will retry in 1 second (count = {})".format(
                    count
                ),
            )
            sleep(1)
            self.__wdt_write(value, count + 1)

    def __wdt_keepalive(self):
        self.__wdt_write(b".")

    def __wdt_stop(self):
        self.__wdt_write(b"V")

    def __wdt_thread(self):
        from time import sleep

        while self.__useLinuxWatchdog:
            if self.__sendKeepAlives:
                self.__wdt_keepalive()
            else:
                self.logger.warning(
                    "Plumber has stopped sending watchdog keepalives..."
                )
                sleep(1)
