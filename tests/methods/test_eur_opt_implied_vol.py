import unittest

from methods.binom_trees import put_eur_binom_tree
from methods.black_scholes import call_eur_bs
from methods.implied_vol_options import implied_vol


class TestImpliedVol(unittest.TestCase):
    def test_normal_case(self):
        kwargs = {"s": 50, "k": 53, "r": 0.2, "t": 5}
        sig = 0.3
        self.assertAlmostEqual(
            sig,
            implied_vol(call_eur_bs, call_eur_bs(sig=sig, **kwargs), kwargs),
        )
        kwargs.update({"n": 30})
        self.assertAlmostEqual(
            sig,
            implied_vol(put_eur_binom_tree, put_eur_binom_tree(sig=sig, **kwargs), kwargs)
        )
