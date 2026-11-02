"""
Terminal Formatting and Presentation Utilities
Renders clean text tables, boxed headers, and aligned summaries without external UI libraries.
Responsibility: Jalakam Prashanth (Pj161) - US11, US36
"""

from typing import List, Dict, Any, Optional


class Formatter:
    """
    Renders cleanly aligned ASCII tables, banners, and structured status reports.
    """

    @staticmethod
    def print_banner(title: str, subtitle: str = "") -> None:
        """Prints a styled box banner."""
        width = 76
        border = "=" * width
        print("\n" + border)
        print(f"  {title.upper()}")
        if subtitle:
            print(f"  {subtitle}")
        print(border)

    @staticmethod
    def print_section(title: str) -> None:
        """Prints a section header."""
        width = 76
        line = "-" * width
        print(f"\n{title}")
        print(line)

    @staticmethod
    def print_success(message: str) -> None:
        """Prints a success message."""
        print(f"[SUCCESS] {message}")

    @staticmethod
    def print_info(message: str) -> None:
        """Prints an informational message."""
        print(f"[INFO] {message}")

    @staticmethod
    def print_warning(message: str) -> None:
        """Prints a warning message."""
        print(f"[WARNING] {message}")

    @staticmethod
    def print_error(message: str) -> None:
        """Prints an error message."""
        print(f"[ERROR] {message}")

    @staticmethod
    def print_table(headers: List[str], rows: List[List[Any]], max_col_widths: Optional[List[int]] = None) -> None:
        """
        Renders a structured ASCII table with aligned columns.
        """
        if not rows:
            print("  (No data records to display)")
            return

        col_count = len(headers)
        # Determine column widths
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for idx in range(min(col_count, len(row))):
                val_len = len(str(row[idx]))
                if val_len > widths[idx]:
                    widths[idx] = val_len

        # Apply maximum column widths if supplied
        if max_col_widths:
            for idx in range(min(col_count, len(max_col_widths))):
                if max_col_widths[idx] and widths[idx] > max_col_widths[idx]:
                    widths[idx] = max_col_widths[idx]

        # Header line
        header_cells = [f"{str(headers[i])[:widths[i]]:<{widths[i]}}" for i in range(col_count)]
        sep_cells = ["-" * widths[i] for i in range(col_count)]

        print("  " + " | ".join(header_cells))
        print("  " + "-+-".join(sep_cells))

        for row in rows:
            row_cells = []
            for i in range(col_count):
                val = str(row[i]) if i < len(row) else ""
                if len(val) > widths[i]:
                    val = val[:widths[i]-3] + "..."
                row_cells.append(f"{val:<{widths[i]}}")
            print("  " + " | ".join(row_cells))

    @staticmethod
    def truncate(text: str, max_length: int = 50) -> str:
        """Truncates string to max_length with ellipsis."""
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."
