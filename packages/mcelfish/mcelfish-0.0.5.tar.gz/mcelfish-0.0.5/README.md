# mcelfish -- MCMC Removal Sampling

Do _removal sampling_ with MCMC, Zippin, or Carle-Strub.

**Usage:**

```
mcelfish --data 19 17 13 1 1
```

```
mcelfish --plot --data 19 17 13 1 1
```


## Installing

```
pip install mcelfish
```

or from source

```
git clone git@github.com:pgdr/mcelfish
pip install -e ./mcelfish
```


## Removal sampling

Suppose that you want to
[estimate the number of apples in an apple tree](https://stats.stackexchange.com/questions/491165/estimating-the-number-of-apples-in-an-apple-tree-using-mcmc)
by repeatedly kicking the tree and counting how many apples fall down.
We make an assumption that there is a (constant) _p_ between 0 and 1,
such that the probability that any given apple falls down when you kick
the tree is _p_.

Suppose that the apple tree contains _N_ apples.  Given a series of
kicks, we want to estimate _N_ and _p_.

We call this problem _removal sampling_.


### Examples

Suppose that `[100, 10, 1, 0]` apples fall down.  In this case, we may
estimate _p_ to be approximately 0.9, and _N_ approximately 111.

Suppose that `[19, 17, 13, 1, 1]` apples fall down.  In this more
complicated case, Bayesian statistics tell us that we should expect
_53 ≤ N ≤ 57_ and _0.4 ≤ p ≤ 0.45_.

![traceplot](https://raw.githubusercontent.com/pgdr/mcelfish/master/assets/traceplot.png)

## Advanced MCMC usage

This package uses [pymc3](https://pypi.org/project/pymc3/).  Tuning the
MCMC run can be done with the parameters `--samplings` and `--tunings`,
e.g.

```
mcelfish --samples 10000 --tunings 5000 --plot --data 19 17 13 1 1
```

We can use `--beta` to output the beta parameters for the posterior.
