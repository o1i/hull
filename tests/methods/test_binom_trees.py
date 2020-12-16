import unittest

from methods.binom_trees import put_eur_binom_tree, call_eur_binom_tree


class TestBlackScholes(unittest.TestCase):
    def test_put_eur_bs(self):
        """Example 15.6 of the book"""
        self.assertAlmostEqual(put_eur_binom_tree(s=42, k=40, r=0.1, sig=0.2, t=0.5, n=100), 0.81, 2)

    def test_call_eur_bs(self):
        """Example 15.6 of the book"""
        self.assertAlmostEqual(call_eur_binom_tree(s=42, k=40, r=0.1, sig=0.2, t=0.5, n=100), 4.76, 2)
