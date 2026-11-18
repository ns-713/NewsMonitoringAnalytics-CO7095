"""
Black-Box Tests for Trending Topics and Keyword Analytics
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Techniques: Frequency Analysis, Stop Word Filtering, Trend Comparison
"""

import unittest
from models.article import NewsArticle
from services.trend_service import TrendService


class TestTrendBlackbox(unittest.TestCase):
    """Black-box test suite for keyword frequency and trending topics."""

    def setUp(self):
        self.service = TrendService()
        self.articles = [
            NewsArticle(
                headline="Quantum Computing Breakthrough in Material Science",
                description="Quantum processors demonstrate novel chemistry simulation.",
                source_name="Nature",
                article_url="http://nature.com/1",
                category="Science",
                publication_date="2026-10-01"
            ),
            NewsArticle(
                headline="Quantum Cryptography Secures Cloud Banking",
                description="Quantum encryption deployed for banking transactions.",
                source_name="TechDaily",
                article_url="http://tech.com/2",
                category="Technology",
                publication_date="2026-10-01"
            ),
            NewsArticle(
                headline="Central Bank Inflation Rates Report",
                description="Inflation cooling across wholesale markets.",
                source_name="Reuters",
                article_url="http://reuters.com/3",
                category="Business",
                publication_date="2026-10-05"
            )
        ]

    def test_tc_bb_trd_01_top_trending_keywords(self):
        """TC-BB-TRD-01: Frequency count of non-stop keywords."""
        trends = self.service.get_keyword_frequencies(self.articles, top_n=5)
        self.assertTrue(len(trends) > 0)
        # "quantum" appears 4 times across headlines and descriptions
        top_kw, count = trends[0]
        self.assertEqual(top_kw, "quantum")
        self.assertEqual(count, 4)

    def test_tc_bb_trd_02_stop_words_exclusion(self):
        """TC-BB-TRD-02: Common English stop words like 'in', 'and', 'the' are excluded."""
        trends = dict(self.service.get_keyword_frequencies(self.articles, top_n=20))
        for stop_word in ["in", "and", "the", "for", "across", "of"]:
            self.assertNotIn(stop_word, trends)

    def test_tc_bb_trd_03_category_frequencies(self):
        """TC-BB-TRD-03: Category distribution counting."""
        cats = self.service.get_category_frequencies(self.articles)
        self.assertEqual(cats["Science"], 1)
        self.assertEqual(cats["Technology"], 1)
        self.assertEqual(cats["Business"], 1)

    def test_tc_bb_trd_04_date_filtered_trending(self):
        """TC-BB-TRD-04: Trends filtered by specific date."""
        oct_first_trends = dict(self.service.get_trending_by_date(self.articles, "2026-10-01"))
        self.assertIn("quantum", oct_first_trends)
        self.assertNotIn("inflation", oct_first_trends)

    def test_tc_bb_trd_05_trend_comparison_between_periods(self):
        """TC-BB-TRD-05: Comparison between two sets of articles."""
        period1 = [self.articles[0]]
        period2 = [self.articles[1], self.articles[2]]
        comp = self.service.compare_trends(period1, period2)
        self.assertEqual(comp["period1_total"], 1)
        self.assertEqual(comp["period2_total"], 2)
        self.assertIsInstance(comp["comparison"], list)


if __name__ == "__main__":
    unittest.main()
