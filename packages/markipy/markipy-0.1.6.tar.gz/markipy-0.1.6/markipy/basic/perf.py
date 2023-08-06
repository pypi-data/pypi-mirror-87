from dataclasses import dataclass
import pandas as pd
import time


@dataclass
class Measure:
    name: str = ''
    min: int = int(1e12)
    mean: int = 0
    total: int = 0
    max: int = 0
    last: int = 0
    count: int = 1

    def __str__(self):
        return f'{self.name}: {self.last * 1e-6} <{self.min * 1e-6},{self.mean * 1e-6},{self.max * 1e-6}> ms'

    def update(self, measure):
        if measure < self.min:
            self.min = measure
        elif measure > self.max:
            self.max = measure
        self.total += measure
        self.mean = int(self.total / self.count)
        self.last = measure
        self.count += 1

    def reset(self):
        self.count = 0
        self.total = 0


class Performance:
    stats = dict()
    _ms: int = int(1e-6)

    def __getitem__(self, key):
        return self.stats[key]

    def new(self, name, time):
        if name not in self.stats:
            self.stats[name] = Measure(name=name, min=time, mean=time, max=time, last=time)
        else:
            self.stats[name].update(time)

    def get(self, name):
        return str(self.stats[name])

    def collect(method):
        def measure(*args, **kw):
            self = args[0]
            ts = time.time_ns()
            result = method(*args, **kw)
            self.performance.new(method.__name__, time.time_ns() - ts)
            self.log.debug(self.grey(self.performance.get(method.__name__)))
            return result

        return measure
