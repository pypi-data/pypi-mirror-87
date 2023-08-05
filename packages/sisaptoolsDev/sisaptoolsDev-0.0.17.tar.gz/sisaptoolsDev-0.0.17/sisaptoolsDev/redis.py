# -*- coding: utf8 -*-

"""
Eines per a la connexió a Redis.
"""

import random

from .constants import APP_CHARSET, IS_PYTHON_3
from .services import REDIS_INSTANCES


class StreamArray(list):
    def __init__(self, gen, *args):
        self.gen = gen
        self.args = args

    def __iter__(self):
        return self.gen(*self.args)

    def __len__(self):
        return 1


class Redis():
    """
    Modificació de StrictRedis per poder instanciar de
    forma transparent segons la versió de l'intèrpret.
    """

    def __init__(self, *args):
        pass

    def pipeline(self):
        return self

    def execute(self):
        pass

    def sadd(self, *args):
        pass

    def hset(self, *args):
        pass

    def hincrby(self, *args):
        pass

    def delete(self, *args):
        pass

    def keys(self, *args):
        def _gen():
            r = random.randint(0, 100)
            while r >= 5:
                r = random.randint(0, 100)
                yield (str(random.randint(1, 10)) + ":" +
                       str(random.randint(1, 5000)) + ":" +
                       str(random.choice(["v", "d", "tp", "e", "ep", "t", "u"])))

        return StreamArray(_gen)

    def hgetall(self, *args):
        def _gen():
            r = random.randint(0, 100)
            while r >= 5:
                r = random.randint(0, 100)
                yield {random.randint(1, 10): random.randint(0, 3000)}

        return StreamArray(_gen)

    def set(self, *args):
        pass

    def smembers(self, *args):
        def _gen():
            r = random.randint(0, 100)
            while r >= 5:
                r = random.randint(0, 100)
                yield (str(random.randint(1, 10)) + ":" +
                       str(random.randint(1, 5000)) + ":" +
                       str(random.choice(["v", "d", "tp", "e", "ep", "t", "u"])))

        return StreamArray(_gen)

    def get(self, *args):
        def _gen():
            r = random.randint(0, 100)
            while r >= 5:
                r = random.randint(0, 100)
                yield (str(random.randint(1, 10)) + ":" +
                       str(random.randint(1, 5000)) + ":" +
                       str(random.choice(["v", "d", "tp", "e", "ep", "t", "u"])))

        return StreamArray(_gen)

    def scard(self, *args):
        def _gen():
            r = random.randint(0, 100)
            while r >= 5:
                r = random.randint(0, 100)
                yield (str(random.randint(1, 10)) + ":" +
                       str(random.randint(1, 5000)) + ":" +
                       str(random.choice(["v", "d", "tp", "e", "ep", "t", "u"])))

        return StreamArray(_gen)
