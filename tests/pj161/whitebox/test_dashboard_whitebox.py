"""
White-Box Tests for Dashboard Aggregation Service
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Statement, Branch, and Loop Coverage
"""

import unittest
import tempfile
from pathlib import Path
from models.article import NewsArticle
from services.news_service import NewsService
from services.alert_service import AlertService
from services.trend_service import TrendService
from services.dashboard_service import DashboardService


class TestDashboardWhitebox(unittest.TestCase):
    """White-box testing covering internal metric computation loops and branches in DashboardService."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.news_service = NewsService(articles_file=base / "art.json", sources_file=base / "src.json")
        self.alert_service = AlertService(rules_file=base / "rul.json", alerts_file=base / "alt.json")
        self.trend_service = TrendService()
        self.dashboard_service = DashboardService(
            news_service=self.news_service,
            alert_service=self.alert_service,
            trend_service=self.trend_service
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_wb_dsh_01_sentiment_unknown_fallback_branch(self):
        """TC-WB-DSH-01: Branch in sentiment aggregator when article has unrecognised sentiment label."""
        art = NewsArticle(
            headline="Headline Test",
            source_name="Source Test",
            article_url="http://test.com/1",
            sentiment="UnknownTone"
        )
        self.news_service.articles.append(art)
        metrics = self.dashboard_service.get_dashboard_metrics()
        # Unrecognised tone falls back to Neutral bucket
        self.assertEqual(metrics["sentiment"]["Neutral"], 1)

    def test_tc_wb_dsh_02_metrics_truncation_limits(self):
        """TC-WB-DSH-02: Statements slicing top 5 categories, top 5 sources, top 10 trends, and latest 5."""
        # Append 10 sample articles from 10 different sources
        for i in range(10):
            self.news_service.articles.append(
                NewsArticle(
                    headline=f"Headline Number {i} with Quantum Term",
                    source_name=f"Source {i}",
                    article_url=f"http://src{i}.com",
                    category="Science" if i % 2 == 0 else "Technology"
                )
            )

        metrics = self.dashboard_service.get_dashboard_metrics()
        self.assertLessEqual(len(metrics["top_sources"]), 5)
        self.assertLessEqual(len(metrics["top_categories"]), 5)
        self.assertLessEqual(len(metrics["latest_articles"]), 5)
        self.assertLessEqual(len(metrics["trending_keywords"]), 10)


if __name__ == "__main__":
    unittest.main()
