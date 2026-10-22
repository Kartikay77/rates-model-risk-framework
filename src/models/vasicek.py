import numpy as np


class VasicekModel:

    def __init__(self, a, b, sigma, r0):
        self.a = a
        self.b = b
        self.sigma = sigma
        self.r0 = r0

    def simulate_paths(self, years, steps_per_year, num_paths, seed=None):
        if seed is not None:
            np.random.seed(seed)

        dt = 1 / steps_per_year
        num_steps = int(years * steps_per_year)
        paths = np.zeros((num_paths, num_steps + 1))
        paths[:, 0] = self.r0

        for i in range(1, num_steps + 1):
            z = np.random.normal(size=num_paths)
            dr = self.a * (self.b - paths[:, i - 1]) * dt + self.sigma * np.sqrt(dt) * z
            paths[:, i] = paths[:, i - 1] + dr

        return paths

    def expected_rate(self, t):
    # TODO
        e_rt = self.b + (self.r0 - self.b) * np.exp(-self.a * t)
        return e_rt


    def rate_variance(self, t):
    # TODO
        var = self.sigma**2
        rate_var = var*(1-np.exp(-2*self.a*t))/(2*self.a)
        return rate_var
    

    def B(self, t, T):
    # TODO
        B = (1-np.exp(-self.a*(T-t)))/self.a
        return B
    
    def A(self, t, T):
        A = np.exp((self.b-(self.sigma**2/(2*self.a**2))) * (self.B(t,T)-(T-t)) - ((self.sigma**2 * self.B(t,T)**2))/(4 * self.a))
        return A
    

    def zero_coupon_bond_price(self, t, T, r_t):
        P = self.A(t,T)*np.exp(-self.B(t,T)*r_t)
        return P


    def monte_carlo_bond_price(self, maturity, steps_per_year=252, num_paths=10000, seed=None):
        paths = self.simulate_paths(maturity, steps_per_year, num_paths, seed)
        dt = 1 / steps_per_year
        integrated_rates = np.sum(paths[:, :-1], axis=1) * dt
        discount_factors = np.exp(-integrated_rates)
        price = np.mean(discount_factors)
        return price



if __name__ == "__main__":
    model = VasicekModel(
    a=0.5,
    b=0.05,
    sigma=0.01,
    r0=0.04
    )

    paths = model.simulate_paths(
    years=5,
    steps_per_year=252,
    num_paths=10000,
    seed=42
    )

    print("Shape:", paths.shape)
    print("Initial mean rate:", np.mean(paths[:, 0]))
    print("1Y mean rate:", np.mean(paths[:, 252]))
    print("5Y mean rate:", np.mean(paths[:, -1]))

    print("5Y minimum rate:", np.min(paths[:, -1]))
    print("5Y maximum rate:", np.max(paths[:, -1]))

    analytical_mean = model.expected_rate(5)
    simulated_mean = np.mean(paths[:, -1])
    error_bps = abs(simulated_mean - analytical_mean) / 0.0001

    print("Analytical 5Y mean:", analytical_mean)
    print("Simulated 5Y mean:", simulated_mean)
    print("Absolute error:", abs(simulated_mean - analytical_mean))
    print("Error in BPS:", error_bps)

    analytical_variance = model.rate_variance(5)
    simulated_variance = np.var(paths[:, -1])

    analytical_std = np.sqrt(analytical_variance)
    simulated_std = np.std(paths[:, -1])

    print("Analytical 5Y variance:", analytical_variance)
    print("Simulated 5Y variance:", simulated_variance)

    print("Analytical 5Y std:", analytical_std)
    print("Simulated 5Y std:", simulated_std)
    print("B(0,5):", model.B(0, 5))

    print("A(0,5):", model.A(0, 5))

    price = model.zero_coupon_bond_price(
        t=0,
        T=5,
        r_t=0.04
    )
    print("Zero-coupon bond price (0,5):", price)

    analytical_price = model.zero_coupon_bond_price(
        t=0,
        T=5,
        r_t=model.r0

    )

    mc_price = model.monte_carlo_bond_price(
        maturity=5,
        steps_per_year=252,
        num_paths=10000,
        seed=42
    )

    print("Analytical bond price:", analytical_price)
    print("Monte Carlo bond price:", mc_price)
    print("Absolute pricing error:", abs(mc_price - analytical_price))