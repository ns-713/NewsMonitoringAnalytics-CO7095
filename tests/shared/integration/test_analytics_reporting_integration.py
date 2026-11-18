"""
Integration Tests: Analytics Aggregation and Reporting Pipeline
Verifies coordination between NewsService data, TrendService, SourceAnalyticsService, and ReportService CSV output.
Shared Integration Test Suite
"""

import unittest
import tempfile
import csv
from pathlib import Path
from services.news_service import NewsService
from services.trend_service import TrendService
from services.source_analytics_service import SourceAnalyticsService
from services.time_analytics_service import TimeAnalyticsService
from services.report_service import ReportService


class TestAnalyticsReportingIntegration(unittest.TestCase):
    """Integration test suite covering stored data analytics aggregation and CSV generation."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.art_file = base / "articles.json"
        self.src_file = base / "sources.json"
        self.export_dir = base / "reports"

        self.news_service = NewsService(articles_file=self.art_file, sources_file=self.src_file)
        self.trend_service = TrendService()
        self.report_service = ReportService(export_dir=self.export_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_int_04_analytics_calculation_and_csv_generation(self):
        """TC-INT-04: Verifies analytics calculation and export from repository articles."""
        self.news_service.add_article(
            headline="Renewable Solar Energy Progress in Europe",
            source_name="EcoDaily",
            article_url="http://eco.com/1"
        )
        self.news_service.add_article(
            headline="Renewable Wind Farms Expand Generation",
            source_name="EcoDaily",
            article_url="http://eco.com/2"
        )

        articles = self.news_service.get_all_articles()
        self.assertEqual(len(articles), 2)

        # 1. Trends
        trends = self.trend_service.get_keyword_frequencies(articles, top_n=5)
        self.assertTrue(any(kw == "renewable" for kw, c in trends))

        # 2. Source distribution
        dist = SourceAnalyticsService.get_source_distribution(articles)
        self.assertEqual(dist[0]["source"], "EcoDaily")
        self.assertEqual(dist[0]["percentage"], 100.0)

        # 3. CSV Exports
        art_csv = self.report_service.export_articles_csv(articles, "test_int_art.csv")
        self.assertTrue(art_csv.exists())

        trend_csv = self.report_service.export_trending_topics_csv(trends, "test_int_trends.csv")
        self.assertTrue(trend_csv.exists())


if __name__ == "__main__":
    unittest.main()
