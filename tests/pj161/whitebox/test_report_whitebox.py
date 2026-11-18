"""
White-Box Tests for Reporting Service
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Statement and Branch Coverage
"""

import unittest
import tempfile
from pathlib import Path
from services.report_service import ReportService


class TestReportWhitebox(unittest.TestCase):
    """White-box testing covering all export methods in ReportService."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.service = ReportService(export_dir=Path(self.temp_dir.name))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_wb_rep_01_export_source_analytics_csv(self):
        """TC-WB-REP-01: Statement coverage of export_source_analytics_csv."""
        dist = [
            {"source": "BBC News", "article_count": 50, "percentage": 50.0},
            {"source": "Reuters", "article_count": 50, "percentage": 50.0}
        ]
        p = self.service.export_source_analytics_csv(dist, "source_test.csv")
        self.assertTrue(p.exists())

    def test_tc_wb_rep_02_export_duplicates_csv(self):
        """TC-WB-REP-02: Statement coverage of export_duplicates_csv."""
        dups = [{
            "article_a_id": "A1",
            "article_a_headline": "Title A",
            "article_a_source": "Src1",
            "article_b_id": "A2",
            "article_b_headline": "Title A",
            "article_b_source": "Src2",
            "reason": "Exact headline",
            "similarity": 1.0
        }]
        p = self.service.export_duplicates_csv(dups, "dup_test.csv")
        self.assertTrue(p.exists())

    def test_tc_wb_rep_03_export_time_trends_csv(self):
        """TC-WB-REP-03: Statement coverage of export_time_trends_csv."""
        daily_counts = {"2026-10-01": 10, "2026-10-02": 15}
        p = self.service.export_time_trends_csv(daily_counts, "time_test.csv")
        self.assertTrue(p.exists())


if __name__ == "__main__":
    unittest.main()
