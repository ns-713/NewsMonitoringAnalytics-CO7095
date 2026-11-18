"""
Black-Box Tests for Reporting and CSV Export Service
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Boundary Testing, Format Verification, Output Schema Testing
"""

import unittest
import tempfile
import csv
from pathlib import Path
from models.article import NewsArticle
from models.alert import Alert
from services.report_service import ReportService


class TestReportBlackbox(unittest.TestCase):
    """Black-box test suite for CSV report export generation."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.export_dir = Path(self.temp_dir.name)
        self.service = ReportService(export_dir=self.export_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_bb_rep_01_export_articles_csv(self):
        """TC-BB-REP-01: Verifies articles CSV header structure and row values."""
        articles = [
            NewsArticle(
                headline="Breakthrough in Solar Cells",
                source_name="EcoNews",
                article_url="http://eco.com/1",
                category="Environment",
                sentiment="Positive",
                sentiment_score=3,
                publication_date="2026-10-10"
            )
        ]
        csv_path = self.service.export_articles_csv(articles, "test_articles.csv")
        self.assertTrue(csv_path.exists())

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, [
                "article_id", "headline", "source_name", "category",
                "sentiment", "sentiment_score", "publication_date", "article_url"
            ])
            row = next(reader)
            self.assertEqual(row[1], "Breakthrough in Solar Cells")
            self.assertEqual(row[2], "EcoNews")
            self.assertEqual(row[3], "Environment")
            self.assertEqual(row[4], "Positive")
            self.assertEqual(row[5], "3")

    def test_tc_bb_rep_02_export_category_distribution_csv(self):
        """TC-BB-REP-02: Verifies category distribution CSV export."""
        cat_counts = {"Technology": 15, "Politics": 10, "Science": 5}
        csv_path = self.service.export_category_distribution_csv(cat_counts, "test_cats.csv")
        self.assertTrue(csv_path.exists())

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, ["Category", "Article Count", "Percentage"])
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            # 15 / 30 = 50.0%
            self.assertEqual(rows[0], ["Technology", "15", "50.0%"])

    def test_tc_bb_rep_03_export_trending_topics_csv(self):
        """TC-BB-REP-03: Verifies trending topics CSV ranking export."""
        trends = [("quantum", 25), ("climate", 18), ("election", 12)]
        csv_path = self.service.export_trending_topics_csv(trends, "test_trends.csv")
        self.assertTrue(csv_path.exists())

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, ["Rank", "Trending Keyword", "Frequency Count"])
            rows = list(reader)
            self.assertEqual(rows[0], ["1", "quantum", "25"])
            self.assertEqual(rows[1], ["2", "climate", "18"])

    def test_tc_bb_rep_04_export_alerts_csv(self):
        """TC-BB-REP-04: Verifies alerts CSV log export."""
        alerts = [
            Alert(
                rule_id="RUL-01",
                keyword="cybersecurity",
                article_id="ART-100",
                headline="Critical Patch Released"
            )
        ]
        csv_path = self.service.export_alerts_csv(alerts, "test_alerts.csv")
        self.assertTrue(csv_path.exists())

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertIn("Matched Keyword", header)
            row = next(reader)
            self.assertEqual(row[2], "cybersecurity")
            self.assertEqual(row[4], "Critical Patch Released")


if __name__ == "__main__":
    unittest.main()
