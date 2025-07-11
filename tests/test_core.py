import json
import os
import sqlite3
import sys
import tempfile
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tamga import Tamga


class TestTamgaCore(unittest.TestCase):
    """Test core Tamga functionality without external dependencies."""

    def setUp(self):
        """Set up test environment with temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.json_file = os.path.join(self.temp_dir, "test.json")
        self.sql_file = os.path.join(self.temp_dir, "test.db")

    def tearDown(self):
        """Clean up temporary files."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_console_logging(self):
        """Test basic console logging functionality."""
        # Just ensure no exceptions are raised
        logger = Tamga(log_to_console=True)
        logger.info("Test info message")
        logger.warning("Test warning")
        logger.error("Test error")
        logger.success("Test success")
        logger.debug("Test debug")
        logger.critical("Test critical")

    def test_console_logging_no_color(self):
        """Test console logging without colors."""
        logger = Tamga(log_to_console=True, is_colored=False)
        logger.info("Test without colors")

    def test_file_logging(self):
        """Test file logging with buffering."""
        logger = Tamga(
            log_to_console=False,
            log_to_file=True,
            log_file=self.log_file,
            buffer_size=2,
        )

        # Write less than buffer size
        logger.info("First message")
        self.assertTrue(os.path.exists(self.log_file))
        self.assertEqual(os.path.getsize(self.log_file), 0)

        # Trigger buffer flush
        logger.info("Second message")
        logger.flush()

        # Check file contents
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            content = f.read()
            self.assertIn("First message", content)
            self.assertIn("Second message", content)
            self.assertIn("INFO", content)

    def test_json_logging(self):
        """Test JSON logging functionality."""
        logger = Tamga(
            log_to_console=False,
            log_to_json=True,
            log_json=self.json_file,
            buffer_size=1,
        )

        logger.error("JSON error message")
        logger.flush()

        # Verify JSON structure
        with open(self.json_file, "r") as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["level"], "ERROR")
            self.assertEqual(data[0]["message"], "JSON error message")
            self.assertIn("timestamp", data[0])

    def test_sql_logging(self):
        """Test SQLite logging functionality."""
        logger = Tamga(
            log_to_console=False,
            log_to_sql=True,
            log_sql=self.sql_file,
            sql_table="test_logs",
        )

        logger.warning("SQL warning message")

        # Verify SQL data
        conn = sqlite3.connect(self.sql_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_logs WHERE level='WARNING'")
        rows = cursor.fetchall()
        conn.close()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "WARNING")  # level
        self.assertEqual(rows[0][1], "SQL warning message")  # message

    def test_multiple_outputs(self):
        """Test logging to multiple outputs simultaneously."""
        logger = Tamga(
            log_to_console=True,
            log_to_file=True,
            log_to_json=True,
            log_file=self.log_file,
            log_json=self.json_file,
            buffer_size=1,
        )

        logger.success("Multi-output message")
        logger.flush()

        # Check both files exist and contain the message
        self.assertTrue(os.path.exists(self.log_file))
        self.assertTrue(os.path.exists(self.json_file))

        with open(self.log_file, "r") as f:
            self.assertIn("Multi-output message", f.read())

        with open(self.json_file, "r") as f:
            data = json.load(f)
            self.assertEqual(data[0]["message"], "Multi-output message")

    def test_custom_log_level(self):
        """Test custom log levels."""
        logger = Tamga(log_to_console=True)
        logger.custom("Custom message", "CUSTOM", "purple")
        # Just ensure no exception is raised

    def test_dir_method(self):
        """Test structured logging with dir method."""
        logger = Tamga(
            log_to_console=False,
            log_to_file=True,
            log_file=self.log_file,
            buffer_size=1,
        )

        logger.dir("User action", user_id=123, action="login", success=True)
        logger.flush()

        with open(self.log_file, "r") as f:
            content = f.read()
            self.assertIn("User action", content)
            self.assertIn("user_id", content)
            self.assertIn("123", content)

    def test_file_rotation(self):
        """Test file rotation when size limit is reached."""
        logger = Tamga(
            log_to_console=False,
            log_to_file=True,
            log_file=self.log_file,
            max_log_size=0.001,  # 1KB
            enable_backup=True,
            buffer_size=1,
        )

        # Write enough data to trigger rotation
        for i in range(100):
            logger.info(f"This is a long message to fill up the file quickly: {i}" * 10)
        logger.flush()

        # Check if backup was created
        backup_files = [f for f in os.listdir(self.temp_dir) if f.endswith(".bak")]
        self.assertGreater(len(backup_files), 0)

    def test_flush_on_deletion(self):
        """Test that buffers are flushed when logger is deleted."""
        logger = Tamga(
            log_to_console=False,
            log_to_file=True,
            log_file=self.log_file,
            buffer_size=10,
        )

        logger.info("Message before deletion")
        del logger  # Should trigger flush

        with open(self.log_file, "r") as f:
            self.assertIn("Message before deletion", f.read())

    def test_timezone_toggle(self):
        """Test timezone display toggle."""
        # Without timezone
        logger1 = Tamga(
            log_to_console=False,
            log_to_file=True,
            log_file=self.log_file,
            show_timezone=False,
            buffer_size=1,
        )
        logger1.info("No timezone")
        logger1.flush()

        # With timezone
        log_file2 = os.path.join(self.temp_dir, "test2.log")
        logger2 = Tamga(
            log_to_console=False,
            log_to_file=True,
            log_file=log_file2,
            show_timezone=True,
            buffer_size=1,
        )
        logger2.info("With timezone")
        logger2.flush()

        # Check content difference
        with open(self.log_file, "r") as f1, open(log_file2, "r") as f2:
            content1 = f1.read()
            content2 = f2.read()
            # The one with timezone should be longer
            self.assertLess(len(content1), len(content2))

    def test_all_log_levels(self):
        """Test all available log level methods."""
        logger = Tamga(
            log_to_console=False,
            log_to_file=True,
            log_file=self.log_file,
            buffer_size=1,
        )

        # Test all methods
        logger.info("Info test")
        logger.warning("Warning test")
        logger.error("Error test")
        logger.success("Success test")
        logger.debug("Debug test")
        logger.critical("Critical test")
        logger.database("Database test")
        logger.metric("Metric test")
        logger.trace("Trace test")
        logger.flush()

        with open(self.log_file, "r") as f:
            content = f.read()
            for level in [
                "INFO",
                "WARNING",
                "ERROR",
                "SUCCESS",
                "DEBUG",
                "CRITICAL",
                "DATABASE",
                "METRIC",
                "TRACE",
            ]:
                self.assertIn(level, content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
