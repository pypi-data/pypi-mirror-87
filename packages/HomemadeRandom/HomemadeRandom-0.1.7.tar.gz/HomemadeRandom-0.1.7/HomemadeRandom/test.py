# if __name__ == "__main__":
#     from HomemadeRandom import HomemadeRandom
# else:
from HomemadeRandom import HomemadeRandom

RVG = HomemadeRandom(rng="desert", seed=10)
for _ in range(10):
    print(RVG.bernoulli(p=0.5))