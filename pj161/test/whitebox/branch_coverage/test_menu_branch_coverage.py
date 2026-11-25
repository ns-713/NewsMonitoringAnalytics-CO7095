"""
White-Box Branch Coverage Tests for MainMenu Navigation and Submenus
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Decision / Branch Coverage across all interactive CLI submenus
"""

import unittest
import tempfile
import io
import sys
from pathlib import Path
from unittest.mock import patch
from interface.menu import MainMenu
from models.article import NewsArticle


class TestMenuBranchCoverage(unittest.TestCase):
    """Deep branch coverage across all decision paths in MainMenu submenus."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.menu = MainMenu()
        self.menu.news_service.articles_file = base / "art.json"
        self.menu.news_service.sources_file = base / "src.json"
        self.menu.alert_service.rules_file = base / "rul.json"
        self.menu.alert_service.alerts_file = base / "alt.json"
        self.menu.report_service.export_dir = base / "reports"

        # Suppress stdout
        self.captured_out = io.StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.captured_out

    def tearDown(self):
        sys.stdout = self.old_stdout
        self.temp_dir.cleanup()

    def test_tc_wb_mnu_branch_sources_crud(self):
        """TC-WB-MNU-B01: Tests manage_news_sources branches (add, list, delete, back)."""
        # Branch: Option 1 (Add source) then 'B'
        with patch("builtins.input", side_effect=["1", "BBC World", "https://bbc.com/feed", "https://bbc.com", "General", "B"]):
            self.menu.manage_news_sources()

        # Branch: Option 2 (List sources) then 'B'
        with patch("builtins.input", side_effect=["2", "B"]):
            self.menu.manage_news_sources()

        # Branch: Option 3 (Remove source) then 'B'
        with patch("builtins.input", side_effect=["3", "1", "B"]):
            self.menu.manage_news_sources()

    def test_tc_wb_mnu_branch_rules_crud(self):
        """TC-WB-MNU-B02: Tests manage_keyword_monitoring branches (add rule, list, delete, back)."""
        # Branch: Option 1 (Add rule) then 'B'
        with patch("builtins.input", side_effect=["1", "MarketAlert", "crypto,stocks", "High", "Finance", "B"]):
            self.menu.manage_keyword_monitoring()

        # Branch: Option 2 (List rules) then 'B'
        with patch("builtins.input", side_effect=["2", "B"]):
            self.menu.manage_keyword_monitoring()

        # Branch: Option 3 (Remove rule) then 'B'
        with patch("builtins.input", side_effect=["3", "1", "B"]):
            self.menu.manage_keyword_monitoring()

    def test_tc_wb_mnu_branch_alerts_actions(self):
        """TC-WB-MNU-B03: Tests view_alerts branches (view all, unread, mark read, clear)."""
        self.menu.news_service.add_article(
            headline="Breaking Market Stocks News",
            source_name="Wire",
            article_url="http://wire.com/stocks1",
            content="Stocks rallied sharply."
        )

        # Branch 1: View all then 'B'
        with patch("builtins.input", side_effect=["1", "B"]):
            self.menu.view_alerts()

        # Branch 2: View unread then 'B'
        with patch("builtins.input", side_effect=["2", "B"]):
            self.menu.view_alerts()

        # Branch 3: Mark read then 'B'
        with patch("builtins.input", side_effect=["3", "B"]):
            self.menu.view_alerts()

        # Branch 4: Clear all alerts then 'B'
        with patch("builtins.input", side_effect=["4", "y", "B"]):
            self.menu.view_alerts()

    def test_tc_wb_mnu_branch_data_management_branches(self):
        """TC-WB-MNU-B04: Tests all sub-options of data_management."""
        # Option 1: Validate
        with patch("builtins.input", side_effect=["1"]):
            self.menu.data_management()

        # Option 2: Backup
        with patch("builtins.input", side_effect=["2"]):
            self.menu.data_management()

        # Option 3: Restore (aborted with 'n')
        with patch("builtins.input", side_effect=["3", "n"]):
            self.menu.data_management()

        # Option 4: Reset (aborted with 'n')
        with patch("builtins.input", side_effect=["4", "n"]):
            self.menu.data_management()

        # Option 0: Back
        with patch("builtins.input", side_effect=["0"]):
            self.menu.data_management()

    def test_tc_wb_mnu_branch_reports_generation_options(self):
        """TC-WB-MNU-B05: Tests generate_reports sub-options 1, 2, 3, 4."""
        self.menu.news_service.add_article(
            headline="Technology Market Report",
            source_name="TechDaily",
            article_url="http://t.org/1"
        )
        for opt in ["1", "2", "3", "4", "B"]:
            with patch("builtins.input", side_effect=[opt]):
                self.menu.generate_reports()

    def test_tc_wb_mnu_branch_view_all_news_pagination(self):
        """TC-WB-MNU-B06: Tests pagination navigation in view_all_news."""
        for i in range(12):
            self.menu.news_service.add_article(
                headline=f"Article Number {i} For Pagination Test",
                source_name="PagSource",
                article_url=f"http://test.com/pag/{i}"
            )
        with patch("builtins.input", side_effect=["N", "P", "B"]):
            self.menu.view_all_news()


if __name__ == "__main__":
    unittest.main()
