import math
from typing import Callable


def put_eur_binom_tree(s: float, k: float, r: float, sig: float, t: float, n: int) -> float:
    """
    Price of a european put option according to the binomial tree model.
    Source: Chapter 13


    :param s: Price of the underlying at time 0
    :param k: Strike
    :param r: Risk free rate
    :param sig: volatility (non-negative)
    :param t: Time to maturity
    :param n: number of steps
    :return: option price
    """
    return binom_tree(s, k, r, sig, t, n, iv_put, fv_eur)


def call_eur_binom_tree(s: float, k: float, r: float, sig: float, t: float, n: int) -> float:
    """
    Price of a european call option according to the binomial tree model.
    Source: Chapter 13
    :param s: Price of the underlying at time 0
    :param k: Strike
    :param r: Risk free rate
    :param sig: volatility (non-negative)
    :param t: Time to maturity
    :param n: number of steps
    :return: option price
    """
    return binom_tree(s, k, r, sig, t, n, iv_call, fv_eur)


def binom_tree(s: float,
               k: float,
               r: float,
               sig: float,
               t: float,
               n: int,
               iv: Callable[[float, float], float],
               fv: Callable) -> float:
    """
    Price of an option from a binomial tree.

    The tree is represented as dictionaries:
    - the keys (i, u, d) denote the step (from i=0, present to i=n at time t in equal increments) and the number of
    times there has been a move up (u) and down (d). While this is overspecified (i=u+d) this should make a subsequent
    implementation of trinomial trees easier.
    - the Values of the dictionary f holds the value of the option
    - the values of the dictionary p holds the probability of being in a node (probabilities sum to 1 within a time
      index i)

    The values of the underlying at each node are computed at decision time based on the keys.

    Source: Chapter 13
    :param s: Price of the underlying at time 0
    :param k: Strike
    :param r: Risk free rate
    :param sig: volatility (non-negative)
    :param t: Time to maturity
    :param n: number of steps
    :param iv: fucntion(s, k) -> float yielding the intrinsic value of the option given underlying s and strike k
    :param fv: function (*, i, pu, i_u, pd, i_d, f, iv) -> float yielding value of the option given
                 i: time index i
                 n: number of time steps
                 t: total time at i=n
                 r: risk free rate
                 pu: (risk neutral) probability of up move
                 i_u: # of up moves at the node
                 pd: (risk neutral) probability of down move
                 i_d: # of down moves at node
                 f: dictionary with option values
                 iv: intrinsic value function
               and downs at the node, value dictionary f and intrinsiv value function iv.
               Function is allowed to depend on only a subset, but in that case must accept **kwargs
    :return: option price
    """
    if sig == 0:
        return iv(s, k)
    f = dict()  # value 'tree'"
    u = math.exp(sig * math.sqrt(t / n))  # up factor
    d = math.exp(-sig * math.sqrt(t / n))  # down factor
    pu = (math.exp(r * t / n) - d) / (u - d)  # probability of up move
    pd = 1 - pu  # probability of down move
    for i_u in range(n+1):  # intrinsic value at T
        f[(n, i_u, n - i_u)] = iv(s * u ** i_u * d ** (n - i_u), k)
    for i in range(n-1, -1, -1):  # update backward in time
        for i_u in range(i+1):
            f[(i, i_u, i - i_u)] = fv(s0=s, i=i, n=n, t=t, r=r, u=u, pu=pu, i_u=i_u, d=d, pd=pd,
                                      i_d=i - i_u, f=f, iv=iv, k=k)  # update
    return f[(0, 0, 0)]


def iv_call(s: float, k: float) -> float:
    """Intrinsic value of a call"""
    return max([0, s - k])


def iv_put(s: float, k: float) -> float:
    """Intrinsic value of a put"""
    return max([0, k - s])


def fv_eur(i: int, n: int, t: float, r: float, pu: float, i_u: int, pd: float, i_d: int, f: dict, **_) -> float:
    """One-Step update for a european option"""
    return (math.exp(- r * t / n) *  # discount
            (pu * f[(i+1, i_u + 1, i_d)] +  # up move
             pd * f[(i+1, i_u, i_d + 1)]  # down move
             ))


def fv_american(s0: float, i: int, n: int, t: float, r: float, u: float, pu: float, i_u: int, d: float,
                pd: float, i_d: int, f: dict, iv: Callable, k, **_) -> float:
    """One-Step update for a european option"""
    return max((math.exp(- r * t / n) *  # discount
               (pu * f[(i+1, i_u + 1, i_d)] +  # up move
                pd * f[(i+1, i_u, i_d + 1)]  # down move
                )),
               iv(s0 * u ** i_u * d ** i_d, k))  # immediate exercise
