__all__ = ["Sink"]

import pickle
from typing import Union
import dill
import redis
from pyplumber.exceptions import SerializationError, DeserializationError


class Sink(redis.Redis):

    """
    The sink is where you dump all the
    data you want to be visible to the
    entire framework. You can use it as
    a key-value data structure using the
    "get" and "set" methods.

    This class inherits from redis.Redis
    and the only difference is that it
    handles serialization and deserialization
    of objects so you can set anything to
    a key.
    """

    def __repr__(self) -> str:

        """
        Representation of this Sink object
        """

        return "<PyPlumber Sink<pool={}>>".format(self.connection_pool)

    def __str__(self) -> str:

        """
        Representation of this Sink object
        """

        return self.__repr__()

    @classmethod
    def _serialize(cls, o: object) -> object:
        if isinstance(o, bool):
            return pickle.dumps(o)
        elif isinstance(o, (str, bytes, int, float)):
            return o
        else:
            try:
                return pickle.dumps(o)
            except:
                try:
                    return dill.dumps(o)
                except:
                    raise SerializationError("Failed to serialize object {}".format(o))

    @classmethod
    def _deserialize(cls, e: Union[str, int, float, bytes]) -> object:
        if isinstance(e, (str, int, float)):
            return e
        else:
            try:
                return e.decode()
            except UnicodeDecodeError:
                try:
                    return pickle.loads(e)
                except:
                    try:
                        return dill.loads(e)
                    except:
                        raise DeserializationError("Failed to deserialize {}".format(e))

    def set(self, key, value, *args, **kwargs):
        return super(Sink, self).set(
            name=key, value=self._serialize(value), *args, **kwargs
        )

    def get(self, key, *args, **kwargs):
        return self._deserialize(super(Sink, self).get(name=key, *args, **kwargs))
