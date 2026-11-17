import numpy as np
import timeit

# Tiered electricity billing for one million households (assumed tariff)
#   0-30 kWh   : 12 KES per kWh
#   31-100 kWh : 16 KES per kWh
#   above 100  : 22 KES per kWh
# Plus a 16% VAT on the energy charge.
rng = np.random.default_rng(42)
kwh = rng.gamma(shape=4.0, scale=20.0, size=1_000_000)   # monthly usage, mean ~80 kWh

def bill_loop():
    bills = []
    for u in kwh:
        if u <= 30:
            c = 12 * u
        elif u <= 100:
            c = 12 * 30 + 16 * (u - 30)
        else:
            c = 12 * 30 + 16 * 70 + 22 * (u - 100)
        bills.append(c * 1.16)
    return bills

def bill_vectorized():
    tier1 = np.minimum(kwh, 30) * 12
    tier2 = np.clip(kwh - 30, 0, 70) * 16
    tier3 = np.maximum(kwh - 100, 0) * 22
    return (tier1 + tier2 + tier3) * 1.16

t_loop = timeit.timeit(bill_loop, number=1)
t_vec = timeit.timeit(bill_vectorized, number=3) / 3

loop_bills = np.array(bill_loop())
bills = bill_vectorized()

print("Results identical:", np.allclose(loop_bills, bills))
print(f"Average bill: {bills.mean():.2f} KES")
print(f"Highest bill: {bills.max():.2f} KES")
print(f"Total revenue: {bills.sum()/1e6:.2f} million KES")
print(f"Households above 100 kWh: {(kwh > 100).mean():.1%}")
print(f"Loop time: {t_loop:.4f} s | Vectorized time: {t_vec:.4f} s")
print(f"Approximate speed-up: {t_loop/t_vec:.1f}x")
