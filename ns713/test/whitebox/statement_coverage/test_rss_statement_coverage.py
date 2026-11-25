"""
White-Box Tests for RSS Ingestion Service
Member 1: Nikitha Sarpur (ns713 - 259060190)
Techniques: Statement, Branch, and Loop Testing
"""

import unittest
import tempfile
from pathlib import Path
from services.rss_service import RssService


class TestRssWhitebox(unittest.TestCase):
    """White-box testing covering internal branches of RssService."""

    def setUp(self):
        self.service = RssService(timeout=2)

    def test_tc_wb_rss_01_fetch_feed_xml_local_file_branches(self):
        """TC-WB-RSS-01: Branch coverage of file:// protocol in fetch_feed_xml."""
        # Non-existent file
        ok_non, _, err_non = self.service.fetch_feed_xml("file:///nonexistent/path/feed.xml")
        self.assertFalse(ok_non)
        self.assertIn("Failed to read local file feed", err_non)

        # Existing local file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".xml", encoding="utf-8") as f:
            f.write("<rss><channel><title>Local</title></channel></rss>")
            temp_path = f.name

        try:
            ok, content, _ = self.service.fetch_feed_xml(f"file://{temp_path}")
            self.assertTrue(ok)
            self.assertIn("<rss>", content)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_tc_wb_rss_05_cross_platform_path_handling(self):
        """TC-WB-RSS-05: Verifies path normalization for both Windows drive letters and POSIX roots."""
        # Test simulated Windows drive URL: file:///C:/data/feed.xml
        simulated_win_url = "file:///C:/nonexistent_drive_test/feed.xml"
        ok_win, _, err_win = self.service.fetch_feed_xml(simulated_win_url)
        self.assertFalse(ok_win)
        self.assertIn("Failed to read local file feed", err_win)

        # Test simulated POSIX absolute path URL: file:///var/log/feed.xml
        simulated_posix_url = "file:///var/nonexistent_posix_test/feed.xml"
        ok_posix, _, err_posix = self.service.fetch_feed_xml(simulated_posix_url)
        self.assertFalse(ok_posix)
        self.assertIn("Failed to read local file feed", err_posix)

    def test_tc_wb_rss_02_parse_pub_date_branches(self):
        """TC-WB-RSS-02: Branch coverage of parse_pub_date."""
        # Empty date branch -> returns current date
        d1 = self.service.parse_pub_date(None)
        self.assertEqual(len(d1), 10)
        self.assertEqual(d1[4], "-")

        # RFC 822 format branch
        d2 = self.service.parse_pub_date("Tue, 15 Sep 2026 09:30:00 +0000")
        self.assertEqual(d2, "2026-09-15")

        # ISO format prefix branch
        d3 = self.service.parse_pub_date("2026-10-24T18:00:00Z")
        self.assertEqual(d3, "2026-10-24")

        # Completely unparseable string fallback
        d4 = self.service.parse_pub_date("unparseable date string")
        self.assertEqual(len(d4), 10)

    def test_tc_wb_rss_03_clean_html_branches(self):
        """TC-WB-RSS-03: Branch coverage of clean_html utility."""
        self.assertEqual(self.service.clean_html(""), "")
        self.assertEqual(self.service.clean_html(None), "")
        html = "<p>Paragraph text with <a href='http://link.com'>link</a> and <b>bold</b>.</p>"
        cleaned = self.service.clean_html(html)
        self.assertEqual(cleaned, "Paragraph text with link and bold.")

    def test_tc_wb_rss_04_parse_rss_empty_and_skip_items(self):
        """TC-WB-RSS-04: Loop and condition coverage in parse_rss_xml for items without title."""
        xml = """<rss version="2.0">
            <channel>
                <item>
                    <!-- Missing title: should be skipped -->
                    <description>No title here</description>
                </item>
                <item>
                    <title>Valid Title</title>
                    <description>Valid item</description>
                </item>
            </channel>
        </rss>"""
        ok, articles, _ = self.service.parse_rss_xml(xml)
        self.assertTrue(ok)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].headline, "Valid Title")


if __name__ == "__main__":
    unittest.main()
