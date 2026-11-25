"""
Unit Tests for Academic Research Component (SMT Solver & Concolic Engine)
Course: CO7095 - Software Measurement and Quality Assurance
Group: Group 19 (Nikitha Sarpur, Sashi Dommaraju, Jyothi Bandalapati, Jalakam Prashanth)
"""

import unittest
from research.smt_solver import Constraint, SMTSolver, DPLLSolver
from research.concolic_engine import ConcolicEngine
from models.article import NewsArticle


class TestSMTConcolicResearch(unittest.TestCase):
    """Verifies theoretical and algorithmic correctness of the SMT and Concolic engines."""

    def test_tc_res_01_smt_solver_satisfiability_and_model_generation(self):
        """TC-RES-01: Verifies SMT solver generates valid satisfying concrete assignment for complex conjunction."""
        constraints = [
            Constraint("headline", "is_not_empty", True, var_type="str"),
            Constraint("source_name", "==", "BBC News", var_type="str"),
            Constraint("sentiment", "in", ["Positive", "Negative", "Neutral"], var_type="str")
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
            Constraint("headline", "is_empty", True, var_type="str"),
            Constraint("headline", "is_not_empty", True, var_type="str")
        ]
        status, model = SMTSolver.check_sat(unsat_constraints)
        self.assertEqual(status, "UNSAT")
        self.assertIsNone(model)

    def test_tc_res_03_smt_solver_claude_benchmarks_and_unbounded_integers(self):
        """TC-RES-03: Verifies SMT solver passes all benchmark constraint queries including unbounded integers."""
        # 1. Headline not empty and length < 3
        c1 = [
            Constraint("h", "is_not_empty", True, var_type="str"),
            Constraint("h", "<", 3, var_type="str", is_length=True)
        ]
        s1, m1 = SMTSolver.check_sat(c1)
        self.assertEqual(s1, "SAT")
        self.assertIn(m1["h"], ["A", "AA"])

        # 2. Set membership with exclusion: s in [A, B] and s != 'A'
        c2 = [Constraint("s", "in", ["A", "B"], var_type="str"), Constraint("s", "!=", "A", var_type="str")]
        s2, m2 = SMTSolver.check_sat(c2)
        self.assertEqual(s2, "SAT")
        self.assertEqual(m2["s"], "B")

        # 3. Numeric contradiction: x <= 5 and x > 5
        c3 = [Constraint("x", "<=", 5, var_type="int"), Constraint("x", ">", 5, var_type="int")]
        s3, m3 = SMTSolver.check_sat(c3)
        self.assertEqual(s3, "UNSAT")
        self.assertIsNone(m3)

        # 4. Integer variable upper bound: x < 10
        c4 = [Constraint("x", "<", 10, var_type="int")]
        s4, m4 = SMTSolver.check_sat(c4)
        self.assertEqual(s4, "SAT")
        self.assertIsInstance(m4["x"], int)
        self.assertLess(m4["x"], 10)

        # 5. Integer variable interval: x >= 5 and x < 10
        c5 = [Constraint("x", ">=", 5, var_type="int"), Constraint("x", "<", 10, var_type="int")]
        s5, m5 = SMTSolver.check_sat(c5)
        self.assertEqual(s5, "SAT")
        self.assertIsInstance(m5["x"], int)
        self.assertTrue(5 <= m5["x"] < 10)

        # 6. Unbounded integer arithmetic test: x > 20000 (proves no artificial ±10000 bound bug)
        c6 = [Constraint("x", ">", 20000, var_type="int")]
        s6, m6 = SMTSolver.check_sat(c6)
        self.assertEqual(s6, "SAT")
        self.assertIsInstance(m6["x"], int)
        self.assertGreater(m6["x"], 20000)

    def test_tc_res_04_dpll_and_dpll_t_integration(self):
        """TC-RES-04: Verifies DPLL SAT solver and integrated DPLL(T) SMT solver."""
        # Pure DPLL: (p or ~q) and (~p or q) and (p or q) -> p=True, q=True
        clauses_sat = [{1, -2}, {-1, 2}, {1, 2}]
        sat, assignment = SMTSolver.solve_dpll(clauses_sat)
        self.assertTrue(sat)
        self.assertTrue(assignment[1])
        self.assertTrue(assignment[2])

        # Integrated DPLL(T): Clause 1: (x > 5 OR x < 0), Clause 2: (x < 10)
        c_clause1 = [Constraint("x", ">", 5, var_type="int"), Constraint("x", "<", 0, var_type="int")]
        c_clause2 = [Constraint("x", "<", 10, var_type="int")]
        status, model = SMTSolver.check_sat_dpll_t([c_clause1, c_clause2])
        self.assertEqual(status, "SAT")
        self.assertIsNotNone(model)
        val = model["x"]
        self.assertTrue(val < 0 or 5 < val < 10)

    def test_tc_res_05_concolic_exploration_steps(self):
        """TC-RES-05: Executes iterative concolic testing steps and verifies test case synthesis."""
        steps = ConcolicEngine.explore_article_validation()
        self.assertEqual(len(steps), 7)

        # Step 1: Nominal Seed SAT, returns valid (True, [])
        self.assertEqual(steps[0].solver_status, "SAT")
        self.assertEqual(steps[0].execution_result[0], True)

        # Step 2: Empty headline -> Invalid
        self.assertEqual(steps[1].execution_result[0], False)
        self.assertIn("Headline cannot be empty.", steps[1].execution_result[1])

        # Step 3: Short headline -> Invalid
        self.assertEqual(steps[2].execution_result[0], False)
        self.assertIn("Headline must be at least 3 characters long.", steps[2].execution_result[1])

        # Step 7: Pruned Infeasible Path
        self.assertEqual(steps[6].solver_status, "UNSAT")
        self.assertIsNone(steps[6].generated_test_input)

    def test_tc_res_06_concolic_exploration_all_members(self):
        """TC-RES-06: Verifies concolic exploration across all 4 team members' modules."""
        results = ConcolicEngine.explore_all_members()
        self.assertIn("ns713", results)
        self.assertIn("sd683", results)
        self.assertIn("jb1080", results)
        self.assertIn("pj161", results)

        # Verify sd683 sentiment concolic exploration
        sd_steps = results["sd683"]
        self.assertEqual(sd_steps[0].execution_result, "Positive")
        self.assertEqual(sd_steps[1].execution_result, "Negative")
        self.assertEqual(sd_steps[2].execution_result, "Neutral")
        self.assertEqual(sd_steps[3].solver_status, "UNSAT")

        # Verify jb1080 duplicate similarity concolic exploration
        jb_steps = results["jb1080"]
        self.assertEqual(jb_steps[0].execution_result, 1.0)
        self.assertEqual(jb_steps[1].execution_result, 0.0)
        self.assertAlmostEqual(jb_steps[2].execution_result, 0.5)

        # Verify pj161 alert rule matching concolic exploration
        pj_steps = results["pj161"]
        self.assertEqual(pj_steps[0].execution_result, True)
        self.assertEqual(pj_steps[1].execution_result, False)


if __name__ == "__main__":
    unittest.main()
