"""
White-Box Statement and Branch Tests for InputHandler
Member 4: Jalakam Prashanth (Pj161 - 259060676)
Covers all methods and exception branches in interface/input_handler.py
"""

import unittest
from unittest.mock import patch
from interface.input_handler import InputHandler


class TestInputHandlerWhitebox(unittest.TestCase):
    """Exhaustive tests for InputHandler interactive terminal methods."""

    def test_get_string_nominal(self):
        with patch("builtins.input", return_value="hello world"):
            val = InputHandler.get_string("Prompt")
            self.assertEqual(val, "hello world")

    def test_get_string_default_fallback(self):
        with patch("builtins.input", return_value=""):
            val = InputHandler.get_string("Prompt", default="my_default")
            self.assertEqual(val, "my_default")

    def test_get_string_retry_when_not_allowed_empty(self):
        with patch("builtins.input", side_effect=["", "valid input"]):
            val = InputHandler.get_string("Prompt", allow_empty=False)
            self.assertEqual(val, "valid input")

    def test_get_string_eof_raises(self):
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(EOFError):
                InputHandler.get_string("Prompt")

    def test_get_choice_valid_direct(self):
        with patch("builtins.input", return_value="B"):
            choice = InputHandler.get_choice("Choose", ["A", "B", "C"])
            self.assertEqual(choice, "B")

    def test_get_choice_case_insensitive(self):
        with patch("builtins.input", return_value="a"):
            choice = InputHandler.get_choice("Choose", ["A", "B", "C"])
            self.assertEqual(choice, "A")

    def test_get_choice_default(self):
        with patch("builtins.input", return_value=""):
            choice = InputHandler.get_choice("Choose", ["A", "B"], default="B")
            self.assertEqual(choice, "B")

    def test_get_choice_retry_then_valid(self):
        with patch("builtins.input", side_effect=["INVALID", "C"]):
            choice = InputHandler.get_choice("Choose", ["A", "B", "C"])
            self.assertEqual(choice, "C")

    def test_get_choice_eof_with_default(self):
        with patch("builtins.input", side_effect=EOFError):
            choice = InputHandler.get_choice("Choose", ["A", "B"], default="A")
            self.assertEqual(choice, "A")

    def test_get_choice_eof_without_default_raises(self):
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(EOFError):
                InputHandler.get_choice("Choose", ["A", "B"])

    def test_get_int_nominal(self):
        with patch("builtins.input", return_value="42"):
            num = InputHandler.get_int("Number")
            self.assertEqual(num, 42)

    def test_get_int_default_fallback(self):
        with patch("builtins.input", return_value=""):
            num = InputHandler.get_int("Number", default=10)
            self.assertEqual(num, 10)

    def test_get_int_min_bound_retry(self):
        with patch("builtins.input", side_effect=["2", "7"]):
            num = InputHandler.get_int("Number", min_val=5)
            self.assertEqual(num, 7)

    def test_get_int_max_bound_retry(self):
        with patch("builtins.input", side_effect=["20", "12"]):
            num = InputHandler.get_int("Number", max_val=15)
            self.assertEqual(num, 12)

    def test_get_int_value_error_retry(self):
        with patch("builtins.input", side_effect=["not_a_number", "99"]):
            num = InputHandler.get_int("Number")
            self.assertEqual(num, 99)

    def test_get_int_eof_with_default(self):
        with patch("builtins.input", side_effect=EOFError):
            num = InputHandler.get_int("Number", default=5)
            self.assertEqual(num, 5)

    def test_get_int_eof_without_default_raises(self):
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(EOFError):
                InputHandler.get_int("Number")

    def test_confirm_yes_options(self):
        with patch("builtins.input", return_value="y"):
            self.assertTrue(InputHandler.confirm("Continue?"))
        with patch("builtins.input", return_value="YES"):
            self.assertTrue(InputHandler.confirm("Continue?"))

    def test_confirm_no_options(self):
        with patch("builtins.input", return_value="n"):
            self.assertFalse(InputHandler.confirm("Continue?"))
        with patch("builtins.input", return_value="anything_else"):
            self.assertFalse(InputHandler.confirm("Continue?"))

    def test_confirm_default(self):
        with patch("builtins.input", return_value=""):
            self.assertTrue(InputHandler.confirm("Continue?", default_yes=True))
        with patch("builtins.input", return_value=""):
            self.assertFalse(InputHandler.confirm("Continue?", default_yes=False))

    def test_confirm_eof_cancelled(self):
        with patch("builtins.input", side_effect=EOFError):
            self.assertFalse(InputHandler.confirm("Continue?"))


if __name__ == "__main__":
    unittest.main()
