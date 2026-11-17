"""
White-Box Tests for Categorisation Service Logic
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Techniques: Statement, Branch, Loop Testing
"""

import unittest
import tempfile
from pathlib import Path
from services.categorisation_service import CategorisationService
from models.article import NewsArticle


class TestCategorisationWhitebox(unittest.TestCase):
    """White-box testing of CategorisationService loop structures and dictionary reloading."""

    def setUp(self):
        self.service = CategorisationService()

    def test_tc_wb_cat_01_empty_combined_text_branch(self):
        """TC-WB-CAT-01: Branch in categorise_text when combined text is completely blank."""
        cat, kws = self.service.categorise_text("", "", "")
        self.assertEqual(cat, "Other")
        self.assertEqual(kws, [])

    def test_tc_wb_cat_02_categorise_article_convenience_method(self):
        """TC-WB-CAT-02: Statement coverage for categorise_article()."""
        art = NewsArticle(
            headline="Hospital Clinical Vaccine Trial",
            source_name="MedNews",
            article_url="http://med.org/1"
        )
        cat, kws = self.service.categorise_article(art)
        self.assertEqual(cat, "Health")
        self.assertIn("vaccine", kws)

    def test_tc_wb_cat_03_get_categories_and_keywords(self):
        """TC-WB-CAT-03: Statements in get_categories and get_keywords_for_category."""
        cats = self.service.get_categories()
        self.assertIn("Technology", cats)
        self.assertIn("Politics", cats)

        tech_kws = self.service.get_keywords_for_category("Technology")
        self.assertIsInstance(tech_kws, list)
        self.assertIn("software", tech_kws)

        invalid_kws = self.service.get_keywords_for_category("NoSuchCategory")
        self.assertEqual(invalid_kws, [])

    def test_tc_wb_cat_04_update_keywords_branches(self):
        """TC-WB-CAT-04: Branch testing for update_keywords (invalid category vs valid)."""
        # Invalid category branch
        res_fail = self.service.update_keywords("InvalidCategoryName", ["kw1"])
        self.assertFalse(res_fail)

        # Valid category branch (using temporary keywords file)
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", encoding="utf-8") as f:
            f.write("{}")
            temp_file = Path(f.name)

        try:
            temp_service = CategorisationService(keywords_file=temp_file)
            res_ok = temp_service.update_keywords("Science", ["particle", "astronomy"])
            self.assertTrue(res_ok)
            self.assertEqual(temp_service.get_keywords_for_category("Science"), ["astronomy", "particle"])
        finally:
            temp_file.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
