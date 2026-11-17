"""
Time-Based Analytics Service
Calculates daily, weekly, and monthly news volume, category evolution, and sentiment trends over time.
Responsibility: Jyothi Bandalapati (Jb1080) - US31
"""

from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any, Optional


class TimeAnalyticsService:
    """
    Groups and tracks article publication frequencies and distributions across temporal buckets.
    """

    @staticmethod
    def parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """
        Parses various string date representations into a datetime object safely.
        """
        if not date_str:
            return None

        # Clean string
        clean_str = str(date_str).strip()

        # Try RFC 822 / RSS dates first
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(clean_str)
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

        for fmt in formats:
            try:
                # Handle possible timezone suffix variations if needed
                return datetime.strptime(date_str[:19] if "T" in date_str and len(date_str) > 19 else date_str, fmt)
            except (ValueError, TypeError):
                continue

        # Simple YYYY-MM-DD prefix fallback
        if len(date_str) >= 10 and date_str[:4].isdigit() and date_str[4] == '-' and date_str[7] == '-':
            try:
                return datetime.strptime(date_str[:10], "%Y-%m-%d")
            except ValueError:
                pass

        return None

    @staticmethod
    def get_daily_statistics(articles: List[Any]) -> Dict[str, int]:
        """
        Counts number of articles published per day (YYYY-MM-DD).
        """
        daily = defaultdict(int)
        for a in articles:
            dt = TimeAnalyticsService.parse_date(getattr(a, "publication_date", ""))
            key = dt.strftime("%Y-%m-%d") if dt else "Unknown Date"
            daily[key] += 1
        return dict(sorted(daily.items(), key=lambda x: x[0]))

    @staticmethod
    def get_weekly_statistics(articles: List[Any]) -> Dict[str, int]:
        """
        Counts number of articles published per calendar week (YYYY-Www).
        """
        weekly = defaultdict(int)
        for a in articles:
            dt = TimeAnalyticsService.parse_date(getattr(a, "publication_date", ""))
            if dt:
                key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
            else:
                key = "Unknown Week"
            weekly[key] += 1
        return dict(sorted(weekly.items(), key=lambda x: x[0]))

    @staticmethod
    def get_monthly_statistics(articles: List[Any]) -> Dict[str, int]:
        """
        Counts number of articles published per month (YYYY-MM).
        """
        monthly = defaultdict(int)
        for a in articles:
            dt = TimeAnalyticsService.parse_date(getattr(a, "publication_date", ""))
            key = dt.strftime("%Y-%m") if dt else "Unknown Month"
            monthly[key] += 1
        return dict(sorted(monthly.items(), key=lambda x: x[0]))

    @staticmethod
    def get_sentiment_trends_over_time(articles: List[Any], bucket: str = "daily") -> Dict[str, Dict[str, int]]:
        """
        Tracks positive, negative, and neutral sentiment count over time buckets.
        bucket: 'daily' or 'monthly'
        """
        trends = defaultdict(lambda: {"Positive": 0, "Negative": 0, "Neutral": 0})
        for a in articles:
            dt = TimeAnalyticsService.parse_date(getattr(a, "publication_date", ""))
            if not dt:
                key = "Unknown"
            elif bucket == "monthly":
                key = dt.strftime("%Y-%m")
            else:
                key = dt.strftime("%Y-%m-%d")

            sent = getattr(a, "sentiment", "Neutral")
            if sent not in ["Positive", "Negative", "Neutral"]:
                sent = "Neutral"
            trends[key][sent] += 1

        return {k: dict(v) for k, v in sorted(trends.items(), key=lambda x: x[0])}

    @staticmethod
    def get_category_trends_over_time(articles: List[Any], bucket: str = "daily") -> Dict[str, Dict[str, int]]:
        """
        Tracks category distribution over time buckets.
        """
        trends = defaultdict(lambda: defaultdict(int))
        for a in articles:
            dt = TimeAnalyticsService.parse_date(getattr(a, "publication_date", ""))
            if not dt:
                key = "Unknown"
            elif bucket == "monthly":
                key = dt.strftime("%Y-%m")
            else:
                key = dt.strftime("%Y-%m-%d")

            cat = getattr(a, "category", "Other")
            trends[key][cat] += 1

        return {k: dict(v) for k, v in sorted(trends.items(), key=lambda x: x[0])}
