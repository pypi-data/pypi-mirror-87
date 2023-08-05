import sys
from math import floor

class DesertIsland(object):
    """
    Good random number generator with cycle length of over 2 billion
    """
    def __init__(self, seed=1):
        self.m=2**31-1
        if not self._seed_check(seed, self.m):
            sys.exit("Seed must be between 1 and 2147483646 (inclusive)")

        self.seed = seed
        self.a=16807
        self.b=127773
        self.c=4.656612875e-10
    
    def next_n(self) -> float:
        k = floor(self.seed/self.b)
        self.seed = self.a*(self.seed - self.b*k) - 2836*k
        if self.seed < 0:
            self.seed += self.m
        
        return self.seed * self.c
    def _seed_check(self, seed, m) -> bool:
        return False if seed < 1 or seed > m else True
    


class Randu(object):
    """
    Bad random number generator. Don't use this one
    """
    def __init__(self, seed=1):
        self.m=2**31
        if not self._seed_check(seed, self.m):
            sys.exit("Seed must be between 1 and 2147483647 (inclusive)")
        self.seed = seed
        self.a=65539
        self.b=127773
        self.c=4.656612875e-10
    
    def next_n(self) -> float:
        self.seed = (self.a * self.seed) % self.m
        return self.seed / self.m
                
    def _seed_check(self, seed, m) -> bool:
        return False if seed < 1 or seed >= m else True