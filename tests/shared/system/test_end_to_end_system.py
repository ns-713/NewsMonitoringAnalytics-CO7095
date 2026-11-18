"""
System Tests: Complete End-to-End Workflow Verification
Simulates entire user journey: Demo Data Loading -> Search & Filtering -> Alert Triggering & Review -> CSV Export
Shared System Test Suite
"""

import unittest
import tempfile
from pathlib import Path
from services.news_service import NewsService
from services.search_service import SearchService
from services.alert_service import AlertService
from services.trend_service import TrendService
from services.report_service import ReportService
from services.dashboard_service import DashboardService


class TestEndToEndSystem(unittest.TestCase):
    """End-to-end full system lifecycle test."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.art_file = base / "articles.json"
        self.src_file = base / "sources.json"
        self.rules_file = base / "rules.json"
        self.alerts_file = base / "alerts.json"
        self.export_dir = base / "reports"

        self.alert_service = AlertService(rules_file=self.rules_file, alerts_file=self.alerts_file)
        self.trend_service = TrendService()
        self.report_service = ReportService(export_dir=self.export_dir)
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

    def test_tc_sys_01_complete_lifecycle(self):
        """TC-SYS-01: Verifies complete system lifecycle without runtime exceptions."""
        # 1. Setup active monitoring rules
        self.alert_service.add_rule(keyword="climate", description="Track climate news")
        self.alert_service.add_rule(keyword="artificial intelligence", description="Track AI")

        # 2. Ingest offline demo dataset
        ok, msg, count = self.news_service.load_demo_data()
        self.assertTrue(ok)
        self.assertGreaterEqual(count, 100)

        # 3. Verify Dashboard Metrics
        metrics = self.dashboard_service.get_dashboard_metrics()
        self.assertEqual(metrics["total_articles"], count)
        self.assertGreater(metrics["total_alerts"], 0)
        self.assertGreater(metrics["unread_alerts"], 0)
        self.assertGreater(metrics["sentiment"]["Positive"], 0)
        self.assertGreater(metrics["sentiment"]["Negative"], 0)

        # 4. Search and Filter Operations
        search_res = SearchService.search_headline(self.news_service.get_all_articles(), "quantum")
        self.assertGreater(len(search_res), 0)

        filter_res = SearchService.filter_by_category(self.news_service.get_all_articles(), "Technology")
        self.assertGreater(len(filter_res), 0)

        # 5. Alert Management: Acknowledge alerts
        unread_before = len(self.alert_service.get_alerts(unread_only=True))
        cleared_count = self.alert_service.mark_all_alerts_read()
        self.assertEqual(cleared_count, unread_before)
        self.assertEqual(len(self.alert_service.get_alerts(unread_only=True)), 0)

        # 6. Reporting and CSV Export
        articles = self.news_service.get_all_articles()
        p1 = self.report_service.export_articles_csv(articles)
        self.assertTrue(p1.exists())
        self.assertGreater(p1.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
