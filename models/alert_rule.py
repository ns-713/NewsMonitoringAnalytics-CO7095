"""
AlertRule Model
Defines criteria for keyword monitoring and alert triggering.
Responsibility: Jalakam Prashanth (Pj161) - US10
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional


class AlertRule:
    """
    Data model representing a keyword alert monitoring rule.
    """

    def __init__(
        self,
        keyword: str,
        description: str = "",
        category_filter: Optional[str] = None,
        enabled: bool = True,
        rule_id: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        self.rule_id = rule_id or f"RUL-{uuid.uuid4().hex[:8].upper()}"
        self.keyword = (keyword or "").strip().lower()
        self.description = (description or "").strip()
        self.category_filter = (category_filter or "").strip() if category_filter else None
        self.enabled = bool(enabled)
        self.created_at = created_at or datetime.now().isoformat()

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validates the alert rule.
        Returns:
            Tuple[bool, List[str]]: (is_valid, list of error messages)
        """
        errors = []
        if not self.keyword:
            errors.append("Monitoring keyword cannot be empty.")
        elif len(self.keyword) < 2:
            errors.append("Monitoring keyword must be at least 2 characters long.")

        return len(errors) == 0, errors

    def matches(self, headline: str, content: str = "", category: str = "") -> bool:
        """
        Evaluates whether an article matches this rule.
        """
        if not self.enabled:
            return False

        if not self.keyword:
            return False

        # Category filter check if specified
        if self.category_filter and self.category_filter.lower() != (category or "").lower():
            return False

        target_text = f"{headline} {content}".lower()
        return self.keyword in target_text

    def to_dict(self) -> Dict[str, Any]:
        """Converts instance to dictionary."""
        return {
            "rule_id": self.rule_id,
            "keyword": self.keyword,
            "description": self.description,
            "category_filter": self.category_filter,
            "enabled": self.enabled,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlertRule":
        """Instantiates AlertRule from dictionary."""
        return cls(
            rule_id=data.get("rule_id"),
            keyword=data.get("keyword", ""),
            description=data.get("description", ""),
            category_filter=data.get("category_filter"),
            enabled=data.get("enabled", True),
            created_at=data.get("created_at")
        )

    def __repr__(self) -> str:
        return f"<AlertRule id={self.rule_id} keyword='{self.keyword}' enabled={self.enabled}>"
