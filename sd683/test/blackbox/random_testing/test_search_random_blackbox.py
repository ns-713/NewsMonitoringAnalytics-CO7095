"""
Random-Based Black-Box Testing for Search Engine
Member: Sashi Dommaraju (Sd683 - 259062044)
Testing Tool: Python unittest + random
Testing Technique: Black-Box (Random-Based)
"""

import unittest
import random
import string
from services.search_service import SearchService
from models.article import NewsArticle


class TestSearchRandomBlackbox(unittest.TestCase):
    """
    Random-Based Black-Box Testing:
    Generates 50 randomized search queries (special characters, whitespace, long strings)
    to confirm SearchService never raises exceptions and handles all inputs safely.
    """

    def setUp(self):
        self.service = SearchService()
        self.sample_articles = [
            NewsArticle(headline="Global Economy Recovers", source_name="Reuters", article_url="https://r.com/1"),
            NewsArticle(headline="New AI Chip Released", source_name="TechDaily", article_url="https://t.com/1")
        ]

    def test_tc_bb_search_random_queries(self):
        """RND-01: Fuzzes search queries with random characters."""
        random.seed(259062044)
        chars = string.ascii_letters + string.digits + string.punctuation + " \t"
        for _ in range(50):
            q_len = random.randint(0, 50)
            rand_query = "".join(random.choices(chars, k=q_len))
            res = self.service.search_headline(self.sample_articles, rand_query)
            self.assertIsInstance(res, list)
            self.assertTrue(len(res) <= len(self.sample_articles))


if __name__ == '__main__':
    unittest.main()
