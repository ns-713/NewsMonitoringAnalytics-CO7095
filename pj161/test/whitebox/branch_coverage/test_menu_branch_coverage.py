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

    def test_tc_wb_mnu_branch_search_news_branches(self):
        """TC-WB-MNU-B07: Tests search_news with various field targets and empty results."""
        self.menu.news_service.add_article(
            headline="Artificial Intelligence in Healthcare",
            source_name="HealthNews",
            article_url="http://health.org/ai",
            content="Deep learning algorithms are transforming diagnostic accuracy in medicine."
        )
        # Search in Headline
        with patch("builtins.input", side_effect=["Artificial", "Headline"]):
            self.menu.search_news()

        # Search in Content
        with patch("builtins.input", side_effect=["algorithms", "Content"]):
            self.menu.search_news()

        # Search in Keywords
        with patch("builtins.input", side_effect=["Medicine", "Keywords"]):
            self.menu.search_news()

        # Search in All
        with patch("builtins.input", side_effect=["Intelligence", "All"]):
            self.menu.search_news()

        # Empty search term
        with patch("builtins.input", side_effect=["", "All"]):
            self.menu.search_news()

    def test_tc_wb_mnu_branch_filter_news_branches(self):
        """TC-WB-MNU-B08: Tests filter_news multi-criteria filtering."""
        self.menu.news_service.add_article(
            headline="Stock Market Closes at Record High",
            source_name="Bloomberg",
            article_url="http://bloomberg.com/record",
            category="Business",
            publication_date="2026-11-20"
        )
        # Filter with specific parameters
        with patch("builtins.input", side_effect=["Bloomberg", "Business", "Positive", "2026-11-01", "2026-11-30"]):
            self.menu.filter_news()

        # Filter with empty / default parameters
        with patch("builtins.input", side_effect=["", "All", "All", "", ""]):
            self.menu.filter_news()

    def test_tc_wb_mnu_branch_analytics_views(self):
        """TC-WB-MNU-B09: Tests view_categories, sentiment, trending, sources, and time analytics."""
        self.menu.news_service.add_article(
            headline="Global Tech Summit Discusses Green Energy",
            source_name="TechWire",
            article_url="http://techwire.com/green",
            category="Technology",
            publication_date="2026-11-22"
        )
        # View categories
        self.menu.view_categories()

        # Sentiment analytics: test custom text analysis (T) then Back (B)
        with patch("builtins.input", side_effect=["T", "Outstanding profit and remarkable success", "B"]):
            self.menu.show_sentiment_analytics()

        # Trending topics: with and without date filter
        with patch("builtins.input", side_effect=["y", "2026-11-22"]):
            self.menu.show_trending_topics()
        with patch("builtins.input", side_effect=["n"]):
            self.menu.show_trending_topics()

        # Source analytics
        self.menu.show_source_analytics()

        # Time analytics: Daily (1), Weekly (2), Monthly (3)
        with patch("builtins.input", side_effect=["1"]):
            self.menu.show_time_analytics()
        with patch("builtins.input", side_effect=["2"]):
            self.menu.show_time_analytics()
        with patch("builtins.input", side_effect=["3"]):
            self.menu.show_time_analytics()

        # Duplicate detection
        self.menu.show_duplicate_detection()

    def test_tc_wb_mnu_branch_export_and_demo(self):
        """TC-WB-MNU-B10: Tests export_csv, load_demo_dataset, and empty state fallbacks."""
        # Empty storage export
        self.menu.export_csv()

        # Add article and export
        self.menu.news_service.add_article(
            headline="Exportable Headline Test",
            source_name="SourceX",
            article_url="http://sourcex.com/exp1"
        )
        self.menu.export_csv()

        # Load demo dataset: confirmed (y) and rejected (n)
        with patch("builtins.input", side_effect=["y"]):
            self.menu.load_demo_dataset()
        with patch("builtins.input", side_effect=["n"]):
            self.menu.load_demo_dataset()

    def test_tc_wb_mnu_branch_rss_modes_and_manual_add(self):
        """TC-WB-MNU-B11: Tests collect_news_from_rss modes and add_news_manually."""
        # RSS mode 0: Back
        with patch("builtins.input", side_effect=["0"]):
            self.menu.collect_news_from_rss()

        # RSS mode 3: Offline demo
        with patch("builtins.input", side_effect=["3"]):
            self.menu.collect_news_from_rss()

        # RSS mode 1 with no sources registered
        with patch("builtins.input", side_effect=["1"]):
            self.menu.collect_news_from_rss()

        # Add news manually: successful addition
        with patch("builtins.input", side_effect=[
            "Quantum Processor Unveiled",
            "Revolutionary chip architecture.",
            "Full article body about computing.",
            "MIT Tech",
            "https://mit.edu",
            "https://mit.edu/chip1",
            "Technology",
            "2026-11-25",
            "quantum, chip"
        ]):
            self.menu.add_news_manually()

    def test_tc_wb_mnu_branch_inspect_and_main_loop(self):
        """TC-WB-MNU-B12: Tests inspect_article and main run event loop branching."""
        ok, msg, art = self.menu.news_service.add_article(
            headline="Inspectable Article Headline",
            source_name="SourceAlpha",
            article_url="http://alpha.org/art1"
        )
        self.assertTrue(ok)
        self.assertIsNotNone(art)
        # Inspect valid ID
        self.menu.inspect_article(art.article_id)

        # Inspect non-existent ID
        self.menu.inspect_article("NONEXISTENT_9999")

        # Main loop: test invalid option '99' then exit '0' with confirm 'y'
        with patch("builtins.input", side_effect=["99", "0", "y"]):
            self.menu.run()


if __name__ == "__main__":
    unittest.main()
