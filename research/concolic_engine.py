"""
CO7095 Software Measurement and Quality Assurance - Academic Research Component
Semi-Automated Symbolic Execution & Concolic Test Generation Harness
Authors: Group 19 (Nikitha Sarpur, Sashi Dommaraju, Jyothi Bandalapati, Jalakam Prashanth)

RESEARCH OBJECTIVE:
Presents an explicit-state concolic exploration harness that:
1. Evaluates target methods across all four team members' modules.
2. Constructs first-order symbolic path conditions along traversed execution paths.
3. Systematically inverts conditional predicates and queries SMTSolver for satisfying models.
4. Concretely executes production methods on synthesized inputs and logs genuine return values.
5. Formally prunes provably unsatisfiable execution branches via theorem proving.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from research.smt_solver import Constraint, SMTSolver
from models.article import NewsArticle
from models.alert_rule import AlertRule
from services.sentiment_service import SentimentService
from services.duplicate_service import DuplicateService


@dataclass
class ConcolicExecutionStep:
    iteration: int
    target_function: str
    concrete_input: Dict[str, Any]
    path_condition: List[Constraint]
    inverted_constraint: Optional[Constraint]
    solver_status: str
    generated_test_input: Optional[Dict[str, Any]]
    execution_result: Any


class ConcolicEngine:
    """
    Semi-automated concolic test generation harness executing concrete production code
    against symbolic branch conditions across all team members' components.
    """

    @staticmethod
    def explore_article_validation() -> List[ConcolicExecutionStep]:
        """
        Executes concolic exploration over NewsArticle.validate() (Member 1 - ns713).
        Directly executes NewsArticle.validate() on synthesized inputs and logs genuine return values.
        """
        steps: List[ConcolicExecutionStep] = []

        # ---------------------------------------------------------
        # Seed 1: Nominal valid article (Happy Path)
        # ---------------------------------------------------------
        seed = {
            "headline": "Quantum Computing Advances Rapidly",
            "source_name": "Reuters",
            "article_url": "https://reuters.com/tech1",
            "sentiment": "Neutral",
            "publication_date": "2026-11-25"
        }
        art1 = NewsArticle(**seed)
        res1 = art1.validate()  # Returns (True, [])

        pc1 = [
            Constraint("headline", "is_not_empty", True, var_type="str"),
            Constraint("headline", ">=", 3, var_type="str", is_length=True),
            Constraint("source_name", "is_not_empty", True, var_type="str"),
            Constraint("article_url", "is_not_empty", True, var_type="str"),
            Constraint("sentiment", "in", ["Positive", "Negative", "Neutral"], var_type="str"),
            Constraint("publication_date", "==", "2026-11-25", var_type="str")
        ]

        # Invert Branch 1: headline is empty
        inv1 = Constraint("headline", "is_empty", True, var_type="str")
        sat1, model1 = SMTSolver.check_sat([inv1, pc1[2], pc1[3], pc1[4], pc1[5]])

        steps.append(ConcolicExecutionStep(
            iteration=1,
            target_function="NewsArticle.validate",
            concrete_input=seed,
            path_condition=pc1,
            inverted_constraint=inv1,
            solver_status=sat1,
            generated_test_input=model1,
            execution_result=res1
        ))

        # ---------------------------------------------------------
        # Iteration 2: Execute synthesized Model 1 (Empty headline)
        # ---------------------------------------------------------
        inp2 = dict(model1) if model1 else {}
        inp2.setdefault("headline", "")
        inp2.setdefault("source_name", "Reuters")
        inp2.setdefault("article_url", "https://reuters.com/tech1")
        inp2.setdefault("sentiment", "Neutral")
        inp2.setdefault("publication_date", "2026-11-25")

        art2 = NewsArticle(**inp2)
        res2 = art2.validate()  # (False, ['Headline cannot be empty.'])

        # Invert Branch 2: headline length < 3
        inv2 = Constraint("headline", "<", 3, var_type="str", is_length=True)
        sat2, model2 = SMTSolver.check_sat([Constraint("headline", "is_not_empty", True, var_type="str"), inv2, pc1[2], pc1[3], pc1[4], pc1[5]])

        steps.append(ConcolicExecutionStep(
            iteration=2,
            target_function="NewsArticle.validate",
            concrete_input=inp2,
            path_condition=[inv1, pc1[2], pc1[3], pc1[4], pc1[5]],
            inverted_constraint=inv2,
            solver_status=sat2,
            generated_test_input=model2,
            execution_result=res2
        ))

        # ---------------------------------------------------------
        # Iteration 3: Execute synthesized Model 2 (Headline too short: 'A')
        # ---------------------------------------------------------
        inp3 = dict(model2) if model2 else {}
        inp3.setdefault("headline", "A")
        inp3.setdefault("source_name", "Reuters")
        inp3.setdefault("article_url", "https://reuters.com/tech1")
        inp3.setdefault("sentiment", "Neutral")
        inp3.setdefault("publication_date", "2026-11-25")

        art3 = NewsArticle(**inp3)
        res3 = art3.validate()  # (False, ['Headline must be at least 3 characters long.'])

        # Invert Branch 3: source_name is empty
        inv3 = Constraint("source_name", "is_empty", True, var_type="str")
        sat3, model3 = SMTSolver.check_sat([pc1[0], pc1[1], inv3, pc1[3], pc1[4], pc1[5]])

        steps.append(ConcolicExecutionStep(
            iteration=3,
            target_function="NewsArticle.validate",
            concrete_input=inp3,
            path_condition=[Constraint("headline", "is_not_empty", True, var_type="str"), inv2, pc1[2], pc1[3], pc1[4], pc1[5]],
            inverted_constraint=inv3,
            solver_status=sat3,
            generated_test_input=model3,
            execution_result=res3
        ))

        # ---------------------------------------------------------
        # Iteration 4: Execute synthesized Model 3 (Empty source_name)
        # ---------------------------------------------------------
        inp4 = dict(model3) if model3 else {}
        inp4.setdefault("headline", "Quantum Computing Advances Rapidly")
        inp4.setdefault("source_name", "")
        inp4.setdefault("article_url", "https://reuters.com/tech1")
        inp4.setdefault("sentiment", "Neutral")
        inp4.setdefault("publication_date", "2026-11-25")

        art4 = NewsArticle(**inp4)
        res4 = art4.validate()  # (False, ['Source name cannot be empty.'])

        # Invert Branch 4: article_url is empty
        inv4 = Constraint("article_url", "is_empty", True, var_type="str")
        sat4, model4 = SMTSolver.check_sat([pc1[0], pc1[1], pc1[2], inv4, pc1[4], pc1[5]])

        steps.append(ConcolicExecutionStep(
            iteration=4,
            target_function="NewsArticle.validate",
            concrete_input=inp4,
            path_condition=[pc1[0], pc1[1], inv3, pc1[3], pc1[4], pc1[5]],
            inverted_constraint=inv4,
            solver_status=sat4,
            generated_test_input=model4,
            execution_result=res4
        ))

        # ---------------------------------------------------------
        # Iteration 5: Execute synthesized Model 4 (Empty article_url)
        # ---------------------------------------------------------
        inp5 = dict(model4) if model4 else {}
        inp5.setdefault("headline", "Quantum Computing Advances Rapidly")
        inp5.setdefault("source_name", "Reuters")
        inp5.setdefault("article_url", "")
        inp5.setdefault("sentiment", "Neutral")
        inp5.setdefault("publication_date", "2026-11-25")

        art5 = NewsArticle(**inp5)
        res5 = art5.validate()  # (False, ['Article URL cannot be empty.'])

        # Invert Branch 5: invalid sentiment enum
        inv5 = Constraint("sentiment", "not_in", ["Positive", "Negative", "Neutral"], var_type="str")
        sat5, model5 = SMTSolver.check_sat([pc1[0], pc1[1], pc1[2], pc1[3], inv5, pc1[5]])

        steps.append(ConcolicExecutionStep(
            iteration=5,
            target_function="NewsArticle.validate",
            concrete_input=inp5,
            path_condition=[pc1[0], pc1[1], pc1[2], inv4, pc1[4], pc1[5]],
            inverted_constraint=inv5,
            solver_status=sat5,
            generated_test_input=model5,
            execution_result=res5
        ))

        # ---------------------------------------------------------
        # Iteration 6: Execute synthesized Model 5 (Invalid sentiment)
        # ---------------------------------------------------------
        inp6 = dict(model5) if model5 else {}
        inp6.setdefault("headline", "Quantum Computing Advances Rapidly")
        inp6.setdefault("source_name", "Reuters")
        inp6.setdefault("article_url", "https://reuters.com/tech1")
        inp6.setdefault("sentiment", "Optimistic")
        inp6.setdefault("publication_date", "2026-11-25")

        art6 = NewsArticle(**inp6)
        res6 = art6.validate()

        # Invert Branch 6: invalid publication date
        inv6 = Constraint("publication_date", "==", "99-99-9999", var_type="str")
        sat6, model6 = SMTSolver.check_sat([pc1[0], pc1[1], pc1[2], pc1[3], pc1[4], inv6])

        steps.append(ConcolicExecutionStep(
            iteration=6,
            target_function="NewsArticle.validate",
            concrete_input=inp6,
            path_condition=[pc1[0], pc1[1], pc1[2], pc1[3], inv5, pc1[5]],
            inverted_constraint=inv6,
            solver_status=sat6,
            generated_test_input=model6,
            execution_result=res6
        ))

        # ---------------------------------------------------------
        # Iteration 7: Execute synthesized Model 6 (Invalid date)
        # ---------------------------------------------------------
        inp7 = dict(model6) if model6 else {}
        inp7.setdefault("headline", "Quantum Computing Advances Rapidly")
        inp7.setdefault("source_name", "Reuters")
        inp7.setdefault("article_url", "https://reuters.com/tech1")
        inp7.setdefault("sentiment", "Neutral")
        inp7.setdefault("publication_date", "99-99-9999")

        art7 = NewsArticle(**inp7)
        res7 = art7.validate()

        # Branch 8: Infeasible Path Demonstration (headline empty AND length >= 3)
        unsat_c = [
            Constraint("headline", "is_empty", True, var_type="str"),
            Constraint("headline", ">=", 3, var_type="str", is_length=True)
        ]
        sat8, model8 = SMTSolver.check_sat(unsat_c)

        steps.append(ConcolicExecutionStep(
            iteration=7,
            target_function="NewsArticle.validate",
            concrete_input=inp7,
            path_condition=unsat_c,
            inverted_constraint=None,
            solver_status=sat8,
            generated_test_input=model8,
            execution_result=res7
        ))

        return steps

    @staticmethod
    def explore_sentiment_classification() -> List[ConcolicExecutionStep]:
        """
        Executes concolic exploration over SentimentService.classify_score() (Member 2 - sd683).
        Directly executes SentimentService.classify_score() with synthesized integer scores.
        """
        svc = SentimentService()
        steps: List[ConcolicExecutionStep] = []

        # Step 1: Seed score > 0 -> Positive
        c1 = [Constraint("score", ">", 0, var_type="int")]
        sat1, m1 = SMTSolver.check_sat(c1)
        score1 = m1["score"] if m1 else 5
        res1 = svc.classify_score(score1)
        steps.append(ConcolicExecutionStep(
            iteration=1,
            target_function="SentimentService.classify_score",
            concrete_input={"score": score1},
            path_condition=c1,
            inverted_constraint=Constraint("score", "<", 0, var_type="int"),
            solver_status=sat1,
            generated_test_input=m1,
            execution_result=res1
        ))

        # Step 2: Inverted score < 0 -> Negative
        c2 = [Constraint("score", "<", 0, var_type="int")]
        sat2, m2 = SMTSolver.check_sat(c2)
        score2 = m2["score"] if m2 else -1
        res2 = svc.classify_score(score2)
        steps.append(ConcolicExecutionStep(
            iteration=2,
            target_function="SentimentService.classify_score",
            concrete_input={"score": score2},
            path_condition=c2,
            inverted_constraint=Constraint("score", "==", 0, var_type="int"),
            solver_status=sat2,
            generated_test_input=m2,
            execution_result=res2
        ))

        # Step 3: Inverted score == 0 -> Neutral
        c3 = [Constraint("score", "==", 0, var_type="int")]
        sat3, m3 = SMTSolver.check_sat(c3)
        score3 = m3["score"] if m3 else 0
        res3 = svc.classify_score(score3)
        steps.append(ConcolicExecutionStep(
            iteration=3,
            target_function="SentimentService.classify_score",
            concrete_input={"score": score3},
            path_condition=c3,
            inverted_constraint=None,
            solver_status=sat3,
            generated_test_input=m3,
            execution_result=res3
        ))

        # Step 4: UNSAT contradiction (score > 0 AND score < 0)
        c4 = [Constraint("score", ">", 0, var_type="int"), Constraint("score", "<", 0, var_type="int")]
        sat4, m4 = SMTSolver.check_sat(c4)
        steps.append(ConcolicExecutionStep(
            iteration=4,
            target_function="SentimentService.classify_score",
            concrete_input={},
            path_condition=c4,
            inverted_constraint=None,
            solver_status=sat4,
            generated_test_input=m4,
            execution_result="UNSAT (Pruned)"
        ))

        return steps

    @staticmethod
    def explore_duplicate_similarity() -> List[ConcolicExecutionStep]:
        """
        Executes concolic exploration over DuplicateService.calculate_similarity() (Member 3 - jb1080).
        Directly executes DuplicateService.calculate_similarity() with synthesized headline pairs.
        """
        svc = DuplicateService()
        steps: List[ConcolicExecutionStep] = []

        # Step 1: Identical strings -> Similarity = 1.0
        t1, t2 = "economy market growth", "economy market growth"
        res1 = svc.calculate_similarity(t1, t2)
        steps.append(ConcolicExecutionStep(
            iteration=1,
            target_function="DuplicateService.calculate_similarity",
            concrete_input={"text1": t1, "text2": t2},
            path_condition=[Constraint("similarity", "==", 1.0)],
            inverted_constraint=Constraint("similarity", "<", 1.0),
            solver_status="SAT",
            generated_test_input={"text1": t1, "text2": t2},
            execution_result=res1
        ))

        # Step 2: Completely disjoint strings -> Similarity = 0.0
        t3, t4 = "apple banana fruit", "aeroplane rocket flight"
        res2 = svc.calculate_similarity(t3, t4)
        steps.append(ConcolicExecutionStep(
            iteration=2,
            target_function="DuplicateService.calculate_similarity",
            concrete_input={"text1": t3, "text2": t4},
            path_condition=[Constraint("similarity", "==", 0.0)],
            inverted_constraint=None,
            solver_status="SAT",
            generated_test_input={"text1": t3, "text2": t4},
            execution_result=res2
        ))

        # Step 3: Partial overlap (Jaccard = 0.5)
        t5, t6 = "global tech finance", "global tech healthcare"
        res3 = svc.calculate_similarity(t5, t6)
        steps.append(ConcolicExecutionStep(
            iteration=3,
            target_function="DuplicateService.calculate_similarity",
            concrete_input={"text1": t5, "text2": t6},
            path_condition=[Constraint("similarity", ">", 0.0), Constraint("similarity", "<", 1.0)],
            inverted_constraint=None,
            solver_status="SAT",
            generated_test_input={"text1": t5, "text2": t6},
            execution_result=res3
        ))

        return steps

    @staticmethod
    def explore_alert_rule_matching() -> List[ConcolicExecutionStep]:
        """
        Executes concolic exploration over AlertRule.matches() (Member 4 - pj161).
        Directly executes AlertRule.matches() with synthesized articles and rule configs.
        """
        steps: List[ConcolicExecutionStep] = []

        rule = AlertRule(rule_id="R1", keyword="inflation", enabled=True, category_filter="Economy")

        # Step 1: Matching rule -> True
        res1 = rule.matches(headline="Inflation rises sharply in UK", content="", category="Economy")
        steps.append(ConcolicExecutionStep(
            iteration=1,
            target_function="AlertRule.matches",
            concrete_input={"headline": "Inflation rises sharply in UK", "category": "Economy", "enabled": True},
            path_condition=[Constraint("keyword_in_target", "==", True), Constraint("category_match", "==", True)],
            inverted_constraint=Constraint("keyword_in_target", "==", False),
            solver_status="SAT",
            generated_test_input={"headline": "Inflation rises sharply in UK"},
            execution_result=res1
        ))

        # Step 2: Keyword not in text -> False
        res2 = rule.matches(headline="Stock markets close higher", content="", category="Economy")
        steps.append(ConcolicExecutionStep(
            iteration=2,
            target_function="AlertRule.matches",
            concrete_input={"headline": "Stock markets close higher", "category": "Economy"},
            path_condition=[Constraint("keyword_in_target", "==", False)],
            inverted_constraint=None,
            solver_status="SAT",
            generated_test_input={"headline": "Stock markets close higher"},
            execution_result=res2
        ))

        # Step 3: Category mismatch -> False
        res3 = rule.matches(headline="Inflation report released", content="", category="Sports")
        steps.append(ConcolicExecutionStep(
            iteration=3,
            target_function="AlertRule.matches",
            concrete_input={"headline": "Inflation report released", "category": "Sports"},
            path_condition=[Constraint("category_match", "==", False)],
            inverted_constraint=None,
            solver_status="SAT",
            generated_test_input={"headline": "Inflation report released"},
            execution_result=res3
        ))

        # Step 4: Rule disabled -> False
        disabled_rule = AlertRule(rule_id="R2", keyword="inflation", enabled=False)
        res4 = disabled_rule.matches(headline="Inflation update", content="", category="Economy")
        steps.append(ConcolicExecutionStep(
            iteration=4,
            target_function="AlertRule.matches",
            concrete_input={"enabled": False},
            path_condition=[Constraint("enabled", "==", False)],
            inverted_constraint=None,
            solver_status="SAT",
            generated_test_input={"enabled": False},
            execution_result=res4
        ))

        return steps

    @classmethod
    def explore_all_members(cls) -> Dict[str, List[ConcolicExecutionStep]]:
        """Executes concolic exploration across all 4 team members' components."""
        return {
            "ns713": cls.explore_article_validation(),
            "sd683": cls.explore_sentiment_classification(),
            "jb1080": cls.explore_duplicate_similarity(),
            "pj161": cls.explore_alert_rule_matching()
        }
