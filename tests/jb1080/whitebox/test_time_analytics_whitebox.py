"""
White-Box Tests for Time-Based Analytics
Member 3: Jyothi Bandalapati (Jb1080 - 259060742)
Techniques: Statement, Branch, and Exception Handling Coverage
"""

import unittest
from models.article import NewsArticle
from services.time_analytics_service import TimeAnalyticsService


class TestTimeAnalyticsWhitebox(unittest.TestCase):
    """White-box testing covering internal date parsing and grouping branches."""

    def test_tc_wb_tim_01_parse_date_format_branches(self):
        """TC-WB-TIM-01: Branch coverage of parse_date for diverse standard date strings."""
        self.assertIsNone(TimeAnalyticsService.parse_date(""))
        self.assertIsNone(TimeAnalyticsService.parse_date(None))

        # YYYY-MM-DD
        dt1 = TimeAnalyticsService.parse_date("2026-10-15")
        self.assertIsNotNone(dt1)
        self.assertEqual(dt1.day, 15)

        # RFC 822 format
        dt2 = TimeAnalyticsService.parse_date("Mon, 10 Nov 2026 14:00:00 GMT")
        self.assertIsNotNone(dt2)
        self.assertEqual(dt2.month, 11)

        # Non-standard invalid string
        dt3 = TimeAnalyticsService.parse_date("invalid-date-format")
        self.assertIsNone(dt3)

    def test_tc_wb_tim_02_daily_weekly_monthly_grouping(self):
        """TC-WB-TIM-02: Statements in grouping articles by daily, weekly, and monthly buckets."""
        articles = [
            NewsArticle(headline="A1", source_name="S", article_url="http://a1.com", publication_date="2026-10-01"),
            NewsArticle(headline="A2", source_name="S", article_url="http://a2.com", publication_date="2026-10-01"),
            NewsArticle(headline="A3", source_name="S", article_url="http://a3.com", publication_date="2026-10-15"),
            NewsArticle(headline="A4", source_name="S", article_url="http://a4.com", publication_date="invalid_date")
        ]

        daily = TimeAnalyticsService.get_daily_statistics(articles)
        self.assertEqual(daily["2026-10-01"], 2)
        self.assertEqual(daily["2026-10-15"], 1)
        self.assertIn("Unknown Date", daily)

        monthly = TimeAnalyticsService.get_monthly_statistics(articles)
        self.assertEqual(monthly["2026-10"], 3)
        self.assertIn("Unknown Month", monthly)

        weekly = TimeAnalyticsService.get_weekly_statistics(articles)
        self.assertGreater(len(weekly), 0)

    def test_tc_wb_tim_03_sentiment_and_category_trends_over_time(self):
        """TC-WB-TIM-03: Statements in get_sentiment_trends_over_time and get_category_trends_over_time."""
        articles = [
            NewsArticle(headline="A1", source_name="S", article_url="http://a.com", publication_date="2026-10-01", sentiment="Positive", category="Technology"),
            NewsArticle(headline="A2", source_name="S", article_url="http://b.com", publication_date="2026-10-01", sentiment="Negative", category="Technology")
        ]

        sent_trends = TimeAnalyticsService.get_sentiment_trends_over_time(articles, bucket="daily")
        self.assertEqual(sent_trends["2026-10-01"]["Positive"], 1)
        self.assertEqual(sent_trends["2026-10-01"]["Negative"], 1)

        cat_trends = TimeAnalyticsService.get_category_trends_over_time(articles, bucket="monthly")
        self.assertEqual(cat_trends["2026-10"]["Technology"], 2)


if __name__ == "__main__":
    unittest.main()
