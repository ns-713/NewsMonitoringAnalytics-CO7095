"""
Boundary Value Analysis for News Article Model
Member: Nikitha Sarpur (ns713 - 259060190)
Testing Tool: Python unittest
Testing Technique: Black-Box (Specification-Based) - Boundary Value Analysis (BVA)
"""

import unittest
from models.article import NewsArticle
from models.news_source import NewsSource


class TestArticleBVA(unittest.TestCase):
    """
    Boundary Value Analysis on string lengths and thresholds:
    - Headline length bounds:
      - 0 chars (below min, invalid)
      - 2 chars (below min, invalid, boundary = 3)
      - 3 chars (at min, valid)
    - Source URL protocol boundaries (unsupported ftp://)
    """

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

    def test_tc_bb_src_04_invalid_url_protocol(self):
        """TC-BB-SRC-04: Boundary - Unsupported protocol (ftp:// instead of http/https/file)."""
        source = NewsSource(
            name="FTP Source",
            feed_url="ftp://files.example.com/rss.xml"
        )
        is_valid, errors = source.validate()
        self.assertFalse(is_valid)
        self.assertTrue(any("must begin with http://" in e for e in errors))


if __name__ == '__main__':
    unittest.main()
