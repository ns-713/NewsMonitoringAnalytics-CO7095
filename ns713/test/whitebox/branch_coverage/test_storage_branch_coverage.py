"""
White-Box Tests for JSON Storage and Persistence Manager
Member 1: Nikitha Sarpur (ns713 - 259060190)
Techniques: Statement Coverage, Branch Testing, Fault Recovery Paths
"""

import unittest
import tempfile
import os
from pathlib import Path
from storage.json_storage import JsonStorage


class TestStorageWhitebox(unittest.TestCase):
    """White-box testing of atomic file writes, backup generation, and corruption fallback."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test_data.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_wb_sto_01_load_nonexistent_returns_default(self):
        """TC-WB-STO-01: Branch in load_data when path.exists() is False."""
        data = JsonStorage.load_data(self.test_file, default=["default_val"])
        self.assertEqual(data, ["default_val"])

    def test_tc_wb_sto_02_load_empty_file_returns_default(self):
        """TC-WB-STO-02: Branch in load_data when file exists but has zero content."""
        self.test_file.write_text("", encoding="utf-8")
        data = JsonStorage.load_data(self.test_file, default=[])
        self.assertEqual(data, [])

    def test_tc_wb_sto_03_atomic_save_and_load(self):
        """TC-WB-STO-03: Statement coverage of atomic write and subsequent load."""
        payload = [{"id": 1, "title": "Article One"}, {"id": 2, "title": "Article Two"}]
        success = JsonStorage.save_data(self.test_file, payload)
        self.assertTrue(success)
        self.assertTrue(self.test_file.exists())

        loaded = JsonStorage.load_data(self.test_file)
        self.assertEqual(loaded, payload)

    def test_tc_wb_sto_04_backup_creation_and_recovery(self):
        """TC-WB-STO-04: Branch testing backup creation on overwrite and corruption recovery."""
        initial_data = [{"version": 1}]
        JsonStorage.save_data(self.test_file, initial_data)

        # Update data with backup creation
        updated_data = [{"version": 2}]
        JsonStorage.save_data(self.test_file, updated_data, create_backup=True)

        bak_file = self.test_file.with_suffix(self.test_file.suffix + ".bak")
        self.assertTrue(bak_file.exists())

        # Corrupt the primary file intentionally
        self.test_file.write_text("{Corrupted JSON Content", encoding="utf-8")

        # load_data should catch JSONDecodeError and recover from .bak
        recovered = JsonStorage.load_data(self.test_file)
        self.assertEqual(recovered, initial_data)

    def test_tc_wb_sto_05_restore_from_backup_branches(self):
        """TC-WB-STO-05: Tests restore_from_backup when backup exists vs does not exist."""
        # Non-existent backup branch
        res_fail = JsonStorage.restore_from_backup(self.test_file)
        self.assertFalse(res_fail)

        # Existing backup branch
        JsonStorage.save_data(self.test_file, ["original"])
        JsonStorage.create_backup(self.test_file)
        self.test_file.write_text("corrupted", encoding="utf-8")

        res_ok = JsonStorage.restore_from_backup(self.test_file)
        self.assertTrue(res_ok)
        self.assertEqual(JsonStorage.load_data(self.test_file), ["original"])

    def test_tc_wb_sto_06_validate_file_branches(self):
        """TC-WB-STO-06: Tests validate_file with missing, invalid, and valid JSON."""
        # Missing
        self.assertFalse(JsonStorage.validate_file(self.test_file))

        # Invalid
        self.test_file.write_text("invalid json syntax", encoding="utf-8")
        self.assertFalse(JsonStorage.validate_file(self.test_file))

        # Valid
        self.test_file.write_text('{"valid": true}', encoding="utf-8")
        self.assertTrue(JsonStorage.validate_file(self.test_file))


if __name__ == "__main__":
    unittest.main()
