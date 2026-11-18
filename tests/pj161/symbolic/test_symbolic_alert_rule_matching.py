"""
Symbolic Execution Research and Test Harness: Alert Rule Matching
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Course: CO7095 - Software Measurement and Quality Assurance

RESEARCH OBJECTIVE:
Symbolically evaluate AlertRule.matches(headline, content, category) to determine
all distinct execution path conditions and solve for inputs triggering each branch.

TARGET FUNCTION:
    def matches(self, headline: str, content: str = "", category: str = "") -> bool:
        if not self.enabled:                                                      # Branch 1
            return False
        if not self.keyword:                                                      # Branch 2
            return False
        if self.category_filter and self.category_filter.lower() != (category or "").lower(): # Branch 3
            return False
        target_text = f"{headline} {content}".lower()
        return self.keyword in target_text                                        # Branch 4

FORMAL SYMBOLIC SPECIFICATION:
    Symbolic Variables:
        E  ∈ {True, False}           (Rule enabled status)
        K  ∈ SymbolicString           (Monitored keyword)
        CF ∈ SymbolicString ∪ {None}  (Category filter)
        H  ∈ SymbolicString           (Article headline)
        C  ∈ SymbolicString           (Article content)
        Cat∈ SymbolicString           (Article category)

    Path Conditions:
        Path 1 (Rule Inactive):         Φ_1 ≡ (E == False) ==> Return False
        Path 2 (Blank Keyword):         Φ_2 ≡ (E == True) ∧ (len(K) == 0) ==> Return False
        Path 3 (Category Mismatch):     Φ_3 ≡ (E == True) ∧ (len(K) > 0) ∧ (CF ≠ None) ∧ (CF ≠ Cat) ==> Return False
        Path 4 (Keyword Match Success): Φ_4 ≡ (E == True) ∧ (len(K) > 0) ∧ (CF == None ∨ CF == Cat) ∧ (K ∈ (H ∪ C)) ==> Return True
        Path 5 (Keyword Absent):        Φ_5 ≡ (E == True) ∧ (len(K) > 0) ∧ (CF == None ∨ CF == Cat) ∧ (K ∉ (H ∪ C)) ==> Return False
"""

import unittest
from models.alert_rule import AlertRule


class TestSymbolicAlertRuleMatching(unittest.TestCase):
    """Symbolic constraint execution for AlertRule.matches()."""

    def test_tc_sym_alt_path_solving(self):
        """
        Executes concrete inputs derived from the 5 formal symbolic path conditions.
        """
        path_test_cases = [
            # (Path ID, Enabled, Keyword, CategoryFilter, Headline, Content, Category, ExpectedResult)
            ("P1_Disabled", False, "climate", None, "Climate Accord Signed", "", "Environment", False),
            ("P2_EmptyKeyword", True, "", None, "Any Headline", "", "General", False),
            ("P3_CategoryMismatch", True, "energy", "Environment", "Energy Bill Debate", "", "Politics", False),
            ("P4_MatchSuccessHeadline", True, "fusion", "Science", "Nuclear Fusion Test", "", "Science", True),
            ("P4_MatchSuccessContent", True, "fusion", None, "Energy Update", "Plasma fusion ignited", "Science", True),
            ("P5_KeywordAbsent", True, "fusion", "Science", "Space Telescope Discovery", "Stars mapped", "Science", False)
        ]

        for path_id, enabled, kw, cat_filter, h, c, cat, expected in path_test_cases:
            with self.subTest(path=path_id):
                rule = AlertRule(keyword=kw, category_filter=cat_filter, enabled=enabled)
                result = rule.matches(headline=h, content=c, category=cat)
                self.assertEqual(result, expected, f"Failed for path {path_id}!")


if __name__ == "__main__":
    unittest.main()
