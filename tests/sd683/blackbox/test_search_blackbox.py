"""
Black-Box Tests for News Search and Multi-Filtering
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Techniques: Equivalence Partitioning, Decision Table Testing, Combinatorial Filtering
"""

import unittest
from models.article import NewsArticle
from services.search_service import SearchService


class TestSearchBlackbox(unittest.TestCase):
    """Black-box test suite for headline, content, keyword, and combined filters."""

    def setUp(self):
        self.sample_articles = [
            NewsArticle(
                headline="Quantum Computing Breakthrough at Cambridge",
                source_name="Nature Scientific",
                article_url="https://nature.com/art1",
                description="Researchers unveil optical qubit processor.",
                content="Full physics review of quantum architecture.",
                category="Science",
                sentiment="Positive",
                publication_date="2026-10-01",
                keywords=["quantum", "computing", "breakthrough"]
            ),
            NewsArticle(
                headline="Inflation Rates Surge Across European Markets",
                source_name="Financial Times",
                article_url="https://ft.com/art2",
                description="Central banks face inflation pressures.",
                content="Economic analysis of interest rate decisions.",
                category="Business",
                sentiment="Negative",
                publication_date="2026-10-15",
                keywords=["inflation", "markets"]
            ),
            NewsArticle(
                headline="Parliament Debates Renewable Solar Tariffs",
                source_name="BBC News",
                article_url="https://bbc.co.uk/art3",
                description="Lawmakers consider subsidies for solar installations.",
                content="Legislative debate on green transition.",
                category="Environment",
                sentiment="Neutral",
                publication_date="2026-10-20",
                keywords=["renewable", "solar", "parliament"]
            )
        ]

    def test_tc_bb_sea_01_headline_search_case_insensitive(self):
        """TC-BB-SEA-01: Headline search matches regardless of case."""
        res1 = SearchService.search_headline(self.sample_articles, "quantum")
        self.assertEqual(len(res1), 1)
        self.assertEqual(res1[0].headline, "Quantum Computing Breakthrough at Cambridge")

        res2 = SearchService.search_headline(self.sample_articles, "QUANTUM")
        self.assertEqual(len(res2), 1)

    def test_tc_bb_sea_02_empty_search_query_returns_all(self):
        """TC-BB-SEA-02: Empty query string returns complete collection."""
        res = SearchService.search_headline(self.sample_articles, "")
        self.assertEqual(len(res), len(self.sample_articles))

    def test_tc_bb_sea_03_no_match_partition(self):
        """TC-BB-SEA-03: Query with zero occurrences returns empty list."""
        res = SearchService.search_headline(self.sample_articles, "NonExistentTopic123")
        self.assertEqual(len(res), 0)

    def test_tc_bb_sea_04_keyword_search(self):
        """TC-BB-SEA-04: Filtering by specific keywords list."""
        res = SearchService.search_keywords(self.sample_articles, "solar")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].category, "Environment")

    def test_tc_bb_sea_05_category_filter(self):
        """TC-BB-SEA-05: Exact category partitioning."""
        res = SearchService.filter_by_category(self.sample_articles, "Business")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].headline, "Inflation Rates Surge Across European Markets")

    def test_tc_bb_sea_06_sentiment_filter(self):
        """TC-BB-SEA-06: Sentiment partition filter."""
        pos = SearchService.filter_by_sentiment(self.sample_articles, "Positive")
        self.assertEqual(len(pos), 1)
        neg = SearchService.filter_by_sentiment(self.sample_articles, "Negative")
        self.assertEqual(len(neg), 1)
        neu = SearchService.filter_by_sentiment(self.sample_articles, "Neutral")
        self.assertEqual(len(neu), 1)

    def test_tc_bb_sea_07_date_range_filter(self):
        """TC-BB-SEA-07: Date boundary filtering."""
        res = SearchService.filter_by_date_range(self.sample_articles, start_date="2026-10-10", end_date="2026-10-25")
        self.assertEqual(len(res), 2)

    def test_tc_bb_sea_08_combined_conjunction_filter(self):
        """TC-BB-SEA-08: Decision table test for combined multiple filter conditions."""
        # Matches article 2: query="markets", source="Financial Times", category="Business", sentiment="Negative"
        res = SearchService.combined_filter(
            self.sample_articles,
            query="markets",
            source="Financial Times",
            category="Business",
            sentiment="Negative",
            start_date="2026-10-01",
            end_date="2026-10-31"
        )
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].headline, "Inflation Rates Surge Across European Markets")


if __name__ == "__main__":
    unittest.main()
