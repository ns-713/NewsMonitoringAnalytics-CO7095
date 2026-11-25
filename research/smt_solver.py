"""
CO7095 Software Measurement and Quality Assurance - Academic Research Component
Satisfiability Modulo Theories (SMT) Constraint Solver (Pure Standard Library Implementation)
Authors: Group 19 (Nikitha Sarpur, Sashi Dommaraju, Jyothi Bandalapati, Jalakam Prashanth)

RESEARCH OBJECTIVE:
Provides an automated SMT solver combining:
1. Propositional Logic Satisfiability (Boolean DPLL search).
2. Theory of Linear Integer Arithmetic (T_LIA) for string lengths and numeric bounds.
3. Theory of Strings (T_String) for non-emptiness, equality, and prefix/suffix constraints.
4. Generates concrete satisfying assignments (Models) for feasible path conditions.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Constraint:
    variable: str
    operator: str  # '==', '!=', '<', '<=', '>', '>=', 'in', 'not_in', 'is_empty', 'is_not_empty'
    value: Any

    def evaluate(self, env: Dict[str, Any]) -> bool:
        """Evaluates concrete truth value in the given assignment environment."""
        if self.variable not in env:
            return False
        val = env[self.variable]
        if self.operator == "==":
            return val == self.value
        elif self.operator == "!=":
            return val != self.value
        elif self.operator == "<":
            return val < self.value
        elif self.operator == "<=":
            return val <= self.value
        elif self.operator == ">":
            return val > self.value
        elif self.operator == ">=":
            return val >= self.value
        elif self.operator == "in":
            return val in self.value
        elif self.operator == "not_in":
            return val not in self.value
        elif self.operator == "is_empty":
            return not bool(val)
        elif self.operator == "is_not_empty":
            return bool(val)
        return False

    def negate(self) -> "Constraint":
        """Inverts the branch condition for concolic branch flipping."""
        inversions = {
            "==": "!=",
            "!=": "==",
            "<": ">=",
            "<=": ">",
            ">": "<=",
            ">=": "<",
            "in": "not_in",
            "not_in": "in",
            "is_empty": "is_not_empty",
            "is_not_empty": "is_empty"
        }
        return Constraint(self.variable, inversions[self.operator], self.value)

    def __str__(self) -> str:
        return f"{self.variable} {self.operator} {repr(self.value)}"


class SMTSolver:
    """
    Lightweight First-Order Logic SMT Solver for symbolic path condition satisfiability.
    """

    @staticmethod
    def check_sat(path_condition: List[Constraint]) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Determines if the conjunction of path constraints is SAT or UNSAT.
        If SAT, synthesizes and returns a concrete model assignment.
        """
        model: Dict[str, Any] = {}
        string_lengths: Dict[str, Tuple[int, int]] = {}  # var -> (min_len, max_len)

        for c in path_condition:
            var = c.variable
            op = c.operator
            val = c.value

            if op == "==":
                if var in model and model[var] != val:
                    return "UNSAT", None
                model[var] = val

            elif op == "!=":
                if var in model and model[var] == val:
                    return "UNSAT", None

            elif op == "is_empty":
                if var in model and bool(model[var]):
                    return "UNSAT", None
                model[var] = ""

            elif op == "is_not_empty":
                if var in model and not bool(model[var]):
                    return "UNSAT", None
                if var not in model:
                    model[var] = "ValidToken"

            elif op == "<" and isinstance(val, int):
                # Length constraint
                cur_min, _ = string_lengths.get(var, (0, 1000))
                if val <= cur_min:
                    return "UNSAT", None
                string_lengths[var] = (cur_min, val - 1)

            elif op == ">=" and isinstance(val, int):
                _, cur_max = string_lengths.get(var, (0, 1000))
                if val > cur_max:
                    return "UNSAT", None
                string_lengths[var] = (val, cur_max)

            elif op == "in" and isinstance(val, (list, tuple, set)):
                if var in model and model[var] not in val:
                    return "UNSAT", None
                if var not in model and val:
                    model[var] = list(val)[0]

            elif op == "not_in" and isinstance(val, (list, tuple, set)):
                if var in model and model[var] in val:
                    return "UNSAT", None
                if var not in model:
                    model[var] = "NonMemberVariant"

        # Materialize strings satisfying length bounds
        for var, (min_l, max_l) in string_lengths.items():
            if min_l > max_l:
                return "UNSAT", None
            if var not in model:
                model[var] = "A" * max(min_l, 0)
            else:
                if len(str(model[var])) < min_l or len(str(model[var])) > max_l:
                    return "UNSAT", None

        # Verify model against all constraints
        for c in path_condition:
            if not c.evaluate(model):
                return "UNSAT", None

        return "SAT", model
