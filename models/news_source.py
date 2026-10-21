"""
NewsSource Model
Represents a registered news outlet or RSS feed provider.
Responsibility: Nikitha Sarpur (ns713) - US03
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional


class NewsSource:
    """
    Data model representing a news source or RSS feed registry entry.
    """

    def __init__(
        self,
        name: str,
        feed_url: str,
        url: str = "",
        category: str = "General",
        enabled: bool = True,
        source_id: Optional[str] = None,
        created_at: Optional[str] = None,
        last_polled_at: Optional[str] = None,
        article_count: int = 0
    ):
        self.source_id = source_id or f"SRC-{uuid.uuid4().hex[:8].upper()}"
        self.name = (name or "").strip()
        self.feed_url = (feed_url or "").strip()
        self.url = (url or "").strip()
        self.category = category or "General"
        self.enabled = bool(enabled)
        self.created_at = created_at or datetime.now().isoformat()
        self.last_polled_at = last_polled_at
        self.article_count = int(article_count) if article_count is not None else 0

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validates source properties.
        Returns:
            Tuple[bool, List[str]]: (is_valid, list of error messages)
        """
        errors = []
        if not self.name:
            errors.append("Source name cannot be empty.")
        if not self.feed_url:
            errors.append("Feed URL cannot be empty.")
        elif not (self.feed_url.startswith("http://") or self.feed_url.startswith("https://") or self.feed_url.startswith("file://")):
            errors.append("Feed URL must begin with http://, https://, or file://")

        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        """Converts instance to JSON dictionary."""
        return {
            "source_id": self.source_id,
            "name": self.name,
            "feed_url": self.feed_url,
            "url": self.url,
            "category": self.category,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "last_polled_at": self.last_polled_at,
            "article_count": self.article_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NewsSource":
        """Instantiates NewsSource from dictionary data."""
        return cls(
            source_id=data.get("source_id"),
            name=data.get("name", ""),
            feed_url=data.get("feed_url", ""),
            url=data.get("url", ""),
            category=data.get("category", "General"),
            enabled=data.get("enabled", True),
            created_at=data.get("created_at"),
            last_polled_at=data.get("last_polled_at"),
            article_count=data.get("article_count", 0)
        )

    def __repr__(self) -> str:
        return f"<NewsSource id={self.source_id} name='{self.name}' enabled={self.enabled}>"
