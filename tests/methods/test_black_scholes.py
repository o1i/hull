import unittest

from data.methods.black_scholes import put_eur_bs, call_eur_bs


class TestBlackScholes(unittest.TestCase):
    def test_put_eur_bs(self):
        """Example 15.6 of the book"""
        self.assertAlmostEqual(put_eur_bs(s=42, k=40, r=0.1, sig=0.2, t=0.5), 0.81, 2)

    def test_call_eur_bs(self):
        """Example 15.6 of the book"""
        self.assertAlmostEqual(call_eur_bs(s=42, k=40, r=0.1, sig=0.2, t=0.5), 4.76, 2)