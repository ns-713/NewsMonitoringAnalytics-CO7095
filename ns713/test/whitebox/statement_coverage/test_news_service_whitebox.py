"""
White-Box Tests for News Service CRUD and Ingestion Operations
Member 1: Nikitha Sarpur (ns713 - 259060190)
Techniques: Statement and Branch Coverage for NewsService & RSS Collection
"""

import unittest
import tempfile
from pathlib import Path
from models.article import NewsArticle
from models.news_source import NewsSource
from services.news_service import NewsService
from services.rss_service import RssService


class TestNewsServiceWhitebox(unittest.TestCase):
    """Exercises all article and source lifecycle operations in NewsService."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.articles_file = base / "articles.json"
        self.sources_file = base / "sources.json"
        self.service = NewsService(
            articles_file=self.articles_file,
            sources_file=self.sources_file
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_wb_ns_01_article_lifecycle_update_and_delete(self):
        """TC-WB-NS-01: Exercises add_article, update_article, and delete_article."""
        # Add article
        ok, msg, art = self.service.add_article(
            headline="Initial Headline for Update",
            source_name="TechDaily",
            article_url="https://tech.org/art1",
            content="Initial technology article content."
        )
        self.assertTrue(ok)
        self.assertIsNotNone(art)
        art_id = art.article_id

        # Update article headline and content (triggers sentiment re-analysis)
        up_ok, up_msg = self.service.update_article(
            art_id,
            {"headline": "Surging Growth in Semiconductor Markets", "content": "Updated positive content."}
        )
        self.assertTrue(up_ok)
        updated_art = self.service.get_article_by_id(art_id)
        self.assertEqual(updated_art.headline, "Surging Growth in Semiconductor Markets")

        # Update non-existent article
        up_fail_ok, _ = self.service.update_article("NONEXISTENT-ID", {"headline": "X"})
        self.assertFalse(up_fail_ok)

        # Invalid update (headline too short)
        inv_ok, inv_msg = self.service.update_article(art_id, {"headline": "A"})
        self.assertFalse(inv_ok)
        self.assertIn("Invalid updates", inv_msg)

        # Delete article
        del_ok, del_msg = self.service.delete_article(art_id)
        self.assertTrue(del_ok)
        self.assertIsNone(self.service.get_article_by_id(art_id))

        # Delete non-existent article
        del_fail_ok, _ = self.service.delete_article("NONEXISTENT-ID")
        self.assertFalse(del_fail_ok)

    def test_tc_wb_ns_02_source_registration_and_removal(self):
        """TC-WB-NS-02: Exercises add_source, get_sources, get_source_by_id, and remove_source."""
        # Add valid source
        ok, msg, src = self.service.add_source(
            name="Reuters Wire",
            feed_url="https://reuters.com/rss",
            category="Business"
        )
        self.assertTrue(ok)
        self.assertIsNotNone(src)
        src_id = src.source_id

        # Retrieve source
        all_sources = self.service.get_sources()
        self.assertEqual(len(all_sources), 1)
        found_src = self.service.get_source_by_id(src_id)
        self.assertIsNotNone(found_src)
        self.assertEqual(found_src.name, "Reuters Wire")

        # Duplicate source registration rejection (same name or URL)
        dup_ok, dup_msg, _ = self.service.add_source(
            name="reuters wire",
            feed_url="https://other.com/feed"
        )
        self.assertFalse(dup_ok)
        self.assertIn("already registered", dup_msg)

        # Invalid source registration (empty name)
        inv_ok, _, _ = self.service.add_source(name="", feed_url="https://valid.com")
        self.assertFalse(inv_ok)

        # Remove source
        rem_ok, _ = self.service.remove_source(src_id)
        self.assertTrue(rem_ok)
        self.assertIsNone(self.service.get_source_by_id(src_id))

        # Remove non-existent source
        rem_fail_ok, _ = self.service.remove_source("NONEXISTENT-SRC")
        self.assertFalse(rem_fail_ok)

    def test_tc_wb_ns_03_import_articles_batch_and_demo_data(self):
        """TC-WB-NS-03: Exercises import_articles_batch with mixed valid, duplicate, and invalid entries."""
        art1 = NewsArticle(
            headline="Alpha Quantum Breakthrough Announced",
            source_name="Wire",
            article_url="https://w.org/alpha",
            content="Superconducting qubits achieve quantum advantage in latest lab tests."
        )
        art2 = NewsArticle(
            headline="Beta Perovskite Solar Cells Advance",
            source_name="Wire",
            article_url="https://w.org/beta",
            content="Photovoltaic efficiency breaks worldwide laboratory records today."
        )
        art_dup = NewsArticle(
            headline="Alpha Quantum Breakthrough Announced",
            source_name="Wire",
            article_url="https://w.org/alpha",
            content="Superconducting qubits achieve quantum advantage in latest lab tests."
        )
        art_inv = NewsArticle(headline="", source_name="Wire", article_url="https://w.org/inv")

        articles = [art1, art2, art_dup, art_inv]
        stats = self.service.import_articles_batch(articles, source_name="Wire")
        self.assertEqual(stats["added"], 2)
        self.assertEqual(stats["duplicates_skipped"], 1)
        self.assertEqual(stats["invalid_skipped"], 1)
        self.assertEqual(stats["total_processed"], 4)

        # Test load_demo_data
        load_ok, load_msg, count = self.service.load_demo_data()
        self.assertTrue(load_ok)
        self.assertGreater(count, 0)

    def test_tc_wb_ns_04_rss_collect_from_feed(self):
        """TC-WB-NS-04: Exercises RssService.collect_from_feed with mock local XML."""
        rss_service = RssService()
        source = NewsSource(
            name="Local Test Feed",
            feed_url="file:///nonexistent/feed.xml"
        )
        ok, arts, err = rss_service.collect_from_feed(source)
        self.assertFalse(ok)
        self.assertIn("Failed to read local file feed", err)

    def test_tc_wb_ns_05_direct_persistence_and_date_helpers(self):
        """TC-WB-NS-05: Direct coverage of save_articles, save_sources, and _is_valid_date."""
        self.assertTrue(NewsArticle._is_valid_date("2026-11-25"))
        self.assertFalse(NewsArticle._is_valid_date("not-a-date"))
        self.assertFalse(NewsArticle._is_valid_date(None))
        self.assertTrue(self.service.save_articles())
        self.assertTrue(self.service.save_sources())
        all_arts = self.service.get_all_articles()
        self.assertIsInstance(all_arts, list)


if __name__ == "__main__":
    unittest.main()
