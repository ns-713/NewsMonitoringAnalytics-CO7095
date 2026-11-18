"""
Concolic Testing Research and Test Harness: CSV Report Export Formatting
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Course: CO7095 - Software Measurement and Quality Assurance

CONCOLIC PROCEDURE:
1. Seed Input: Export standard article without special characters to CSV.
2. Symbolic Constraint Analysis:
       Branch 1: Field contains comma (requires quote escaping)
       Branch 2: Field contains double quotes (requires escaping quotes as "")
       Branch 3: Field contains newline character
       Branch 4: Field is None or empty string
3. Branch Inversion & Input Generation: Synthesize articles containing commas, quotes, and newlines.
4. Concrete Execution & Output Parsing: Re-read the written CSV to confirm structural integrity.
"""

import unittest
import tempfile
import csv
from pathlib import Path
from models.article import NewsArticle
from services.report_service import ReportService


class TestConcolicCsvExport(unittest.TestCase):
    """Concolic testing harness targeting CSV escaping and encoding branches."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.service = ReportService(export_dir=Path(self.temp_dir.name))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_con_csv_execution_and_branch_negation(self):
        """
        Executes concrete seed, injects boundary delimiter mutations, and verifies valid CSV parsing.
        """
        # Step 1: Concrete Seed Input (Simple alphanumeric strings)
        seed_art = NewsArticle(
            headline="Standard Clean Headline",
            source_name="SimpleSource",
            article_url="http://simple.com/1"
        )
        csv1 = self.service.export_articles_csv([seed_art], "seed.csv")
        with open(csv1, "r", encoding="utf-8") as f:
            rows1 = list(csv.reader(f))
            self.assertEqual(len(rows1), 2)  # Header + 1 row

        # Step 2: Negate Condition 1 (Inject Comma - tests RFC 4180 escaping)
        comma_art = NewsArticle(
            headline="Breaking, Market, and Economy Report",
            source_name="Global, Wire",
            article_url="http://wire.com/1"
        )
        csv2 = self.service.export_articles_csv([comma_art], "comma.csv")
        with open(csv2, "r", encoding="utf-8") as f:
            rows2 = list(csv.reader(f))
            # Column count must remain exactly 8 despite commas inside fields
            self.assertEqual(len(rows2[1]), 8)
            self.assertEqual(rows2[1][1], "Breaking, Market, and Economy Report")

        # Step 3: Negate Condition 2 (Inject Double Quotes)
        quote_art = NewsArticle(
            headline='Headline with "Quoted Phrase" Inside',
            source_name='Source "Alpha"',
            article_url="http://quote.com/1"
        )
        csv3 = self.service.export_articles_csv([quote_art], "quote.csv")
        with open(csv3, "r", encoding="utf-8") as f:
            rows3 = list(csv.reader(f))
            self.assertEqual(len(rows3[1]), 8)
            self.assertEqual(rows3[1][1], 'Headline with "Quoted Phrase" Inside')


if __name__ == "__main__":
    unittest.main()
