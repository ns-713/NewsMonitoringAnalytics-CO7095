"""
Symbolic Execution Research and Test Harness: Sentiment Scoring and Classification
Member 2: Sashi Dommaraju (Sd683 - 259062044)
Course: CO7095 - Software Measurement and Quality Assurance

RESEARCH OBJECTIVE:
Symbolically formulate the relationship between lexical match counts (Positive Matches P, Negative Matches N),
the calculated score S = P - N, and the resulting classification label L.

TARGET FUNCTION:
    def classify_score(self, score: int) -> str:
        if score > 0:
            return "Positive"
        elif score < 0:
            return "Negative"
        else:
            return "Neutral"

FORMAL SYMBOLIC SPECIFICATION:
    Symbolic Variables:
        P ∈ ℤ, P ≥ 0  (count of positive lexicon tokens matched)
        N ∈ ℤ, N ≥ 0  (count of negative lexicon tokens matched)
        S = P - N     (score function)

    Path Conditions:
        Path 1 (Positive): Φ_1 ≡ (P - N > 0) ≡ (P > N)
        Path 2 (Negative): Φ_2 ≡ (P - N < 0) ≡ (P < N)
        Path 3 (Neutral) : Φ_3 ≡ (P - N == 0) ≡ (P == N)
"""

import unittest
from services.sentiment_service import SentimentService


class TestSymbolicSentimentScoring(unittest.TestCase):
    """Symbolic constraint verification and test input synthesizer for SentimentService."""

    def setUp(self):
        self.service = SentimentService()

    def test_tc_sym_sen_path_condition_solving(self):
        """
        Solves constraints for each symbolic path condition and verifies code execution.
        """
        symbolic_test_matrix = [
            # (Path ID, P_val, N_val, Expected Score, Expected Label, Constraint Expression)
            ("P1_StrictlyPositive", 4, 1, 3, "Positive", "P > N"),
            ("P1_BoundaryPositive", 1, 0, 1, "Positive", "P - N == 1"),
            ("P2_StrictlyNegative", 1, 5, -4, "Negative", "P < N"),
            ("P2_BoundaryNegative", 0, 1, -1, "Negative", "N - P == 1"),
            ("P3_ZeroBoth", 0, 0, 0, "Neutral", "P == N == 0"),
            ("P3_EqualPositiveNegative", 3, 3, 0, "Neutral", "P == N > 0")
        ]

        for path_id, p_count, n_count, exp_score, exp_label, constraint in symbolic_test_matrix:
            with self.subTest(path=path_id, constraint=constraint):
                # Calculate score symbolically
                score = self.service.calculate_score(p_count, n_count)
                self.assertEqual(score, exp_score)

                # Classify score
                label = self.service.classify_score(score)
                self.assertEqual(label, exp_label)


if __name__ == "__main__":
    unittest.main()
