"""
News Management Service
Central business logic service coordinating article creation, updates, source registry, and storage.
Responsibility: Nikitha Sarpur (ns713) - US01, US02, US03, US12, US25
"""

from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

from config.settings import ARTICLES_FILE, SOURCES_FILE, DEMO_DATASET_FILE
from models.article import NewsArticle
from models.news_source import NewsSource
from storage.json_storage import JsonStorage
from services.categorisation_service import CategorisationService
from services.sentiment_service import SentimentService
from services.duplicate_service import DuplicateService
from services.alert_service import AlertService


class NewsService:
    """
    Coordinates CRUD operations on articles and sources, automatically triggering
    enrichment (categorisation, sentiment), duplicate prevention, and alert generation.
    """

    def __init__(
        self,
        articles_file: Optional[Any] = None,
        sources_file: Optional[Any] = None,
        categorisation_service: Optional[CategorisationService] = None,
        sentiment_service: Optional[SentimentService] = None,
        duplicate_service: Optional[DuplicateService] = None,
        alert_service: Optional[AlertService] = None
    ):
        # Handle case where services are passed positionally
        if isinstance(articles_file, CategorisationService):
            categorisation_service = articles_file
            articles_file = None
        if isinstance(sources_file, SentimentService):
            sentiment_service = sources_file
            sources_file = None

        self.articles_file = articles_file or ARTICLES_FILE
        self.sources_file = sources_file or SOURCES_FILE

        self.categorisation_service = categorisation_service or CategorisationService()
        self.sentiment_service = sentiment_service or SentimentService()
        self.duplicate_service = duplicate_service or DuplicateService()
        self.alert_service = alert_service or AlertService()

        self.articles: List[NewsArticle] = []
        self.sources: List[NewsSource] = []
        self.load_all()

    def load_all(self) -> None:
        """Loads articles and sources from disk."""
        raw_articles = JsonStorage.load_data(self.articles_file, default=[])
        self.articles = [NewsArticle.from_dict(d) for d in raw_articles if isinstance(d, dict)]

        raw_sources = JsonStorage.load_data(self.sources_file, default=[])
        self.sources = [NewsSource.from_dict(d) for d in raw_sources if isinstance(d, dict)]

    def save_articles(self) -> bool:
        """Persists articles to storage."""
        data = [a.to_dict() for a in self.articles]
        return JsonStorage.save_data(self.articles_file, data)

    def save_sources(self) -> bool:
        """Persists sources to storage."""
        data = [s.to_dict() for s in self.sources]
        return JsonStorage.save_data(self.sources_file, data)

    # ----------------------------------------------------
    # Article Operations
    # ----------------------------------------------------

    def add_article(
        self,
        headline: str,
        source_name: str,
        article_url: str = "",
        description: str = "",
        content: str = "",
        source_url: str = "",
        publication_date: Optional[str] = None,
        category: Optional[str] = None,
        allow_duplicates: bool = False
    ) -> Tuple[bool, str, Optional[NewsArticle]]:
        """
        Creates, enriches, validates, and stores a new news article.
        """
        # Ensure default URL if omitted
        if not article_url:
            article_url = f"https://local.news/{abs(hash(headline))}"

        candidate = NewsArticle(
            headline=headline,
            source_name=source_name,
            article_url=article_url,
            description=description,
            content=content,
            source_url=source_url,
            publication_date=publication_date
        )

        is_valid, errors = candidate.validate()
        if not is_valid:
            return False, f"Validation failed: {'; '.join(errors)}", None

        # Duplicate detection check
        if not allow_duplicates:
            is_dup, reason, _ = self.duplicate_service.check_duplicate(candidate, self.articles)
            if is_dup:
                return False, f"Duplicate detected: {reason}", None

        # Automatic categorisation if not specified or "Other"
        if not category or category == "Other":
            cat, kws = self.categorisation_service.categorise_article(candidate)
            candidate.category = cat
            candidate.keywords = kws
        else:
            candidate.category = category

        # Automatic sentiment analysis
        self.sentiment_service.analyse_article(candidate)

        # Store article
        self.articles.append(candidate)
        self.save_articles()

        # Update source article count
        self._increment_source_count(candidate.source_name)

        # Process monitoring alerts
        self.alert_service.process_article(candidate)

        return True, "Article added successfully.", candidate

    def get_article_by_id(self, article_id: str) -> Optional[NewsArticle]:
        """Finds article by ID."""
        for a in self.articles:
            if a.article_id == article_id:
                return a
        return None

    def get_all_articles(self) -> List[NewsArticle]:
        """Returns all articles, sorted by publication date descending."""
        return sorted(self.articles, key=lambda a: a.publication_date or "", reverse=True)

    def update_article(self, article_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        """Updates fields of an existing article."""
        article = self.get_article_by_id(article_id)
        if not article:
            return False, "Article not found."

        for key, val in updates.items():
            if hasattr(article, key):
                setattr(article, key, val)

        is_valid, errors = article.validate()
        if not is_valid:
            self.load_all()  # revert from disk
            return False, f"Invalid updates: {'; '.join(errors)}"

        # Re-run sentiment if headline or content changed
        if "headline" in updates or "content" in updates or "description" in updates:
            self.sentiment_service.analyse_article(article)

        self.save_articles()
        return True, "Article updated successfully."

    def delete_article(self, article_id: str) -> Tuple[bool, str]:
        """Deletes an article by ID."""
        article = self.get_article_by_id(article_id)
        if not article:
            return False, "Article not found."

        self.articles.remove(article)
        self.save_articles()
        return True, f"Article '{article_id}' removed."

    def import_articles_batch(
        self,
        new_articles: List[NewsArticle],
        source_name: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Batch imports articles from RSS or file, filtering duplicates and enriching records.
        """
        added_count = 0
        skipped_dup = 0
        invalid_count = 0

        for candidate in new_articles:
            is_valid, _ = candidate.validate()
            if not is_valid:
                invalid_count += 1
                continue

            is_dup, _, _ = self.duplicate_service.check_duplicate(candidate, self.articles)
            if is_dup:
                skipped_dup += 1
                continue

            # Categorise and score sentiment
            cat, kws = self.categorisation_service.categorise_article(candidate)
            candidate.category = cat
            candidate.keywords = kws
            self.sentiment_service.analyse_article(candidate)

            self.articles.append(candidate)
            added_count += 1

        if added_count > 0:
            self.save_articles()
            # Trigger alerts
            self.alert_service.process_articles_batch(self.articles[-added_count:])

        if source_name:
            self._increment_source_count(source_name, added_count)

        return {
            "added": added_count,
            "duplicates_skipped": skipped_dup,
            "invalid_skipped": invalid_count,
            "total_processed": len(new_articles)
        }

    # ----------------------------------------------------
    # Source Operations
    # ----------------------------------------------------

    def add_source(
        self,
        name: str,
        feed_url: str,
        url: str = "",
        category: str = "General"
    ) -> Tuple[bool, str, Optional[NewsSource]]:
        """Registers a new RSS news source."""
        source = NewsSource(name=name, feed_url=feed_url, url=url, category=category)
        is_valid, errors = source.validate()
        if not is_valid:
            return False, "; ".join(errors), None

        for existing in self.sources:
            if existing.name.lower() == source.name.lower() or existing.feed_url.lower() == source.feed_url.lower():
                return False, f"Source '{source.name}' or feed URL already registered.", None

        self.sources.append(source)
        self.save_sources()
        return True, "News source registered.", source

    def get_sources(self) -> List[NewsSource]:
        """Returns all registered news sources."""
        return list(self.sources)

    def get_source_by_id(self, source_id: str) -> Optional[NewsSource]:
        """Finds source by ID."""
        for s in self.sources:
            if s.source_id == source_id:
                return s
        return None

    def remove_source(self, source_id: str) -> Tuple[bool, str]:
        """Removes a source by ID."""
        source = self.get_source_by_id(source_id)
        if not source:
            return False, "Source not found."
        self.sources.remove(source)
        self.save_sources()
        return True, f"Source '{source.name}' removed."

    def _increment_source_count(self, source_name: str, count: int = 1) -> None:
        """Internal helper to update tracked article count on source."""
        for s in self.sources:
            if s.name.lower() == source_name.lower():
                s.article_count += count
                s.last_polled_at = datetime.now().isoformat()
                self.save_sources()
                break

    def load_demo_data(self) -> Tuple[bool, str, int]:
        """
        Loads the offline demonstration dataset into the active repository.
        """
        demo_raw = JsonStorage.load_data(DEMO_DATASET_FILE, default=[])
        if not demo_raw:
            return False, "Demo dataset file is empty or missing.", 0

        demo_articles = [NewsArticle.from_dict(d) for d in demo_raw if isinstance(d, dict)]
        stats = self.import_articles_batch(demo_articles)
        return True, f"Loaded demo data. Added {stats['added']} articles ({stats['duplicates_skipped']} duplicates skipped).", stats['added']
