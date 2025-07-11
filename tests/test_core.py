import json
import os
import sqlite3
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tamga import Tamga


def test_console_logging():
    """Ensure console logging works without errors."""
    logger = Tamga(log_to_console=True)
    logger.info("Test info message")
    logger.warning("Test warning")
    logger.error("Test error")
    logger.success("Test success")
    logger.debug("Test debug")
    logger.critical("Test critical")


def test_console_logging_no_color():
    """Console logging without colors should not raise."""
    logger = Tamga(log_to_console=True, is_colored=False)
    logger.info("Test without colors")


def test_file_logging(tmp_path: Path):
    log_file = tmp_path / "test.log"
    logger = Tamga(
        log_to_console=False, log_to_file=True, log_file=str(log_file), buffer_size=2
    )

    logger.info("First message")
    assert log_file.exists()
    assert log_file.stat().st_size == 0

    logger.info("Second message")
    logger.flush()

    assert log_file.exists()
    content = log_file.read_text()
    assert "First message" in content
    assert "Second message" in content
    assert "INFO" in content


def test_json_logging(tmp_path: Path):
    json_file = tmp_path / "test.json"
    logger = Tamga(
        log_to_console=False, log_to_json=True, log_json=str(json_file), buffer_size=1
    )

    logger.error("JSON error message")
    logger.flush()

    with json_file.open() as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["level"] == "ERROR"
        assert data[0]["message"] == "JSON error message"
        assert "timestamp" in data[0]


def test_sql_logging(tmp_path: Path):
    sql_file = tmp_path / "test.db"
    logger = Tamga(
        log_to_console=False,
        log_to_sql=True,
        log_sql=str(sql_file),
        sql_table="test_logs",
    )

    logger.warning("SQL warning message")

    conn = sqlite3.connect(sql_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_logs WHERE level='WARNING'")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 1
    assert rows[0][0] == "WARNING"
    assert rows[0][1] == "SQL warning message"


def test_multiple_outputs(tmp_path: Path):
    log_file = tmp_path / "test.log"
    json_file = tmp_path / "test.json"
    logger = Tamga(
        log_to_console=True,
        log_to_file=True,
        log_to_json=True,
        log_file=str(log_file),
        log_json=str(json_file),
        buffer_size=1,
    )

    logger.success("Multi-output message")
    logger.flush()

    assert log_file.exists()
    assert json_file.exists()

    assert "Multi-output message" in log_file.read_text()
    with json_file.open() as f:
        data = json.load(f)
        assert data[0]["message"] == "Multi-output message"


def test_custom_log_level():
    logger = Tamga(log_to_console=True)
    logger.custom("Custom message", "CUSTOM", "purple")


def test_dir_method(tmp_path: Path):
    log_file = tmp_path / "test.log"
    logger = Tamga(
        log_to_console=False, log_to_file=True, log_file=str(log_file), buffer_size=1
    )

    logger.dir("User action", user_id=123, action="login", success=True)
    logger.flush()

    content = log_file.read_text()
    assert "User action" in content
    assert "user_id" in content
    assert "123" in content


def test_file_rotation(tmp_path: Path):
    log_file = tmp_path / "test.log"
    logger = Tamga(
        log_to_console=False,
        log_to_file=True,
        log_file=str(log_file),
        max_log_size=0.001,
        enable_backup=True,
        buffer_size=1,
    )

    for i in range(100):
        logger.info(f"This is a long message to fill up the file quickly: {i}" * 10)
    logger.flush()

    backup_files = [f for f in os.listdir(tmp_path) if f.endswith(".bak")]
    assert len(backup_files) > 0


def test_flush_on_deletion(tmp_path: Path):
    log_file = tmp_path / "test.log"
    logger = Tamga(
        log_to_console=False, log_to_file=True, log_file=str(log_file), buffer_size=10
    )

    logger.info("Message before deletion")
    del logger

    assert "Message before deletion" in log_file.read_text()


def test_timezone_toggle(tmp_path: Path):
    log_file1 = tmp_path / "test.log"
    logger1 = Tamga(
        log_to_console=False,
        log_to_file=True,
        log_file=str(log_file1),
        show_timezone=False,
        buffer_size=1,
    )
    logger1.info("No timezone")
    logger1.flush()

    log_file2 = tmp_path / "test2.log"
    logger2 = Tamga(
        log_to_console=False,
        log_to_file=True,
        log_file=str(log_file2),
        show_timezone=True,
        buffer_size=1,
    )
    logger2.info("With timezone")
    logger2.flush()

    content1 = log_file1.read_text()
    content2 = log_file2.read_text()
    assert len(content1) < len(content2)


def test_all_log_levels(tmp_path: Path):
    log_file = tmp_path / "test.log"
    logger = Tamga(
        log_to_console=False, log_to_file=True, log_file=str(log_file), buffer_size=1
    )

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

    content = log_file.read_text()
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
        assert level in content
