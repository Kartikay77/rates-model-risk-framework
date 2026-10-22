import numpy as np
import matplotlib.pyplot as plt
from curves.yield_curve import yield_curve
class BondPricer:

    def __init__(self, curve):
        self.curve = curve

    def zero_coupon_bond(self, face_value, maturity):
        # TODO
        df = self.curve.discount_factor(maturity)
        return face_value * df
        

    def coupon_bond(self, face_value, coupon_rate, maturity, frequency=1):
        # TODO
        num_payments = int(maturity * frequency)
        coupon_payment = 0
        total_value = 0
        coupon_payment = face_value * coupon_rate  / frequency
        for i in range(1,num_payments+1): # for periodic payments
            payment_time = i / frequency
            total_value += coupon_payment * self.curve.discount_factor(payment_time)
        principal_pv = face_value * self.curve.discount_factor(maturity)
        total_value += principal_pv
        return total_value
bond_pricer = BondPricer(yield_curve)

if __name__ == "__main__":
    print(
        "5Y zero coupon:",
        bond_pricer.zero_coupon_bond(1000, 5)
    )

    print(
        "5Y 5% annual coupon:",
        bond_pricer.coupon_bond(
            face_value=1000,
            coupon_rate=0.05,
            maturity=5,
            frequency=1
        )
    )

    print(
        "5Y 5% semiannual coupon:",
        bond_pricer.coupon_bond(
            face_value=1000,
            coupon_rate=0.05,
            maturity=5,
            frequency=2
        )
    )