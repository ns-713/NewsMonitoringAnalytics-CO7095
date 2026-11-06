"""
Sentiment Analysis Service
Rule-based text sentiment evaluation using lexical dictionaries.
Responsibility: Sashi Dommaraju (Sd683) - US16, US28

LIMITATIONS:
1. Context Ignorance: Words are scored as standalone tokens without grammatical dependency trees.
2. Sarcasm & Irony: Sarcastic remarks containing positive words will be falsely classified as positive.
3. Negation: Simple phrases like "not good" or "never failed" require heuristic or syntactic handling.
4. Domain Ambiguity: Words like 'crush' or 'beat' in Sports may represent victory rather than violence.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from config.settings import (
    POSITIVE_WORDS_FILE,
    NEGATIVE_WORDS_FILE,
    SENTIMENT_POSITIVE,
    SENTIMENT_NEGATIVE,
    SENTIMENT_NEUTRAL
)
from storage.json_storage import JsonStorage


class SentimentService:
    """
    Evaluates text sentiment by matching tokens against positive and negative lexicons.
    """

    def __init__(
        self,
        positive_words_file: Optional[Path] = None,
        negative_words_file: Optional[Path] = None
    ):
        self.pos_file = positive_words_file or POSITIVE_WORDS_FILE
        self.neg_file = negative_words_file or NEGATIVE_WORDS_FILE
        self.positive_words: set[str] = set()
        self.negative_words: set[str] = set()
        self.load_dictionaries()

    def load_dictionaries(self) -> None:
        """Loads positive and negative word sets from persistence."""
        pos_data = JsonStorage.load_data(self.pos_file, default=[])
        neg_data = JsonStorage.load_data(self.neg_file, default=[])

        self.positive_words = {w.strip().lower() for w in pos_data if isinstance(w, str) and w.strip()}
        self.negative_words = {w.strip().lower() for w in neg_data if isinstance(w, str) and w.strip()}

    def tokenize(self, text: str) -> List[str]:
        """
        Splits text into cleaned lower-case alphabetic tokens.
        """
        if not text:
            return []
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = cleaned.split()
        return tokens

    def calculate_score(self, positive_count: int, negative_count: int) -> int:
        """
        Calculates sentiment score: positive_count - negative_count.
        """
        return positive_count - negative_count

    def classify_score(self, score: int) -> str:
        """
        Classifies numeric score into sentiment category.
        Score > 0 -> Positive
        Score < 0 -> Negative
        Score == 0 -> Neutral
        """
        if score > 0:
            return SENTIMENT_POSITIVE
        elif score < 0:
            return SENTIMENT_NEGATIVE
        else:
            return SENTIMENT_NEUTRAL

    def analyse_text(self, text: str) -> Dict[str, Any]:
        """
        Analyses a string for sentiment polarity.
        Returns:
            Dict containing score, label, counts, and matched word lists.
        """
        tokens = self.tokenize(text)
        if not tokens:
            return {
                "score": 0,
                "label": SENTIMENT_NEUTRAL,
                "positive_count": 0,
                "negative_count": 0,
                "positive_words": [],
                "negative_words": []
            }

        matched_pos = []
        matched_neg = []

        for token in tokens:
            if token in self.positive_words:
                matched_pos.append(token)
            elif token in self.negative_words:
                matched_neg.append(token)

        pos_count = len(matched_pos)
        neg_count = len(matched_neg)
        score = self.calculate_score(pos_count, neg_count)
        label = self.classify_score(score)

        return {
            "score": score,
            "label": label,
            "positive_count": pos_count,
            "negative_count": neg_count,
            "positive_words": matched_pos,
            "negative_words": matched_neg
        }

    def analyse_article(self, article) -> Dict[str, Any]:
        """Analyses an entire NewsArticle instance."""
        combined_text = article.full_text()
        result = self.analyse_text(combined_text)
        article.sentiment = result["label"]
        article.sentiment_score = result["score"]
        return result
