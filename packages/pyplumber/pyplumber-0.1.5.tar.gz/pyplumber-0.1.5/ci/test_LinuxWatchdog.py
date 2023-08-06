from pyplumber import Task, Plumber, Sink
from time import sleep
from threading import Thread
import random


def setup2():
    class Starter(Task):
        def execute(self):
            self.set("test", 0)

    class RandomFailDude(Task):
        def execute(self):
            fail = random.choice([True, False])
            if fail:
                raise Exception
            return

    class EndAfterFour(Task):
        def setup(self):
            self._dict["counter"] = 0

        def execute(self):
            self._dict["counter"] += 1
            self.plumber.stop_watchdog()
            if self._dict["counter"] > 4:
                self.terminate()
            return True

    plumber = Plumber(use_linux_watchdog=True)

    return plumber, Starter, RandomFailDude, EndAfterFour


def test_LinuxWatchdog_terminate():
    plumber, Starter, RandomFailDude, EndAfterFour = setup2()
    starter = plumber.add(Starter)
    rf = plumber.add(RandomFailDude, dependencies=[starter], wdt_action="terminate")
    end = plumber.add(EndAfterFour, dependencies=[rf], output=True)
    plumber.setup()
    plumber.start()
    for result in plumber.loop():
        print(result)
        for key in result.keys():
            assert result[key] == True
