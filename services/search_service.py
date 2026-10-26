"""
Search and Filtering Service
Performs multi-criteria and case-insensitive querying over news articles.
Responsibility: Sashi Dommaraju (Sd683) - US04, US05, US18, US29
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from services.time_analytics_service import TimeAnalyticsService


class SearchService:
    """
    Provides multi-field filtering, substring matching, and combined query filtering.
    """

    @staticmethod
    def search_headline(articles: List[Any], query: str) -> List[Any]:
        """Filters articles containing query substring in headline."""
        if not query or not query.strip():
            return list(articles)
        q = query.strip().lower()
        return [a for a in articles if q in getattr(a, "headline", "").lower()]

    @staticmethod
    def search_content(articles: List[Any], query: str) -> List[Any]:
        """Filters articles containing query substring in content or description."""
        if not query or not query.strip():
            return list(articles)
        q = query.strip().lower()
        return [
            a for a in articles
            if q in getattr(a, "content", "").lower() or q in getattr(a, "description", "").lower()
        ]

    @staticmethod
    def search_keywords(articles: List[Any], keyword: str) -> List[Any]:
        """Filters articles matching a specific keyword."""
        if not keyword or not keyword.strip():
            return list(articles)
        kw = keyword.strip().lower()
        matched = []
        for a in articles:
            article_kws = [k.lower() for k in getattr(a, "keywords", [])]
            if kw in article_kws or kw in getattr(a, "headline", "").lower():
                matched.append(a)
        return matched

    @staticmethod
    def filter_by_source(articles: List[Any], source_name: str) -> List[Any]:
        """Filters articles from a specific source."""
        if not source_name or not source_name.strip():
            return list(articles)
        s = source_name.strip().lower()
        return [a for a in articles if s in getattr(a, "source_name", "").lower()]

    @staticmethod
    def filter_by_category(articles: List[Any], category: str) -> List[Any]:
        """Filters articles matching a given category."""
        if not category or not category.strip():
            return list(articles)
        c = category.strip().lower()
        return [a for a in articles if c == getattr(a, "category", "").lower()]

    @staticmethod
    def filter_by_sentiment(articles: List[Any], sentiment: str) -> List[Any]:
        """Filters articles matching a sentiment class."""
        if not sentiment or not sentiment.strip():
            return list(articles)
        sent = sentiment.strip().lower()
        return [a for a in articles if sent == getattr(a, "sentiment", "").lower()]

    @staticmethod
    def filter_by_date_range(
        articles: List[Any],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """Filters articles published between start_date and end_date (inclusive)."""
        dt_start = TimeAnalyticsService.parse_date(start_date) if start_date else None
        dt_end = TimeAnalyticsService.parse_date(end_date) if end_date else None

        filtered = []
        for a in articles:
            dt_pub = TimeAnalyticsService.parse_date(getattr(a, "publication_date", ""))
            if not dt_pub:
                continue

            if dt_start and dt_pub.date() < dt_start.date():
                continue
            if dt_end and dt_pub.date() > dt_end.date():
                continue

            filtered.append(a)
        return filtered

    @staticmethod
    def combined_filter(
        articles: List[Any],
        query: Optional[str] = None,
        source: Optional[str] = None,
        category: Optional[str] = None,
        sentiment: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Applies a conjunction of filters across the article collection.
        """
        results = list(articles)

        if query and query.strip():
            q = query.strip().lower()
            results = [
                a for a in results
                if q in getattr(a, "headline", "").lower()
                or q in getattr(a, "content", "").lower()
                or q in getattr(a, "description", "").lower()
            ]

        if source and source.strip():
            results = SearchService.filter_by_source(results, source)

        if category and category.strip() and category.strip().lower() != "all":
            results = SearchService.filter_by_category(results, category)

        if sentiment and sentiment.strip() and sentiment.strip().lower() != "all":
            results = SearchService.filter_by_sentiment(results, sentiment)

        if start_date or end_date:
            results = SearchService.filter_by_date_range(results, start_date, end_date)

        return results
