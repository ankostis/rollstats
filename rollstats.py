#!/usr/bin/env python
"""
From: https://jonisalonen.com/2014/efficient-and-accurate-rolling-standard-deviation/

## SYNTAX:

    rollstats.py <wsize> <prior_avg> <prior_stdev> [num] ...

## Sample run:

```bash
./rollstats.py 3 10 0  10 10 10 12 14 12 16 20 12 17 35 10 10 10 10
0: 10 --> 0.00
1: 12 --> 1.15
2: 14 --> 2.00
3: 12 --> 2.00
4: 16 --> 3.06
5: 20 --> 5.03
6: 12 --> 5.29
7: 17 --> 3.61
8: 35 --> 12.90
9: 10 --> 14.43
10: 10 --> 0.00
11: 10 --> 0.00
```
"""
#%%
from typing import Final
from math import sqrt

# %%
class RollingStats:
    def __init__(self, window_size, avg, variance):
        self.WSIZE: Final[int] = window_size
        self.avg = avg
        self.variance = variance

    @property
    def stdev(self):
        # Break from recipe!!
        # If no `abs()`, sqrt screams about ValueError: math domain error
        return sqrt(abs(self.variance))

    def update(self, x_inp, x_out):
        dval = x_inp - x_out
        oldavg = self.avg
        self.avg = newavg = self.avg + dval / self.WSIZE
        self.variance += dval * (x_inp - newavg + x_out - oldavg) / (self.WSIZE - 1)

    def roll_stats(self, *items: int):
        for i in range(len(items) - self.WSIZE):
            x_out = items[i]
            x_inp = items[i + self.WSIZE - 1]
            self.update(x_inp, x_out)
            yield f"{i}: {x_inp} --> {self.stdev:.2f}"

#%%
def main(wsize, prior_avg, prior_stdev, *items):
    l = [wsize, prior_avg, prior_stdev, *items]
    wsize, prior_avg, prior_stdev, *items = [int(i) for i in l]
    rs = RollingStats(wsize, prior_avg, prior_stdev)
    print("\n".join(rs.roll_stats(*items)))


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])

#%%
# Sample run

# main(3, 10, 0, 10, 10, 10, 12, 14, 12, 16, 20, 12, 17, 35, 10, 10, 10, 10)
