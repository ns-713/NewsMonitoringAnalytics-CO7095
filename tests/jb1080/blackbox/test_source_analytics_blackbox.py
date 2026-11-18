"""
Black-Box Tests for News Source Analytics
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Techniques: Descriptive Statistics, Percentage Distributions, Profile Segmentation
"""

import unittest
from models.article import NewsArticle
from services.source_analytics_service import SourceAnalyticsService


class TestSourceAnalyticsBlackbox(unittest.TestCase):
    """Black-box test suite for source distributions, category breakdown, and tone profiles."""

    def setUp(self):
        self.articles = [
            NewsArticle(headline="A1", source_name="BBC News", article_url="http://a1.com", category="Politics", sentiment="Positive"),
            NewsArticle(headline="A2", source_name="BBC News", article_url="http://a2.com", category="Politics", sentiment="Negative"),
            NewsArticle(headline="A3", source_name="BBC News", article_url="http://a3.com", category="Business", sentiment="Neutral"),
            NewsArticle(headline="A4", source_name="Reuters", article_url="http://a4.com", category="Technology", sentiment="Positive"),
            NewsArticle(headline="A5", source_name="Reuters", article_url="http://a5.com", category="Technology", sentiment="Positive")
        ]

    def test_tc_bb_srcan_01_source_counts(self):
        """TC-BB-SRCAN-01: Verification of article counts per source."""
        counts = SourceAnalyticsService.get_source_counts(self.articles)
        self.assertEqual(counts["BBC News"], 3)
        self.assertEqual(counts["Reuters"], 2)

    def test_tc_bb_srcan_02_source_percentage_distribution(self):
        """TC-BB-SRCAN-02: Verification that source percentage shares sum to 100%."""
        dist = SourceAnalyticsService.get_source_distribution(self.articles)
        self.assertEqual(len(dist), 2)
        total_pct = sum(item["percentage"] for item in dist)
        self.assertAlmostEqual(total_pct, 100.0, places=1)
        self.assertEqual(dist[0]["source"], "BBC News")
        self.assertEqual(dist[0]["percentage"], 60.0)

    def test_tc_bb_srcan_03_category_distribution_per_source(self):
        """TC-BB-SRCAN-03: Category counts grouped by source."""
        cat_dist = SourceAnalyticsService.get_category_distribution_by_source(self.articles)
        self.assertEqual(cat_dist["BBC News"]["Politics"], 2)
        self.assertEqual(cat_dist["BBC News"]["Business"], 1)
        self.assertEqual(cat_dist["Reuters"]["Technology"], 2)

    def test_tc_bb_srcan_04_sentiment_distribution_per_source(self):
        """TC-BB-SRCAN-04: Sentiment proportions per source."""
        sent_dist = SourceAnalyticsService.get_sentiment_distribution_by_source(self.articles)
        bbc = sent_dist["BBC News"]
        self.assertEqual(bbc["positive"], 1)
        self.assertEqual(bbc["negative"], 1)
        self.assertEqual(bbc["neutral"], 1)
        self.assertEqual(bbc["total"], 3)

        reuters = sent_dist["Reuters"]
        self.assertEqual(reuters["positive"], 2)
        self.assertEqual(reuters["positive_pct"], 100.0)

    def test_tc_bb_srcan_05_empty_article_list_handling(self):
        """TC-BB-SRCAN-05: Empty collection returns empty distribution safely."""
        dist = SourceAnalyticsService.get_source_distribution([])
        self.assertEqual(dist, [])


if __name__ == "__main__":
    unittest.main()
