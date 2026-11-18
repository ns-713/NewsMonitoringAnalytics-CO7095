"""
White-Box Tests for MainMenu Navigation and Actions
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Statement and Branch Testing with Mocked Terminal Input
"""

import unittest
import tempfile
import io
import sys
from pathlib import Path
from unittest.mock import patch
from interface.menu import MainMenu
from models.article import NewsArticle


class TestMenuWhitebox(unittest.TestCase):
    """White-box testing covering menu action methods in MainMenu."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.menu = MainMenu()
        # Redirect storage files to temporary directory
        self.menu.news_service.articles_file = base / "art.json"
        self.menu.news_service.sources_file = base / "src.json"
        self.menu.alert_service.rules_file = base / "rul.json"
        self.menu.alert_service.alerts_file = base / "alt.json"
        self.menu.report_service.export_dir = base / "reports"

        # Suppress terminal prints during menu test execution
        self.captured_out = io.StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.captured_out

    def tearDown(self):
        sys.stdout = self.old_stdout
        self.temp_dir.cleanup()

    def test_tc_wb_mnu_01_dashboard_and_reports_execution(self):
        """TC-WB-MNU-01: Exercises show_dashboard, generate_reports, and export_csv."""
        with patch("builtins.input", side_effect=["1", "B", "1"]):
            self.menu.show_dashboard()
            self.menu.generate_reports()

            # Add article and test export
            self.menu.news_service.add_article(
                headline="Sample Quantum Article for Menu",
                source_name="TestSource",
                article_url="http://test.com/q1"
            )
            self.menu.export_csv()
            self.menu.view_categories()
            self.menu.show_time_analytics()

    def test_tc_wb_mnu_02_view_all_news_back(self):
        """TC-WB-MNU-02: Exercises view_all_news with mocked 'B' back command."""
        self.menu.news_service.add_article(
            headline="Article For Pagination",
            source_name="Src",
            article_url="http://src.com/pag1"
        )
        with patch("builtins.input", side_effect=["B"]):
            self.menu.view_all_news()

    def test_tc_wb_mnu_03_manage_sources_back(self):
        """TC-WB-MNU-03: Exercises manage_news_sources with mocked 'B' exit."""
        with patch("builtins.input", side_effect=["B"]):
            self.menu.manage_news_sources()

    def test_tc_wb_mnu_04_manage_rules_back(self):
        """TC-WB-MNU-04: Exercises manage_keyword_monitoring with mocked 'B' exit."""
        with patch("builtins.input", side_effect=["B"]):
            self.menu.manage_keyword_monitoring()

    def test_tc_wb_mnu_05_view_alerts_back(self):
        """TC-WB-MNU-05: Exercises view_alerts with mocked 'B' exit."""
        with patch("builtins.input", side_effect=["B"]):
            self.menu.view_alerts()

    def test_tc_wb_mnu_06_data_management_back(self):
        """TC-WB-MNU-06: Exercises data_management options."""
        with patch("builtins.input", side_effect=["1"]):  # Option 1: validate
            self.menu.data_management()
        with patch("builtins.input", side_effect=["2"]):  # Option 2: backup
            self.menu.data_management()


if __name__ == "__main__":
    unittest.main()
