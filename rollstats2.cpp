/**
 * Rolling avg, stdev with compile-sized array pre-filled with the same init-value on runtime.
 *
 * SYNTAX:
 *     rollstats <wsize> [num] ...
 *
 * SAMPLE:
 *
 * ```bash
 * /rollstats2.exe 10 12 14 12 16 20 12 17 35 10 10 10 10
 * 1: 12 --> 10.67 ± 1
 * 2: 14 --> 15.33 ± 9.055
 * 3: 12 --> 19.33 ± 14.76
 * 4: 16 --> 20.67 ± 15.56
 * 5: 20 --> 22.67 ± 16.43
 * 6: 12 --> 22.67 ± 16.43
 * 7: 17 --> 23 ± 16.64
 * 8: 35 --> 28 ± 15.72
 * 9: 10 --> 27.33 ± 14.59
 * 10: 10 --> 25 ± 11.18
 * 11: 10 --> 16.67 ± 12.88
 * 12: 10 --> 16.67 ± 12.88
 * ```
 *
 * Adapted from:
 * https://jonisalonen.com/2014/efficient-and-accurate-rolling-standard-deviation/
 */
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>

using Stats = std::pair<float, float>;

// V: a numeric type of the items to stat, like: int, double
template <typename V, int WSIZE>
class RollingStats {
 public:
  RollingStats(const V init_val) : items{init_val} { avg = init_val; }

  float stdev() {
    // Depart from recipe, conventionally-computed variances are never negative.
    return sqrt(abs(var));
  }

  void update(const V x_inp) {
    const auto x_out = items[i];
    items[i] = x_inp;
    i = (i + 1) % WSIZE;

    const auto dval = x_inp - x_out;
    const auto oldavg = avg;
    avg = avg + (float)dval / WSIZE;
    var += dval * (x_inp - avg + x_out - oldavg) / (WSIZE - 1);
  }

  // protected:  // No protection, adults may inspect them.
  // Index in `items` of the next item to pop-out and overwrite.
  uint i = 0;
  float avg;
  float var = 0;
  V items[WSIZE];
};

int main(const int argc, const char *argv[]) {
  if (argc < 2) {
    std::cerr << "syntax: " << argv[0] << " <wsize> [<num>...]";
    return -1;
  }
  // Lots of problems with `atoi`, parse failures return 0, but...fast & simple.
  const auto x0 = atoi(argv[1]);
  auto rs = RollingStats<int, 3>(x0);
  for (int i = 2; i < argc; i++) {
    auto item = atoi(argv[i]);
    rs.update(item);
    std::cout << i - 1 << ": " << item << " --> " << std::setprecision(4)
              << rs.avg << " ± " << rs.stdev() << '\n';
  }
}
