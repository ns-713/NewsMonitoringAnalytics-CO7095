"""
White-Box Tests for Alert Rules and Monitoring Service
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Statement, Branch, and Condition Coverage
"""

import unittest
import tempfile
from pathlib import Path
from models.alert_rule import AlertRule
from models.alert import Alert
from services.alert_service import AlertService


class TestAlertWhitebox(unittest.TestCase):
    """White-box testing covering all branch decisions in AlertRule and AlertService."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.rules_file = base / "rules.json"
        self.alerts_file = base / "alerts.json"
        self.service = AlertService(rules_file=self.rules_file, alerts_file=self.alerts_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_wb_alt_01_alert_rule_matches_branches(self):
        """TC-WB-ALT-01: Exercises every conditional branch in AlertRule.matches()."""
        # Branch 1: not enabled -> returns False
        r_disabled = AlertRule(keyword="tech", enabled=False)
        self.assertFalse(r_disabled.matches("Tech headline"))

        # Branch 2: empty keyword -> returns False
        r_nokw = AlertRule(keyword="", enabled=True)
        self.assertFalse(r_nokw.matches("Tech headline"))

        # Branch 3: category_filter specified but does not match -> returns False
        r_cat = AlertRule(keyword="tech", category_filter="Technology")
        self.assertFalse(r_cat.matches("Tech headline", category="Health"))

        # Branch 4: category matches, keyword in headline -> returns True
        self.assertTrue(r_cat.matches("Tech headline", category="Technology"))

        # Branch 5: keyword in content rather than headline -> returns True
        self.assertTrue(r_cat.matches("Headline", content="Deep tech content", category="Technology"))

    def test_tc_wb_alt_02_alert_rule_validate_branches(self):
        """TC-WB-ALT-02: Branch coverage of AlertRule.validate()."""
        # Empty keyword branch
        r1 = AlertRule(keyword="")
        valid1, err1 = r1.validate()
        self.assertFalse(valid1)

        # 1-char keyword branch
        r2 = AlertRule(keyword="x")
        valid2, err2 = r2.validate()
        self.assertFalse(valid2)

        # Valid keyword
        r3 = AlertRule(keyword="climate")
        valid3, err3 = r3.validate()
        self.assertTrue(valid3)

    def test_tc_wb_alt_03_toggle_and_delete_rule_branches(self):
        """TC-WB-ALT-03: Branch coverage of toggle_rule and delete_rule."""
        # Non-existent rule branch
        ok1, msg1 = self.service.toggle_rule("NON_EXISTENT")
        self.assertFalse(ok1)

        ok2, msg2 = self.service.delete_rule("NON_EXISTENT")
        self.assertFalse(ok2)

        # Existing rule toggle branch
        _, _, rule = self.service.add_rule("market")
        self.assertTrue(rule.enabled)

        ok3, _ = self.service.toggle_rule(rule.rule_id)
        self.assertTrue(ok3)
        self.assertFalse(rule.enabled)

        # Existing rule delete branch
        ok4, _ = self.service.delete_rule(rule.rule_id)
        self.assertTrue(ok4)
        self.assertEqual(len(self.service.get_rules()), 0)

    def test_tc_wb_alt_04_mark_all_alerts_read_branch(self):
        """TC-WB-ALT-04: Statement coverage of mark_all_alerts_read."""
        self.service.alerts = [
            Alert(rule_id="R1", keyword="k1", article_id="A1", headline="H1", status=Alert.STATUS_UNREAD),
            Alert(rule_id="R2", keyword="k2", article_id="A2", headline="H2", status=Alert.STATUS_UNREAD)
        ]
        count = self.service.mark_all_alerts_read()
        self.assertEqual(count, 2)
        self.assertEqual(len(self.service.get_alerts(unread_only=True)), 0)


if __name__ == "__main__":
    unittest.main()
