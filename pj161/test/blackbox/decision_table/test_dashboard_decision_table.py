"""
Black-Box Tests for Dashboard Service
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Boundary Testing, Aggregation Verification, State Summarisation
"""

import unittest
import tempfile
from pathlib import Path
from models.article import NewsArticle
from services.news_service import NewsService
from services.alert_service import AlertService
from services.trend_service import TrendService
from services.dashboard_service import DashboardService


class TestDashboardBlackbox(unittest.TestCase):
    """Black-box test suite for dashboard telemetry and metrics computation."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.art_file = base / "articles.json"
        self.src_file = base / "sources.json"
        self.rules_file = base / "rules.json"
        self.alerts_file = base / "alerts.json"

        self.alert_service = AlertService(rules_file=self.rules_file, alerts_file=self.alerts_file)
        self.trend_service = TrendService()
        self.news_service = NewsService(
            articles_file=self.art_file,
            sources_file=self.src_file,
            alert_service=self.alert_service
        )
        self.dashboard_service = DashboardService(
            news_service=self.news_service,
            alert_service=self.alert_service,
            trend_service=self.trend_service
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_bb_dsh_01_empty_dashboard_metrics(self):
        """TC-BB-DSH-01: Boundary test - Fresh repository returns zero-valued metrics safely."""
        metrics = self.dashboard_service.get_dashboard_metrics()
        self.assertEqual(metrics["total_articles"], 0)
        self.assertEqual(metrics["total_alerts"], 0)
        self.assertEqual(metrics["unread_alerts"], 0)
        self.assertEqual(metrics["sentiment"]["Positive"], 0)
        self.assertEqual(metrics["latest_articles"], [])

    def test_tc_bb_dsh_02_populated_dashboard_metrics(self):
        """TC-BB-DSH-02: Verifies telemetry when articles and rules are present."""
        self.alert_service.add_rule(keyword="fusion", description="Track fusion")
        self.news_service.add_article(
            headline="Nuclear Fusion Energy Milestone",
            source_name="Science Daily",
            article_url="http://sci.com/fusion"
        )

        metrics = self.dashboard_service.get_dashboard_metrics()
        self.assertEqual(metrics["total_articles"], 1)
        self.assertEqual(metrics["active_rules"], 1)
        self.assertEqual(metrics["total_alerts"], 1)
        self.assertEqual(metrics["unread_alerts"], 1)
        self.assertEqual(len(metrics["latest_articles"]), 1)


if __name__ == "__main__":
    unittest.main()
