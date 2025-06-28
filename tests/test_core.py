"""
Core functionality tests for Tamga logger
"""

import json
import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

from tamga import Tamga


class TestCoreLogging:
    """Test core logging functionality"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def logger(self, temp_dir):
        """Create a logger instance with test configuration"""
        return Tamga(
            logToFile=True,
            logToJSON=True,
            logToSQL=True,
            logFile=os.path.join(temp_dir, "test.log"),
            logJSON=os.path.join(temp_dir, "test.json"),
            logSQL=os.path.join(temp_dir, "test.db"),
            bufferSize=5,
            showTimezone=False,
        )

    def test_console_logging(self, capsys):
        """Test console output"""
        logger = Tamga(logToConsole=True, isColored=False)

        logger.info("Test info message")
        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "Test info message" in captured.out

    def test_all_log_levels(self, logger, capsys):
        """Test all built-in log levels"""
        test_cases = [
            (logger.info, "INFO", "Test info"),
            (logger.warning, "WARNING", "Test warning"),
            (logger.error, "ERROR", "Test error"),
            (logger.success, "SUCCESS", "Test success"),
            (logger.debug, "DEBUG", "Test debug"),
            (logger.critical, "CRITICAL", "Test critical"),
            (logger.database, "DATABASE", "Test database"),
            (logger.mail, "MAIL", "Test mail"),
            (logger.metric, "METRIC", "Test metric"),
            (logger.trace, "TRACE", "Test trace"),
        ]

        for log_method, level, message in test_cases:
            log_method(message)
            captured = capsys.readouterr()
            assert level in captured.out
            assert message in captured.out

    def test_custom_log_level(self, capsys):
        """Test custom log levels"""
        logger = Tamga(isColored=False)
        logger.custom("Custom message", "CUSTOM", "purple")

        captured = capsys.readouterr()
        assert "CUSTOM" in captured.out
        assert "Custom message" in captured.out

    def test_file_logging(self, logger, temp_dir):
        """Test file logging functionality"""
        logger.info("Test file logging")
        logger.error("Test error logging")
        logger.flush()

        log_file = os.path.join(temp_dir, "test.log")
        assert os.path.exists(log_file)

        with open(log_file, "r") as f:
            content = f.read()
            assert "Test file logging" in content
            assert "Test error logging" in content

    def test_json_logging(self, logger, temp_dir):
        """Test JSON logging functionality"""
        logger.info("Test JSON logging")
        logger.flush()

        json_file = os.path.join(temp_dir, "test.json")
        assert os.path.exists(json_file)

        with open(json_file, "r") as f:
            data = json.load(f)
            assert isinstance(data, list)
            assert len(data) > 0
            assert data[0]["message"] == "Test JSON logging"
            assert data[0]["level"] == "INFO"

    def test_sql_logging(self, logger, temp_dir):
        """Test SQLite logging functionality"""
        logger.info("Test SQL logging")
        logger.error("SQL error test")

        sql_file = os.path.join(temp_dir, "test.db")
        assert os.path.exists(sql_file)

        conn = sqlite3.connect(sql_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs")
        rows = cursor.fetchall()
        conn.close()

        assert len(rows) >= 2
        assert any("Test SQL logging" in str(row) for row in rows)

    def test_dir_logging(self, logger, capsys):
        """Test dir() method with structured data"""
        logger.dir(
            "User action",
            user_id="12345",
            action="login",
            ip="192.168.1.1",
            success=True,
        )

        captured = capsys.readouterr()
        assert "User action" in captured.out
        assert "'user_id': '12345'" in captured.out
        assert "'action': 'login'" in captured.out

    def test_buffer_functionality(self, temp_dir):
        """Test buffer mechanism"""
        logger = Tamga(
            logToFile=True,
            logFile=os.path.join(temp_dir, "buffer_test.log"),
            bufferSize=10,
        )

        # Write less than buffer size
        for i in range(5):
            logger.info(f"Message {i}")

        # File should be empty (buffered)
        with open(os.path.join(temp_dir, "buffer_test.log"), "r") as f:
            assert f.read() == ""

        # Force flush
        logger.flush()

        # Now file should have content
        with open(os.path.join(temp_dir, "buffer_test.log"), "r") as f:
            content = f.read()
            for i in range(5):
                assert f"Message {i}" in content

    def test_auto_buffer_flush(self, temp_dir):
        """Test automatic buffer flush when size is reached"""
        logger = Tamga(
            logToFile=True,
            logFile=os.path.join(temp_dir, "auto_flush.log"),
            bufferSize=3,
        )

        # Write exactly buffer size
        for i in range(3):
            logger.info(f"Message {i}")

        # File should have content (auto-flushed)
        with open(os.path.join(temp_dir, "auto_flush.log"), "r") as f:
            content = f.read()
            assert len(content) > 0

    def test_file_rotation(self, temp_dir):
        """Test file rotation when max size is reached"""
        logger = Tamga(
            logToFile=True,
            logFile=os.path.join(temp_dir, "rotate.log"),
            maxLogSize=0.001,  # 1KB for quick rotation
            enableBackup=True,
            bufferSize=1,
        )

        # Generate enough logs to trigger rotation
        for i in range(100):
            logger.info("x" * 100)  # Long message

        # Check for backup files
        backup_files = list(Path(temp_dir).glob("rotate.log.*.bak"))
        assert len(backup_files) > 0

    def test_colored_output(self, capsys):
        """Test colored console output"""
        logger = Tamga(isColored=True)
        logger.info("Colored message")

        captured = capsys.readouterr()
        assert "\033[" in captured.out  # ANSI escape codes

    def test_no_color_output(self, capsys):
        """Test non-colored console output"""
        logger = Tamga(isColored=False)
        logger.info("Plain message")

        captured = capsys.readouterr()
        assert "\033[" not in captured.out  # No ANSI codes

    def test_timezone_display(self, capsys):
        """Test timezone in timestamps"""
        logger = Tamga(showTimezone=True, isColored=False)
        logger.info("With timezone")

        captured = capsys.readouterr()
        # Should contain date | time | timezone pattern
        assert captured.out.count("|") >= 2

    def test_no_timezone_display(self, capsys):
        """Test no timezone in timestamps"""
        logger = Tamga(showTimezone=False, isColored=False)
        logger.info("Without timezone")

        captured = capsys.readouterr()
        # Should contain only date | time pattern
        assert captured.out.count("|") == 1

    def test_multiple_outputs(self, temp_dir):
        """Test logging to multiple outputs simultaneously"""
        logger = Tamga(
            logToConsole=True,
            logToFile=True,
            logToJSON=True,
            logToSQL=True,
            logFile=os.path.join(temp_dir, "multi.log"),
            logJSON=os.path.join(temp_dir, "multi.json"),
            logSQL=os.path.join(temp_dir, "multi.db"),
            bufferSize=1,
        )

        logger.info("Multi-output test")

        # Check all outputs
        assert os.path.exists(os.path.join(temp_dir, "multi.log"))
        assert os.path.exists(os.path.join(temp_dir, "multi.json"))
        assert os.path.exists(os.path.join(temp_dir, "multi.db"))

    def test_thread_safety(self, temp_dir):
        """Test thread-safe logging"""
        import threading

        logger = Tamga(
            logToFile=True,
            logFile=os.path.join(temp_dir, "thread.log"),
            bufferSize=10,
        )

        def log_messages(thread_id):
            for i in range(10):
                logger.info(f"Thread {thread_id} - Message {i}")

        threads = []
        for i in range(5):
            t = threading.Thread(target=log_messages, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logger.flush()

        with open(os.path.join(temp_dir, "thread.log"), "r") as f:
            content = f.read()
            # Check all threads logged
            for i in range(5):
                assert f"Thread {i}" in content
