"""
Integration Tests: Keyword Monitoring and Alert Pipeline
Verifies coordination between NewsService ingestion and AlertService rule matching.
Shared Integration Test Suite
"""

import unittest
import tempfile
from pathlib import Path
from services.news_service import NewsService
from services.alert_service import AlertService


class TestMonitoringAlertIntegration(unittest.TestCase):
    """Integration test suite covering article ingestion and automated alert triggering."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.art_file = base / "articles.json"
        self.src_file = base / "sources.json"
        self.rules_file = base / "rules.json"
        self.alerts_file = base / "alerts.json"

        self.alert_service = AlertService(rules_file=self.rules_file, alerts_file=self.alerts_file)
        self.news_service = NewsService(
            articles_file=self.art_file,
            sources_file=self.src_file,
            alert_service=self.alert_service
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_int_03_ingestion_spawns_keyword_alert(self):
        """TC-INT-03: Setting rule for 'semiconductor' automatically raises alert upon article ingestion."""
        self.alert_service.add_rule(keyword="semiconductor", description="Track chip news")

        # Ingest matching article
        ok, _, art = self.news_service.add_article(
            headline="Global Semiconductor Production Reaches New High",
            source_name="TechDaily",
            article_url="http://tech.com/chips"
        )
        self.assertTrue(ok)

        # Confirm alert was generated and persisted
        alerts = self.alert_service.get_alerts()
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].keyword, "semiconductor")
        self.assertEqual(alerts[0].article_id, art.article_id)
        self.assertEqual(alerts[0].status, "UNREAD")


if __name__ == "__main__":
    unittest.main()
