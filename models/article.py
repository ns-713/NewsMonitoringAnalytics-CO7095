"""
NewsArticle Model
Represents a structured news article with metadata, content, and analytics results.
Responsibility: Nikitha Sarpur (ns713) - US01, US25
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional


class NewsArticle:
    """
    Data model representing an individual news article.
    """

    def __init__(
        self,
        headline: str,
        source_name: str,
        article_url: str,
        description: str = "",
        content: str = "",
        source_url: str = "",
        publication_date: Optional[str] = None,
        category: str = "Other",
        sentiment: str = "Neutral",
        sentiment_score: int = 0,
        keywords: Optional[List[str]] = None,
        article_id: Optional[str] = None,
        created_timestamp: Optional[str] = None
    ):
        self.article_id = article_id or f"ART-{uuid.uuid4().hex[:8].upper()}"
        self.headline = (headline or "").strip()
        self.description = (description or "").strip()
        self.content = (content or "").strip()
        self.source_name = (source_name or "").strip()
        self.source_url = (source_url or "").strip()
        self.article_url = (article_url or "").strip()
        self.publication_date = publication_date or datetime.now().strftime("%Y-%m-%d")
        self.category = category or "Other"
        self.sentiment = sentiment or "Neutral"
        self.sentiment_score = int(sentiment_score) if sentiment_score is not None else 0
        self.keywords = list(keywords) if keywords else []
        self.created_timestamp = created_timestamp or datetime.now().isoformat()

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validates required fields and basic data constraints.
        Returns:
            Tuple[bool, List[str]]: (is_valid, list of error messages)
        """
        errors = []
        if not self.headline:
            errors.append("Headline cannot be empty.")
        elif len(self.headline) < 3:
            errors.append("Headline must be at least 3 characters long.")

        if not self.source_name:
            errors.append("Source name cannot be empty.")

        if not self.article_url:
            errors.append("Article URL cannot be empty.")

        if self.sentiment not in ["Positive", "Negative", "Neutral"]:
            errors.append(f"Invalid sentiment '{self.sentiment}'. Must be Positive, Negative, or Neutral.")

        if self.publication_date:
            if not self._is_valid_date(self.publication_date):
                errors.append(f"Invalid publication date '{self.publication_date}'. Must be a valid date format.")

        return len(errors) == 0, errors

    @staticmethod
    def _is_valid_date(date_str: str) -> bool:
        """Validates publication date string without external service dependencies (preserves architectural layering)."""
        if not date_str or not isinstance(date_str, str):
            return False
        clean_str = date_str.strip()
        try:
            from email.utils import parsedate_to_datetime
            if parsedate_to_datetime(clean_str) is not None:
                return True
        except Exception:
            pass

        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S GMT",
            "%a, %d %b %Y %H:%M:%S",
            "%d/%m/%Y",
            "%m/%d/%Y"
        ]
        target = clean_str[:19] if "T" in clean_str and len(clean_str) > 19 else clean_str
        for fmt in formats:
            try:
                datetime.strptime(target, fmt)
                return True
            except (ValueError, TypeError):
                continue
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Converts model instance to JSON-serializable dictionary."""
        return {
            "article_id": self.article_id,
            "headline": self.headline,
            "description": self.description,
            "content": self.content,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "article_url": self.article_url,
            "publication_date": self.publication_date,
            "category": self.category,
            "sentiment": self.sentiment,
            "sentiment_score": self.sentiment_score,
            "keywords": self.keywords,
            "created_timestamp": self.created_timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NewsArticle":
        """Instantiates NewsArticle from dictionary data."""
        return cls(
            article_id=data.get("article_id"),
            headline=data.get("headline", ""),
            description=data.get("description", ""),
            content=data.get("content", ""),
            source_name=data.get("source_name", "Unknown Source"),
            source_url=data.get("source_url", ""),
            article_url=data.get("article_url", ""),
            publication_date=data.get("publication_date"),
            category=data.get("category", "Other"),
            sentiment=data.get("sentiment", "Neutral"),
            sentiment_score=data.get("sentiment_score", 0),
            keywords=data.get("keywords", []),
            created_timestamp=data.get("created_timestamp")
        )

    def full_text(self) -> str:
        """Returns concatenated text for searching and NLP processing."""
        parts = [self.headline, self.description, self.content]
        return " ".join([p for p in parts if p]).strip()

    def __repr__(self) -> str:
        return f"<NewsArticle id={self.article_id} headline='{self.headline[:30]}...' source='{self.source_name}'>"
