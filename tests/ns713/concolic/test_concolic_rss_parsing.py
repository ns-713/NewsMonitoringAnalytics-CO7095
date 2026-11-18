"""
Concolic Testing Research and Test Harness: RSS XML Parsing
Member 1: Nikitha Sarpur (ns713 - 259060190)
Course: CO7095 - Software Measurement and Quality Assurance

CONCOLIC TESTING PROCEDURE:
1. Concrete Execution: Execute RssService.parse_rss_xml() with initial concrete XML seed.
2. Symbolic Tracking: Monitor branch decisions (<item> presence, <title> non-empty, <link> presence).
3. Branch Condition Inversion: Negate specific branch conditions to generate new test fixtures.
4. Re-execution & Path Divergence: Execute the mutated concrete inputs and verify path exploration.
"""

import unittest
from services.rss_service import RssService


class TestConcolicRssParsing(unittest.TestCase):
    """Concolic testing engine targeting RssService.parse_rss_xml()."""

    def setUp(self):
        self.service = RssService()

    def test_tc_con_rss_execution_and_branch_negation(self):
        """
        Demonstrates step-by-step concolic path exploration through branch negation.
        """
        # Step 1: Initial Concrete Seed Input (Happy Path)
        seed_xml = """<rss version="2.0">
            <channel>
                <item>
                    <title>Global Market Growth</title>
                    <link>https://news.org/1</link>
                    <pubDate>Mon, 05 Oct 2026 10:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>"""

        # Concrete run 1
        ok1, arts1, err1 = self.service.parse_rss_xml(seed_xml)
        self.assertTrue(ok1)
        self.assertEqual(len(arts1), 1)

        # Path constraint recorded:
        # phi_1 = (Root is RSS) and (Items > 0) and (Title is not None) and (Title != "")

        # Step 2: Negate Branch Condition: Title == ""
        # Negated Condition: (Title is None or Title == "")
        negated_title_xml = """<rss version="2.0">
            <channel>
                <item>
                    <!-- Negated condition: empty title -->
                    <title></title>
                    <link>https://news.org/1</link>
                </item>
            </channel>
        </rss>"""

        # Concrete run 2 with generated input
        ok2, arts2, err2 = self.service.parse_rss_xml(negated_title_xml)
        self.assertTrue(ok2)
        # Branch divergence verified: item was skipped
        self.assertEqual(len(arts2), 0)

        # Step 3: Negate Branch Condition: Root is Valid XML
        # Negated Condition: ParseError in XML
        malformed_negated_xml = "<rss><channel><item><title>Unclosed Tag"

        # Concrete run 3
        ok3, arts3, err3 = self.service.parse_rss_xml(malformed_negated_xml)
        self.assertFalse(ok3)
        self.assertIn("Malformed XML", err3)

        # Step 4: Negate Branch Condition: Items > 0
        # Negated Condition: len(items) == 0 (Empty Channel)
        empty_channel_xml = "<rss version='2.0'><channel><title>Empty</title></channel></rss>"
        ok4, arts4, err4 = self.service.parse_rss_xml(empty_channel_xml)
        self.assertTrue(ok4)
        self.assertEqual(len(arts4), 0)


if __name__ == "__main__":
    unittest.main()
