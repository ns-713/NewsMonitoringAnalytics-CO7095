"""
Black-Box Tests for Rule-Based Sentiment Analysis
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Techniques: Equivalence Partitioning, Boundary Value Analysis
"""

import unittest
from services.sentiment_service import SentimentService


class TestSentimentBlackbox(unittest.TestCase):
    """Black-box test suite for lexical sentiment scoring and classification."""

    def setUp(self):
        self.service = SentimentService()

    def test_tc_bb_sen_01_positive_partition(self):
        """TC-BB-SEN-01: Text with positive polarity."""
        res = self.service.analyse_text("Massive economic growth, great success, and sustained innovation.")
        self.assertEqual(res["label"], "Positive")
        self.assertGreater(res["score"], 0)
        self.assertTrue(any(w in ["growth", "success", "innovation"] for w in res["positive_words"]))

    def test_tc_bb_sen_02_negative_partition(self):
        """TC-BB-SEN-02: Text with negative polarity."""
        res = self.service.analyse_text("Severe financial crisis, corporate bankruptcy, and extensive job loss.")
        self.assertEqual(res["label"], "Negative")
        self.assertLess(res["score"], 0)
        self.assertTrue(any(w in ["crisis", "bankruptcy", "loss"] for w in res["negative_words"]))

    def test_tc_bb_sen_03_neutral_zero_matches(self):
        """TC-BB-SEN-03: Neutral text with no matching lexicon tokens."""
        res = self.service.analyse_text("The committee convened at nine o'clock in the regional hall.")
        self.assertEqual(res["label"], "Neutral")
        self.assertEqual(res["score"], 0)
        self.assertEqual(res["positive_count"], 0)
        self.assertEqual(res["negative_count"], 0)

    def test_tc_bb_sen_04_neutral_balanced_boundary(self):
        """TC-BB-SEN-04: Boundary test where positive count equals negative count (Score = 0)."""
        # Contains 1 positive ("success") and 1 negative ("failure")
        res = self.service.analyse_text("The project observed both initial success and subsequent failure.")
        self.assertEqual(res["score"], 0)
        self.assertEqual(res["label"], "Neutral")
        self.assertEqual(res["positive_count"], 1)
        self.assertEqual(res["negative_count"], 1)

    def test_tc_bb_sen_05_punctuation_and_casing_insensitivity(self):
        """TC-BB-SEN-05: Punctuation stripping and uppercase handling."""
        res = self.service.analyse_text("VICTORY!!! OUTSTANDING SUCCESS, PROSPERITY???")
        self.assertEqual(res["label"], "Positive")
        self.assertGreaterEqual(res["positive_count"], 2)

    def test_tc_bb_sen_06_empty_string_input(self):
        """TC-BB-SEN-06: Empty text boundary."""
        res = self.service.analyse_text("")
        self.assertEqual(res["label"], "Neutral")
        self.assertEqual(res["score"], 0)


if __name__ == "__main__":
    unittest.main()
