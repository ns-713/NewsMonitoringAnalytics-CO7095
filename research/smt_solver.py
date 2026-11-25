"""
CO7095 Software Measurement and Quality Assurance - Academic Research Component
Satisfiability Modulo Theories (SMT) Constraint Solver (Pure Standard Library Implementation)
Authors: Group 19 (Nikitha Sarpur, Sashi Dommaraju, Jyothi Bandalapati, Jalakam Prashanth)

RESEARCH OBJECTIVE:
Provides an automated SMT solver combining:
1. Propositional Logic Satisfiability (genuine Davis-Putnam-Logemann-Loveland / DPLL search).
2. Theory of Linear Integer Arithmetic (T_LIA) for integer variables and inequalities.
3. Theory of Strings (T_String) for non-emptiness, length bounds, and finite string sets.
4. Synthesizes concrete satisfying assignments (Models) for feasible path conditions.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
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

        # Automatic adaptation: if comparing string length against an integer
        if isinstance(val, str) and isinstance(self.value, int) and self.operator in ("<", "<=", ">", ">="):
            actual_val = len(val)
        else:
            actual_val = val

        try:
            if self.operator == "==":
                return actual_val == self.value
            elif self.operator == "!=":
                return actual_val != self.value
            elif self.operator == "<":
                return actual_val < self.value
            elif self.operator == "<=":
                return actual_val <= self.value
            elif self.operator == ">":
                return actual_val > self.value
            elif self.operator == ">=":
                return actual_val >= self.value
            elif self.operator == "in":
                return actual_val in self.value
            elif self.operator == "not_in":
                return actual_val not in self.value
            elif self.operator == "is_empty":
                return not bool(actual_val)
            elif self.operator == "is_not_empty":
                return bool(actual_val)
        except TypeError:
            return False
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


class DPLLSolver:
    """
    Propositional Logic SAT Solver implementing the Davis-Putnam-Logemann-Loveland (DPLL) algorithm.
    Clauses are sets of literals: positive int = variable, negative int = negated variable.
    """
    @staticmethod
    def solve(clauses: List[Set[int]]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        assignment: Dict[int, bool] = {}
        result, final_assignment = DPLLSolver._dpll(clauses, assignment)
        if result:
            return True, final_assignment
        return False, None

    @staticmethod
    def _dpll(clauses: List[Set[int]], assignment: Dict[int, bool]) -> Tuple[bool, Dict[int, bool]]:
        # 1. Unit Propagation
        while True:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            unit_lit = next(iter(unit_clauses[0]))
            var = abs(unit_lit)
            val = (unit_lit > 0)
            assignment[var] = val
            simplified = DPLLSolver._simplify(clauses, unit_lit)
            if simplified is None:
                return False, {}
            clauses = simplified

        # 2. Check if all clauses are satisfied (empty formula)
        if not clauses:
            return True, assignment

        # 3. Check if an empty clause exists (conflict -> backtrack)
        if any(len(c) == 0 for c in clauses):
            return False, {}

        # 4. Pure Literal Elimination
        all_lits = set().union(*clauses) if clauses else set()
        pure_lits = {lit for lit in all_lits if -lit not in all_lits}
        for lit in pure_lits:
            var = abs(lit)
            val = (lit > 0)
            assignment[var] = val
            simplified = DPLLSolver._simplify(clauses, lit)
            if simplified is None:
                return False, {}
            clauses = simplified
            if not clauses:
                return True, assignment

        # 5. Branching Search (Heuristic: choose first unassigned variable)
        all_vars = {abs(lit) for c in clauses for lit in c}
        unassigned = [v for v in all_vars if v not in assignment]
        if not unassigned:
            return True, assignment
        branch_var = unassigned[0]

        # Branch True
        assign_true = dict(assignment)
        assign_true[branch_var] = True
        c_true = DPLLSolver._simplify(clauses, branch_var)
        if c_true is not None:
            sat, res = DPLLSolver._dpll(c_true, assign_true)
            if sat:
                return True, res

        # Branch False (Backtracking step)
        assign_false = dict(assignment)
        assign_false[branch_var] = False
        c_false = DPLLSolver._simplify(clauses, -branch_var)
        if c_false is not None:
            sat, res = DPLLSolver._dpll(c_false, assign_false)
            if sat:
                return True, res

        return False, {}

    @staticmethod
    def _simplify(clauses: List[Set[int]], literal: int) -> Optional[List[Set[int]]]:
        simplified = []
        for c in clauses:
            if literal in c:
                continue  # Clause satisfied by literal
            if -literal in c:
                new_c = c - {-literal}
                if not new_c:
                    return None  # Empty clause reached: conflict
                simplified.append(new_c)
            else:
                simplified.append(set(c))
        return simplified


class SMTSolver:
    """
    Lightweight First-Order Logic SMT Solver for symbolic path condition satisfiability.
    Combines DPLL Propositional Satisfiability with Theory Solvers for Linear Integer
    Arithmetic (T_LIA) and Theory of Strings (T_String).
    """

    @staticmethod
    def dpll(clauses: List[Set[int]]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        """Exposes the DPLL Boolean satisfiability solver."""
        return DPLLSolver.solve(clauses)

    @staticmethod
    def check_sat(path_condition: List[Constraint]) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Determines if the conjunction of path constraints is SAT or UNSAT using
        domain propagation across T_LIA and T_String.
        If SAT, synthesizes and returns a concrete model assignment.
        """
        # Phase 1: Determine variable domains (Integer vs String)
        var_types: Dict[str, str] = {}
        for c in path_condition:
            var = c.variable
            if c.operator in ("is_empty", "is_not_empty"):
                var_types[var] = "str"
            elif c.operator in ("in", "not_in"):
                if isinstance(c.value, (list, tuple, set)) and any(isinstance(x, str) for x in c.value):
                    var_types[var] = "str"
            elif c.operator in ("==", "!=") and isinstance(c.value, str):
                var_types[var] = "str"

        for c in path_condition:
            var = c.variable
            if var not in var_types:
                if isinstance(c.value, int) and c.operator in ("<", "<=", ">", ">="):
                    if var.lower() in ("h", "headline", "source", "source_name", "url", "article_url", "title", "content", "sentiment"):
                        var_types[var] = "str"
                    else:
                        var_types[var] = "int"

        # Phase 2: Theory Domain Trackers
        int_domains: Dict[str, Tuple[int, int, Set[int]]] = {}  # var -> (min_val, max_val, forbidden_values)
        str_lengths: Dict[str, Tuple[int, int]] = {}  # var -> (min_len, max_len)
        allowed_sets: Dict[str, Set[Any]] = {}
        forbidden_sets: Dict[str, Set[Any]] = {}
        exact_assignments: Dict[str, Any] = {}

        for c in path_condition:
            var = c.variable
            op = c.operator
            val = c.value
            v_type = var_types.get(var, "int" if isinstance(val, int) else "str")

            if op == "==":
                if var in exact_assignments and exact_assignments[var] != val:
                    return "UNSAT", None
                exact_assignments[var] = val

            elif op == "!=":
                forbidden_sets.setdefault(var, set()).add(val)
                if var in exact_assignments and exact_assignments[var] == val:
                    return "UNSAT", None

            elif op == "in" and isinstance(val, (list, tuple, set)):
                allowed = set(val)
                if var in allowed_sets:
                    allowed_sets[var] = allowed_sets[var].intersection(allowed)
                else:
                    allowed_sets[var] = allowed
                if not allowed_sets[var]:
                    return "UNSAT", None

            elif op == "not_in" and isinstance(val, (list, tuple, set)):
                forbidden_sets.setdefault(var, set()).update(val)

            elif op == "is_empty":
                str_lengths[var] = (0, 0)
                exact_assignments[var] = ""

            elif op == "is_not_empty":
                cur_min, cur_max = str_lengths.get(var, (0, 1000))
                str_lengths[var] = (max(cur_min, 1), cur_max)

            elif op in ("<", "<=", ">", ">=") and isinstance(val, int):
                if v_type == "int":
                    cur_min, cur_max, forb = int_domains.get(var, (-10000, 10000, set()))
                    if op == "<":
                        cur_max = min(cur_max, val - 1)
                    elif op == "<=":
                        cur_max = min(cur_max, val)
                    elif op == ">":
                        cur_min = max(cur_min, val + 1)
                    elif op == ">=":
                        cur_min = max(cur_min, val)
                    if cur_min > cur_max:
                        return "UNSAT", None
                    int_domains[var] = (cur_min, cur_max, forb)
                else:
                    # String length constraint
                    cur_min, cur_max = str_lengths.get(var, (0, 1000))
                    if op == "<":
                        cur_max = min(cur_max, val - 1)
                    elif op == "<=":
                        cur_max = min(cur_max, val)
                    elif op == ">":
                        cur_min = max(cur_min, val + 1)
                    elif op == ">=":
                        cur_min = max(cur_min, val)
                    if cur_min > cur_max:
                        return "UNSAT", None
                    str_lengths[var] = (cur_min, cur_max)

        # Phase 3: Model Synthesis
        model: Dict[str, Any] = dict(exact_assignments)

        # 1. Allowed / Forbidden sets
        for var, allowed in allowed_sets.items():
            forbidden = forbidden_sets.get(var, set())
            valid_candidates = [x for x in allowed if x not in forbidden]
            if not valid_candidates:
                return "UNSAT", None
            if var in model:
                if model[var] not in valid_candidates:
                    return "UNSAT", None
            else:
                model[var] = valid_candidates[0]

        # 2. Check forbidden sets against exact assignments
        for var, forbidden in forbidden_sets.items():
            if var in model and model[var] in forbidden:
                return "UNSAT", None

        # 3. Synthesize integer variables
        for var, (cur_min, cur_max, forb) in int_domains.items():
            if var in model:
                if model[var] < cur_min or model[var] > cur_max or model[var] in forb:
                    return "UNSAT", None
            else:
                forbidden = forbidden_sets.get(var, set()).union(forb)
                chosen = None
                # Prefer 0 or natural small positive integers
                preferred_candidates = [0, 1, 5, -1] + list(range(cur_min, cur_max + 1))
                for candidate in preferred_candidates:
                    if cur_min <= candidate <= cur_max and candidate not in forbidden:
                        chosen = candidate
                        break
                if chosen is None:
                    return "UNSAT", None
                model[var] = chosen

        # 4. Synthesize string variables with length bounds
        for var, (min_l, max_l) in str_lengths.items():
            if min_l > max_l:
                return "UNSAT", None
            if var in model:
                if len(str(model[var])) < min_l or len(str(model[var])) > max_l:
                    return "UNSAT", None
            else:
                forbidden = forbidden_sets.get(var, set())
                candidate_str = "A" * max(min_l, 0)
                if candidate_str in forbidden:
                    candidate_str = "B" * max(min_l, 0)
                model[var] = candidate_str

        # 5. Materialize remaining unassigned variables
        for c in path_condition:
            var = c.variable
            if var not in model:
                v_type = var_types.get(var, "str")
                forbidden = forbidden_sets.get(var, set())
                if v_type == "int":
                    for cand in (0, 1, 2, -1):
                        if cand not in forbidden:
                            model[var] = cand
                            break
                else:
                    for cand in ("ValidToken", "SampleValue", "TestText"):
                        if cand not in forbidden:
                            model[var] = cand
                            break

        # Phase 4: Final Formal Model Verification
        for c in path_condition:
            if not c.evaluate(model):
                return "UNSAT", None

        return "SAT", model
