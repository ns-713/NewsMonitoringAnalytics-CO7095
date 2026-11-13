"""
Symbolic Execution Research and Test Harness: NewsArticle.validate()
Member 1: Nikitha Sarpur (ns713 - 259060190)
Course: CO7095 - Software Measurement and Quality Assurance

RESEARCH OBJECTIVE:
Symbolically evaluate the execution tree of NewsArticle.validate() to construct path conditions,
solve path constraints, and automatically generate inputs covering all feasibility branches.

TARGET FUNCTION:
    def validate(self):
        errors = []
        if not self.headline:                                       # Branch 1
            errors.append("Headline cannot be empty.")
        elif len(self.headline) < 3:                                # Branch 2
            errors.append("Headline must be at least 3 characters long.")
        if not self.source_name:                                    # Branch 3
            errors.append("Source name cannot be empty.")
        if not self.article_url:                                    # Branch 4
            errors.append("Article URL cannot be empty.")
        if self.sentiment not in ["Positive", "Negative", "Neutral"]: # Branch 5
            errors.append(...)
        return len(errors) == 0, errors

SYMBOLIC VARIABLES:
    H  = SymbolicString(headline),      L_H = len(H)
    SN = SymbolicString(source_name),   L_SN = len(SN)
    AU = SymbolicString(article_url),   L_AU = len(AU)
    S  = SymbolicString(sentiment)
"""

import unittest
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from models.article import NewsArticle


@dataclass
class SymbolicConstraint:
    variable: str
    operator: str
    value: Any

    def __str__(self) -> str:
        return f"{self.variable} {self.operator} {repr(self.value)}"


@dataclass
class ExecutionPath:
    path_id: str
    path_condition: List[SymbolicConstraint]
    expected_valid: bool
    generated_concrete_input: Dict[str, Any]


class SymbolicArticleValidationEngine:
    """
    Simulated symbolic execution engine analyzing NewsArticle.validate() execution paths.
    """

    @staticmethod
    def explore_paths() -> List[ExecutionPath]:
        """
        Explores all distinct symbolic path conditions through the validation function.
        """
        paths = []

        # Path 1: H == "" (Branch 1 True)
        paths.append(ExecutionPath(
            path_id="P1",
            path_condition=[
                SymbolicConstraint("L_H", "==", 0),
                SymbolicConstraint("L_SN", ">", 0),
                SymbolicConstraint("L_AU", ">", 0),
                SymbolicConstraint("S", "in", ["Positive", "Negative", "Neutral"])
            ],
            expected_valid=False,
            generated_concrete_input={
                "headline": "",
                "source_name": "BBC News",
                "article_url": "https://bbc.com/1",
                "sentiment": "Positive"
            }
        ))

        # Path 2: L_H in {1, 2} (Branch 1 False, Branch 2 True)
        paths.append(ExecutionPath(
            path_id="P2",
            path_condition=[
                SymbolicConstraint("L_H", ">", 0),
                SymbolicConstraint("L_H", "<", 3),
                SymbolicConstraint("L_SN", ">", 0),
                SymbolicConstraint("L_AU", ">", 0),
                SymbolicConstraint("S", "in", ["Positive", "Negative", "Neutral"])
            ],
            expected_valid=False,
            generated_concrete_input={
                "headline": "UK",
                "source_name": "BBC News",
                "article_url": "https://bbc.com/1",
                "sentiment": "Neutral"
            }
        ))

        # Path 3: SN == "" (Branch 3 True)
        paths.append(ExecutionPath(
            path_id="P3",
            path_condition=[
                SymbolicConstraint("L_H", ">=", 3),
                SymbolicConstraint("L_SN", "==", 0),
                SymbolicConstraint("L_AU", ">", 0),
                SymbolicConstraint("S", "in", ["Positive", "Negative", "Neutral"])
            ],
            expected_valid=False,
            generated_concrete_input={
                "headline": "Prime Minister Announces General Elections",
                "source_name": "",
                "article_url": "https://bbc.com/1",
                "sentiment": "Positive"
            }
        ))

        # Path 4: AU == "" (Branch 4 True)
        paths.append(ExecutionPath(
            path_id="P4",
            path_condition=[
                SymbolicConstraint("L_H", ">=", 3),
                SymbolicConstraint("L_SN", ">", 0),
                SymbolicConstraint("L_AU", "==", 0),
                SymbolicConstraint("S", "in", ["Positive", "Negative", "Neutral"])
            ],
            expected_valid=False,
            generated_concrete_input={
                "headline": "Major Breakthrough in Nuclear Fusion Energy",
                "source_name": "Nature Scientific",
                "article_url": "",
                "sentiment": "Positive"
            }
        ))

        # Path 5: S not in Valid Sentiments (Branch 5 True)
        paths.append(ExecutionPath(
            path_id="P5",
            path_condition=[
                SymbolicConstraint("L_H", ">=", 3),
                SymbolicConstraint("L_SN", ">", 0),
                SymbolicConstraint("L_AU", ">", 0),
                SymbolicConstraint("S", "not in", ["Positive", "Negative", "Neutral"])
            ],
            expected_valid=False,
            generated_concrete_input={
                "headline": "Global Market Indices Open Higher",
                "source_name": "Bloomberg",
                "article_url": "https://bloomberg.com/market",
                "sentiment": "Optimistic"  # Invalid label
            }
        ))

        # Path 6: Completely Satisfying Path (All Branches Pass)
        paths.append(ExecutionPath(
            path_id="P6",
            path_condition=[
                SymbolicConstraint("L_H", ">=", 3),
                SymbolicConstraint("L_SN", ">", 0),
                SymbolicConstraint("L_AU", ">", 0),
                SymbolicConstraint("S", "in", ["Positive", "Negative", "Neutral"])
            ],
            expected_valid=True,
            generated_concrete_input={
                "headline": "Central Bank Decreases Base Interest Rates",
                "source_name": "Reuters",
                "article_url": "https://reuters.com/rates",
                "sentiment": "Positive"
            }
        ))

        return paths


class TestSymbolicArticleValidation(unittest.TestCase):
    """Executes symbolically synthesized test cases on NewsArticle.validate()."""

    def setUp(self):
        self.paths = SymbolicArticleValidationEngine.explore_paths()

    def test_tc_sym_art_all_paths_feasible(self):
        """Validates that each symbolic path condition correctly corresponds to code execution."""
        for path in self.paths:
            inp = path.generated_concrete_input
            article = NewsArticle(
                headline=inp["headline"],
                source_name=inp["source_name"],
                article_url=inp["article_url"],
                sentiment=inp["sentiment"]
            )
            is_valid, errors = article.validate()

            with self.subTest(path_id=path.path_id):
                self.assertEqual(
                    is_valid,
                    path.expected_valid,
                    f"Path {path.path_id} constraint evaluation mismatch! Constraints: {[str(c) for c in path.path_condition]}"
                )


if __name__ == "__main__":
    unittest.main()
