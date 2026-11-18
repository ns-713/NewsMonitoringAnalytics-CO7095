"""
Black-Box Tests for Duplicate News Detection Service
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Techniques: Equivalence Partitioning, Boundary Value Analysis, Similarity Matching
"""

import unittest
from models.article import NewsArticle
from services.duplicate_service import DuplicateService


class TestDuplicateBlackbox(unittest.TestCase):
    """Black-box test suite for URL, headline, fingerprint, and similarity duplicate detection."""

    def setUp(self):
        self.service = DuplicateService(threshold=0.70)
        self.existing_article = NewsArticle(
            headline="Global Leaders Sign Milestone Climate Treaty in Paris",
            source_name="BBC News",
            article_url="https://bbc.co.uk/news/climate-treaty-2026",
            article_id="ART-ORIG01"
        )

    def test_tc_bb_dup_01_exact_url_duplicate(self):
        """TC-BB-DUP-01: Candidate with identical article URL."""
        candidate = NewsArticle(
            headline="Different Headline Wire Report",
            source_name="Reuters",
            article_url="https://bbc.co.uk/news/climate-treaty-2026",  # Same URL
            article_id="ART-CAND01"
        )
        is_dup, reason, matched = self.service.check_duplicate(candidate, [self.existing_article])
        self.assertTrue(is_dup)
        self.assertIn("URL", reason)
        self.assertEqual(matched.article_id, "ART-ORIG01")

    def test_tc_bb_dup_02_url_normalisation_duplicate(self):
        """TC-BB-DUP-02: URLs matching after stripping protocol, www, trailing slashes, and query params."""
        candidate = NewsArticle(
            headline="Different Headline Text",
            source_name="Reuters",
            article_url="http://www.bbc.co.uk/news/climate-treaty-2026/?utm_source=twitter#top",
            article_id="ART-CAND02"
        )
        is_dup, reason, matched = self.service.check_duplicate(candidate, [self.existing_article])
        self.assertTrue(is_dup)
        self.assertIn("URL", reason)

    def test_tc_bb_dup_03_exact_normalised_headline_duplicate(self):
        """TC-BB-DUP-03: Candidate with same words, differing only in casing and punctuation."""
        candidate = NewsArticle(
            headline="global leaders sign milestone climate treaty in paris!!!",
            source_name="Another Source",
            article_url="https://another.com/story-123",
            article_id="ART-CAND03"
        )
        is_dup, reason, matched = self.service.check_duplicate(candidate, [self.existing_article])
        self.assertTrue(is_dup)
        self.assertIn("headline", reason.lower())

    def test_tc_bb_dup_04_fingerprint_token_order_duplicate(self):
        """TC-BB-DUP-04: Candidate with identical non-stop tokens arranged in different order."""
        candidate = NewsArticle(
            headline="Milestone Climate Treaty Signed in Paris by Global Leaders",
            source_name="Guardian Wire",
            article_url="https://guardian.com/story-789",
            article_id="ART-CAND04"
        )
        is_dup, reason, matched = self.service.check_duplicate(candidate, [self.existing_article])
        self.assertTrue(is_dup)

    def test_tc_bb_dup_05_high_similarity_near_duplicate(self):
        """TC-BB-DUP-05: Jaccard similarity meets threshold (>= 0.70)."""
        candidate = NewsArticle(
            headline="Global Leaders Sign Milestone Climate Treaty in Paris Accord",
            source_name="Wire News",
            article_url="https://wire.com/news/101",
            article_id="ART-CAND05"
        )
        is_dup, reason, matched = self.service.check_duplicate(candidate, [self.existing_article])
        self.assertTrue(is_dup)
        self.assertIn("similarity", reason.lower())

    def test_tc_bb_dup_06_unique_article_non_duplicate(self):
        """TC-BB-DUP-06: Distinct article is recognised as unique."""
        candidate = NewsArticle(
            headline="Championship Football Victory at Wembley Stadium",
            source_name="Sports Daily",
            article_url="https://sports.com/football-win",
            article_id="ART-CAND06"
        )
        is_dup, reason, matched = self.service.check_duplicate(candidate, [self.existing_article])
        self.assertFalse(is_dup)
        self.assertIsNone(matched)


if __name__ == "__main__":
    unittest.main()
