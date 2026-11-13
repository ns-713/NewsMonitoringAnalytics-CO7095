"""
Random-Based Black-Box Testing (Fuzzing / Generative Input Generation)
Member: Nikitha Sarpur (ns713 - 259060190)
Testing Tool: Python unittest + random
Testing Technique: Black-Box (Random-Based)
"""

import unittest
import random
import string
from models.article import NewsArticle


class TestArticleRandomBlackbox(unittest.TestCase):
    """
    Random-Based Black-Box Testing:
    Generates randomized inputs, special characters, and Unicode to verify NewsArticle.validate()
    never raises unhandled exceptions.
    """

    def test_tc_bb_art_random_headline_fuzzing(self):
        """RND-01: Fuzzes headlines with random length strings and verifies validate() stability."""
        random.seed(259060190)
        chars = string.ascii_letters + string.digits + string.punctuation + " \t"
        for _ in range(50):
            length = random.randint(0, 100)
            rand_hl = "".join(random.choices(chars, k=length))
            article = NewsArticle(
                headline=rand_hl,
                source_name="Random Source",
                article_url="https://example.com/fuzz"
            )
            is_valid, errors = article.validate()
            self.assertIsInstance(is_valid, bool)
            self.assertIsInstance(errors, list)
            stripped_len = len(rand_hl.strip())
            if stripped_len < 3:
                self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
