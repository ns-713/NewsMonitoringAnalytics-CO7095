"""
Black-Box Tests for News Article Model and Validation
Member 1: Nikitha Sarpur (ns713 - 259060190)
Techniques: Equivalence Partitioning, Boundary Value Analysis, Robustness Testing
"""

import unittest
from models.article import NewsArticle


class TestArticleBlackbox(unittest.TestCase):
    """Black-box test suite for NewsArticle model and input validation."""

    def test_tc_bb_art_01_valid_article(self):
        """TC-BB-ART-01: Valid article with all standard fields."""
        article = NewsArticle(
            headline="Global Leaders Sign Climate Accord",
            source_name="BBC News",
            article_url="https://bbc.co.uk/news/climate-01",
            description="Leaders agree on emissions targets.",
            content="Full report on international emissions pact.",
            category="Environment",
            sentiment="Positive",
            sentiment_score=3
        )
        is_valid, errors = article.validate()
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        self.assertTrue(article.article_id.startswith("ART-"))

    def test_tc_bb_art_02_empty_headline_bva(self):
        """TC-BB-ART-02: Boundary Value Analysis - Empty headline."""
        article = NewsArticle(
            headline="",
            source_name="Reuters",
            article_url="https://reuters.com/news/1"
        )
        is_valid, errors = article.validate()
        self.assertFalse(is_valid)
        self.assertIn("Headline cannot be empty.", errors)

    def test_tc_bb_art_03_short_headline_boundary(self):
        """TC-BB-ART-03: Boundary Value Analysis - 2 characters (below min length 3)."""
        article = NewsArticle(
            headline="AI",
            source_name="TechDaily",
            article_url="https://techdaily.com/ai"
        )
        is_valid, errors = article.validate()
        self.assertFalse(is_valid)
        self.assertIn("Headline must be at least 3 characters long.", errors)

    def test_tc_bb_art_04_min_valid_headline_boundary(self):
        """TC-BB-ART-04: Boundary Value Analysis - 3 characters (exact min length)."""
        article = NewsArticle(
            headline="War",
            source_name="Global News",
            article_url="https://globalnews.org/war"
        )
        is_valid, errors = article.validate()
        self.assertTrue(is_valid)

    def test_tc_bb_art_05_missing_source_name(self):
        """TC-BB-ART-05: Missing source name partition."""
        article = NewsArticle(
            headline="Valid Headline Text",
            source_name="",
            article_url="https://example.com/art1"
        )
        is_valid, errors = article.validate()
        self.assertFalse(is_valid)
        self.assertIn("Source name cannot be empty.", errors)

    def test_tc_bb_art_06_missing_article_url(self):
        """TC-BB-ART-06: Missing article URL partition."""
        article = NewsArticle(
            headline="Valid Headline Text",
            source_name="BBC News",
            article_url=""
        )
        is_valid, errors = article.validate()
        self.assertFalse(is_valid)
        self.assertIn("Article URL cannot be empty.", errors)

    def test_tc_bb_art_07_invalid_sentiment_class(self):
        """TC-BB-ART-07: Equivalence partitioning - Invalid sentiment label."""
        article = NewsArticle(
            headline="Market update report",
            source_name="Bloomberg",
            article_url="https://bloomberg.com/1",
            sentiment="ExtremelyGood"
        )
        is_valid, errors = article.validate()
        self.assertFalse(is_valid)
        self.assertTrue(any("Invalid sentiment" in e for e in errors))

    def test_tc_bb_art_08_special_characters_and_unicode(self):
        """TC-BB-ART-08: Robustness - Special characters, accented glyphs, and emoji."""
        article = NewsArticle(
            headline="Café & naïve résumé: Tokyo 2026 £50m surge! 🚀",
            source_name="Le Monde (Français)",
            article_url="https://lemonde.fr/article/1"
        )
        is_valid, errors = article.validate()
        self.assertTrue(is_valid)
        self.assertIn("Café", article.headline)

    def test_tc_bb_art_09_very_long_content_partition(self):
        """TC-BB-ART-09: Robustness - Very long article content (10,000+ characters)."""
        long_body = "Comprehensive analytical report. " * 500
        article = NewsArticle(
            headline="Exhaustive Sector Review",
            source_name="Industry Standard",
            article_url="https://standard.com/report",
            content=long_body
        )
        is_valid, errors = article.validate()
        self.assertTrue(is_valid)
        self.assertGreater(len(article.content), 10000)

    def test_tc_bb_art_10_whitespace_trimming(self):
        """TC-BB-ART-10: Equivalence partitioning - Whitespace padding is stripped."""
        article = NewsArticle(
            headline="   Headline with Padding   ",
            source_name="   BBC News   ",
            article_url="   https://bbc.co.uk/padded   "
        )
        self.assertEqual(article.headline, "Headline with Padding")
        self.assertEqual(article.source_name, "BBC News")
        self.assertEqual(article.article_url, "https://bbc.co.uk/padded")


if __name__ == "__main__":
    unittest.main()
