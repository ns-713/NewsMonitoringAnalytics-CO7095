"""
White-Box Tests for News Article Model
Member 1: Nikitha Sarpur (ns713 - 259060190)
Techniques: Statement, Branch, and Condition Coverage
"""

import unittest
from models.article import NewsArticle


class TestArticleWhitebox(unittest.TestCase):
    """White-box internal structural test suite for NewsArticle methods."""

    def test_tc_wb_art_01_all_validation_branches(self):
        """TC-WB-ART-01: Exercises every conditional branch in NewsArticle.validate()."""
        # Branch 1 True (empty headline)
        art1 = NewsArticle(headline="", source_name="Src", article_url="http://a.com")
        valid1, err1 = art1.validate()
        self.assertFalse(valid1)
        self.assertIn("Headline cannot be empty.", err1)

        # Branch 1 Elif (headline < 3 chars)
        art2 = NewsArticle(headline="AB", source_name="Src", article_url="http://a.com")
        valid2, err2 = art2.validate()
        self.assertFalse(valid2)
        self.assertIn("Headline must be at least 3 characters long.", err2)

        # Branch 2 True (empty source_name)
        art3 = NewsArticle(headline="ABC", source_name="", article_url="http://a.com")
        valid3, err3 = art3.validate()
        self.assertFalse(valid3)
        self.assertIn("Source name cannot be empty.", err3)

        # Branch 3 True (empty article_url)
        art4 = NewsArticle(headline="ABC", source_name="Src", article_url="")
        valid4, err4 = art4.validate()
        self.assertFalse(valid4)
        self.assertIn("Article URL cannot be empty.", err4)

        # Branch 4 True (invalid sentiment)
        art5 = NewsArticle(headline="ABC", source_name="Src", article_url="http://a.com", sentiment="InvalidTone")
        valid5, err5 = art5.validate()
        self.assertFalse(valid5)
        self.assertTrue(any("Invalid sentiment" in e for e in err5))

        # All branches False (Valid)
        art6 = NewsArticle(headline="Valid Title", source_name="Src", article_url="http://a.com", sentiment="Neutral")
        valid6, err6 = art6.validate()
        self.assertTrue(valid6)
        self.assertEqual(len(err6), 0)

    def test_tc_wb_art_04_publication_date_validation_branches(self):
        """TC-WB-ART-04: Exercises publication date validation branch and format parsing."""
        # Invalid date string branch (e.g. 99-99-9999 or corrupt text)
        art_inv1 = NewsArticle(
            headline="Invalid Date Headline",
            source_name="Src",
            article_url="http://a.com",
            publication_date="99-99-9999"
        )
        valid_inv1, errs_inv1 = art_inv1.validate()
        self.assertFalse(valid_inv1)
        self.assertTrue(any("Invalid publication date" in e for e in errs_inv1))

        art_inv2 = NewsArticle(
            headline="Corrupt Date String",
            source_name="Src",
            article_url="http://a.com",
            publication_date="not-a-valid-date"
        )
        valid_inv2, errs_inv2 = art_inv2.validate()
        self.assertFalse(valid_inv2)
        self.assertTrue(any("Invalid publication date" in e for e in errs_inv2))

        # Valid ISO date branch
        art_val1 = NewsArticle(
            headline="Valid ISO Date",
            source_name="Src",
            article_url="http://a.com",
            publication_date="2026-11-25"
        )
        valid_val1, errs_val1 = art_val1.validate()
        self.assertTrue(valid_val1)
        self.assertEqual(len(errs_val1), 0)

        # Valid RFC 822 RSS date branch
        art_val2 = NewsArticle(
            headline="Valid RFC Date",
            source_name="Src",
            article_url="http://a.com",
            publication_date="Wed, 25 Nov 2026 12:00:00 +0000"
        )
        valid_val2, errs_val2 = art_val2.validate()
        self.assertTrue(valid_val2)
        self.assertEqual(len(errs_val2), 0)

    def test_tc_wb_art_02_serialization_roundtrip(self):
        """TC-WB-ART-02: Exercises to_dict() and from_dict() data integrity."""
        original = NewsArticle(
            headline="Sample Headline",
            source_name="Sample Source",
            article_url="https://sample.com/1",
            description="Sample description",
            content="Sample long content",
            category="Technology",
            sentiment="Positive",
            sentiment_score=5,
            keywords=["tech", "innovation"]
        )
        d = original.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["headline"], original.headline)

        reconstructed = NewsArticle.from_dict(d)
        self.assertEqual(reconstructed.article_id, original.article_id)
        self.assertEqual(reconstructed.headline, original.headline)
        self.assertEqual(reconstructed.sentiment_score, 5)
        self.assertEqual(reconstructed.keywords, ["tech", "innovation"])

    def test_tc_wb_art_03_full_text_concatenation_branches(self):
        """TC-WB-ART-03: Tests full_text() branch conditions with partial and full fields."""
        # Only headline
        art1 = NewsArticle(headline="Only Title", source_name="Src", article_url="http://a.com")
        self.assertEqual(art1.full_text(), "Only Title")

        # Headline and description
        art2 = NewsArticle(headline="Title", description="Desc", source_name="Src", article_url="http://a.com")
        self.assertEqual(art2.full_text(), "Title Desc")

        # Headline, description, and content
        art3 = NewsArticle(headline="Title", description="Desc", content="Body", source_name="Src", article_url="http://a.com")
        self.assertEqual(art3.full_text(), "Title Desc Body")

    def test_tc_wb_art_04_repr_output(self):
        """TC-WB-ART-04: Exercises __repr__ format."""
        art = NewsArticle(headline="Title Here", source_name="BBC", article_url="http://a.com")
        r = repr(art)
        self.assertIn("NewsArticle", r)
        self.assertIn("BBC", r)


if __name__ == "__main__":
    unittest.main()
