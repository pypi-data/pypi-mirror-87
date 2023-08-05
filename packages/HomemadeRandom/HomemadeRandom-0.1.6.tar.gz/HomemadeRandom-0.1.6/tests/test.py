from HomemadeRandom import Random

RV = Random(rng="desert", seed=10)

print("=====uniform====")
for _ in range(15):
    print(RV.uniform(0,10))

print("=====exponential====")
for _ in range(15):
    print(RV.exponential(5))

print("=====triangular====")
for _ in range(15):
    print(RV.triangular(0, 10, 6))

print("=====normal====")
for _ in range(15):
    print(RV.normal(5, 2))

print("=====weibull====")
for _ in range(15):
    print(RV.weibull(2, 5))

print("=====gamma====")
for _ in range(15):
    print(RV.gamma(1.5,2))

print("=====bernoulli====")
for _ in range(15):
    print(RV.bernoulli(p=0.5))


print("=====binomial====")
for _ in range(15):
    print(RV.binomial(50, 0.3))

print("=====geometric====")
for _ in range(15):
    print(RV.geometric(0.4, 0))


print("=====poisson====")
for _ in range(15):
    print(RV.poisson(10))