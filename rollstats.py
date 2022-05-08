#!/usr/bin/env python
"""
Rolling avg, stdev, starting with an empty OR a pre-filled circular-buffer.

# SYNTAX:
    rollstats.py <wsize> [num] ...

# Sample run:

```bash
./rollstats.py 3  10 10 10 12 14 12 16 20 12 17 35 10 10 10 10
0: 10 --> 10.00 ± 0.00
1: 10 --> 10.00 ± 0.00
2: 10 --> 10.00 ± 0.00
3: 12 --> 10.67 ± 1.15
4: 14 --> 12.00 ± 2.00
5: 12 --> 12.67 ± 1.15
6: 16 --> 14.00 ± 2.00
7: 20 --> 16.00 ± 4.00
8: 12 --> 16.00 ± 4.00
9: 17 --> 16.33 ± 4.04
10: 35 --> 21.33 ± 12.10
11: 10 --> 20.67 ± 12.90
12: 10 --> 18.33 ± 14.43
13: 10 --> 10.00 ± 0.00
14: 10 --> 10.00 ± 0.00
```

- Adapted from:
  https://jonisalonen.com/2014/efficient-and-accurate-rolling-standard-deviation/
- Project home: https://github.com/ankostis/rollstats
"""
# %%
from typing import Union, Iterable
from numbers import Number
from math import sqrt

# %%


class RollingStats:
    __doc__ = __doc__
    #: index in `items` of the next item to pop-out and overwrite
    i: int = 0

    def __init__(self, wsize_or_items: Union[int, list[int]]):
        try:
            self.WSIZE = int(wsize_or_items)
            self.items = []
            self.avg = self.variance = 0
        except TypeError:
            from statistics import mean, stdev

            self.WSIZE = len(wsize_or_items)
            self.items = wsize_or_items
            self.avg = mean(self.items)
            self.variance = stdev(self.items) ** 2

    @property
    def stdev(self):
        # Break from recipe!!
        # If no `abs()`, sqrt screams about ValueError: math domain error
        return sqrt(abs(self.variance))

    def update(self, x_inp: Union[int, Number]):
        l = self.items
        N = self.WSIZE
        nitems = len(l)
        if nitems < N:
            l.append(x_inp)  # insertion repeated below
            if nitems == 0:
                self.avg = x_inp
                self.variance = 0
                return
            nitems += (nitems == 1)  # avoid DivBy0 below
        else:
            nitems = N
        i = self.i
        x_out, l[i] = l[i], x_inp
        self.i = (i + 1) % N

        dval = x_inp - x_out
        oldavg = self.avg
        self.avg = newavg = self.avg + dval / nitems
        self.variance += dval * \
            (x_inp - newavg + x_out - oldavg) / (nitems - 1)


# %%


def main(wsize, *items):
    wsize, *items = [float(i) for i in [wsize, *items]]
    rs = RollingStats(wsize)
    for i, x_inp in enumerate(items):
        rs.update(x_inp)
        print(f"{i}: {x_inp} --> {rs.avg:.2f} ± {rs.stdev:.2f}")


# %%
if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])

# %%
# Sample run auto-populate

# wsize = 3
# main(wsize, 10, 10, 10, 12, 14, 12, 16, 20, 12, 17, 35, 10, 10, 10, 10)

# %%
# Sample run with prepared list

# wsize = 3
# l = [10, 10, 10, 12, 14, 12, 16, 20, 12, 17, 35, 10, 10, 10, 10]
# rs = RollingStats(l[:wsize])
# items = l[wsize:]
# stats = rs.roll_stats(items)
# print("\n".join(
#     f"{i}: {x_inp} --> {avg:.2f} ± {stdev:.2f}"
#     for i, (x_inp, (avg, stdev)) in enumerate(zip(items, stats))))
