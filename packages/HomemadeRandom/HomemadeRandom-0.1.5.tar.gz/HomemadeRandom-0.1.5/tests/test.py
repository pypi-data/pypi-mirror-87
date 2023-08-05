import HomemadeRandom

RV = HomemadeRandom(rng="desert", seed=10)

# generate 15 random numbers from a Bernoulli distribution
for _ in range(15):
    print(RV.bernoulli(p=0.5))

# generate 100 random numbers from a Normal distribution
for _ in range(100):
    print(RV.normal(mu=0, sigma=5))