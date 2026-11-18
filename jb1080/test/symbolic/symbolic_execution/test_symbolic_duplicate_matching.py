"""
Symbolic Execution Research and Test Harness: Duplicate Detection Similarity Matching
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Course: CO7095 - Software Measurement and Quality Assurance

RESEARCH OBJECTIVE:
Symbolically analyze the Jaccard similarity function:
    J(A, B) = |A ∩ B| / |A ∪ B|
Determine the boundary constraints under threshold θ = 0.70 to classify article pairs as duplicates vs unique.

FORMAL SYMBOLIC SPECIFICATION:
    Let A, B be token sets:
        n_A = |A|, n_B = |B|
        k = |A ∩ B| (intersection count)
        u = |A ∪ B| = n_A + n_B - k (union count)

    Constraint Formulation:
        J(A, B) = k / (n_A + n_B - k)
        Path 1 (Duplicate Flagged): J(A, B) ≥ 0.70  ==>  k ≥ 0.70 * (n_A + n_B - k)  ==>  1.70 * k ≥ 0.70 * (n_A + n_B)
        Path 2 (Unique / Non-Duplicate): J(A, B) < 0.70  ==>  1.70 * k < 0.70 * (n_A + n_B)
"""

import unittest
from services.duplicate_service import DuplicateService


class TestSymbolicDuplicateMatching(unittest.TestCase):
    """Symbolic constraint evaluation of token similarity thresholds in DuplicateService."""

    def setUp(self):
        self.threshold = 0.70
        self.service = DuplicateService(threshold=self.threshold)

    def test_tc_sym_dup_threshold_boundary_solving(self):
        """
        Solves constraints for boundary token sets to verify exact decision transitions at θ = 0.70.
        """
        # Test Case 1: Identical sets: n_A = 10, n_B = 10, k = 10, u = 10 -> J = 1.0 (>= 0.70)
        s1 = "wordone wordtwo wordthree wordfour wordfive wordsix wordseven wordeight wordnine wordten"
        sim1 = self.service.calculate_similarity(s1, s1)
        self.assertEqual(sim1, 1.0)
        self.assertGreaterEqual(sim1, self.threshold)

        # Test Case 2: Boundary above threshold: 7 common tokens out of 10 union -> J = 7/10 = 0.70 (>= 0.70)
        tokens_common = "t1 t2 t3 t4 t5 t6 t7"
        text_a = f"{tokens_common} a8 a9"
        text_b = f"{tokens_common} b8"
        # Set A = {t1..t7, a8, a9} (|A| = 9)
        # Set B = {t1..t7, b8} (|B| = 8)
        # Intersection = 7 {t1..t7}
        # Union = {t1..t7, a8, a9, b8} (|Union| = 10)
        # J = 7 / 10 = 0.70
        sim2 = self.service.calculate_similarity(text_a, text_b)
        self.assertAlmostEqual(sim2, 0.70, places=2)
        self.assertTrue(sim2 >= self.threshold)

        # Test Case 3: Boundary strictly below threshold: 6 common tokens out of 10 union -> J = 6/10 = 0.60 (< 0.70)
        text_c = f"t1 t2 t3 t4 t5 t6 c7 c8"
        text_d = f"t1 t2 t3 t4 t5 t6 d7 d8"
        # Set C = {t1..t6, c7, c8} (|C| = 8)
        # Set D = {t1..t6, d7, d8} (|D| = 8)
        # Intersection = 6 {t1..t6}
        # Union = {t1..t6, c7, c8, d7, d8} (|Union| = 10)
        # J = 6 / 10 = 0.60
        sim3 = self.service.calculate_similarity(text_c, text_d)
        self.assertAlmostEqual(sim3, 0.60, places=2)
        self.assertFalse(sim3 >= self.threshold)


if __name__ == "__main__":
    unittest.main()
