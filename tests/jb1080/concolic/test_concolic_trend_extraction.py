"""
Concolic Testing Research and Test Harness: Keyword Token Extraction
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Course: CO7095 - Software Measurement and Quality Assurance

CONCOLIC PROCEDURE:
1. Seed Input: Execute extract_keywords() with standard sentence.
2. Symbolic Constraint Collection:
       Condition 1: len(t) >= min_length (default 3)
       Condition 2: not t.isdigit()
       Condition 3: t not in stop_words
3. Invert Condition 1: Generate token with length < 3.
4. Invert Condition 2: Generate numeric token.
5. Invert Condition 3: Generate token in stop_words.
6. Concrete Execution & Divergence Check: Confirm non-compliant tokens are correctly dropped.
"""

import unittest
from services.trend_service import TrendService


class TestConcolicTrendExtraction(unittest.TestCase):
    """Concolic testing harness targeting TrendService.extract_keywords()."""

    def setUp(self):
        self.service = TrendService()

    def test_tc_con_trd_execution_and_branch_negation(self):
        """
        Executes concrete seed, negates token filter branches, and verifies path behavior.
        """
        # Step 1: Concrete Seed Input (All conditions satisfied)
        seed_text = "quantum processor algorithm"
        extracted_1 = self.service.extract_keywords(seed_text)
        self.assertEqual(extracted_1, ["quantum", "processor", "algorithm"])

        # Step 2: Negate Condition 1 (len(token) < 3)
        # Synthesize tokens with length 1 and 2
        negated_len_text = "ai ox quantum"
        extracted_2 = self.service.extract_keywords(negated_len_text)
        # "ai" and "ox" (len 2) are dropped; only "quantum" remains
        self.assertEqual(extracted_2, ["quantum"])

        # Step 3: Negate Condition 2 (token is numeric)
        negated_num_text = "quantum 2026 400 algorithm"
        extracted_3 = self.service.extract_keywords(negated_num_text)
        self.assertEqual(extracted_3, ["quantum", "algorithm"])

        # Step 4: Negate Condition 3 (token is in stop_words)
        negated_stop_text = "quantum in the about with algorithm"
        extracted_4 = self.service.extract_keywords(negated_stop_text)
        self.assertEqual(extracted_4, ["quantum", "algorithm"])


if __name__ == "__main__":
    unittest.main()
