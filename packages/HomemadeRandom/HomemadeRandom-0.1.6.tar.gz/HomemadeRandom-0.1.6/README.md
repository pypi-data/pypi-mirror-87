# Random Variate Generator
This package provides access to a few frequently used discrete and continuous distributions.


## Installation
### Normal Installation
`pip install HomemadeRandom`

## API Details and Examples

Start using the library by running  
`from HomemadeRandom import Random`  

Initialize a HomemadeRandom object with two parameters: type of base random number generator and a seed.  
Select a base random number generator from the following:  
1. "desert" - desert island. A good LCG (linear congruential generator).
    * The seed must be between 1 and 2147483646 (inclusive)
2. "randu" - bad LCG
    * The seed must be between 1 and 2147483647 (inclusive)


Example:  
`RV = Random('desert', seed=10)`

#### Discrete Distributions
1. Bernoulli  
`RV.bernoulli(p=0.5)`  
Parameter: (optional) p: floats. 0 <= p <= 1. Probability of a success event

2. Binomial  
`RV.binomial(n, p)`  
Parameter: n: int. n > 0. Total number of trials  
Parameter: p: floats. 0 <= p <= 1. Probability of a success event  

3. Geometric  
`RV.geometric(p, mode=0)`  
Parameter: p: floats. 0 <= p <= 1. Probability of a success event  
Parameter: (optional) mode: int. Mode 0 is the fast and direct way. Any other mode will use the other implementation, which was implemented for academic purpose.  

4. Poisson  
`RV.poisson(lmbda)`  
Parameter: lmbda: floats. lmbda >= 0. Number of arrivals in one time unit  

#### Continuous Distributions
1. Uniform  
`RV.uniform(a=0, b=1)`  
Parameter: (optional) a: floats. lower bound of uniform distribution, inclusive  
Parameter: (optional) b: floats. upper bound of uniform distribution, exclusive  

2. Exponential  
`RV.exponential(lmbda)`  
Parameter: lmbda: mean time between events  

3. Normal  
`RV.normal(mu=0, sigma=1.0)`  
Parameter: (optional) mu: floats. mean of a normal distribution
Parameter: (optional) sigma: floats. standard deviation of a normal distribution
  
4. Gamma  
`RV.gamma(alpha, beta)`  
Parameter: alpha: floats. shape parameter  
Parameter: beta: floats. rate parameter  

5. Weibull  
`RV.weibull(alpha, beta)`  
Parameter: alpha: floats. shape parameter  
Parameter: beta: floats. scale parameter  

6. Triangular  
`RV.triangular(low=0.0, high=1.0, mode=None)`  
Parameter: low: floats. lower limit  
Parameter: high: floats. upper limit  
Parameter: mode: floats. number with highest probability where a <= c <= b


See `tests/test.py` for actual usage or 
download/clone the project and execute `python test.py` inside the tests directory 