"""
White-Box Tests for Sentiment Analysis Service
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Techniques: Statement, Branch, and Boundary Coverage
"""

import unittest
from services.sentiment_service import SentimentService
from models.article import NewsArticle


class TestSentimentWhitebox(unittest.TestCase):
    """White-box testing covering internal scoring and classification branches."""

    def setUp(self):
        self.service = SentimentService()

    def test_tc_wb_sen_01_classify_score_all_three_branches(self):
        """TC-WB-SEN-01: Exercises all 3 paths in classify_score()."""
        # Branch 1: score > 0
        self.assertEqual(self.service.classify_score(5), "Positive")
        self.assertEqual(self.service.classify_score(1), "Positive")

        # Branch 2: score < 0
        self.assertEqual(self.service.classify_score(-5), "Negative")
        self.assertEqual(self.service.classify_score(-1), "Negative")

        # Branch 3: score == 0
        self.assertEqual(self.service.classify_score(0), "Neutral")

    def test_tc_wb_sen_02_tokenize_branches(self):
        """TC-WB-SEN-02: Branch coverage in tokenize() for empty vs populated strings."""
        self.assertEqual(self.service.tokenize(""), [])
        self.assertEqual(self.service.tokenize(None), [])
        tokens = self.service.tokenize("Hello, World! 123 Testing.")
        self.assertEqual(tokens, ["hello", "world", "123", "testing"])

    def test_tc_wb_sen_03_analyse_article_convenience_method(self):
        """TC-WB-SEN-03: Statements in analyse_article() updating model fields."""
        art = NewsArticle(
            headline="Massive Economic Growth and Win",
            source_name="Financial",
            article_url="http://news.com/1"
        )
        res = self.service.analyse_article(art)
        self.assertEqual(art.sentiment, "Positive")
        self.assertGreater(art.sentiment_score, 0)
        self.assertEqual(res["label"], "Positive")


if __name__ == "__main__":
    unittest.main()
