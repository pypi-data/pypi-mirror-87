from pyplumber import Task, Plumber, Sink
from time import sleep
from threading import Thread
import random


def setup1():
    class Printer(Task):
        def execute(self):
            data = self.get("test")
            print(data)
            self.terminate()
            return data

    class Incrementer(Task):
        def setup(self):
            self._dict["delay"] = 1
            self._dict["data"] = 0

        def execute(self):
            data = int(self.get("test"))
            self.set("test", data + 1)

    class Starter(Task):
        def execute(self):
            self.set("test", 0)

    plumber = Plumber()

    start = plumber.add(Starter)
    inc = plumber.add(Incrementer, dependencies=[start])
    out = plumber.add(Printer, dependencies=[inc], output=True)

    return plumber


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
            if self._dict["counter"] > 4:
                self.terminate()
            return True

    plumber = Plumber()

    return plumber, Starter, RandomFailDude, EndAfterFour


def test_Watchdog_warn():
    plumber, Starter, RandomFailDude, EndAfterFour = setup2()
    starter = plumber.add(Starter)
    rf = plumber.add(RandomFailDude, dependencies=[starter], wdt_action="warn")
    end = plumber.add(EndAfterFour, dependencies=[rf], output=True)
    plumber.setup()
    plumber.start()
    assert isinstance(end.plumber, Plumber)
    assert isinstance(end.sink, Sink)
    for result in plumber.loop():
        print(result)
        for key in result.keys():
            assert result[key] == True


def test_Watchdog_restart():
    plumber, Starter, RandomFailDude, EndAfterFour = setup2()
    starter = plumber.add(Starter)
    rf = plumber.add(RandomFailDude, dependencies=[starter], wdt_action="restart")
    end = plumber.add(EndAfterFour, dependencies=[rf], output=True)
    plumber.setup()
    plumber.start()
    for result in plumber.loop():
        for key in result.keys():
            assert result[key] == True


def test_Watchdog_terminate():
    plumber, Starter, RandomFailDude, EndAfterFour = setup2()
    starter = plumber.add(Starter)
    rf = plumber.add(RandomFailDude, dependencies=[starter], wdt_action="terminate")
    end = plumber.add(EndAfterFour, dependencies=[rf], output=True)
    plumber.setup()
    plumber.start()
    for result in plumber.loop():
        for key in result.keys():
            assert result[key] == True


def test_Watchdog_unallowed_action():
    plumber, Starter, RandomFailDude, EndAfterFour = setup2()
    starter = plumber.add(Starter)
    try:
        rf = plumber.add(RandomFailDude, dependencies=[starter], wdt_action="oopsy")
        raise Exception
    except:
        pass


def test_Plumber_unallowed_adding():
    plumber, _, _, _ = setup2()
    try:
        rf = plumber.add(Thread, dependencies=[], wdt_action="oopsy")
        raise Exception
    except:
        pass


def test_Full():
    plumber = setup1()
    plumber.setup()
    plumber.start()
    for result in plumber.loop():
        for key in result:
            assert result[key] == "1"
    for result in plumber.loop():
        for key in result:
            assert result[key] == "1"


def test_PlumberPrinting():
    plumber = setup1()
    print(plumber.__str__())
    print(plumber.__repr__())
    print(plumber.name)
    plumber.print(file="out.png")
