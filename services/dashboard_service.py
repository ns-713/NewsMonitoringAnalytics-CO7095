"""
Dashboard Service
Aggregates real-time statistical summaries for the interactive CLI dashboard view.
Responsibility: Jalakam Prashanth (Pj161) - US11, US34, US36
"""

from typing import Dict, Any, List
from services.trend_service import TrendService
from services.source_analytics_service import SourceAnalyticsService


class DashboardService:
    """
    Computes system-wide snapshot metrics for instantaneous dashboard rendering.
    """

    def __init__(self, news_service, alert_service, trend_service: TrendService):
        self.news_service = news_service
        self.alert_service = alert_service
        self.trend_service = trend_service

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """
        Gathers high-level telemetry and status indicators.
        """
        articles = self.news_service.get_all_articles()
        sources = self.news_service.get_sources()
        rules = self.alert_service.get_rules()
        alerts = self.alert_service.get_alerts()

        # Sentiment breakdown
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
        for a in articles:
            s = getattr(a, "sentiment", "Neutral")
            if s in sentiment_counts:
                sentiment_counts[s] += 1
            else:
                sentiment_counts["Neutral"] += 1

        # Categories
        cat_freq = self.trend_service.get_category_frequencies(articles)
        top_categories = list(cat_freq.items())[:5]

        # Sources
        src_counts = SourceAnalyticsService.get_source_counts(articles)
        top_sources = list(src_counts.items())[:5]

        # Trending keywords
        trending = self.trend_service.get_keyword_frequencies(articles, top_n=10)

        # Unread alerts
        unread_alerts_count = sum(1 for a in alerts if a.status == "UNREAD")

        return {
            "total_articles": len(articles),
            "total_sources": len(sources),
            "active_rules": len([r for r in rules if r.enabled]),
            "total_alerts": len(alerts),
            "unread_alerts": unread_alerts_count,
            "sentiment": sentiment_counts,
            "top_categories": top_categories,
            "top_sources": top_sources,
            "trending_keywords": trending,
            "latest_articles": articles[:5]
        }
