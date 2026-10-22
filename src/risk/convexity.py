from curves.yield_curve import yield_curve
from pricing.bonds import BondPricer

shift = 0.0001

original_pricer = BondPricer(yield_curve)

up_curve = yield_curve.shifted_curve(shift)
down_curve = yield_curve.shifted_curve(-shift)

up_pricer = BondPricer(up_curve)
down_pricer = BondPricer(down_curve)

up_price = up_pricer.coupon_bond(
    face_value=1000,
    coupon_rate=0.05,
    maturity=5,
    frequency=1
)

down_price = down_pricer.coupon_bond(
    face_value=1000,
    coupon_rate=0.05,
    maturity=5,
    frequency=1
)

original_price = original_pricer.coupon_bond(
    face_value=1000,
    coupon_rate=0.05,
    maturity=5,
    frequency=1
)

convexity = (down_price+up_price - 2*original_price) / (original_price*(shift**2))
print("Convexity:", convexity)