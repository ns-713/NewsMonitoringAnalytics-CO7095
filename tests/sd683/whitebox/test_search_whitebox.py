"""
White-Box Tests for Search and Filtering Logic
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Techniques: Statement, Branch, and Condition Testing
"""

import unittest
from models.article import NewsArticle
from services.search_service import SearchService


class TestSearchWhitebox(unittest.TestCase):
    """White-box branch coverage testing of SearchService."""

    def setUp(self):
        self.articles = [
            NewsArticle(
                headline="AI Algorithm Breakthrough",
                source_name="TechDaily",
                article_url="https://techdaily.com/1",
                description="Short summary",
                content="Deep learning optimization body",
                category="Technology",
                sentiment="Positive",
                publication_date="2026-10-01",
                keywords=["ai", "algorithm"]
            ),
            NewsArticle(
                headline="Market Downturn and Deficit",
                source_name="Financial Gazette",
                article_url="https://gazette.com/1",
                description="Fiscal deficit warning",
                content="Stock drop analysis",
                category="Business",
                sentiment="Negative",
                publication_date="2026-10-15",
                keywords=["deficit", "market"]
            )
        ]

    def test_tc_wb_sea_01_search_content_branches(self):
        """TC-WB-SEA-01: Branch coverage of search_content with match in content vs description."""
        # Match in content
        r1 = SearchService.search_content(self.articles, "optimization")
        self.assertEqual(len(r1), 1)

        # Match in description
        r2 = SearchService.search_content(self.articles, "fiscal")
        self.assertEqual(len(r2), 1)

        # Empty query branch
        r3 = SearchService.search_content(self.articles, "   ")
        self.assertEqual(len(r3), 2)

    def test_tc_wb_sea_02_filter_by_source_branches(self):
        """TC-WB-SEA-02: Branch coverage of filter_by_source."""
        # Empty source branch
        self.assertEqual(len(SearchService.filter_by_source(self.articles, "")), 2)
        # Valid source
        self.assertEqual(len(SearchService.filter_by_source(self.articles, "TechDaily")), 1)
        # Non-matching source
        self.assertEqual(len(SearchService.filter_by_source(self.articles, "NonExistent")), 0)

    def test_tc_wb_sea_03_filter_by_date_range_branches(self):
        """TC-WB-SEA-03: Branch coverage of filter_by_date_range."""
        # Start date only
        r1 = SearchService.filter_by_date_range(self.articles, start_date="2026-10-10")
        self.assertEqual(len(r1), 1)

        # End date only
        r2 = SearchService.filter_by_date_range(self.articles, end_date="2026-10-10")
        self.assertEqual(len(r2), 1)

        # Both start and end
        r3 = SearchService.filter_by_date_range(self.articles, start_date="2026-10-01", end_date="2026-10-31")
        self.assertEqual(len(r3), 2)

        # Out of bounds
        r4 = SearchService.filter_by_date_range(self.articles, start_date="2026-11-01")
        self.assertEqual(len(r4), 0)

    def test_tc_wb_sea_04_combined_filter_branch_permutations(self):
        """TC-WB-SEA-04: Multi-branch testing in combined_filter."""
        # All filters set to "All" or None
        r_all = SearchService.combined_filter(
            self.articles,
            query=None,
            source=None,
            category="All",
            sentiment="All"
        )
        self.assertEqual(len(r_all), 2)

        # Category and sentiment branches
        r_cat = SearchService.combined_filter(self.articles, category="Technology")
        self.assertEqual(len(r_cat), 1)

        r_sent = SearchService.combined_filter(self.articles, sentiment="Negative")
        self.assertEqual(len(r_sent), 1)


if __name__ == "__main__":
    unittest.main()
