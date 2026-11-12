"""
Reporting and CSV Export Service
Generates structured analytical summaries and exports CSV tabular datasets.
Responsibility: Jalakam Prashanth (Pj161) - US24, US35
"""

import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.settings import GENERATED_REPORTS_DIR
from services.source_analytics_service import SourceAnalyticsService
from services.trend_service import TrendService
from services.time_analytics_service import TimeAnalyticsService
from services.duplicate_service import DuplicateService


class ReportService:
    """
    Coordinates aggregation of metrics across domain services and writes CSV report exports.
    """

    def __init__(self, export_dir: Optional[Path] = None):
        self.export_dir = export_dir or GENERATED_REPORTS_DIR
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_articles_csv(self, articles: List[Any], filename: str = "articles_report.csv") -> Path:
        """Exports full article collection to CSV."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.export_dir / filename
        fieldnames = [
            "article_id", "headline", "source_name", "category",
            "sentiment", "sentiment_score", "publication_date", "article_url"
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in articles:
                writer.writerow({
                    "article_id": getattr(a, "article_id", ""),
                    "headline": getattr(a, "headline", ""),
                    "source_name": getattr(a, "source_name", ""),
                    "category": getattr(a, "category", ""),
                    "sentiment": getattr(a, "sentiment", ""),
                    "sentiment_score": getattr(a, "sentiment_score", 0),
                    "publication_date": getattr(a, "publication_date", ""),
                    "article_url": getattr(a, "article_url", "")
                })

        return filepath

    def export_category_distribution_csv(self, category_counts: Dict[str, int], filename: str = "category_distribution.csv") -> Path:
        """Exports category frequency table."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.export_dir / filename
        total = sum(category_counts.values())

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Article Count", "Percentage"])
            for cat, count in category_counts.items():
                pct = round((count / total) * 100, 2) if total > 0 else 0.0
                writer.writerow([cat, count, f"{pct}%"])

        return filepath

    def export_source_analytics_csv(self, source_distribution: List[Dict[str, Any]], filename: str = "source_analytics.csv") -> Path:
        """Exports news source distribution table."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.export_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Source Name", "Article Count", "Share Percentage"])
            for row in source_distribution:
                writer.writerow([row["source"], row["article_count"], f"{row['percentage']}%"])

        return filepath

    def export_trending_topics_csv(self, trends: List[tuple], filename: str = "trending_topics.csv") -> Path:
        """Exports top trending keywords."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.export_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Trending Keyword", "Frequency Count"])
            for idx, (kw, count) in enumerate(trends, 1):
                writer.writerow([idx, kw, count])

        return filepath

    def export_alerts_csv(self, alerts: List[Any], filename: str = "alerts_report.csv") -> Path:
        """Exports generated keyword alerts."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.export_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Alert ID", "Rule ID", "Matched Keyword", "Article ID", "Headline", "Alert Date", "Status"])
            for a in alerts:
                writer.writerow([
                    getattr(a, "alert_id", ""),
                    getattr(a, "rule_id", ""),
                    getattr(a, "keyword", ""),
                    getattr(a, "article_id", ""),
                    getattr(a, "headline", ""),
                    getattr(a, "alert_date", ""),
                    getattr(a, "status", "")
                ])

        return filepath

    def export_duplicates_csv(self, duplicates: List[Dict[str, Any]], filename: str = "duplicates_report.csv") -> Path:
        """Exports duplicate detection findings."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.export_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Article A ID", "Article A Headline", "Source A",
                "Article B ID", "Article B Headline", "Source B",
                "Detection Reason", "Token Similarity"
            ])
            for d in duplicates:
                writer.writerow([
                    d["article_a_id"], d["article_a_headline"], d["article_a_source"],
                    d["article_b_id"], d["article_b_headline"], d["article_b_source"],
                    d["reason"], d["similarity"]
                ])

        return filepath

    def export_time_trends_csv(self, daily_counts: Dict[str, int], filename: str = "time_trends.csv") -> Path:
        """Exports daily publication volume over time."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.export_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date (YYYY-MM-DD)", "Articles Published"])
            for dt, count in daily_counts.items():
                writer.writerow([dt, count])

        return filepath
