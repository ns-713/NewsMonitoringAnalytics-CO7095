"""
Categorisation Service
Rule-based news article categorisation using keyword matching dictionaries.
Responsibility: Sashi Dommaraju (Sd683) - US06, US17, US28
Note: Strictly rule-based, deterministic keyword matching; not an AI/ML model.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from config.settings import CATEGORY_KEYWORDS_FILE, CATEGORIES, DEFAULT_CATEGORY
from storage.json_storage import JsonStorage


class CategorisationService:
    """
    Categorises text and news articles into pre-defined categories based on
    keyword dictionary occurrence counts.
    """

    def __init__(self, keywords_file: Optional[Path] = None):
        self.keywords_file = keywords_file or CATEGORY_KEYWORDS_FILE
        self.category_keywords: Dict[str, List[str]] = {}
        self.load_keywords()

    def load_keywords(self) -> None:
        """Loads category keyword dictionaries from storage."""
        data = JsonStorage.load_data(self.keywords_file, default={})
        if isinstance(data, dict) and data:
            self.category_keywords = {
                cat: [kw.lower() for kw in kws if isinstance(kw, str)]
                for cat, kws in data.items()
            }
        else:
            self.category_keywords = {}

    def categorise_text(
        self,
        headline: str = "",
        description: str = "",
        content: str = ""
    ) -> Tuple[str, List[str]]:
        """
        Determines the most matching category for the provided text.
        Returns:
            Tuple[str, List[str]]: (assigned_category, list_of_triggering_keywords)
        """
        combined_text = f"{headline} {description} {content}".lower()
        if not combined_text.strip():
            return DEFAULT_CATEGORY, []

        scores: Dict[str, int] = {}
        matched_kws: Dict[str, List[str]] = {}

        for category, keywords in self.category_keywords.items():
            if category == DEFAULT_CATEGORY:
                continue

            matches = []
            for kw in keywords:
                # Use word boundary search for clean matching
                escaped = re.escape(kw)
                pattern = rf"\b{escaped}\b"
                found_count = len(re.findall(pattern, combined_text))
                if found_count > 0:
                    matches.append(kw)

            if matches:
                scores[category] = len(matches)
                matched_kws[category] = matches

        if not scores:
            return DEFAULT_CATEGORY, []

        # Find category with highest match count
        sorted_categories = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        top_category, _ = sorted_categories[0]

        return top_category, matched_kws.get(top_category, [])

    def categorise_article(self, article) -> Tuple[str, List[str]]:
        """Categorises a NewsArticle object directly."""
        return self.categorise_text(
            headline=article.headline,
            description=article.description,
            content=article.content
        )

    def get_categories(self) -> List[str]:
        """Returns all supported category names."""
        return list(CATEGORIES)

    def get_keywords_for_category(self, category: str) -> List[str]:
        """Returns registered keywords for a specific category."""
        return list(self.category_keywords.get(category, []))

    def update_keywords(self, category: str, keywords: List[str]) -> bool:
        """Updates and persists keywords for a category."""
        if category not in CATEGORIES:
            return False
        cleaned = sorted(list(set(kw.strip().lower() for kw in keywords if kw.strip())))
        self.category_keywords[category] = cleaned
        return JsonStorage.save_data(self.keywords_file, self.category_keywords)
