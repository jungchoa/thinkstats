"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import bisect
from math import sqrt


def counts(xs):
    c = {}
    for x in xs:
        c.setdefault(x, 0)
        c[x] += 1
    return c


def pmf(xs):
    num = float(len(xs))
    c = counts(xs)
    for k, v in c:
        c[k] = v / num
    return c


def mean(t):
    """Computes the mean of a sequence of numbers.

    Args:
        t: sequence of numbers

    Returns:
        float
    """
    if not t:
        return
    return float(sum(t)) / len(t)


def mean_variance(t):
    """Computes the mean and variance of a sequence of numbers.

    Args:
        t: sequence of numbers

    Returns:
        tuple of two floats
    """
    mu = mean(t)
    if not mu:
        return None, None
    var = variance(t, mu)
    return mu, var


def trim(t, p=0.01):
    """Trims the largest and smallest elements of t.

    Args:
        t: sequence of numbers
        p: fraction of values to trim off each end

    Returns:
        sequence of values
    """
    n = int(p * len(t))
    return sorted(t)[n:-n]


def trimmed_mean(t, p=0.01):
    """Computes the trimmed mean of a sequence of numbers.

    Side effect: sorts the list.

    Args:
        t: sequence of numbers
        p: fraction of values to trim off each end

    Returns:
        float
    """
    return mean(trim(t, p))


def trimmed_mean_variance(t, p=0.01):
    """Computes the trimmed mean and variance of a sequence of numbers.

    Side effect: sorts the list.

    Args:
        t: sequence of numbers
        p: fraction of values to trim off each end

    Returns:
        float
    """
    return mean_variance(trim(t, p))


def variance(t, mu=None):
    """Computes the variance of a sequence of numbers.

    Args:
        t: sequence of numbers
        mu: value around which to compute the variance; by default,
            computes the mean.

    Returns:
        float
    """
    if mu is None:
        mu = mean(t)

    # compute the squared deviations and return their mean.
    dev2 = [(x - mu)**2 for x in t]
    return mean(dev2)


def standard_deviation(t, mu=None):
    return sqrt(variance(t, mu))


std_dev = standard_deviation


def binomial(n, k, d={}):
    """Compute the binomial coefficient "n choose k".

    Args:
      n: number of trials
      k: number of successes
      d: map from (n,k) tuples to cached results

    Returns:
      int
    """
    if k == 0:
        return 1
    if n == 0:
        return 0

    try:
        return d[n, k]
    except KeyError:
        res = binomial(n-1, k) + binomial(n-1, k-1)
        d[n, k] = res
        return res


class Interpolator(object):
    """Represents a mapping between sorted sequences; performs linear interp.

    Attributes:
        xs: sorted list
        ys: sorted list
    """
    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def lookup(self, x):
        """Looks up x and returns the corresponding value of y."""
        return self._bisect(x, self.xs, self.ys)

    def reverse(self, y):
        """Looks up y and returns the corresponding value of x."""
        return self._bisect(y, self.ys, self.xs)

    def _bisect(self, x, xs, ys):
        """Helper function."""
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]
        i = bisect.bisect(xs, x)
        frac = 1.0 * (x - xs[i-1]) / (xs[i] - xs[i-1])
        y = ys[i-1] + frac * 1.0 * (ys[i] - ys[i-1])
        return y
