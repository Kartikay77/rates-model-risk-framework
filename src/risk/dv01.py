from curves.yield_curve import yield_curve
from pricing.bonds import BondPricer

up_curve = yield_curve.shifted_curve(0.0001)
down_curve = yield_curve.shifted_curve(-0.0001)

up_pricer = BondPricer(up_curve)
down_pricer = BondPricer(down_curve)

price_up = up_pricer.coupon_bond(
    # fill arguments 
    # 1bp = 0.01% = 0.0001
    face_value=1000,
    coupon_rate =0.05,
    maturity = 5,
    frequency=1
)

price_down = down_pricer.coupon_bond(
    # fill arguments 
    # 1bp = 0.01% = 0.0001
    face_value=1000,
    coupon_rate =0.05,
    maturity = 5,
    frequency=1
)

dv01 = (price_down - price_up) / 2

print(yield_curve.zero_rate(5))
print(up_curve.zero_rate(5))
print(down_curve.zero_rate(5))
print("Price with rates +1bp:", price_up)
print("Price with rates -1bp:", price_down)
print("DV01:", dv01)
