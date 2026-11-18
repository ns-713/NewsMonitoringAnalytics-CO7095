"""
Concolic Testing Research and Test Harness: Rule-Based News Categorisation
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Course: CO7095 - Software Measurement and Quality Assurance

CONCOLIC PROCEDURE:
1. Seed Execution: Execute categorise_text() with concrete input triggering Category X.
2. Symbolic Constraint Accumulation: Record keyword match condition count(Cat_k) >= 1.
3. Constraint Negation: Invert the keyword presence condition (count(Cat_k) == 0).
4. Automated Input Generation: Synthesize new text satisfying negated constraints.
5. Re-Execution & Branch Verification: Confirm execution transitions to fallback category ("Other").
"""

import unittest
from services.categorisation_service import CategorisationService


class TestConcolicCategorisation(unittest.TestCase):
    """Concolic testing engine targeting CategorisationService.categorise_text()."""

    def setUp(self):
        self.service = CategorisationService()

    def test_tc_con_cat_execution_and_branch_negation(self):
        """
        Demonstrates concolic execution exploring Technology -> Business -> Other paths.
        """
        # Step 1: Concrete Run 1 (Seed Input: Technology keywords)
        concrete_text_1 = "New artificial intelligence software and algorithm released."
        cat1, kws1 = self.service.categorise_text(headline=concrete_text_1)

        self.assertEqual(cat1, "Technology")
        self.assertIn("algorithm", kws1)

        # Recorded Path Condition:
        # Φ_1 = ("algorithm" ∈ Text ∨ "software" ∈ Text) ∧ Count(Tech) > Count(Other_Categories)

        # Step 2: Negate Condition on Technology
        # Negated Condition: Count(Tech) == 0 ∧ Count(Business) > 0
        generated_input_2 = "Stock market and investment revenue increased this quarter."

        # Concrete Run 2 with negated condition
        cat2, kws2 = self.service.categorise_text(headline=generated_input_2)
        self.assertEqual(cat2, "Business")
        self.assertTrue(any(k in ["market", "investment", "revenue"] for k in kws2))

        # Step 3: Negate All Category Match Conditions
        # Negated Condition: ∀ C ∈ Categories, Count(C) == 0
        generated_input_3 = "The quiet stone bridge rested over the calm winding stream."

        # Concrete Run 3
        cat3, kws3 = self.service.categorise_text(headline=generated_input_3)
        self.assertEqual(cat3, "Other")
        self.assertEqual(len(kws3), 0)


if __name__ == "__main__":
    unittest.main()
