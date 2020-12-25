from typing import Callable

import numpy as np
from scipy.optimize import minimize, Bounds


def implied_vol(func: Callable, price: float, kwargs: dict):
    """
    Finds the volatility yielding the searched for price
    :param func: Function to be used for price finding. "sig" must be a valid argument.
    :param price: target price
    :param kwargs: all required arguments for func except sig
    :return: target sig
    """
    def deviation(sig):
        return (func(sig=sig, **kwargs) - price) ** 2

    return minimize(deviation, [0.2], bounds=Bounds([0], [np.inf])).x[0]
