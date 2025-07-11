import asyncio
import json
import os
import sqlite3
import threading
from datetime import datetime
from typing import Any, Dict

from .constants import LOG_LEVELS
from .utils.colors import Color
from .utils.time import (
    current_date,
    current_time,
    current_timestamp,
    current_timezone,
)


class Tamga:
    """
    A modern logging utility that supports console, file, and JSON logging with colored output.
    """

    LOG_LEVELS = LOG_LEVELS

    __slots__ = [
        # Output configuration
        "console_output",
        "colored_output",
        "file_output",
        "json_output",
        "mongo_output",
        "sql_output",
        # Display settings
        "show_date",
        "show_time",
        "show_timezone",
        # File paths and configurations
        "file_path",
        "json_path",
        "sql_path",
        "sql_table_name",
        # MongoDB configuration
        "mongo_uri",
        "mongo_database_name",
        "mongo_collection_name",
        # Notification settings
        "notify_services",
        "notify_levels",
        "notify_title",
        "notify_format",
        # Size limits and buffering
        "max_file_size_mb",
        "max_json_size_mb",
        "max_sql_size_mb",
        "enable_backup",
        "buffer_size",
        # Computed values
        "max_level_width",
        # Internal state (private)
        "_mongo_client",
        "_apprise",
        "_notify_executor",
        "_file_buffer",
        "_json_buffer",
        "_buffer_lock",
        "_color_cache",
        "_json_file_handle",
        "_file_path_handle",
    ]

    def __init__(
        self,
        # Output configuration
        console_output: bool = True,
        colored_output: bool = True,
        file_output: bool = False,
        json_output: bool = False,
        mongo_output: bool = False,
        sql_output: bool = False,
        # Display settings
        show_date: bool = True,
        show_time: bool = True,
        show_timezone: bool = False,
        # File paths and configurations
        file_path: str = "tamga.log",
        json_path: str = "tamga.json",
        sql_path: str = "tamga.db",
        sql_table_name: str = "logs",
        # MongoDB configuration
        mongo_uri: str = None,
        mongo_database_name: str = "tamga",
        mongo_collection_name: str = "logs",
        # Notification settings
        notify_services: list = None,
        notify_levels: list = [],
        notify_title: str = "{appname}: {level} - {date}",
        notify_format: str = "text",
        # Size limits and buffering
        max_file_size_mb: int = 10,
        max_json_size_mb: int = 10,
        max_sql_size_mb: int = 50,
        enable_backup: bool = True,
        buffer_size: int = 50,
    ):
        """
        Initialize Tamga with optional features.

        Args:
            console_output: Enable logging to console (default: True)
            colored_output: Enable colored console output (default: True)
            file_output: Enable logging to a file (default: False)
            json_output: Enable logging to a JSON file (default: False)
            mongo_output: Enable logging to MongoDB (default: False)
            sql_output: Enable logging to SQL database (default: False)
            show_date: Show day in console logs (default: True)
            show_time: Show time in console logs (default: True)
            show_timezone: Show timezone in console logs (default: False)
            file_path: Path to the log file (default: "tamga.log")
            json_path: Path to the JSON log file (default: "tamga.json")
            sql_path: Path to the SQL log file (default: "tamga.db")
            sql_table_name: SQL table name for logs (default: "logs")
            mongo_uri: MongoDB connection URI
            mongo_database_name: MongoDB database name (default: "tamga")
            mongo_collection_name: MongoDB collection name (default: "logs")
            notify_services: List of Apprise notification service URLs
            notify_levels: List of log levels to send notifications for (default: includes NOTIFY)
            notify_title: Template for notification titles (default: "{appname}: {level} - {date}")
            notify_format: Notification format type - text/markdown/html (default: "text")
            max_file_size_mb: Maximum size in MB for log file (default: 10)
            max_json_size_mb: Maximum size in MB for JSON file (default: 10)
            max_sql_size_mb: Maximum size in MB for SQL file (default: 50)
            enable_backup: Enable backup when max size is reached (default: True)
            buffer_size: Number of logs to buffer before writing to file (default: 50)
        """
        # Output configuration
        self.console_output = console_output
        self.colored_output = colored_output
        self.file_output = file_output
        self.json_output = json_output
        self.mongo_output = mongo_output
        self.sql_output = sql_output

        # Display settings
        self.show_date = show_date
        self.show_time = show_time
        self.show_timezone = show_timezone

        # File paths and configurations
        self.file_path = file_path
        self.json_path = json_path
        self.sql_path = sql_path
        self.sql_table_name = sql_table_name

        # MongoDB configuration
        self.mongo_uri = mongo_uri
        self.mongo_database_name = mongo_database_name
        self.mongo_collection_name = mongo_collection_name

        # Notification settings
        self.notify_services = notify_services or []
        self.notify_levels = list(set(notify_levels + ["NOTIFY"]))
        self.notify_title = notify_title
        self.notify_format = notify_format

        # Size limits and buffering
        self.max_file_size_mb = max_file_size_mb
        self.max_json_size_mb = max_json_size_mb
        self.max_sql_size_mb = max_sql_size_mb
        self.enable_backup = enable_backup
        self.buffer_size = buffer_size

        # Computed values
        self.max_level_width = max(len(level) for level in self.LOG_LEVELS)

        # Internal state (private)
        self._mongo_client = None
        self._apprise = None
        self._notify_executor = None
        self._file_buffer = []
        self._json_buffer = []
        self._buffer_lock = threading.Lock()
        self._color_cache = {}
        self._json_file_handle = None
        self._file_path_handle = None

        self._init_services()

    def _init_services(self):
        """Initialize external services and create necessary files."""
        if self.mongo_output:
            self._init_mongo()

        if self.file_output:
            self._ensure_file_exists(self.file_path)
            try:
                self._file_path_handle = open(
                    self.file_path, "a", encoding="utf-8", buffering=8192
                )
            except Exception:
                pass

        if self.json_output:
            self._init_json_file()

        if self.sql_output:
            self._init_sql_db()

    def _init_mongo(self):
        """Initialize MongoDB connection."""
        try:
            import motor.motor_asyncio

            client = motor.motor_asyncio.AsyncIOMotorClient(
                self.mongo_uri, tls=True, tlsAllowInvalidCertificates=True
            )
            self._mongo_client = client[self.mongo_database_name][
                self.mongo_collection_name
            ]
            self._log_internal("Connected to MongoDB", "TAMGA", "lime")
        except Exception as e:
            self._log_internal(f"Failed to connect to MongoDB: {e}", "CRITICAL", "red")

    def _init_apprise(self):
        """Lazy initialize Apprise for performance."""
        if self._apprise is None and self.notify_services:
            try:
                import apprise

                self._apprise = apprise.Apprise()

                for service in self.notify_services:
                    self._apprise.add(service)

                from concurrent.futures import ThreadPoolExecutor

                self._notify_executor = ThreadPoolExecutor(
                    max_workers=2, thread_name_prefix="tamga-notify"
                )

                self._log_internal(
                    f"Notification services initialized: {len(self.notify_services)} services",
                    "TAMGA",
                    "lime",
                )
            except ImportError:
                self._log_internal(
                    "Apprise not installed. Install with: pip install tamga[notifications]",
                    "WARNING",
                    "amber",
                )
            except Exception as e:
                self._log_internal(
                    f"Failed to initialize notifications: {e}", "ERROR", "red"
                )

    def _send_notification_async(self, message: str, level: str, title: str = None):
        """Send notification asynchronously without blocking."""
        if not self.notify_services or not self._apprise:
            return

        def send():
            try:
                final_title = title or self.notify_title.format(
                    appname="Tamga",
                    level=level,
                    date=current_date(),
                    time=current_time(),
                )
                formatted_message = self._apply_default_template(message, level)

                self._apprise.notify(
                    body=formatted_message,
                    title=final_title,
                    body_format=self.notify_format,
                )
            except Exception as e:
                self._log_internal(f"Notification failed: {e}", "ERROR", "red")

        if self._notify_executor:
            self._notify_executor.submit(send)
        else:
            threading.Thread(target=send, daemon=True).start()

    def _apply_default_template(self, message: str, level: str) -> str:
        """Apply notification templates using the unified apprise module."""
        try:
            from .utils.apprise import format_notification

            return format_notification(
                message, level, current_date(), current_time(), self.notify_format
            )
        except Exception as e:
            self._log_internal(
                f"Failed to apply notification template: {e}", "ERROR", "red"
            )
            return message

    def _init_json_file(self):
        """Initialize JSON log file."""
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _init_sql_db(self):
        """Initialize SQLite database."""
        self._ensure_file_exists(self.sql_path)
        with sqlite3.connect(self.sql_path) as conn:
            conn.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.sql_table_name}
                (level TEXT, message TEXT, date TEXT, time TEXT,
                timezone TEXT, timestamp REAL)"""
            )

    def _ensure_file_exists(self, filepath: str):
        """Ensure file exists, create if not."""
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
            open(filepath, "w", encoding="utf-8").close()

    def _format_timestamp(self) -> str:
        """Format timestamp string based on settings."""
        parts = []
        if self.show_date:
            parts.append(current_date())
        if self.show_time:
            parts.append(current_time())
        if self.show_timezone:
            parts.append(current_timezone())
        return " | ".join(parts) if parts else ""

    def _log_internal(self, message: str, level: str, color: str):
        """Internal logging for Tamga messages."""
        if self.console_output:
            self._write_to_console(message, level, color)

    def log(self, message: str, level: str, color: str) -> None:
        """
        Main logging method that handles all types of logs.
        """

        log_data = {
            "message": message,
            "level": level,
            "color": color,
            "timestamp": self._format_timestamp(),
            "date": current_date(),
            "time": current_time(),
            "timezone": current_timezone(),
            "unix_timestamp": current_timestamp(),
        }

        if self.console_output:
            self._write_to_console(message, level, color)

        if self.file_output:
            self._buffer_file_write(log_data)

        if self.json_output:
            self._buffer_json_write(log_data)

        if self.sql_output:
            self._write_to_sql(log_data)

        if level in self.notify_levels and self.notify_services:
            if self._apprise is None:
                self._init_apprise()

            self._send_notification_async(message, level)

        if self.mongo_output:
            self._write_to_mongo_async(log_data)

    def _buffer_file_write(self, log_data: Dict[str, Any]):
        """Buffer file writes for better performance."""
        with self._buffer_lock:
            self._file_buffer.append(log_data)
            if len(self._file_buffer) >= self.buffer_size:
                self._flush_file_buffer()

    def _buffer_json_write(self, log_data: Dict[str, Any]):
        """Buffer JSON writes for better performance."""
        with self._buffer_lock:
            self._json_buffer.append(log_data)
            if len(self._json_buffer) >= self.buffer_size:
                self._flush_json_buffer()

    def _flush_file_buffer(self):
        """Flush file buffer to disk."""
        if not self._file_buffer:
            return

        self._handle_file_rotation(self.file_path, self.max_file_size_mb)

        try:
            if self._file_path_handle and not self._file_path_handle.closed:
                for log_data in self._file_buffer:
                    file_timestamp = f"{log_data['date']} | {log_data['time']} | {log_data['timezone']}"
                    self._file_path_handle.write(
                        f"[{file_timestamp}] {log_data['level']}: {log_data['message']}\n"
                    )
                self._file_path_handle.flush()
            else:
                with open(self.file_path, "a", encoding="utf-8") as f:
                    for log_data in self._file_buffer:
                        file_timestamp = f"{log_data['date']} | {log_data['time']} | {log_data['timezone']}"
                        f.write(
                            f"[{file_timestamp}] {log_data['level']}: {log_data['message']}\n"
                        )
            self._file_buffer.clear()
        except Exception as e:
            self._log_internal(f"Failed to write to file: {e}", "ERROR", "red")

    def _flush_json_buffer(self):
        """Flush JSON buffer to disk efficiently."""
        if not self._json_buffer:
            return

        self._handle_file_rotation(self.json_path, self.max_json_size_mb)

        try:
            with open(self.json_path, "r+", encoding="utf-8") as f:
                f.seek(0, 2)
                file_size = f.tell()

                if file_size > 2:
                    f.seek(file_size - 2)
                    f.write(",\n")
                else:
                    f.seek(0)
                    f.write("[\n")

                entries = [
                    json.dumps(
                        {
                            "level": log["level"],
                            "message": log["message"],
                            "date": log["date"],
                            "time": log["time"],
                            "timezone": log["timezone"],
                            "timestamp": log["unix_timestamp"],
                        },
                        ensure_ascii=False,
                        separators=(",", ":"),
                    )
                    for log in self._json_buffer
                ]

                f.write(",\n".join(entries))
                f.write("\n]")

            self._json_buffer.clear()
        except Exception as e:
            self._log_internal(f"Failed to write to JSON: {e}", "ERROR", "red")

    def _get_color_codes(self, color: str) -> tuple:
        """Get cached color codes for performance."""
        if color not in self._color_cache:
            self._color_cache[color] = (Color.text(color), Color.background(color))
        return self._color_cache[color]

    def _write_to_console(self, message: str, level: str, color: str):
        """Write formatted log entry to console."""
        if not self.colored_output:
            timestamp = self._format_timestamp()
            if timestamp:
                print(f"[ {timestamp} ]  {level:<{self.max_level_width}}  {message}")
            else:
                print(f"{level:<{self.max_level_width}}  {message}")
            return

        text_color, bg_color = self._get_color_codes(color)

        output_parts = []

        if self.show_date or self.show_time or self.show_timezone:
            output_parts.append(f"{Color.text('gray')}[{Color.end_code}")

            content_parts = []

            if self.show_date:
                content_parts.append(
                    f"{Color.text('indigo')}{current_date()}{Color.end_code}"
                )

            if self.show_time:
                content_parts.append(
                    f"{Color.text('violet')}{current_time()}{Color.end_code}"
                )

            if self.show_timezone:
                content_parts.append(
                    f"{Color.text('purple')}{current_timezone()}{Color.end_code}"
                )

            if content_parts:
                separator = f"{Color.text('gray')} | {Color.end_code}"
                output_parts.append(separator.join(content_parts))

            output_parts.append(f"{Color.text('gray')}]{Color.end_code}")

        level_str = (
            f"{bg_color}"
            f"{Color.style('bold')}"
            f" {level:<{self.max_level_width}} "
            f"{Color.end_code}"
        )

        output_parts.append(level_str)
        output_parts.append(f"{text_color}{message}{Color.end_code}")

        print(" ".join(output_parts))

    def _write_to_sql(self, log_data: Dict[str, Any]):
        """Write log entry to SQL database."""
        self._handle_file_rotation(self.sql_path, self.max_sql_size_mb)

        try:
            with sqlite3.connect(self.sql_path) as conn:
                conn.execute(
                    f"INSERT INTO {self.sql_table_name} VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        log_data["level"],
                        log_data["message"],
                        log_data["date"],
                        log_data["time"],
                        log_data["timezone"] or "",
                        log_data["unix_timestamp"],
                    ),
                )
        except Exception as e:
            self._log_internal(f"Failed to write to SQL: {e}", "ERROR", "red")

    def _write_to_mongo_async(self, log_data: Dict[str, Any]):
        """Write to MongoDB asynchronously."""
        if self._mongo_client is None:
            return

        async def write():
            try:
                await self._mongo_client.insert_one(
                    {
                        "level": log_data["level"],
                        "message": log_data["message"],
                        "date": log_data["date"],
                        "time": log_data["time"],
                        "timezone": log_data["timezone"],
                        "timestamp": log_data["unix_timestamp"],
                    }
                )
            except Exception as e:
                self._log_internal(f"Failed to write to MongoDB: {e}", "ERROR", "red")

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(write())
            else:
                loop.run_until_complete(write())
        except RuntimeError:
            asyncio.run(write())

    def _check_file_size(self, filepath: str, max_size_mb: int) -> bool:
        """Check if file size exceeds the maximum size limit."""
        try:
            return os.path.getsize(filepath) >= (max_size_mb * 1024 * 1024)
        except OSError:
            return False

    def _create_backup(self, filepath: str):
        """Create a backup of the file with timestamp."""
        if not os.path.exists(filepath):
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{filepath}.{timestamp}.bak"

        try:
            import shutil

            shutil.copy2(filepath, backup_path)
        except Exception as e:
            self._log_internal(f"Failed to create backup: {e}", "ERROR", "red")

    def _handle_file_rotation(self, filepath: str, max_size_mb: int):
        """Handle file rotation when size limit is reached."""
        if not self._check_file_size(filepath, max_size_mb):
            return

        if filepath == self.file_path and self._file_path_handle:
            self._file_path_handle.close()
            self._file_path_handle = None

        if self.enable_backup:
            self._create_backup(filepath)

        try:
            if filepath.endswith(".json"):
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump([], f)
            elif filepath.endswith(".db"):
                with sqlite3.connect(filepath) as conn:
                    conn.execute(f"DELETE FROM {self.sql_table_name}")
            else:
                open(filepath, "w", encoding="utf-8").close()

            if filepath == self.file_path:
                self._file_path_handle = open(
                    self.file_path, "a", encoding="utf-8", buffering=8192
                )
        except Exception as e:
            self._log_internal(f"Failed to rotate file: {e}", "ERROR", "red")

    def flush(self):
        """Flush all buffers to disk."""
        with self._buffer_lock:
            if self._file_buffer:
                self._flush_file_buffer()
            if self._json_buffer:
                self._flush_json_buffer()

    def __del__(self):
        """Cleanup when logger is destroyed."""
        try:
            self.flush()
            if self._notify_executor:
                self._notify_executor.shutdown(wait=False)

            if self._file_path_handle and not self._file_path_handle.closed:
                self._file_path_handle.close()
        except Exception:
            pass

    def info(self, message: str) -> None:
        self.log(message, "INFO", "sky")

    def warning(self, message: str) -> None:
        self.log(message, "WARNING", "amber")

    def error(self, message: str) -> None:
        self.log(message, "ERROR", "rose")

    def success(self, message: str) -> None:
        self.log(message, "SUCCESS", "emerald")

    def debug(self, message: str) -> None:
        self.log(message, "DEBUG", "indigo")

    def critical(self, message: str) -> None:
        self.log(message, "CRITICAL", "red")

    def database(self, message: str) -> None:
        self.log(message, "DATABASE", "green")

    def notify(self, message: str, title: str = None, services: list = None) -> None:
        """
        Send a notification through configured services.

        Args:
            message: Notification message
            title: Optional custom title (overrides template)
            services: Optional list of services (overrides defaults)
        """
        self.log(message, "NOTIFY", "purple")

        if services:
            try:
                import apprise

                temp_apprise = apprise.Apprise()
                for service in services:
                    temp_apprise.add(service)

                final_title = title or self.notify_title.format(
                    appname="Tamga",
                    level="NOTIFY",
                    date=current_date(),
                    time=current_time(),
                )

                temp_apprise.notify(
                    body=message, title=final_title, body_format=self.notify_format
                )
            except Exception as e:
                self._log_internal(f"Custom notification failed: {e}", "ERROR", "red")
        elif self.notify_services:
            self._send_notification_async(message, "NOTIFY", title)

    def metric(self, message: str) -> None:
        self.log(message, "METRIC", "cyan")

    def trace(self, message: str) -> None:
        self.log(message, "TRACE", "gray")

    def custom(self, message: str, level: str, color: str) -> None:
        self.log(message, level, color)

    def dir(self, message: str, **kwargs) -> None:
        """Log message with additional key-value data."""
        if kwargs:
            data_str = json.dumps(
                kwargs, ensure_ascii=False, separators=(",", ":")
            ).replace('"', "'")
            log_message = f"{message} | {data_str}"
        else:
            log_message = message

        self.log(log_message, "DIR", "yellow")
