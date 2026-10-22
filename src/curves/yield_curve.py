import numpy as np


class YieldCurve:

    def __init__(self, maturities, zero_rates):
        # TODO
        self.maturities = np.array(maturities)
        self.zero_rates = np.array(zero_rates)

    def zero_rate(self, maturity):
        # TODO
        return np.interp(maturity, self.maturities, self.zero_rates)

    def discount_factor(self, maturity):
        # TODO
        zero_rate = self.zero_rate(maturity)
        return np.exp(-zero_rate * maturity)
    
    def forward_rate(self, start, end):
        if end <= start:
            raise ValueError("End maturity must be greater than start maturity")

        r_start = self.zero_rate(start)
        r_end = self.zero_rate(end)

        return (r_end * end - r_start * start) / (end - start)

    def shifted_curve(self, shift):
        new_zero_rates = self.zero_rates + shift
        return YieldCurve(self.maturities, new_zero_rates)

maturities = np.array([
    0.5, 1, 2, 3, 5, 7, 10
])

zero_rates = np.array([
    0.0400,
    0.0410,
    0.0425,
    0.0435,
    0.0450,
    0.0460,
    0.0470
])

yield_curve = YieldCurve(maturities, zero_rates)

if __name__ == "__main__":

    print("1Y zero rate:", yield_curve.zero_rate(1))
    print("4Y zero rate:", yield_curve.zero_rate(4))

    print("1Y DF:", yield_curve.discount_factor(1))
    print("5Y DF:", yield_curve.discount_factor(5))
    print("10Y DF:", yield_curve.discount_factor(10))

    print("1Y-2Y forward:", yield_curve.forward_rate(1, 2))
    print("2Y-5Y forward:", yield_curve.forward_rate(2, 5))
    print("5Y-10Y forward:", yield_curve.forward_rate(5, 10))