"""
Source Analytics Service
Calculates source publication volume, category distributions, and tone profiles.
Responsibility: Jyothi Bandalapati (Jb1080) - US09, US21, US33

DISCLAIMER:
Article volume metrics quantify publication activity and RSS collection ingestion.
They DO NOT measure journalistic credibility, factual reliability, or reporting quality.
"""

from collections import Counter, defaultdict
from typing import List, Dict, Any


class SourceAnalyticsService:
    """
    Computes activity statistics, category breakdowns, and sentiment distributions
    segmented across news sources.
    """

    @staticmethod
    def get_source_counts(articles: List[Any]) -> Dict[str, int]:
        """Returns map of source_name to article count."""
        counter = Counter([getattr(a, "source_name", "Unknown") for a in articles])
        return dict(counter.most_common())

    @staticmethod
    def get_source_distribution(articles: List[Any]) -> List[Dict[str, Any]]:
        """
        Calculates percentage share of total articles published by each source.
        """
        total = len(articles)
        if total == 0:
            return []

        counts = SourceAnalyticsService.get_source_counts(articles)
        distribution = []
        for source, count in counts.items():
            percentage = round((count / total) * 100, 2)
            distribution.append({
                "source": source,
                "article_count": count,
                "percentage": percentage
            })
        return distribution

    @staticmethod
    def get_category_distribution_by_source(articles: List[Any]) -> Dict[str, Dict[str, int]]:
        """
        Returns category breakdown for each news source.
        """
        breakdown = defaultdict(lambda: defaultdict(int))
        for a in articles:
            source = getattr(a, "source_name", "Unknown")
            category = getattr(a, "category", "Other")
            breakdown[source][category] += 1

        return {src: dict(cats) for src, cats in breakdown.items()}

    @staticmethod
    def get_sentiment_distribution_by_source(articles: List[Any]) -> Dict[str, Dict[str, Any]]:
        """
        Computes sentiment counts and percentages for each news source.
        """
        data = defaultdict(lambda: {"Positive": 0, "Negative": 0, "Neutral": 0, "Total": 0})
        for a in articles:
            src = getattr(a, "source_name", "Unknown")
            sent = getattr(a, "sentiment", "Neutral")
            if sent not in ["Positive", "Negative", "Neutral"]:
                sent = "Neutral"
            data[src][sent] += 1
            data[src]["Total"] += 1

        result = {}
        for src, counts in data.items():
            tot = counts["Total"]
            result[src] = {
                "positive": counts["Positive"],
                "negative": counts["Negative"],
                "neutral": counts["Neutral"],
                "total": tot,
                "positive_pct": round((counts["Positive"] / tot) * 100, 1) if tot > 0 else 0.0,
                "negative_pct": round((counts["Negative"] / tot) * 100, 1) if tot > 0 else 0.0,
                "neutral_pct": round((counts["Neutral"] / tot) * 100, 1) if tot > 0 else 0.0
            }
        return result

    @staticmethod
    def compare_sources(articles: List[Any], source_names: List[str]) -> Dict[str, Any]:
        """
        Produces side-by-side comparison between specified news sources.
        """
        filtered = [a for a in articles if getattr(a, "source_name", "") in source_names]
        return {
            "counts": SourceAnalyticsService.get_source_counts(filtered),
            "sentiment": SourceAnalyticsService.get_sentiment_distribution_by_source(filtered),
            "categories": SourceAnalyticsService.get_category_distribution_by_source(filtered)
        }
