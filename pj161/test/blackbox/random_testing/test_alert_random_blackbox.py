"""
Random-Based Black-Box Testing for Keyword Alert Engine
Member: Jalakam Prashanth (Pj161 - 259060676)
Testing Tool: Python unittest + random
Testing Technique: Black-Box (Random-Based)
"""

import unittest
import random
import string
from models.alert_rule import AlertRule
from models.article import NewsArticle


class TestAlertRandomBlackbox(unittest.TestCase):
    """
    Random-Based Black-Box Testing:
    Generates 50 randomized keywords and articles to verify AlertRule.matches()
    always returns a boolean and never crashes.
    """

    def test_tc_bb_alert_random_matching(self):
        """RND-01: Fuzzes keyword matching with random text strings."""
        random.seed(259060676)
        chars = string.ascii_letters + string.digits + " "
        for _ in range(50):
            rand_kw = "".join(random.choices(chars, k=random.randint(1, 15)))
            rule = AlertRule(keyword=rand_kw, description="Random Rule", enabled=True)
            
            article = NewsArticle(
                headline="Random Tech Announcement with " + rand_kw,
                source_name="Tech Outlet",
                article_url="https://tech.org/rand"
            )
            matched = rule.matches(article)
            self.assertIsInstance(matched, bool)


if __name__ == '__main__':
    unittest.main()
