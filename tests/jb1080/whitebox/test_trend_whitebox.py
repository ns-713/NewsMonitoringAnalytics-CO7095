"""
White-Box Tests for Trending Topics Logic
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Techniques: Statement, Branch, and Loop Testing
"""

import unittest
from models.article import NewsArticle
from services.trend_service import TrendService


class TestTrendWhitebox(unittest.TestCase):
    """White-box branch and loop coverage testing of TrendService."""

    def setUp(self):
        self.service = TrendService()

    def test_tc_wb_trd_01_extract_keywords_branches(self):
        """TC-WB-TRD-01: Branch coverage in extract_keywords for numbers, short words, and punctuation."""
        self.assertEqual(self.service.extract_keywords(""), [])
        self.assertEqual(self.service.extract_keywords(None), [])

        # Filter out 1-2 letter words and pure numbers
        tokens = self.service.extract_keywords("A to 123 4567 quantum AI algorithm.")
        self.assertIn("quantum", tokens)
        self.assertIn("algorithm", tokens)
        self.assertNotIn("123", tokens)
        self.assertNotIn("4567", tokens)

    def test_tc_wb_trd_02_use_content_flag_branch(self):
        """TC-WB-TRD-02: Branch in get_keyword_frequencies testing use_content=True vs False."""
        art = NewsArticle(
            headline="Headline Word Alpha",
            description="Description Word Beta",
            content="Content Word Gamma",
            source_name="S1",
            article_url="http://s1.com"
        )
        freq_without = dict(self.service.get_keyword_frequencies([art], use_content=False))
        self.assertIn("alpha", freq_without)
        self.assertIn("beta", freq_without)
        self.assertNotIn("gamma", freq_without)

        freq_with = dict(self.service.get_keyword_frequencies([art], use_content=True))
        self.assertIn("gamma", freq_with)

    def test_tc_wb_trd_03_compare_trends_zero_delta(self):
        """TC-WB-TRD-03: Branch coverage in compare_trends with equal frequencies."""
        art1 = NewsArticle(headline="Constant Topic", source_name="S", article_url="http://a.com")
        art2 = NewsArticle(headline="Constant Topic", source_name="S", article_url="http://b.com")

        res = self.service.compare_trends([art1], [art2])
        self.assertEqual(res["period1_total"], 1)
        self.assertEqual(res["period2_total"], 1)
        comp = res["comparison"]
        self.assertTrue(any(c["keyword"] == "constant" and c["change"] == 0 for c in comp))


if __name__ == "__main__":
    unittest.main()
