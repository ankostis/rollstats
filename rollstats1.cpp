/**
 * Rolling avg, stdev starting with an empty (runtime sized) std::vector.
 *
 * SYNTAX:
 *     rollstats <wsize> [num] ...
 *
 * Sample run:
 *
 * ```bash
 * ./rollstats 3  10 10 10 12 14 12 16 20 12 17 35 10 10 10 10
 * 0: 10 --> 10 ± 0
 * 1: 10 --> 10 ± 0
 * 2: 10 --> 10 ± 0
 * 3: 12 --> 10.67 ± 1
 * 4: 14 --> 12 ± 1.732
 * 5: 12 --> 12.67 ± 1
 * 6: 16 --> 14 ± 1.732
 * 7: 20 --> 16 ± 3.873
 * 8: 12 --> 16 ± 3.873
 * 9: 17 --> 16.33 ± 4
 * 10: 35 --> 21.33 ± 12.08
 * 11: 10 --> 20.67 ± 12.88
 * 12: 10 --> 18.33 ± 14.42
 * 13: 10 --> 10 ± 0
 * 14: 10 --> 10 ± 0
 * ```
 *
 * Adapted from:
 * https://jonisalonen.com/2014/efficient-and-accurate-rolling-standard-deviation/
 */
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <utility>
#include <vector>

using Stats = std::pair<float, float>;

template <typename V>  // a numeric type of the items to stat, like: int, double
class RollingStats {
 public:
  // NOTE: ensure `wsize` not 0
  RollingStats(const uint wsize) : WSIZE(wsize) { items.reserve(wsize); }

  float stdev() {
    // Depart from recipe, conventionally-computed variances are never negative.
    return sqrt(abs(var));
  }

  void update(const V x_inp) {
    auto nitems = items.size();
    if (nitems < WSIZE) {
      items.push_back(x_inp);  // insertion repeated below
      if (nitems == 0) {
        avg = x_inp;
        var = 0;
        return;
      }
      nitems += (nitems == 1);  // avoid DivBy0 below
    } else {
      nitems = WSIZE;
    }
    const auto x_out = items[i];
    items[i] = x_inp;
    i = (i + 1) % WSIZE;

    const auto dval = x_inp - x_out;
    const auto oldavg = avg;
    avg = avg + (float)dval / nitems;
    var += dval * (x_inp - avg + x_out - oldavg) / (nitems - 1);
  }

  // protected:  // No protection, adults may inspect them.
  const uint WSIZE;
  // Index in `items` of the next item to pop-out and overwrite.
  uint i = 0;
  float avg;
  float var;
  std::vector<V> items;
};

int main(const int argc, const char *argv[]) {
  if (argc < 2) {
    std::cerr << "syntax: " << argv[0] << " <wsize> [<num>...]";
    return -1;
  }
  // Lots of problems with `atoi`, parse failures return 0, but...fast & simple.
  const auto wsize = atoi(argv[1]);
  auto rs = RollingStats<int>(wsize);
  for (int i = 2; i < argc; i++) {
    auto item = atoi(argv[i]);
    rs.update(item);
    std::cout << i - 2 << ": " << item << " --> " << std::setprecision(4)
              << rs.avg << " ± " << rs.stdev() << '\n';
  }
}
