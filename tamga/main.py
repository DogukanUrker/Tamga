import asyncio
import json
import os
import sqlite3
import threading
from datetime import datetime
from typing import Any, Dict

from .constants import LOG_LEVELS
from .utils.colors import Color
from .utils.mail import Mail
from .utils.time import currentDate, currentTime, currentTimeStamp, currentTimeZone


class Tamga:
    """
    A modern logging utility that supports console, file, and JSON logging with colored output.
    """

    LOG_LEVELS = LOG_LEVELS

    def __init__(
        self,
        isColored: bool = True,
        logToFile: bool = False,
        logToJSON: bool = False,
        logToConsole: bool = True,
        logToMongo: bool = False,
        logToSQL: bool = False,
        logToAPI: bool = False,
        sendMail: bool = False,
        showTimezone: bool = True,
        mongoURI: str = None,
        mongoDatabaseName: str = "tamga",
        mongoCollectionName: str = "logs",
        logFile: str = "tamga.log",
        logJSON: str = "tamga.json",
        logSQL: str = "tamga.db",
        sqlTable: str = "logs",
        smtpServer: str = None,
        smtpPort: int = None,
        smtpMail: str = None,
        smtpPassword: str = None,
        smtpReceivers: list = None,
        mailLevels: list = ["MAIL"],
        apiURL: str = None,
        maxLogSize: int = 10,
        maxJsonSize: int = 10,
        maxSqlSize: int = 50,
        enableBackup: bool = True,
        bufferSize: int = 50,
    ):
        """
        Initialize Tamga with optional features.

        Args:
            logToFile: Enable logging to a file (default: False)
            logToJSON: Enable logging to a JSON file (default: False)
            logToConsole: Enable logging to console (default: True)
            logToMongo: Enable logging to MongoDB (default: False)
            logToSQL: Enable logging to SQL database (default: False)
            logToAPI: Enable logging to an API (default: False)
            sendMail: Enable sending logs via email (default: False)
            mongoURI: MongoDB connection URI
            mongoDatabaseName: MongoDB database name (default: "tamga")
            mongoCollectionName: MongoDB collection name (default: "logs")
            logFile: Path to the log file (default: "tamga.log")
            logJSON: Path to the JSON log file (default: "tamga.json")
            logSQL: Path to the SQL log file (default: "tamga.db")
            sqlTable: SQL table name for logs (default: "logs")
            smtpServer: SMTP server address
            smtpPort: SMTP server port
            smtpMail: SMTP email address
            smtpPassword: SMTP email password
            smtpReceivers: List of email addresses to receive logs
            mailLevels: List of log levels to send via email (default: ["MAIL"])
            apiURL: URL of the API to send logs to
            maxLogSize: Maximum size in MB for log file (default: 10)
            maxJsonSize: Maximum size in MB for JSON file (default: 10)
            maxSqlSize: Maximum size in MB for SQL file (default: 50)
            enableBackup: Enable backup when max size is reached (default: True)
            showTimezone: Show timezone in logs (default: True)
            bufferSize: Number of logs to buffer before writing to file (default: 50)
        """
        self.isColored = isColored
        self.logToFile = logToFile
        self.logToJSON = logToJSON
        self.logToConsole = logToConsole
        self.logToMongo = logToMongo
        self.logToSQL = logToSQL
        self.logToAPI = logToAPI
        self.sendMail = sendMail
        self.showTimezone = showTimezone
        self.mongoURI = mongoURI
        self.mongoDatabaseName = mongoDatabaseName
        self.mongoCollectionName = mongoCollectionName
        self.logFile = logFile
        self.logJSON = logJSON
        self.logSQL = logSQL
        self.sqlTable = sqlTable
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.smtpMail = smtpMail
        self.smtpPassword = smtpPassword
        self.smtpReceivers = smtpReceivers
        self.mailLevels = mailLevels
        self.apiURL = apiURL
        self.maxLogSize = maxLogSize
        self.maxJsonSize = maxJsonSize
        self.maxSqlSize = maxSqlSize
        self.enableBackup = enableBackup
        self.bufferSize = bufferSize

        self.maxLevelWidth = max(len(level) for level in self.LOG_LEVELS)
        self._mongo_client = None
        self._mail_client = None
        self._file_buffer = []
        self._json_buffer = []
        self._buffer_lock = threading.Lock()

        self._init_services()

    def _init_services(self):
        """Initialize external services and create necessary files."""
        if self.logToMongo:
            self._init_mongo()

        if self.sendMail:
            self._init_mail()

        if self.logToFile:
            self._ensure_file_exists(self.logFile)

        if self.logToJSON:
            self._init_json_file()

        if self.logToSQL:
            self._init_sql_db()

    def _init_mongo(self):
        """Initialize MongoDB connection."""
        try:
            import motor.motor_asyncio

            client = motor.motor_asyncio.AsyncIOMotorClient(
                self.mongoURI, tls=True, tlsAllowInvalidCertificates=True
            )
            self._mongo_client = client[self.mongoDatabaseName][
                self.mongoCollectionName
            ]
            self._log_internal("Connected to MongoDB", "TAMGA", "lime")
        except Exception as e:
            self._log_internal(f"Failed to connect to MongoDB: {e}", "CRITICAL", "red")

    def _init_mail(self):
        """Initialize mail client."""
        self._mail_client = Mail(
            serverAddress=self.smtpServer,
            portNumber=self.smtpPort,
            userName=self.smtpMail,
            userPassword=self.smtpPassword,
            senderEmail=self.smtpMail,
            receiverEmails=self.smtpReceivers,
        )

    def _init_json_file(self):
        """Initialize JSON log file."""
        if not os.path.exists(self.logJSON):
            with open(self.logJSON, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _init_sql_db(self):
        """Initialize SQLite database."""
        self._ensure_file_exists(self.logSQL)
        with sqlite3.connect(self.logSQL) as conn:
            conn.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.sqlTable}
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
        parts = [currentDate(), currentTime()]
        if self.showTimezone:
            parts.append(currentTimeZone())
        return " | ".join(parts)

    def _log_internal(self, message: str, level: str, color: str):
        """Internal logging for Tamga messages."""
        if self.logToConsole:
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
            "date": currentDate(),
            "time": currentTime(),
            "timezone": currentTimeZone(),
            "unix_timestamp": currentTimeStamp(),
        }

        if self.logToConsole:
            self._write_to_console(message, level, color)

        if self.logToFile:
            self._buffer_file_write(log_data)

        if self.logToJSON:
            self._buffer_json_write(log_data)

        if self.logToSQL:
            self._write_to_sql(log_data)

        if self.sendMail and level in self.mailLevels:
            self._send_mail_async(message, level)

        if self.logToAPI:
            self._write_to_api_async(log_data)

        if self.logToMongo:
            self._write_to_mongo_async(log_data)

    def _buffer_file_write(self, log_data: Dict[str, Any]):
        """Buffer file writes for better performance."""
        with self._buffer_lock:
            self._file_buffer.append(log_data)
            if len(self._file_buffer) >= self.bufferSize:
                self._flush_file_buffer()

    def _buffer_json_write(self, log_data: Dict[str, Any]):
        """Buffer JSON writes for better performance."""
        with self._buffer_lock:
            self._json_buffer.append(log_data)
            if len(self._json_buffer) >= self.bufferSize:
                self._flush_json_buffer()

    def _flush_file_buffer(self):
        """Flush file buffer to disk."""
        if not self._file_buffer:
            return

        self._handle_file_rotation(self.logFile, self.maxLogSize)

        try:
            with open(self.logFile, "a", encoding="utf-8") as f:
                for log_data in self._file_buffer:
                    f.write(
                        f"[{log_data['timestamp']}] {log_data['level']}: {log_data['message']}\n"
                    )
            self._file_buffer.clear()
        except Exception as e:
            self._log_internal(f"Failed to write to file: {e}", "ERROR", "red")

    def _flush_json_buffer(self):
        """Flush JSON buffer to disk efficiently."""
        if not self._json_buffer:
            return

        self._handle_file_rotation(self.logJSON, self.maxJsonSize)

        try:
            with open(self.logJSON, "r+", encoding="utf-8") as f:
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
                    )
                    for log in self._json_buffer
                ]

                f.write(",\n".join(entries))
                f.write("\n]")

            self._json_buffer.clear()
        except Exception as e:
            self._log_internal(f"Failed to write to JSON: {e}", "ERROR", "red")

    def _write_to_console(self, message: str, level: str, color: str):
        """Write formatted log entry to console."""
        if not self.isColored:
            print(
                f"[{self._format_timestamp()}]  {level:<{self.maxLevelWidth}}  {message}"
            )
            return

        prefix_parts = [
            f"{Color.text('gray')}[{Color.endCode}",
            f"{Color.text('indigo')}{currentDate()}{Color.endCode}",
            f"{Color.text('gray')}|{Color.endCode}",
            f"{Color.text('violet')}{currentTime()}{Color.endCode}",
        ]

        if self.showTimezone:
            prefix_parts.extend(
                [
                    f"{Color.text('gray')}|{Color.endCode}",
                    f"{Color.text('purple')}{currentTimeZone()}{Color.endCode}",
                ]
            )

        prefix_parts.append(f"{Color.text('gray')}]{Color.endCode}")
        prefix = " ".join(prefix_parts)

        level_str = (
            f"{Color.background(color)}"
            f"{Color.style('bold')}"
            f" {level:<{self.maxLevelWidth}} "
            f"{Color.endCode}"
        )

        print(f"{prefix} {level_str} {Color.text(color)}{message}{Color.endCode}")

    def _write_to_sql(self, log_data: Dict[str, Any]):
        """Write log entry to SQL database."""
        self._handle_file_rotation(self.logSQL, self.maxSqlSize)

        try:
            with sqlite3.connect(self.logSQL) as conn:
                conn.execute(
                    f"INSERT INTO {self.sqlTable} VALUES (?, ?, ?, ?, ?, ?)",
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

    def _send_mail_async(self, message: str, level: str):
        """Send mail asynchronously."""
        if self._mail_client is None:
            return

        def send():
            try:
                self._mail_client.sendMail(
                    emailSubject=f"TAMGA: {level} Log - {currentDate()}",
                    messageContent=message,
                    logLevel=level,
                )
            except Exception as e:
                self._log_internal(f"Failed to send mail: {e}", "ERROR", "red")

        threading.Thread(target=send, daemon=True).start()

    def _write_to_api_async(self, log_data: Dict[str, Any]):
        """Write to API asynchronously."""

        def send():
            try:
                import requests

                requests.post(
                    self.apiURL,
                    json={
                        "level": log_data["level"],
                        "message": log_data["message"],
                        "date": log_data["date"],
                        "time": log_data["time"],
                        "timezone": log_data["timezone"],
                        "timestamp": log_data["unix_timestamp"],
                    },
                    timeout=5,
                )
            except Exception as e:
                self._log_internal(f"Failed to send to API: {e}", "ERROR", "red")

        threading.Thread(target=send, daemon=True).start()

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

        if self.enableBackup:
            self._create_backup(filepath)

        try:
            if filepath.endswith(".json"):
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump([], f)
            elif filepath.endswith(".db"):
                with sqlite3.connect(filepath) as conn:
                    conn.execute(f"DELETE FROM {self.sqlTable}")
            else:
                open(filepath, "w", encoding="utf-8").close()
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

    def mail(self, message: str) -> None:
        self.log(message, "MAIL", "neutral")
        if not self.sendMail:
            self._log_internal("Mail logging is not enabled!", "WARNING", "amber")

    def metric(self, message: str) -> None:
        self.log(message, "METRIC", "cyan")

    def trace(self, message: str) -> None:
        self.log(message, "TRACE", "gray")

    def custom(self, message: str, level: str, color: str) -> None:
        self.log(message, level, color)

    def dir(self, message: str, **kwargs) -> None:
        """Log message with additional key-value data."""
        if kwargs:
            data_str = json.dumps(kwargs, ensure_ascii=False).replace('"', "'")
            log_message = f"{message} | {data_str}"
        else:
            log_message = message

        self.log(log_message, "DIR", "yellow")
