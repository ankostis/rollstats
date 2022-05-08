# Rollstats

Calculate rolling stdev, in python & C++.

Adapted from [The Mindful Programmer (jonisalonen)](https://jonisalonen.com/2014/efficient-and-accurate-rolling-standard-deviation/)
(had also [replied earlier in this SO](https://stackoverflow.com/a/14638138/548792)).

In that post, the rolling formulas are eventually given like that
(transcribed here with an iterative viepoint):

$$
\newcommand{\Var}{\operatorname{Var}}
\begin{align}
    \overline{x_{new}} &= \overline{x_{old}}  + \frac{x_{inp} - x_{out}}{N}  \\

    \Var[x_{new}] &= \Var[x_{old}] + (x_{inp} - x_{out})
        \times (x_{inp} - \overline{x_{new}} + x_{out} - \overline{x_{old}})  \\

    \sigma[x] &= \sqrt{|\Var[x]|}
\end{align}
$$

that depend on the numbers *entering* and *exiting* the
$N$ sized circular-buffer, respectively:

- $x_{inp}$
- $x_{out}$

and on the mean values of that buffer, *before* and *after* the swap, respectively:

- $\overline{x_{old}}$
- $\overline{x_{new}}$

**NOTE:** the original post lacked the  absolute ($|...|$) inside the root($\sqrt{}$),
discovered its need by experiments.  Conventionally calculated variance
(with sum-of-squared-diffs) is never negative.

## Implementations

All classes compute the *average*, *variance* and *standard-deviation* after
each new element has been inserted in the circular buffer.

- `rollstats.py` - start with empty OR a pre-filled circular-buffer
- `rollstats.cpp` - start with empty std::vector (runtime sized)

## Quickstart

### Command-line

#### Python implementation

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

#### C++ implementation

```bash
./rollstats 3  10 10 10 12 14 12 16 20 12 17 35 10 10 10 10
0: 10 --> 10 ± 0
1: 10 --> 10 ± 0
2: 10 --> 10 ± 0
3: 12 --> 10.67 ± 1
4: 14 --> 12 ± 1.732
5: 12 --> 12.67 ± 1
6: 16 --> 14 ± 1.732
7: 20 --> 16 ± 3.873
8: 12 --> 16 ± 3.873
9: 17 --> 16.33 ± 4
10: 35 --> 21.33 ± 12.08
11: 10 --> 20.67 ± 12.88
12: 10 --> 18.33 ± 14.42
13: 10 --> 10 ± 0
14: 10 --> 10 ± 0
```

### Python code

#### Auto-populate circular-buffer from the very 1st item

...like the command-line does:

```python
wsize = 3
main(wsize, 10, 10, 10, 12, 14, 12, 16, 20, 12, 17, 35, 10, 10, 10, 10)
```

#### Start with a pre-filled list

...alternative run to validate the correctness of the results:

```python
ize = 3
l = [10, 10, 10, 12, 14, 12, 16, 20, 12, 17, 35, 10, 10, 10, 10]
rs = RollingStats(l[:wsize])
items = l[wsize:]
stats = rs.roll_stats(items)
print("\n".join(
    f"{i}: {x_inp} --> {avg:.2f} ± {stdev:.2f}"
    for i, (x_inp, (avg, stdev)) in enumerate(zip(items, stats))))
```