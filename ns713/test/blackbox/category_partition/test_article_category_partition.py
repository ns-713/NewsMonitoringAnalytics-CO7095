"""
Category Partition Testing for News Article and Source Models
Member: Nikitha Sarpur (ns713 - 259060190)
Testing Tool: Python unittest
Testing Technique: Black-Box (Specification-Based) - Category Partitioning
"""

import unittest
from models.article import NewsArticle
from models.news_source import NewsSource


class TestArticleCategoryPartition(unittest.TestCase):
    """
    Category Partition Test Suite for NewsArticle & NewsSource.
    Partitions:
    - P1: Complete valid article with all standard fields
    - P2: Missing source name partition
    - P3: Missing article URL partition
    - P4: Invalid sentiment label partition
    - P5: Robustness: special characters, accented glyphs, and emoji
    - P6: Robustness: long article content
    - P7: Whitespace trimming partition
    - P8: Source validation partitions (valid HTTPS, empty name, empty URL, file protocol)
    """

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
            headline="Café & naïve résumé: Tokyo 2026 surge! 🚀",
            source_name="Le Monde (Français)",
            article_url="https://lemonde.fr/article/1"
        )
        is_valid, errors = article.validate()
        self.assertTrue(is_valid)
        self.assertIn("Café", article.headline)

    def test_tc_bb_art_09_very_long_content_partition(self):
        """TC-BB-ART-09: Robustness - Very long article content."""
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

    def test_tc_bb_src_01_valid_source(self):
        """TC-BB-SRC-01: Valid news source with HTTPS feed URL."""
        source = NewsSource(
            name="BBC News",
            feed_url="https://feeds.bbci.co.uk/news/rss.xml",
            url="https://bbc.co.uk",
            category="World News"
        )
        is_valid, errors = source.validate()
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        self.assertTrue(source.source_id.startswith("SRC-"))

    def test_tc_bb_src_02_empty_source_name(self):
        """TC-BB-SRC-02: Equivalence partition - Empty source name."""
        source = NewsSource(name="", feed_url="https://example.com/rss.xml")
        is_valid, errors = source.validate()
        self.assertFalse(is_valid)
        self.assertIn("Source name cannot be empty.", errors)

    def test_tc_bb_src_03_empty_feed_url(self):
        """TC-BB-SRC-03: Equivalence partition - Empty feed URL."""
        source = NewsSource(name="Valid Source", feed_url="")
        is_valid, errors = source.validate()
        self.assertFalse(is_valid)
        self.assertIn("Feed URL cannot be empty.", errors)

    def test_tc_bb_src_05_file_protocol_valid(self):
        """TC-BB-SRC-05: Local file protocol (file://) support for offline testing."""
        source = NewsSource(name="Local Feed", feed_url="file:///tmp/sample_feed.xml")
        is_valid, errors = source.validate()
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
