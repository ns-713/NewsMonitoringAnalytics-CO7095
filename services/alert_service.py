"""
Alert and Keyword Monitoring Service
Manages keyword monitoring rules and generates notifications when articles match.
Responsibility: Jalakam Prashanth (Pj161) - US10, US22, US23, US34
"""

from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from models.alert_rule import AlertRule
from models.alert import Alert
from config.settings import ALERT_RULES_FILE, ALERTS_FILE
from storage.json_storage import JsonStorage


class AlertService:
    """
    Evaluates monitoring rules against ingested articles and persists triggered notifications.
    """

    def __init__(
        self,
        rules_file: Optional[Path] = None,
        alerts_file: Optional[Path] = None
    ):
        self.rules_file = rules_file or ALERT_RULES_FILE
        self.alerts_file = alerts_file or ALERTS_FILE
        self.rules: List[AlertRule] = []
        self.alerts: List[Alert] = []
        self.load_all()

    def load_all(self) -> None:
        """Loads rules and alerts from storage."""
        rules_raw = JsonStorage.load_data(self.rules_file, default=[])
        self.rules = [AlertRule.from_dict(r) for r in rules_raw if isinstance(r, dict)]

        alerts_raw = JsonStorage.load_data(self.alerts_file, default=[])
        self.alerts = [Alert.from_dict(a) for a in alerts_raw if isinstance(a, dict)]

    def save_rules(self) -> bool:
        """Saves monitoring rules to disk."""
        data = [r.to_dict() for r in self.rules]
        return JsonStorage.save_data(self.rules_file, data)

    def save_alerts(self) -> bool:
        """Saves generated alerts to disk."""
        data = [a.to_dict() for a in self.alerts]
        return JsonStorage.save_data(self.alerts_file, data)

    def add_rule(
        self,
        keyword: str,
        description: str = "",
        category_filter: Optional[str] = None
    ) -> Tuple[bool, str, Optional[AlertRule]]:
        """
        Creates and persists a new monitoring rule.
        """
        rule = AlertRule(
            keyword=keyword,
            description=description,
            category_filter=category_filter
        )
        is_valid, errors = rule.validate()
        if not is_valid:
            return False, "; ".join(errors), None

        # Check for duplicate keyword + category rule
        for existing in self.rules:
            if existing.keyword.lower() == rule.keyword.lower() and existing.category_filter == rule.category_filter:
                return False, f"Rule for keyword '{rule.keyword}' already exists.", None

        self.rules.append(rule)
        self.save_rules()
        return True, "Alert rule created successfully.", rule

    def get_rules(self, enabled_only: bool = False) -> List[AlertRule]:
        """Returns registered monitoring rules."""
        if enabled_only:
            return [r for r in self.rules if r.enabled]
        return list(self.rules)

    def get_rule_by_id(self, rule_id: str) -> Optional[AlertRule]:
        """Finds rule by rule_id."""
        for r in self.rules:
            if r.rule_id == rule_id:
                return r
        return None

    def toggle_rule(self, rule_id: str) -> Tuple[bool, str]:
        """Enables or disables a rule."""
        rule = self.get_rule_by_id(rule_id)
        if not rule:
            return False, "Rule not found."
        rule.enabled = not rule.enabled
        self.save_rules()
        status_str = "enabled" if rule.enabled else "disabled"
        return True, f"Rule '{rule.keyword}' is now {status_str}."

    def delete_rule(self, rule_id: str) -> Tuple[bool, str]:
        """Deletes a rule by rule_id."""
        rule = self.get_rule_by_id(rule_id)
        if not rule:
            return False, "Rule not found."
        self.rules.remove(rule)
        self.save_rules()
        return True, f"Rule '{rule_id}' removed."

    def process_article(self, article) -> List[Alert]:
        """
        Evaluates an article against all enabled rules.
        Creates alerts for any matches, avoiding duplicate alerts for same article+rule.
        """
        created_alerts = []
        for rule in self.rules:
            if not rule.enabled:
                continue

            if rule.matches(article.headline, article.content, article.category):
                # Check if alert already exists for this rule and article
                already_alerted = any(
                    a.rule_id == rule.rule_id and a.article_id == article.article_id
                    for a in self.alerts
                )
                if not already_alerted:
                    new_alert = Alert(
                        rule_id=rule.rule_id,
                        keyword=rule.keyword,
                        article_id=article.article_id,
                        headline=article.headline
                    )
                    self.alerts.append(new_alert)
                    created_alerts.append(new_alert)

        if created_alerts:
            self.save_alerts()

        return created_alerts

    def process_articles_batch(self, articles: List[Any]) -> List[Alert]:
        """Processes multiple articles and returns all generated alerts."""
        all_new = []
        for article in articles:
            alerts = self.process_article(article)
            all_new.extend(alerts)
        return all_new

    def get_alerts(self, unread_only: bool = False) -> List[Alert]:
        """Returns alerts, optionally filtered by unread status."""
        active = [a for a in self.alerts if not a.dismissed]
        if unread_only:
            return [a for a in active if a.status == Alert.STATUS_UNREAD]
        return active

    def mark_alert_read(self, alert_id: str) -> bool:
        """Marks an alert as read."""
        for a in self.alerts:
            if a.alert_id == alert_id:
                a.mark_as_read()
                self.save_alerts()
                return True
        return False

    def mark_all_alerts_read(self) -> int:
        """Marks all unread alerts as read."""
        count = 0
        for a in self.alerts:
            if a.status == Alert.STATUS_UNREAD and not a.dismissed:
                a.mark_as_read()
                count += 1
        if count > 0:
            self.save_alerts()
        return count
