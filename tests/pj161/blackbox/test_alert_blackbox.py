"""
Black-Box Tests for Keyword Monitoring and Alert Management
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Equivalence Partitioning, Boundary Testing, State Transition Testing
"""

import unittest
import tempfile
from pathlib import Path
from models.article import NewsArticle
from models.alert_rule import AlertRule
from services.alert_service import AlertService


class TestAlertBlackbox(unittest.TestCase):
    """Black-box test suite for alert rules, matching triggers, and alert status transitions."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.rules_file = Path(self.temp_dir.name) / "rules.json"
        self.alerts_file = Path(self.temp_dir.name) / "alerts.json"
        self.service = AlertService(rules_file=self.rules_file, alerts_file=self.alerts_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_bb_alt_01_create_valid_rule(self):
        """TC-BB-ALT-01: Create active keyword monitoring rule."""
        ok, msg, rule = self.service.add_rule(
            keyword="climate",
            description="Track climate news",
            category_filter="Environment"
        )
        self.assertTrue(ok)
        self.assertIsNotNone(rule)
        self.assertEqual(rule.keyword, "climate")
        self.assertEqual(rule.category_filter, "Environment")

    def test_tc_bb_alt_02_empty_keyword_boundary(self):
        """TC-BB-ALT-02: Boundary test - Empty keyword rule fails validation."""
        ok, msg, rule = self.service.add_rule(keyword="")
        self.assertFalse(ok)
        self.assertIn("cannot be empty", msg)

    def test_tc_bb_alt_03_short_keyword_boundary(self):
        """TC-BB-ALT-03: Boundary test - 1 character keyword fails min length 2."""
        ok, msg, rule = self.service.add_rule(keyword="a")
        self.assertFalse(ok)
        self.assertIn("at least 2 characters", msg)

    def test_tc_bb_alt_04_trigger_alert_on_matching_article(self):
        """TC-BB-ALT-04: Alert generated when ingested article matches active rule keyword."""
        self.service.add_rule(keyword="cybersecurity", description="Track exploits")
        article = NewsArticle(
            headline="New Cybersecurity Alert on Enterprise Gateways",
            source_name="TechDaily",
            article_url="http://tech.com/1"
        )
        new_alerts = self.service.process_article(article)
        self.assertEqual(len(new_alerts), 1)
        self.assertEqual(new_alerts[0].keyword, "cybersecurity")
        self.assertEqual(new_alerts[0].status, "UNREAD")

    def test_tc_bb_alt_05_category_constraint_prevents_mismatched_alert(self):
        """TC-BB-ALT-05: Decision table - Rule constrained to Environment does not fire on Technology article."""
        self.service.add_rule(
            keyword="energy",
            category_filter="Environment"
        )
        tech_article = NewsArticle(
            headline="Clean Energy In High-Performance Computing",
            source_name="TechNews",
            article_url="http://tech.com/2",
            category="Technology"  # Mismatch with Environment
        )
        alerts = self.service.process_article(tech_article)
        self.assertEqual(len(alerts), 0)

    def test_tc_bb_alt_06_state_transition_unread_to_read(self):
        """TC-BB-ALT-06: State Transition - UNREAD alert is updated to READ."""
        self.service.add_rule(keyword="breakthrough")
        art = NewsArticle(headline="Major Medical Breakthrough", source_name="Med", article_url="http://m.com/1")
        alerts = self.service.process_article(art)
        alert_id = alerts[0].alert_id

        # Verify initial state
        unread = self.service.get_alerts(unread_only=True)
        self.assertEqual(len(unread), 1)

        # Transition state
        ok = self.service.mark_alert_read(alert_id)
        self.assertTrue(ok)

        # Verify post-transition state
        unread_after = self.service.get_alerts(unread_only=True)
        self.assertEqual(len(unread_after), 0)

    def test_tc_bb_alt_07_prevent_duplicate_repeated_alerts(self):
        """TC-BB-ALT-07: Ingesting the same article twice does not spawn duplicate alerts."""
        self.service.add_rule(keyword="quantum")
        art = NewsArticle(headline="Quantum Discovery", source_name="Nature", article_url="http://n.com/1")

        alerts_run_1 = self.service.process_article(art)
        self.assertEqual(len(alerts_run_1), 1)

        alerts_run_2 = self.service.process_article(art)
        self.assertEqual(len(alerts_run_2), 0)  # Suppressed repeated alert


if __name__ == "__main__":
    unittest.main()
