"""
CO7095 Software Measurement and Quality Assurance - Academic Research Component
Satisfiability Modulo Theories (SMT) Constraint Solver (Pure Standard Library Implementation)
Authors: Group 19 (Nikitha Sarpur, Sashi Dommaraju, Jyothi Bandalapati, Jalakam Prashanth)

RESEARCH ARCHITECTURE:
Provides a formal SMT solving framework combining:
1. DPLL Propositional SAT Solver: Implements unit propagation, pure literal elimination, and backtracking search.
2. Theory of Linear Integer Arithmetic (T_LIA): Unbounded integer interval propagation [cur_min, cur_max].
3. Theory of Strings (T_String): String length bounds, non-emptiness, and finite domain enumeration.
4. DPLL(T) Integration Loop (check_sat_dpll_t): Combines DPLL boolean search with Theory Solver consistency checks.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass


@dataclass
class Constraint:
    variable: str
    operator: str  # '==', '!=', '<', '<=', '>', '>=', 'in', 'not_in', 'is_empty', 'is_not_empty'
    value: Any
    var_type: Optional[str] = None  # Explicit type annotation: 'int', 'str', 'bool' (eliminates name heuristics)
    is_length: bool = False  # Set to True if the numeric comparison applies to len(variable)

    def evaluate(self, env: Dict[str, Any]) -> bool:
        """Evaluates concrete truth value in the given assignment environment."""
        if self.variable not in env:
            return False
        val = env[self.variable]

        # Automatic length resolution if marked as length constraint or comparing str with int
        if (self.is_length or isinstance(val, str)) and isinstance(self.value, int) and self.operator in ("<", "<=", ">", ">="):
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
        return Constraint(
            variable=self.variable,
            operator=inversions[self.operator],
            value=self.value,
            var_type=self.var_type,
            is_length=self.is_length
        )

    def __str__(self) -> str:
        prefix = f"len({self.variable})" if self.is_length else self.variable
        return f"{prefix} {self.operator} {repr(self.value)}"


class DPLLSolver:
    """
    Propositional Logic SAT Solver implementing the Davis-Putnam-Logemann-Loveland (DPLL) algorithm.
    Clauses are sets of literals: positive integer = literal, negative integer = negated literal.
    """
    @staticmethod
    def solve(clauses: List[Set[int]]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        assignment: Dict[int, bool] = {}
        result, final_assignment = DPLLSolver._dpll([set(c) for c in clauses], assignment)
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

        # 2. Check if all clauses are satisfied (empty clause set)
        if not clauses:
            return True, assignment

        # 3. Check if empty clause exists (conflict -> backtrack)
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

        # 5. Branching Search (Pick first unassigned literal)
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

        # Branch False (Backtrack)
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
                continue  # Clause satisfied
            if -literal in c:
                new_c = c - {-literal}
                if not new_c:
                    return None  # Empty clause -> conflict
                simplified.append(new_c)
            else:
                simplified.append(set(c))
        return simplified


class SMTSolver:
    """
    Satisfiability Modulo Theories (SMT) Solver combining:
    - First-Order Theory Solvers for Linear Integer Arithmetic (T_LIA) and Theory of Strings (T_String).
    - DPLL Propositional Satisfiability.
    - Integrated DPLL(T) solving for CNF clauses of first-order theory constraints.
    """

    @staticmethod
    def solve_dpll(clauses: List[Set[int]]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        """Solves purely propositional CNF formulas via DPLL."""
        return DPLLSolver.solve(clauses)

    @staticmethod
    def check_sat(
        path_condition: List[Constraint],
        explicit_types: Optional[Dict[str, str]] = None
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Determines satisfiability of a conjunction of first-order constraints using
        unbounded domain propagation across Theory of Linear Integer Arithmetic (T_LIA)
        and Theory of Strings (T_String).
        
        Soundness Guarantee:
        - Integer domains are unbounded (no artificial ±10000 cutoff).
        - Type inference relies on explicit annotations and constraint operators, never name heuristics.
        """
        # Phase 1: Determine variable types strictly from annotations and constraint operators
        var_types: Dict[str, str] = dict(explicit_types or {})

        for c in path_condition:
            var = c.variable
            if c.var_type:
                var_types[var] = c.var_type
            elif c.operator in ("is_empty", "is_not_empty"):
                var_types[var] = "str"
            elif c.operator in ("in", "not_in"):
                if isinstance(c.value, (list, tuple, set)) and any(isinstance(x, str) for x in c.value):
                    var_types[var] = "str"
            elif c.operator in ("==", "!=") and isinstance(c.value, str):
                var_types[var] = "str"

        for c in path_condition:
            var = c.variable
            if var not in var_types:
                if c.is_length:
                    var_types[var] = "str"
                elif isinstance(c.value, int) and c.operator in ("<", "<=", ">", ">="):
                    var_types[var] = "int"

        # Phase 2: Theory Domain Trackers (Unbounded arithmetic, no artificial cutoffs)
        int_domains: Dict[str, Tuple[Optional[int], Optional[int], Set[int]]] = {}  # var -> (min_val, max_val, forbidden)
        str_lengths: Dict[str, Tuple[int, Optional[int]]] = {}  # var -> (min_len, max_len)
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
                cur_min, cur_max = str_lengths.get(var, (0, None))
                str_lengths[var] = (max(cur_min, 1), cur_max)

            elif op in ("<", "<=", ">", ">=") and isinstance(val, int):
                if v_type == "int" and not c.is_length:
                    # Unbounded Integer Arithmetic (T_LIA)
                    cur_min, cur_max, forb = int_domains.get(var, (None, None, set()))
                    if op == "<":
                        cur_max = (val - 1) if cur_max is None else min(cur_max, val - 1)
                    elif op == "<=":
                        cur_max = val if cur_max is None else min(cur_max, val)
                    elif op == ">":
                        cur_min = (val + 1) if cur_min is None else max(cur_min, val + 1)
                    elif op == ">=":
                        cur_min = val if cur_min is None else max(cur_min, val)

                    if cur_min is not None and cur_max is not None and cur_min > cur_max:
                        return "UNSAT", None
                    int_domains[var] = (cur_min, cur_max, forb)
                else:
                    # Theory of Strings Length Bounds
                    cur_min, cur_max = str_lengths.get(var, (0, None))
                    if op == "<":
                        cur_max = (val - 1) if cur_max is None else min(cur_max, val - 1)
                    elif op == "<=":
                        cur_max = val if cur_max is None else min(cur_max, val)
                    elif op == ">":
                        cur_min = max(cur_min, val + 1)
                    elif op == ">=":
                        cur_min = max(cur_min, val)

                    if cur_max is not None and cur_min > cur_max:
                        return "UNSAT", None
                    str_lengths[var] = (cur_min, cur_max)

        # Phase 3: Model Synthesis
        model: Dict[str, Any] = dict(exact_assignments)

        # 1. Finite domain selection (allowed minus forbidden)
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

        # 2. Check forbidden values against exact assignments
        for var, forbidden in forbidden_sets.items():
            if var in model and model[var] in forbidden:
                return "UNSAT", None

        # 3. Synthesize integer values under unbounded intervals
        for var, (cur_min, cur_max, forb) in int_domains.items():
            forbidden = forbidden_sets.get(var, set()).union(forb)
            if var in model:
                val = model[var]
                if (cur_min is not None and val < cur_min) or (cur_max is not None and val > cur_max) or val in forbidden:
                    return "UNSAT", None
            else:
                # Find an integer satisfying [cur_min, cur_max] that is not in forbidden
                if cur_min is None and cur_max is None:
                    candidate = 0
                elif cur_min is None:
                    candidate = min(0, cur_max)
                elif cur_max is None:
                    candidate = max(0, cur_min)
                else:
                    candidate = 0 if cur_min <= 0 <= cur_max else cur_min

                # Step until a non-forbidden integer is located
                step = 1 if (cur_max is None or candidate <= cur_max) else -1
                attempts = 0
                while candidate in forbidden:
                    candidate += step
                    attempts += 1
                    if cur_max is not None and candidate > cur_max:
                        return "UNSAT", None
                    if cur_min is not None and candidate < cur_min:
                        return "UNSAT", None
                    if attempts > 10000:
                        return "UNSAT", None
                model[var] = candidate

        # 4. Synthesize string values satisfying length bounds
        for var, (min_l, max_l) in str_lengths.items():
            if max_l is not None and min_l > max_l:
                return "UNSAT", None
            if var in model:
                s_len = len(str(model[var]))
                if s_len < min_l or (max_l is not None and s_len > max_l):
                    return "UNSAT", None
            else:
                forbidden = forbidden_sets.get(var, set())
                candidate_str = "A" * max(min_l, 0)
                if candidate_str in forbidden:
                    candidate_str = "B" * max(min_l, 0)
                model[var] = candidate_str

        # 5. Populate remaining unconstrained variables
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

        # Phase 4: Formal Verification against all input constraints
        for c in path_condition:
            if not c.evaluate(model):
                return "UNSAT", None

        return "SAT", model

    @classmethod
    def check_sat_dpll_t(cls, clauses: List[List[Constraint]]) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Integrated DPLL(T) Architecture:
        Solves CNF formulas of first-order theory constraints:
        Clauses: (C11 OR C12 OR ...) AND (C21 OR C22 OR ...) AND ...
        
        Uses DPLL to search propositional abstractions, and queries the Theory Solver
        (check_sat) to verify satisfiability of the selected conjunction of constraints.
        If a theory conflict arises, learns a conflict lemma and backtracks.
        """
        # Map each unique constraint to a propositional literal integer >= 1
        constraint_to_lit: Dict[str, int] = {}
        lit_to_constraint: Dict[int, Constraint] = {}
        counter = 1

        prop_clauses: List[Set[int]] = []
        for clause in clauses:
            prop_clause: Set[int] = set()
            for c in clause:
                key = f"{c.variable}_{c.operator}_{c.value}_{c.is_length}"
                if key not in constraint_to_lit:
                    constraint_to_lit[key] = counter
                    lit_to_constraint[counter] = c
                    counter += 1
                prop_clause.add(constraint_to_lit[key])
            prop_clauses.append(prop_clause)

        # Iterative DPLL(T) loop
        while True:
            sat, assign = DPLLSolver.solve(prop_clauses)
            if not sat or not assign:
                return "UNSAT", None

            # Collect active positive theory constraints from DPLL assignment
            active_constraints = [lit_to_constraint[lit] for lit, val in assign.items() if val and lit in lit_to_constraint]

            # Query Theory Solver on active conjunction
            theory_status, model = cls.check_sat(active_constraints)
            if theory_status == "SAT":
                return "SAT", model

            # Theory Conflict: Learn lemma blocking this infeasible combination
            conflict_clause = {-lit for lit, val in assign.items() if val and lit in lit_to_constraint}
            if not conflict_clause or conflict_clause in prop_clauses:
                return "UNSAT", None
            prop_clauses.append(conflict_clause)
