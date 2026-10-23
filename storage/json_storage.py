"""
JSON Storage Manager
Provides robust, atomic, and safe JSON persistence with backup and recovery support.
Responsibilities: Nikitha Sarpur (ns713 - US12) & Jalakam Prashanth (Pj161 - Data Management)
"""

import json
import os
import shutil
from pathlib import Path
from typing import Any, Optional, Union


class JsonStorage:
    """
    Handles local filesystem JSON persistence with atomic writes, backup generation,
    and corrupted data recovery.
    """

    @staticmethod
    def load_data(filepath: Union[str, Path], default: Any = None) -> Any:
        """
        Safely loads data from a JSON file.
        If file does not exist, returns the default value (or empty list if default is None).
        If file is corrupted, attempts recovery from .bak if present, else returns default.
        """
        path = Path(filepath)
        if default is None:
            default = []

        if not path.exists():
            return default

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return default
                return json.loads(content)
        except (json.JSONDecodeError, OSError) as e:
            # Check for backup file
            bak_path = path.with_suffix(path.suffix + ".bak")
            if bak_path.exists():
                try:
                    with open(bak_path, "r", encoding="utf-8") as bf:
                        bak_content = bf.read().strip()
                        if bak_content:
                            return json.loads(bak_content)
                except Exception:
                    pass
            return default

    @staticmethod
    def save_data(filepath: Union[str, Path], data: Any, create_backup: bool = True) -> bool:
        """
        Atomically saves data to a JSON file.
        Writes first to a temporary file, flushes to disk, and replaces the target file.
        Optionally creates a backup file before writing.
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create backup if file exists and has content
        if create_backup and path.exists() and path.stat().st_size > 0:
            bak_path = path.with_suffix(path.suffix + ".bak")
            try:
                shutil.copy2(path, bak_path)
            except OSError:
                pass

        temp_path = path.with_suffix(f"{path.suffix}.tmp_{os.getpid()}")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            # Atomic replace
            os.replace(temp_path, path)
            return True
        except (OSError, TypeError, ValueError) as err:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass
            return False

    @staticmethod
    def create_backup(filepath: Union[str, Path]) -> Optional[Path]:
        """
        Creates an explicit .bak copy of the target file.
        """
        path = Path(filepath)
        if not path.exists():
            return None

        bak_path = path.with_suffix(path.suffix + ".bak")
        try:
            shutil.copy2(path, bak_path)
            return bak_path
        except OSError:
            return None

    @staticmethod
    def restore_from_backup(filepath: Union[str, Path]) -> bool:
        """
        Restores the file from its corresponding .bak copy if available.
        """
        path = Path(filepath)
        bak_path = path.with_suffix(path.suffix + ".bak")
        if not bak_path.exists():
            return False

        try:
            shutil.copy2(bak_path, path)
            return True
        except OSError:
            return False

    @staticmethod
    def validate_file(filepath: Union[str, Path]) -> bool:
        """
        Checks whether a file exists and contains valid JSON syntax.
        """
        path = Path(filepath)
        if not path.exists():
            return False
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
            return True
        except Exception:
            return False
