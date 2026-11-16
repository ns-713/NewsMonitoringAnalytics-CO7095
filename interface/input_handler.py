"""
Input Handler Utilities
Provides safe terminal input acquisition, type casting, validation, and back navigation.
Responsibility: Jalakam Prashanth (Pj161) - US36
"""

from typing import Optional, List, Callable


class InputHandler:
    """
    Robust interactive input helpers preventing terminal exceptions and validating user input.
    """

    @staticmethod
    def get_string(prompt: str, default: str = "", allow_empty: bool = True) -> str:
        """Prompts for a string input with optional default value."""
        suffix = f" [{default}]: " if default else ": "
        try:
            val = input(f"{prompt}{suffix}").strip()
            if not val and default:
                return default
            if not allow_empty and not val:
                print("  Input cannot be empty. Please try again.")
                return InputHandler.get_string(prompt, default, allow_empty)
            return val
        except (KeyboardInterrupt, EOFError):
            print("\n  Input cancelled.")
            return default

    @staticmethod
    def get_choice(prompt: str, choices: List[str], default: Optional[str] = None) -> str:
        """Prompts user to select from a list of valid string choices (case-insensitive)."""
        lower_choices = [c.lower() for c in choices]
        while True:
            val = InputHandler.get_string(prompt, default=default or "", allow_empty=bool(default))
            if not val and default:
                return default
            if val.lower() in lower_choices:
                # Return the matching canonical choice string
                idx = lower_choices.index(val.lower())
                return choices[idx]
            print(f"  Invalid selection. Please choose from: {', '.join(choices)}")

    @staticmethod
    def get_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None, default: Optional[int] = None) -> Optional[int]:
        """Prompts user for integer input within optional bounds."""
        default_str = str(default) if default is not None else ""
        while True:
            val_str = InputHandler.get_string(prompt, default=default_str, allow_empty=(default is not None))
            if not val_str and default is not None:
                return default
            try:
                num = int(val_str)
                if min_val is not None and num < min_val:
                    print(f"  Value must be at least {min_val}.")
                    continue
                if max_val is not None and num > max_val:
                    print(f"  Value must be at most {max_val}.")
                    continue
                return num
            except ValueError:
                print("  Please enter a valid whole number.")

    @staticmethod
    def confirm(prompt: str, default_yes: bool = True) -> bool:
        """Prompts for a simple yes/no confirmation."""
        default_label = "Y/n" if default_yes else "y/N"
        try:
            choice = input(f"{prompt} ({default_label}): ").strip().lower()
            if not choice:
                return default_yes
            return choice in ["y", "yes"]
        except (KeyboardInterrupt, EOFError):
            return False
