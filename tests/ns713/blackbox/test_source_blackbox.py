"""
Black-Box Tests for News Source Registry
Member 1: Nikitha Sarpur (ns713 - 259060190)
Techniques: Equivalence Partitioning, Boundary Value Analysis
"""

import unittest
from models.news_source import NewsSource


class TestSourceBlackbox(unittest.TestCase):
    """Black-box test suite for NewsSource model validation."""

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
        source = NewsSource(
            name="",
            feed_url="https://example.com/rss.xml"
        )
        is_valid, errors = source.validate()
        self.assertFalse(is_valid)
        self.assertIn("Source name cannot be empty.", errors)

    def test_tc_bb_src_03_empty_feed_url(self):
        """TC-BB-SRC-03: Equivalence partition - Empty feed URL."""
        source = NewsSource(
            name="Valid Source",
            feed_url=""
        )
        is_valid, errors = source.validate()
        self.assertFalse(is_valid)
        self.assertIn("Feed URL cannot be empty.", errors)

    def test_tc_bb_src_04_invalid_url_protocol(self):
        """TC-BB-SRC-04: Robustness - Unsupported protocol (ftp:// instead of http/https/file)."""
        source = NewsSource(
            name="FTP Source",
            feed_url="ftp://files.example.com/rss.xml"
        )
        is_valid, errors = source.validate()
        self.assertFalse(is_valid)
        self.assertTrue(any("must begin with http://" in e for e in errors))

    def test_tc_bb_src_05_file_protocol_valid(self):
        """TC-BB-SRC-05: Local file protocol (file://) support for offline testing."""
        source = NewsSource(
            name="Local Feed",
            feed_url="file:///tmp/test_feed.xml"
        )
        is_valid, errors = source.validate()
        self.assertTrue(is_valid)


if __name__ == "__main__":
    unittest.main()
