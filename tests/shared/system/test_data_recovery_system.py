"""
System Tests: Persistence Resilience, Corrupted Data Recovery, and Atomic Storage Guarantees
Shared System Test Suite
"""

import unittest
import tempfile
import json
from pathlib import Path
from storage.json_storage import JsonStorage
from services.news_service import NewsService


class TestDataRecoverySystem(unittest.TestCase):
    """System-level validation of persistence robustness and backup failover."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)
        self.art_file = self.base / "articles.json"
        self.src_file = self.base / "sources.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_sys_02_corrupted_json_recovery_system(self):
        """TC-SYS-02: Confirms service recovers clean backup if active storage is corrupted."""
        # 1. Initialise valid data and backup
        news_svc = NewsService(articles_file=self.art_file, sources_file=self.src_file)
        news_svc.add_article(
            headline="Initial Solid State Headline",
            source_name="Verified Wire",
            article_url="http://wire.com/1"
        )
        self.assertEqual(len(news_svc.articles), 1)

        # 2. Simulate subsequent update which generates backup
        news_svc.add_article(
            headline="Second Solid State Headline",
            source_name="Verified Wire",
            article_url="http://wire.com/2"
        )
        self.assertEqual(len(news_svc.articles), 2)

        # 3. Simulate sudden disk corruption on primary file
        with open(self.art_file, "w", encoding="utf-8") as f:
            f.write("{MALFORMED_UNFINISHED_JSON_STREAM...")

        # 4. Instantiate fresh NewsService (simulating restart)
        # It must safely catch JSONDecodeError and restore from articles.json.bak
        recovered_svc = NewsService(articles_file=self.art_file, sources_file=self.src_file)
        self.assertGreater(len(recovered_svc.articles), 0)
        self.assertEqual(recovered_svc.articles[0].headline, "Initial Solid State Headline")


if __name__ == "__main__":
    unittest.main()
