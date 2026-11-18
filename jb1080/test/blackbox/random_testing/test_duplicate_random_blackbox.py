"""
Random-Based Black-Box Testing for Duplicate Detection
Member: Jyothi Bandalapati (Jb1080 - 259060742)
Testing Tool: Python unittest + random
Testing Technique: Black-Box (Random-Based)
"""

import unittest
import random
import string
from services.duplicate_service import DuplicateService
from models.article import NewsArticle


class TestDuplicateRandomBlackbox(unittest.TestCase):
    """
    Random-Based Black-Box Testing:
    Generates 50 randomized headlines and token permutations to ensure
    DuplicateService.calculate_similarity() always returns a float in [0.0, 1.0].
    """

    def setUp(self):
        self.service = DuplicateService()

    def test_tc_bb_dup_random_similarity(self):
        """RND-01: Generates random token strings and checks similarity boundedness."""
        random.seed(259060742)
        words = ["apple", "banana", "climate", "market", "technology", "quantum", "energy", "solar", "drone", "cyber"]
        for _ in range(50):
            len_a = random.randint(1, 8)
            len_b = random.randint(1, 8)
            text_a = " ".join(random.choices(words, k=len_a))
            text_b = " ".join(random.choices(words, k=len_b))
            
            sim = self.service.calculate_similarity(text_a, text_b)
            self.assertIsInstance(sim, float)
            self.assertGreaterEqual(sim, 0.0)
            self.assertLessEqual(sim, 1.0)


if __name__ == '__main__':
    unittest.main()
