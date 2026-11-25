"""
Unit Tests for Academic Research Component (SMT Solver & Automated Concolic Engine)
Course: CO7095 - Software Measurement and Quality Assurance
Group: Group 19
"""

import unittest
from research.smt_solver import Constraint, SMTSolver
from research.concolic_engine import ConcolicEngine
from models.article import NewsArticle


class TestSMTConcolicResearch(unittest.TestCase):
    """Verifies theoretical and algorithmic correctness of the automated SMT and Concolic engines."""

    def test_tc_res_01_smt_solver_satisfiability_and_model_generation(self):
        """TC-RES-01: Verifies SMT solver generates valid satisfying concrete assignment for complex conjunction."""
        constraints = [
            Constraint("headline", "is_not_empty", True),
            Constraint("source_name", "==", "BBC News"),
            Constraint("sentiment", "in", ["Positive", "Negative", "Neutral"])
        ]
        status, model = SMTSolver.check_sat(constraints)
        self.assertEqual(status, "SAT")
        self.assertIsNotNone(model)
        self.assertEqual(model["source_name"], "BBC News")
        self.assertIn(model["sentiment"], ["Positive", "Negative", "Neutral"])
        self.assertTrue(bool(model["headline"]))

    def test_tc_res_02_smt_solver_unsat_proof(self):
        """TC-RES-02: Verifies SMT solver formally detects and prunes unsatisfiable branch constraints."""
        unsat_constraints = [
            Constraint("headline", "is_empty", True),
            Constraint("headline", "is_not_empty", True)
        ]
        status, model = SMTSolver.check_sat(unsat_constraints)
        self.assertEqual(status, "UNSAT")
        self.assertIsNone(model)

    def test_tc_res_03_automated_concolic_exploration_steps(self):
        """TC-RES-03: Executes iterative concolic testing steps and verifies automated test case synthesis."""
        steps = ConcolicEngine.explore_article_validation()
        self.assertEqual(len(steps), 5)

        # Step 1: Nominal Seed SAT
        self.assertEqual(steps[0].solver_status, "SAT")
        self.assertIsNotNone(steps[0].generated_test_input)

        # Step 5: Pruned Infeasible Path
        self.assertEqual(steps[4].solver_status, "UNSAT")
        self.assertIsNone(steps[4].generated_test_input)

        # Verify generated test cases execute against actual domain model without crashes
        for s in steps:
            if s.generated_test_input:
                art = NewsArticle(
                    headline=s.generated_test_input.get("headline", "Default Title"),
                    source_name=s.generated_test_input.get("source_name", "Default Source"),
                    article_url=s.generated_test_input.get("article_url", "https://default.org"),
                    sentiment=s.generated_test_input.get("sentiment", "Neutral")
                )
                valid, errors = art.validate()
                self.assertIsInstance(valid, bool)
                self.assertIsInstance(errors, list)


if __name__ == "__main__":
    unittest.main()
