"""
Black-Box Tests for Rule-Based Categorisation Service
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Techniques: Equivalence Partitioning, Decision Table, Boundary Testing
"""

import unittest
from services.categorisation_service import CategorisationService


class TestCategorisationBlackbox(unittest.TestCase):
    """Black-box test suite for keyword-based news categorisation."""

    def setUp(self):
        self.service = CategorisationService()

    def test_tc_bb_cat_01_politics_partition(self):
        """TC-BB-CAT-01: Correctly classifies article into Politics."""
        cat, kws = self.service.categorise_text(
            headline="Parliament Passes New Government Election Legislation",
            description="Lawmakers approved democratic voting reform."
        )
        self.assertEqual(cat, "Politics")
        self.assertIn("parliament", kws)

    def test_tc_bb_cat_02_technology_partition(self):
        """TC-BB-CAT-02: Correctly classifies article into Technology."""
        cat, kws = self.service.categorise_text(
            headline="New Cybersecurity Algorithm Protects Cloud Computing",
            description="Engineers release software patch."
        )
        self.assertEqual(cat, "Technology")
        self.assertTrue(any(k in ["cybersecurity", "cloud", "computing", "software", "algorithm"] for k in kws))

    def test_tc_bb_cat_03_health_partition(self):
        """TC-BB-CAT-03: Correctly classifies article into Health."""
        cat, kws = self.service.categorise_text(
            headline="Hospital Clinical Trial Tests Novel Cancer Vaccine",
            description="Doctors report promising therapeutic results."
        )
        self.assertEqual(cat, "Health")
        self.assertIn("cancer", kws)

    def test_tc_bb_cat_04_sports_partition(self):
        """TC-BB-CAT-04: Correctly classifies article into Sports."""
        cat, kws = self.service.categorise_text(
            headline="Football Team Clinches Championship Trophy at Stadium",
            description="Coach and athletes celebrate victory."
        )
        self.assertEqual(cat, "Sports")
        self.assertIn("football", kws)

    def test_tc_bb_cat_05_environment_partition(self):
        """TC-BB-CAT-05: Correctly classifies article into Environment."""
        cat, kws = self.service.categorise_text(
            headline="Renewable Solar and Wind Projects Cut Global Carbon Emissions",
            description="International climate agreement targets sustainability."
        )
        self.assertEqual(cat, "Environment")
        self.assertIn("climate", kws)

    def test_tc_bb_cat_06_fallback_to_other_empty_partition(self):
        """TC-BB-CAT-06: Text without keyword matches falls back to 'Other'."""
        cat, kws = self.service.categorise_text(
            headline="Abstract Theoretical Discussion on General Topics",
            description="Random prose without sector terms."
        )
        self.assertEqual(cat, "Other")
        self.assertEqual(len(kws), 0)

    def test_tc_bb_cat_07_empty_string_input(self):
        """TC-BB-CAT-07: Completely empty text input falls back to 'Other'."""
        cat, kws = self.service.categorise_text("", "", "")
        self.assertEqual(cat, "Other")
        self.assertEqual(len(kws), 0)

    def test_tc_bb_cat_08_ambiguous_multi_domain_text(self):
        """TC-BB-CAT-08: Decision table: when keywords from multiple categories exist, highest count wins."""
        # Contains 1 Technology keyword ("algorithm") and 3 Business keywords ("stock", "market", "profit")
        cat, kws = self.service.categorise_text(
            headline="Stock Market Algorithm Drives Huge Corporate Profit",
            description="Financial investment boom."
        )
        self.assertEqual(cat, "Business")


if __name__ == "__main__":
    unittest.main()
