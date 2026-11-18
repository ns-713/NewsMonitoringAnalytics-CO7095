"""
White-Box Tests for Duplicate Detection Logic
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Techniques: Statement, Branch, and Boundary Testing
"""

import unittest
from models.article import NewsArticle
from services.duplicate_service import DuplicateService


class TestDuplicateWhitebox(unittest.TestCase):
    """White-box testing covering every decision branch in DuplicateService."""

    def setUp(self):
        self.service = DuplicateService()

    def test_tc_wb_dup_01_normalise_url_branches(self):
        """TC-WB-DUP-01: Branch coverage of normalise_url with various protocols and query strings."""
        self.assertEqual(self.service.normalise_url(""), "")
        self.assertEqual(self.service.normalise_url(None), "")
        self.assertEqual(
            self.service.normalise_url("https://www.example.com/path/?ref=1#top"),
            "example.com/path"
        )
        self.assertEqual(
            self.service.normalise_url("http://example.com/article/"),
            "example.com/article"
        )

    def test_tc_wb_dup_02_calculate_similarity_branches(self):
        """TC-WB-DUP-02: Branch coverage in calculate_similarity."""
        # Both empty and identical
        self.assertEqual(self.service.calculate_similarity("", ""), 1.0)
        # One empty
        self.assertEqual(self.service.calculate_similarity("Quantum", ""), 0.0)
        # Complete overlap
        self.assertEqual(self.service.calculate_similarity("Quantum Computing", "Quantum Computing"), 1.0)
        # Partial overlap: tokens A={quantum, computing}, B={quantum, physics}
        # intersection = 1, union = 3, similarity = 1/3 = 0.333
        sim = self.service.calculate_similarity("Quantum Computing", "Quantum Physics")
        self.assertAlmostEqual(sim, 0.333, places=2)

    def test_tc_wb_dup_03_find_all_duplicates_pairwise_loop(self):
        """TC-WB-DUP-03: Statement and nested loop testing of find_all_duplicates()."""
        articles = [
            NewsArticle(headline="Article A Title", source_name="S1", article_url="http://s1.com/a"),
            NewsArticle(headline="Article B Unique", source_name="S2", article_url="http://s2.com/b"),
            NewsArticle(headline="Article A Title", source_name="S3", article_url="http://s3.com/c")  # Duplicate of A
        ]
        dups = self.service.find_all_duplicates(articles)
        self.assertEqual(len(dups), 1)
        self.assertEqual(dups[0]["article_a_headline"], "Article A Title")
        self.assertEqual(dups[0]["article_b_headline"], "Article A Title")

    def test_tc_wb_dup_04_skip_self_comparison_branch(self):
        """TC-WB-DUP-04: Confirms that candidate does not match itself if present in existing list."""
        art = NewsArticle(headline="Standalone Story", source_name="S1", article_url="http://s.com/1", article_id="ART-SAME")
        is_dup, _, _ = self.service.check_duplicate(art, [art])
        self.assertFalse(is_dup)


if __name__ == "__main__":
    unittest.main()
