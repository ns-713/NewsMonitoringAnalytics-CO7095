"""
Services package for News Monitoring and Analytics Application.
"""

from services.news_service import NewsService
from services.rss_service import RssService
from services.search_service import SearchService
from services.categorisation_service import CategorisationService
from services.sentiment_service import SentimentService
from services.duplicate_service import DuplicateService
from services.trend_service import TrendService
from services.source_analytics_service import SourceAnalyticsService
from services.time_analytics_service import TimeAnalyticsService
from services.alert_service import AlertService
from services.report_service import ReportService
from services.dashboard_service import DashboardService

__all__ = [
    "NewsService",
    "RssService",
    "SearchService",
    "CategorisationService",
    "SentimentService",
    "DuplicateService",
    "TrendService",
    "SourceAnalyticsService",
    "TimeAnalyticsService",
    "AlertService",
    "ReportService",
    "DashboardService"
]
