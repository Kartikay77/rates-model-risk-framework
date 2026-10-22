from curves.yield_curve import yield_curve
class SwapPricer:

    def __init__(self, curve):
        self.curve = curve

    def par_swap_rate(self, maturity, frequency=2):
        # TODO
        num_payments = int(maturity * frequency)
        alpha = 1/frequency
        discount_sum = 0

        for i in range(1, num_payments + 1):
            payment_time = i / frequency
            df = self.curve.discount_factor(payment_time)

            discount_sum += alpha * df
        final_df = self.curve.discount_factor(maturity)
        S = (1 - final_df) / discount_sum
        return S
    
    def fixed_leg_pv(self, notional, fixed_rate, maturity, frequency=2):
        num_payments = int(maturity * frequency)
        alpha = 1/frequency
        fixed_leg_pv = 0

        for i in range(1, num_payments + 1):
            payment_time = i / frequency
            df = self.curve.discount_factor(payment_time)

            fixed_leg_pv += notional * fixed_rate * alpha * df
        # final_df = self.curve.discount_factor(maturity)
        # fixed_leg_pv += notional * final_df
        return fixed_leg_pv
    
    def floating_leg_pv(self, notional, maturity, frequency=2):
        # num_payments = int(maturity * frequency)
        df = self.curve.discount_factor(maturity)
        pv = notional *(1-df)
        return pv
    
    def swap_value(self, notional, fixed_rate, maturity, frequency=2, pay_fixed=True):
        fixed_pv = self.fixed_leg_pv(notional, fixed_rate, maturity, frequency)
        floating_pv = self.floating_leg_pv(notional, maturity, frequency)
        if pay_fixed:
            return floating_pv - fixed_pv
        else:
            return fixed_pv - floating_pv
        


if __name__ == "__main__":
    swap_pricer = SwapPricer(yield_curve)

    print(
        "5Y annual par swap rate:",
        swap_pricer.par_swap_rate(5, frequency=1)
    )

    print(
        "5Y semiannual par swap rate:",
        swap_pricer.par_swap_rate(5, frequency=2)
    )
    annual_rate = swap_pricer.par_swap_rate(5, frequency=1)
    semiannual_rate = swap_pricer.par_swap_rate(5, frequency=2)

    print("5Y annual:", annual_rate * 100, "%")
    print("5Y semiannual:", semiannual_rate * 100, "%")

    print(
    "Fixed leg PV:",
    swap_pricer.fixed_leg_pv(
        notional=1_000_000,
        fixed_rate=0.05,
        maturity=5,
        frequency=2
    )
    )

    print(
    "Floating leg PV:",
    swap_pricer.floating_leg_pv(
        notional=1_000_000,
        maturity=5
        # frequency=2
    )
    )
    print(
    "Pay-fixed swap value:",
    swap_pricer.swap_value(
        notional=1_000_000,
        fixed_rate=0.05,
        maturity=5,
        frequency=2,
        pay_fixed=True
    )
    )

    print(
        "Receive-fixed swap value:",
        swap_pricer.swap_value(
            notional=1_000_000,
            fixed_rate=0.05,
            maturity=5,
            frequency=2,
            pay_fixed=False
        )
    )

    par_rate = swap_pricer.par_swap_rate(
        maturity=5,
        frequency=2
    )

    print(
        "Swap value at par rate:",
        swap_pricer.swap_value(
            notional=1_000_000,
            fixed_rate=par_rate,
            maturity=5,
            frequency=2,
            pay_fixed=True
        )
    )