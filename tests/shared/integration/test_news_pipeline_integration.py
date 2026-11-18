"""
Integration Tests: End-to-End News Ingestion Pipeline
Verifies coordination between NewsService, CategorisationService, SentimentService, DuplicateService, and Storage.
Shared Integration Test Suite
"""

import unittest
import tempfile
from pathlib import Path
from services.news_service import NewsService
from services.categorisation_service import CategorisationService
from services.sentiment_service import SentimentService
from services.duplicate_service import DuplicateService
from services.alert_service import AlertService


class TestNewsPipelineIntegration(unittest.TestCase):
    """Integration test suite covering article intake, enrichment, and duplicate prevention."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.art_file = base / "articles.json"
        self.src_file = base / "sources.json"
        self.rules_file = base / "rules.json"
        self.alerts_file = base / "alerts.json"

        self.cat_svc = CategorisationService()
        self.sent_svc = SentimentService()
        self.dup_svc = DuplicateService()
        self.alert_svc = AlertService(rules_file=self.rules_file, alerts_file=self.alerts_file)

        self.news_svc = NewsService(
            articles_file=self.art_file,
            sources_file=self.src_file,
            categorisation_service=self.cat_svc,
            sentiment_service=self.sent_svc,
            duplicate_service=self.dup_svc,
            alert_service=self.alert_svc
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_int_01_manual_article_automatic_enrichment(self):
        """TC-INT-01: Manual article addition automatically determines category and sentiment score."""
        ok, msg, art = self.news_svc.add_article(
            headline="Hospital Doctors Announce Successful Cancer Vaccine Breakthrough",
            source_name="Medical Journal",
            article_url="http://medjournal.org/art1"
        )
        self.assertTrue(ok)
        self.assertIsNotNone(art)
        self.assertEqual(art.category, "Health")
        self.assertEqual(art.sentiment, "Positive")
        self.assertGreater(art.sentiment_score, 0)
        self.assertTrue(self.art_file.exists())

    def test_tc_int_02_duplicate_prevention_blocks_insertion(self):
        """TC-INT-02: Pipeline blocks near-duplicate article and preserves database count."""
        # Insert initial article
        ok1, _, _ = self.news_svc.add_article(
            headline="Central Bank Decreases Benchmark Interest Rates",
            source_name="Financial News",
            article_url="http://finnews.org/rates"
        )
        self.assertTrue(ok1)
        self.assertEqual(len(self.news_svc.get_all_articles()), 1)

        # Attempt to insert identical URL duplicate
        ok2, msg2, _ = self.news_svc.add_article(
            headline="Different Title on Rates",
            source_name="Wire News",
            article_url="http://finnews.org/rates"
        )
        self.assertFalse(ok2)
        self.assertIn("Duplicate detected", msg2)
        self.assertEqual(len(self.news_svc.get_all_articles()), 1)


if __name__ == "__main__":
    unittest.main()
