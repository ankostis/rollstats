# Rollstats

Calculate rolling stdev in python.

Adapted from [The Mindful Programmer (jonisalonen)](https://jonisalonen.com/2014/efficient-and-accurate-rolling-standard-deviation/)
who had also [replied earlier in this SO](https://stackoverflow.com/a/14638138/548792).

## Quickstart

### command-line

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

### python code: auto-populate sample-list from the very 1st item

...like the command-line does:

```python
wsize = 3
main(wsize, 10, 10, 10, 12, 14, 12, 16, 20, 12, 17, 35, 10, 10, 10, 10)
```

### python code:  start with a prepared list

...alternative run to validate the correctness of the results:

```python
wsize = 3
l = [10, 10, 10, 12, 14, 12, 16, 20, 12, 17, 35, 10, 10, 10, 10]
rs = RollingStats(l[:wsize])
print("\n".join(rs.roll_stats(*l[wsize:])))
```