from time import sleep
from pyplumber import Task, Sink


def setup():
    class Tester(Task):
        def setup(self):
            super(Tester, self).setup()
            self._dict["counter"] = 0
            self.set("test", self._dict["counter"])

        def execute(self):
            super(Tester, self).execute()
            self.set("test", self._dict["counter"])

        def loop(self):
            super(Tester, self).loop()
            self._dict["counter"] += 1
            sleep(1)

    tester = Tester()
    sink = Sink()
    tester.setSink(sink)
    return tester


def test_setup():
    tester = setup()
    tester.setup()
    assert tester.get("test") == str(0)


def test_general_task():
    task = Task()
    print(task.__repr__())
    print(task.__str__())


def test_execute():
    tester = setup()
    tester.setup()
    tester.start()
    start_val = int(tester.get("test"))
    sleep(1)
    tester.execute()
    end_val = int(tester.get("test"))
    assert (end_val - start_val) == 1