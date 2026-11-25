"""
Duplicate News Detection Service
Identifies identical and near-duplicate articles using URLs, normalized text, fingerprints, and similarity.
Responsibility: Jyothi Bandalapati (Jb1080) - US08, US20, US33
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Set
from config.settings import STOP_WORDS_FILE, SIMILARITY_THRESHOLD
from storage.json_storage import JsonStorage


class DuplicateService:
    """
    Detects duplicate news items using exact URL matching, normalized headlines,
    lexical fingerprinting, and Jaccard token similarity.
    """

    def __init__(self, stop_words_file: Optional[Path] = None, threshold: float = SIMILARITY_THRESHOLD):
        self.stop_words_file = stop_words_file or STOP_WORDS_FILE
        self.threshold = threshold
        self.stop_words: Set[str] = set()
        self.load_stop_words()

    def load_stop_words(self) -> None:
        """Loads stop words from persistence."""
        words = JsonStorage.load_data(self.stop_words_file, default=[])
        self.stop_words = {w.strip().lower() for w in words if isinstance(w, str) and w.strip()}

    @staticmethod
    def normalise_url(url: str) -> str:
        """Normalises URL for comparison (removes protocol, www, trailing slashes, tracking queries)."""
        if not url:
            return ""
        norm = url.strip().lower()
        norm = re.sub(r"^https?://(www\.)?", "", norm)
        norm = norm.split("?")[0].split("#")[0]
        return norm.rstrip("/")

    def normalise_headline(self, headline: str) -> str:
        """
        Strips punctuation, removes stop words, and normalises whitespace.
        """
        if not headline:
            return ""
        cleaned = re.sub(r"[^\w\s]", " ", headline.lower())
        tokens = [t for t in cleaned.split() if t not in self.stop_words and len(t) > 1]
        return " ".join(tokens)

    def headline_fingerprint(self, headline: str) -> str:
        """
        Generates an order-independent fingerprint from unique sorted non-stop tokens.
        """
        norm = self.normalise_headline(headline)
        tokens = sorted(list(set(norm.split())))
        return " ".join(tokens)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculates Jaccard similarity between two text snippets based on token sets.
        Similarity = |A ∩ B| / |A ∪ B|
        """
        norm1 = self.normalise_headline(text1)
        norm2 = self.normalise_headline(text2)

        set1 = set(norm1.split())
        set2 = set(norm2.split())

        if not set1 and not set2:
            return 1.0 if text1.strip() == text2.strip() else 0.0
        if not set1 or not set2:
            return 0.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return float(intersection) / float(union) if union > 0 else 0.0

    def check_duplicate(
        self,
        candidate,
        existing_articles: List[Any]
    ) -> Tuple[bool, str, Optional[Any]]:
        """
        Checks whether a candidate article is a duplicate of any existing article.
        Returns:
            Tuple[bool, str, Optional[NewsArticle]]:
            (is_duplicate, reason_string, matched_existing_article)
        """
        cand_url = self.normalise_url(candidate.article_url)
        cand_headline_norm = self.normalise_headline(candidate.headline)
        cand_fingerprint = self.headline_fingerprint(candidate.headline)

        for existing in existing_articles:
            if existing is candidate:
                continue

            # 0. Identical Article ID Match
            if candidate.article_id and existing.article_id and candidate.article_id == existing.article_id:
                return True, f"Identical article ID matched with '{existing.article_id}'", existing

            # 1. Exact URL Match
            exist_url = self.normalise_url(existing.article_url)
            if cand_url and exist_url and cand_url == exist_url:
                return True, f"Identical article URL matched with '{existing.article_id}'", existing

            # 2. Exact Normalised Headline Match
            exist_headline_norm = self.normalise_headline(existing.headline)
            if cand_headline_norm and exist_headline_norm and cand_headline_norm == exist_headline_norm:
                return True, f"Exact normalised headline matched with '{existing.article_id}'", existing

            # 3. Identical Token Fingerprint
            exist_fingerprint = self.headline_fingerprint(existing.headline)
            if cand_fingerprint and exist_fingerprint and cand_fingerprint == exist_fingerprint:
                return True, f"Headline lexical fingerprint matched with '{existing.article_id}'", existing

            # 4. Token Similarity Threshold
            similarity = self.calculate_similarity(candidate.headline, existing.headline)
            if similarity >= self.threshold:
                pct = int(similarity * 100)
                return True, f"High headline similarity ({pct}%) with '{existing.article_id}'", existing

        return False, "Unique article", None

    def find_all_duplicates(self, articles: List[Any]) -> List[Dict[str, Any]]:
        """
        Scans an entire list of articles and returns detected duplicate pairs and groups.
        """
        duplicates = []
        seen: Set[str] = set()

        for i in range(len(articles)):
            for j in range(i + 1, len(articles)):
                art_a = articles[i]
                art_b = articles[j]

                is_dup, reason, _ = self.check_duplicate(art_b, [art_a])
                if is_dup:
                    pair_key = tuple(sorted([art_a.article_id, art_b.article_id]))
                    if pair_key not in seen:
                        seen.add(pair_key)
                        similarity = self.calculate_similarity(art_a.headline, art_b.headline)
                        duplicates.append({
                            "article_a_id": art_a.article_id,
                            "article_a_headline": art_a.headline,
                            "article_a_source": art_a.source_name,
                            "article_b_id": art_b.article_id,
                            "article_b_headline": art_b.headline,
                            "article_b_source": art_b.source_name,
                            "reason": reason,
                            "similarity": round(similarity, 3)
                        })

        return duplicates
