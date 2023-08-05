from math import log as _log, sqrt as _sqrt, ceil as _ceil, e as _e, sin as _sin, cos as _cos, pi as _pi, exp as _exp
from .base_rv_generators.rv_generators import *


class Random:
    def __init__(self, rng="desert", seed=1):
        """
        instantiate a random number generator

        :param rng:
            1. "desert" - desert island. A good LCG (linear congruential generator)
            2. "randu" - bad LCG
        :param seed: default to 0 if not provided
        """
        if rng == "desert":
            self.RNG = DesertIsland(seed)
        elif rng == "randu":
            self.RNG = Randu(seed)

    def random(self):
        """
        generate the next random number with uniform(0,1]
        """
        return self.RNG.next_n()

# -----------------------------------------------------
# ------------- Continuous Distributions --------------
# -----------------------------------------------------

    def uniform(self, a=0, b=1):
        """
        :param a: lower bound of uniform distribution, inclusive
        :param b: upper bound of uniform distribution, exclusive
        :return: a random uniformly distributed number between a and b
        """
        return a + (b-a) * self.random()

    def exponential(self, lmbda):
        """
        :param lmbda: mean time between events
        :return: the time between events in a Poisson process
        """
        return (-1/lmbda) * _log(1.0 - self.random())

    def triangular(self, low=0.0, high=1.0, mode=None):
        """
        :param low: lower limit
        :param high: upper limit
        :param mode: number with highest probability where a <= c <= b
        :return: triangular random variate
        """
        u = self.random()

        # F(c) = (c-a)/(b-a)
        f_c = (mode-low) / (high-low)

        if u < f_c:
            return low + _sqrt(u*(mode-low)*(high-low))
        else:
            return high - _sqrt((1-u)*(high-mode)*(high-low))

    def normal(self, mu=0, sigma=1.0):
        """
        :param mu: mean
        :param sigma: standard deviation
        :return: random number under a normal distribution with specified mean and standard deviation
        """
        u1, u2 = self.random(), self.random()
        z1 = _sqrt(-2.0*_log(u1))*_cos(2*_pi*u2)
        z2 = _sqrt(-2.0*_log(u1))*_sin(2*_pi*u2)
        return mu + z1 * sigma

    def weibull(self, alpha, beta):
        """
        :param alpha: shape parameter
        :param beta: scale parameter
        :return: random number under a Weibull distribution
        """
        u = 1 - self.random()
        return beta * (-_log(u) ** (1/alpha))

    def gamma(self, alpha, beta):
        """
        :param alpha: shape parameter
        :param beta: rate parameter
        :return: random number under a Gamma distribution
        """
        if alpha <= 0 or beta <= 0:
            raise ValueError("alpha and beta must be greater than 0")

        if alpha == 1.0:
            # same as expo(beta)
            return -_log(1.0 - self.random()) * beta
        elif alpha > 1.0:
            # the algorithm is from Simulation Modeling and Analysis (Law and Kelton)
            # from Cheng (1977)
            a = 1 / _sqrt(2*alpha - 1)
            b = alpha - _log(4)
            q = alpha + 1/a
            theta = 4.5
            d = 1 + _log(theta)

            while True:
                u1, u2 = self.random(), 1 - self.random()

                v = a * _log(u1 / (1-u1))
                y = alpha * _exp(v)
                z = (u1**2) * u2
                w = b + q*v - y

                if (w + d - theta*z) >= 0 or w >= _log(z):
                    return y * beta

        else:
            # if alpha < 1.0
            # the algorithm is from Simulation Modeling and Analysis (Law and Kelton) 
            # and denoted in Ahrens and Dieter (1974)
            b = (_e + alpha)/_e
            u1 = self.random()

            while True:
                p = b*u1
                u2 = self.random()
                if p > 1.0:
                    y = -_log((b-p) / alpha)
                    if u2 <= y ** (alpha-1):
                        break
                else:
                    y = p ** (1/alpha)
                    if u2 <= _exp(-y):
                        break
            return y * beta

# -----------------------------------------------------
# ------------- Discrete Distributions ----------------
# -----------------------------------------------------

    def bernoulli(self, p=0.5) -> int:
        """
        :param p: probability of a success event
        :return: 1 if a success event is observed, 0 otherwise
        """
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1, inclusive")

        return 1 if self.random() <= p else 0

    def binomial(self, n, p) -> int:
        """
        :param n: total number of trials
        :param p: probability of success event in a Bernoulli trial
        :return: number of successes in n trials
        """
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1, inclusive")
        if n < 0 or type(n) is not int:
            raise ValueError("n must be an integer >= 0")

        x = 0
        for i in range(n):
            if self.random() < p:
                x += 1
        return x

    def geometric(self, p, mode=0) -> int:
        """
        :param p: probability of success event in a Bernoulli trial
        :param mode: mode 0 is the fast and direct way.
                    mode other than "0" count the number of Bernoulli trials until a success event is observed
        :return: number of Bernoulli trials needed until a success event is observed
        """
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1, inclusive")

        if mode == 0:
            return _ceil(_log(1-self.random()) / _log(1-p))
        else:
            trial, count = 0, 0
            while trial == 0:
                trial = self.bernoulli(p)
                count += 1
            return count

    def poisson(self, lmbda) -> int:
        """
        Using Acceptance-Rejection Method

        :param lmbda: number of arrivals in one time unit
        :return: number of arrivals in one time unit
        """
        threshold = _exp(-lmbda)
        p = 1
        x = -1

        while p > threshold:
            p *= self.random()
            x += 1

        return x
