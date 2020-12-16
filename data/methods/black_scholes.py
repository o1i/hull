import math

from scipy.stats import norm


def put_eur_bs(s: float, k: float, r: float, sig: float, t: float) -> float:
    """
    Price of a european put option according to the Black-Scholes-Merton model.
    Source: Chapter 15
    :param s: Price of the underlying at time 0
    :param k: Strike
    :param r: Risk free rate
    :param sig: volatility (non-negative)
    :param t: Time to maturity
    :return: option price
    """
    d1 = (math.log(s / k) + (r + sig ** 2 / 2) * t) / (sig * math.sqrt(t))
    return k * math.exp(-r * t) * norm.cdf(-d1 + sig * math.sqrt(t)) - s * norm.cdf(-d1)


def call_eur_bs(s: float, k: float, r: float, sig: float, t: float) -> float:
    """
    Price of a european call option according to the Black-Scholes-Merton model.
    Source: Chapter 15
    :param s: Price of the underlying at time 0
    :param k: Strike
    :param r: Risk free rate
    :param sig: volatility (non-negative)
    :param t: Time to maturity
    :return: option price
    """
    d1 = (math.log(s / k) + (r + sig ** 2 / 2) * t) / (sig * math.sqrt(t))
    return - k * math.exp(-r * t) * norm.cdf(d1 - sig * math.sqrt(t)) + s * norm.cdf(d1)
