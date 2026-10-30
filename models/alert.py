"""
Alert Model
Represents a triggered keyword notification event.
Responsibility: Jalakam Prashanth (Pj161) - US22, US23
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional


class Alert:
    """
    Data model representing a generated notification when an article matches a monitored rule.
    """

    STATUS_UNREAD = "UNREAD"
    STATUS_READ = "READ"

    def __init__(
        self,
        rule_id: str,
        keyword: str,
        article_id: str,
        headline: str,
        alert_id: Optional[str] = None,
        alert_date: Optional[str] = None,
        status: str = STATUS_UNREAD,
        dismissed: bool = False
    ):
        self.alert_id = alert_id or f"ALT-{uuid.uuid4().hex[:8].upper()}"
        self.rule_id = rule_id
        self.keyword = keyword
        self.article_id = article_id
        self.headline = headline
        self.alert_date = alert_date or datetime.now().isoformat()
        self.status = status if status in [self.STATUS_UNREAD, self.STATUS_READ] else self.STATUS_UNREAD
        self.dismissed = bool(dismissed)

    def mark_as_read(self) -> None:
        """Marks alert as read."""
        self.status = self.STATUS_READ

    def dismiss(self) -> None:
        """Dismisses the alert."""
        self.dismissed = True

    def to_dict(self) -> Dict[str, Any]:
        """Converts instance to dictionary."""
        return {
            "alert_id": self.alert_id,
            "rule_id": self.rule_id,
            "keyword": self.keyword,
            "article_id": self.article_id,
            "headline": self.headline,
            "alert_date": self.alert_date,
            "status": self.status,
            "dismissed": self.dismissed
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Alert":
        """Instantiates Alert from dictionary."""
        return cls(
            alert_id=data.get("alert_id"),
            rule_id=data.get("rule_id", ""),
            keyword=data.get("keyword", ""),
            article_id=data.get("article_id", ""),
            headline=data.get("headline", ""),
            alert_date=data.get("alert_date"),
            status=data.get("status", cls.STATUS_UNREAD),
            dismissed=data.get("dismissed", False)
        )

    def __repr__(self) -> str:
        return f"<Alert id={self.alert_id} keyword='{self.keyword}' status={self.status}>"
