"""
Trending Topics and Keyword Analytics Service
Identifies high-frequency terms, topic momentum, category distributions, and trend shifts.
Responsibility: Jyothi Bandalapati (Jb1080) - US07, US19, US32
"""

import re
from collections import Counter
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional, Set
from config.settings import STOP_WORDS_FILE
from storage.json_storage import JsonStorage


class TrendService:
    """
    Extracts trending terms and statistical topic distributions from article collections.
    """

    def __init__(self, stop_words_file: Optional[Path] = None):
        self.stop_words_file = stop_words_file or STOP_WORDS_FILE
        self.stop_words: Set[str] = set()
        self.load_stop_words()

    def load_stop_words(self) -> None:
        """Loads stop words list."""
        words = JsonStorage.load_data(self.stop_words_file, default=[])
        self.stop_words = {w.strip().lower() for w in words if isinstance(w, str) and w.strip()}

    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extracts meaningful word tokens from text, filtering out stop words and numbers.
        """
        if not text:
            return []
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = cleaned.split()
        return [
            t for t in tokens
            if len(t) >= min_length and not t.isdigit() and t not in self.stop_words
        ]

    def get_keyword_frequencies(
        self,
        articles: List[Any],
        top_n: int = 10,
        use_content: bool = False
    ) -> List[Tuple[str, int]]:
        """
        Calculates frequency of non-stop keywords across the given articles.
        Returns:
            List of (keyword, frequency_count) sorted descending.
        """
        counter = Counter()
        for article in articles:
            text = f"{article.headline} {article.description}"
            if use_content:
                text += f" {article.content}"
            keywords = self.extract_keywords(text)
            counter.update(keywords)

        return counter.most_common(top_n)

    def get_category_frequencies(self, articles: List[Any]) -> Dict[str, int]:
        """
        Counts number of articles per category.
        """
        counter = Counter([getattr(a, "category", "Other") for a in articles])
        return dict(counter.most_common())

    def get_trending_by_date(
        self,
        articles: List[Any],
        target_date: str,
        top_n: int = 10
    ) -> List[Tuple[str, int]]:
        """
        Retrieves top trending keywords for articles published on a specific date.
        """
        matching = [
            a for a in articles
            if getattr(a, "publication_date", "").startswith(target_date)
        ]
        return self.get_keyword_frequencies(matching, top_n=top_n)

    def compare_trends(
        self,
        period1_articles: List[Any],
        period2_articles: List[Any],
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Compares trending keywords between two periods to highlight emerging or fading topics.
        """
        p1_freq = dict(self.get_keyword_frequencies(period1_articles, top_n=50))
        p2_freq = dict(self.get_keyword_frequencies(period2_articles, top_n=50))

        all_keywords = set(p1_freq.keys()).union(set(p2_freq.keys()))
        comparisons = []

        for kw in all_keywords:
            c1 = p1_freq.get(kw, 0)
            c2 = p2_freq.get(kw, 0)
            delta = c2 - c1
            comparisons.append({
                "keyword": kw,
                "period1_count": c1,
                "period2_count": c2,
                "change": delta
            })

        # Sort by absolute change descending
        comparisons.sort(key=lambda x: abs(x["change"]), reverse=True)

        return {
            "period1_total": len(period1_articles),
            "period2_total": len(period2_articles),
            "comparison": comparisons[:top_n]
        }
