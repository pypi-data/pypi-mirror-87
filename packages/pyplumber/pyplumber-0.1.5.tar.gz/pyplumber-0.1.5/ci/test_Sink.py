from time import sleep
from pyplumber import Sink


def echo(arg):
    return arg


def setup():
    return "test", Sink()


def test_reprs():
    _, sink = setup()
    print(sink.__repr__())
    print(sink.__str__())
    assert sink.__str__() == sink.__repr__()


def test_int():
    key, sink = setup()
    # Integer
    inp = 1
    sink.set(key, inp)
    ans = sink.get(key)
    assert isinstance(ans, str)
    assert str(inp) == ans


def test_float():
    key, sink = setup()
    # Float
    inp = 1.23
    sink.set(key, inp)
    ans = sink.get(key)
    assert isinstance(ans, str)
    assert str(inp) == ans


def test_str():
    key, sink = setup()
    # String
    inp = "Test"
    sink.set(key, inp)
    ans = sink.get(key)
    assert isinstance(ans, str)
    assert str(inp) == ans


def test_bytes():
    key, sink = setup()
    # Bytes
    inp = b"Test"
    sink.set(key, inp)
    ans = sink.get(key)
    assert isinstance(ans, str)
    assert inp.decode() == ans


def test_func():
    key, sink = setup()
    # Function
    inp = echo
    sink.set(key, inp)
    ans = sink.get(key)
    assert ans(123) == 123


def test_generator():
    key, sink = setup()
    inp = (num ** 2 for num in range(5))
    try:
        sink.set(key, inp)
        raise Exception("Could pickle a generator and shouldn't")
    except:
        return


def test_unpickle_fail():
    import pickle

    _, sink = setup()
    try:
        sink._deserialize(b"\x80\x04}q\x00X\x01\x10\x00\x00aj\x01K{s.")
        raise Exception("Could unpickle corrupted data and shouldn't")
    except:
        return


def test_deserialize_int():
    _, sink = setup()
    assert sink._serialize(1) == 1
    assert sink._deserialize(1) == 1


def test_deserialize_bool():
    _, sink = setup()
    sink.set("test", True)
    assert sink.get("test")
    sink.set("test", False)
    assert not sink.get("test")


def test_force_dill():
    _, sink = setup()
    inp = compile("", "", "exec")
    enc = sink._serialize(inp)
    assert sink._deserialize(enc) == inp
