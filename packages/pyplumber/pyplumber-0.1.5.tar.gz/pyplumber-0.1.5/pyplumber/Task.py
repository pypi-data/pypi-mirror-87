__all__ = ["Task"]

from multiprocessing import Process, Manager
import abc
from pyplumber import Sink


class Task(Process):

    """
    Task is an abstract class that, when inherited,
    will represent a daemon task that runs indefinetely,
    providing data or performing a task when requested.

    One should implement the methods "setup", "loop" and
    "execute", which are the three main methods of this
    class. "setup" is executed once, "execute" is called
    on every pipeline loop and "loop" runs in background
    continuously.

    Data visible to the whole framework can be manipulated
    through "get" and "set" methods. Data visible to the
    object only can be manipulated through the object
    "self._dict".
    """

    def __init__(self, *args, **kwargs) -> None:
        super(Task, self).__init__(*args, **kwargs)
        self.daemon = True
        self.__manager = Manager()
        self.__sink = None
        self.__plumber = None
        self._dict = self.__manager.dict()

    def __repr__(self) -> str:

        """
        Representation of this Task object
        """

        return "<PyPlumber Task (name={}, alive={})>".format(self.name, self.is_alive())

    def __str__(self) -> str:

        """
        Representation of this Task object
        """

        return self.__repr__()

    @property
    def plumber(self):
        return self.__plumber

    @property
    def sink(self):
        return self.__sink

    @abc.abstractmethod
    def setup(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def loop(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        while True:
            self.loop(*args, **kwargs)

    def setSink(self, sink: Sink) -> None:
        self.__sink = sink

    def setPlumber(self, plumber) -> None:
        self.__plumber = plumber

    def terminate(self) -> None:
        self.__plumber.stop()

    def get(self, key, *args, **kwargs):
        return self.__sink.get(key, *args, **kwargs)

    def set(self, key, value, *args, **kwargs):
        return self.__sink.set(key, value, *args, **kwargs)
