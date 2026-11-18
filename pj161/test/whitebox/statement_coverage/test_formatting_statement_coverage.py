"""
White-Box Tests for Terminal Formatting Utilities
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Techniques: Statement, Branch, and Loop Testing
"""

import unittest
import io
import sys
from interface.formatting import Formatter


class TestFormattingWhitebox(unittest.TestCase):
    """White-box testing covering presentation methods in Formatter."""

    def test_tc_wb_fmt_01_truncate_branches(self):
        """TC-WB-FMT-01: Branch coverage of Formatter.truncate()."""
        self.assertEqual(Formatter.truncate(""), "")
        self.assertEqual(Formatter.truncate(None), "")
        self.assertEqual(Formatter.truncate("Short", 10), "Short")
        self.assertEqual(Formatter.truncate("This is a very long headline sentence", 15), "This is a ve...")

    def test_tc_wb_fmt_02_banner_and_section(self):
        """TC-WB-FMT-02: Statements in print_banner and print_section."""
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            Formatter.print_banner("Title", "Subtitle")
            Formatter.print_section("Section Header")
            Formatter.print_success("Success msg")
            Formatter.print_info("Info msg")
            Formatter.print_warning("Warning msg")
            Formatter.print_error("Error msg")
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("TITLE", output)
        self.assertIn("Subtitle", output)
        self.assertIn("Section Header", output)
        self.assertIn("[SUCCESS]", output)
        self.assertIn("[INFO]", output)
        self.assertIn("[WARNING]", output)
        self.assertIn("[ERROR]", output)

    def test_tc_wb_fmt_03_print_table_branches(self):
        """TC-WB-FMT-03: Statements and branches in print_table with empty and populated rows."""
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            # Empty rows branch
            Formatter.print_table(["Col1", "Col2"], [])
            # Populated rows branch with max_col_widths
            Formatter.print_table(
                headers=["ID", "Name", "Very Long Description Column"],
                rows=[["1", "Alice", "This is an extraordinarily long text cell that should be truncated"], ["2", "Bob", "Short"]],
                max_col_widths=[5, 10, 20]
            )
        finally:
            sys.stdout = old_stdout

        out = captured.getvalue()
        self.assertIn("(No data records to display)", out)
        self.assertIn("Alice", out)
        self.assertIn("Bob", out)


if __name__ == "__main__":
    unittest.main()
