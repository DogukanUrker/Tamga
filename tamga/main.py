from .utils.colors import Color
from .utils.time import currentDate, currentTime, currentTimeZone, currentTimeStamp
import json
import os
import motor.motor_asyncio
import asyncio
import sqlite3


class Tamga:
    """
    A modern logging utility that supports console, file, and JSON logging with colored output.
    """

    # Define valid log levels and their associated colors
    LOG_LEVELS = {
        "INFO": "sky",
        "WARNING": "amber",
        "ERROR": "rose",
        "SUCCESS": "emerald",
        "DEBUG": "indigo",
        "CRITICAL": "red",
        "DATABASE": "green",
        "MAIL": "neutral",
        "METRIC": "cyan",
        "TRACE": "gray",
    }

    def __init__(
        self,
        logToFile: bool = False,
        logToJSON: bool = False,
        logToConsole: bool = True,
        logToMongo: bool = False,
        logToSQL: bool = False,
        mongoURI: str = None,
        mongoDatabaseName: str = "tamga",
        mongoCollectionName: str = "logs",
        logFile: str = "tamga.log",
        logJSON: str = "tamga.json",
        logSQL: str = "tamga.db",
        sqlTable: str = "logs",
    ):
        """
        Initialize Tamga with optional file and JSON logging.

        Args:
            logToFile: Enable logging to a file (default: False)
            logToJSON: Enable logging to a JSON file (default: False)
            logToConsole: Enable logging to console (default: True)
            logToMongo: Enable logging to MongoDB (default: False)
            mongoURI: MongoDB connection URI
            mongoDatabaseName: MongoDB database name (default: "tamga")
            mongoCollectionName: MongoDB collection name (default: "logs")
        """
        self.logToFile = logToFile
        self.logToJSON = logToJSON
        self.logToConsole = logToConsole
        self.logToMongo = logToMongo
        self.logToSQL = logToSQL
        self.mongoURI = mongoURI
        self.mongoDatabaseName = mongoDatabaseName
        self.mongoCollectionName = mongoCollectionName
        self.logFile = logFile
        self.logJSON = logJSON
        self.logSQL = logSQL
        self.sqlTable = sqlTable

        global client
        client = None

        if self.logToMongo:
            try:
                client = motor.motor_asyncio.AsyncIOMotorClient(
                    self.mongoURI, tls=True, tlsAllowInvalidCertificates=True
                )
                client = client[mongoDatabaseName][mongoCollectionName]
                self._writeToConsole("Connected to MongoDB", "TAMGA", "lime")
            except Exception as e:
                self.critical(f"TAMGA: Failed to connect to MongoDB: {e}")

        # Initialize JSON file with empty array if it doesn't exist
        if self.logToJSON and not os.path.exists(self.logJSON):
            with open(self.logJSON, "w") as file:
                json.dump([], file)

        if self.logToFile and not os.path.exists(self.logFile):
            with open(self.logFile, "w") as file:
                file.write("")

        if self.logToSQL and not os.path.exists(self.logSQL):
            with open(self.logSQL, "w") as file:
                file.write("")
            conn = sqlite3.connect(self.logSQL)
            c = conn.cursor()

            # Check if table exists, create if not
            c.execute(
                f"CREATE TABLE IF NOT EXISTS {self.sqlTable} (level TEXT, message TEXT, date TEXT, time TEXT, timezone TEXT, timestamp REAL)"
            )

    def log(self, message: str, level: str, color: str) -> None:
        """
        Main logging method that handles all types of logs.

        Args:
            message: The message to log
            level: The log level
            color: Color for console output
        """
        if self.logToFile:
            self._writeToFile(message, level)

        if self.logToJSON:
            self._writeToJSON(message, level)

        if self.logToConsole:
            self._writeToConsole(message, level, color)

        if self.logToSQL:
            self._writeToSQL(message, level)

        if self.logToMongo:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self._writeToMongo(message, level, client))
            else:
                loop.run_until_complete(self._writeToMongo(message, level, client))

        return None

    def _writeToFile(self, message: str, level: str) -> None:
        """Write log entry to file."""
        with open(self.logFile, "a") as file:
            file.write(
                f"[{currentDate()} | {currentTime()} | {currentTimeZone()}] {level}: {message}\n"
            )
        return None

    def _writeToJSON(self, message: str, level: str) -> None:
        """Write log entry to JSON file."""
        logEntry = {
            "level": level,
            "message": message,
            "date": currentDate(),
            "time": currentTime(),
            "timezone": currentTimeZone(),
            "timestamp": currentTimeStamp(),
        }

        # Read existing logs
        with open(self.logJSON, "r") as file:
            logs = json.load(file)

        # Append new log
        logs.append(logEntry)

        # Write back all logs
        with open(self.logJSON, "w") as file:
            json.dump(logs, file, indent=2)

        return None

    def _writeToConsole(self, message: str, level: str, color: str) -> None:
        """Write formatted log entry to console."""
        print(
            f"{Color.text('gray')}["
            f"{Color.endCode}{Color.text('indigo')}{currentDate()}"
            f"{Color.endCode} {Color.text('gray')}|"
            f"{Color.endCode} {Color.text('violet')}{currentTime()}"
            f"{Color.text('gray')} |"
            f"{Color.endCode} {Color.text('purple')}{currentTimeZone()}"
            f"{Color.text('gray')}]{Color.endCode} "
            f"{Color.background(color)}{Color.style('bold')} {level} "
            f"{Color.endCode} {Color.text(color)}{message}{Color.endCode}"
        )
        return None

    def _writeToSQL(self, message: str, level: str) -> None:
        conn = sqlite3.connect(self.logSQL)
        c = conn.cursor()
        c.execute(
            f"INSERT INTO {self.sqlTable} (level, message, date, time, timezone, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (
                level,
                message,
                currentDate(),
                currentTime(),
                currentTimeZone(),
                currentTimeStamp(),
            ),
        )
        conn.commit()
        conn.close()
        return None

    async def _writeToMongo(self, message: str, level: str, client) -> None:
        if client is None:
            await self._writeToFile(
                "TAMGA: MongoDB client is not initialized!", "CRITICAL"
            )
            return None
        await client.insert_one(
            {
                "level": level,
                "message": message,
                "date": currentDate(),
                "time": currentTime(),
                "timezone": currentTimeZone(),
                "timestamp": currentTimeStamp(),
            }
        )
        return None

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

    def metric(self, message: str) -> None:
        self.log(message, "METRIC", "cyan")

    def trace(self, message: str) -> None:
        self.log(message, "TRACE", "gray")

    def custom(self, message: str, level: str, color: str) -> None:
        self.log(message, level, color)
