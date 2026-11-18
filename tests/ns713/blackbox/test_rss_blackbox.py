"""
Black-Box Tests for RSS Collection and XML Ingestion
Member 1: Nikitha Sarpur (ns713 - 259060190)
Techniques: Specification-Based Testing, Fault Injection, Edge-Case Handling
"""

import unittest
from services.rss_service import RssService


class TestRssBlackbox(unittest.TestCase):
    """Black-box testing of RSS parsing, malformed payload isolation, and demo fallback."""

    def setUp(self):
        self.service = RssService(timeout=2)

    def test_tc_bb_rss_01_valid_rss_xml(self):
        """TC-BB-RSS-01: Correctly formed RSS 2.0 XML string."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Tech News</title>
                <item>
                    <title>Major Quantum Leap</title>
                    <link>https://technews.com/art1</link>
                    <description>Physicists demonstrated coherent qubit array.</description>
                    <pubDate>Mon, 10 Nov 2026 14:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>"""
        ok, articles, err = self.service.parse_rss_xml(xml, default_source_name="Tech News")
        self.assertTrue(ok)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].headline, "Major Quantum Leap")
        self.assertEqual(articles[0].source_name, "Tech News")
        self.assertEqual(articles[0].publication_date, "2026-11-10")

    def test_tc_bb_rss_02_malformed_xml_handling(self):
        """TC-BB-RSS-02: Corrupted/unclosed XML tag does not crash service."""
        corrupted_xml = "<rss><channel><title>Broken XML<item><title>Unclosed</rss>"
        ok, articles, err = self.service.parse_rss_xml(corrupted_xml)
        self.assertFalse(ok)
        self.assertEqual(len(articles), 0)
        self.assertIn("Malformed XML", err)

    def test_tc_bb_rss_03_empty_xml_string(self):
        """TC-BB-RSS-03: Empty XML input handling."""
        ok, articles, err = self.service.parse_rss_xml("   ")
        self.assertFalse(ok)
        self.assertIn("empty", err.lower())

    def test_tc_bb_rss_04_missing_optional_fields_fallback(self):
        """TC-BB-RSS-04: Item with missing pubDate and description generates valid article."""
        xml = """<rss version="2.0">
            <channel>
                <item>
                    <title>Headline Only Article</title>
                    <link>https://example.com/item1</link>
                </item>
            </channel>
        </rss>"""
        ok, articles, err = self.service.parse_rss_xml(xml)
        self.assertTrue(ok)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].headline, "Headline Only Article")
        self.assertIsNotNone(articles[0].publication_date)

    def test_tc_bb_rss_05_atom_feed_support(self):
        """TC-BB-RSS-05: Atom syndication feed XML parsing."""
        atom_xml = """<?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <title>Atom Feed Example</title>
            <entry>
                <title>Solar Cell Breakthrough</title>
                <link href="https://example.com/atom1" />
                <summary>High efficiency perovskite layer.</summary>
                <updated>2026-11-05T12:00:00Z</updated>
            </entry>
        </feed>"""
        ok, articles, err = self.service.parse_rss_xml(atom_xml, default_source_name="Atom Feed")
        self.assertTrue(ok)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].headline, "Solar Cell Breakthrough")

    def test_tc_bb_rss_06_offline_demo_feed(self):
        """TC-BB-RSS-06: Verification of offline fallback feed retrieval."""
        articles = self.service.load_offline_demo_feed()
        self.assertIsInstance(articles, list)
        self.assertGreaterEqual(len(articles), 100)


if __name__ == "__main__":
    unittest.main()
