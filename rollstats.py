class RollingStats:
    def __init__(self, window_size, avg, variance):
        self.N: Final[int] = window_size
        self.avg = avg
        self.variance = variance

    @property
    def stdev(self):
        return sqrt(self.variance)

    def update(self, x_inp, x_out):
        dval = x_inp - x_out
        oldavg = self.avg
        self.avg = newavg = self.avg + dval / self.N
        self.variance += dval * (x_inp - newavg + x_out - oldavg) / (self.N - 1)
