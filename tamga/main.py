from .utils.colors import Color
from .utils.time import currentDate, currentTime, currentTimeZone, currentTimeStamp
import json
import os
import motor.motor_asyncio
import asyncio


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
    }

    def __init__(
        self,
        logToFile: bool = False,
        logToJSON: bool = False,
        logToConsole: bool = True,
        logToMongo: bool = False,
        mongoURI: str = None,
        mongoDatabaseName: str = "tamga",
        mongoCollectionName: str = "logs",
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
        self.mongoURI = mongoURI

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
        if self.logToJSON and not os.path.exists("tamga.json"):
            with open("tamga.json", "w") as logFile:
                json.dump([], logFile)

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

        if self.logToMongo:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self._writeToMongo(message, level, client))
            else:
                loop.run_until_complete(self._writeToMongo(message, level, client))

        return None

    def _writeToFile(self, message: str, level: str) -> None:
        """Write log entry to file."""
        with open("tamga.log", "a") as logFile:
            logFile.write(
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
        with open("tamga.json", "r") as logFile:
            logs = json.load(logFile)

        # Append new log
        logs.append(logEntry)

        # Write back all logs
        with open("tamga.json", "w") as logFile:
            json.dump(logs, logFile, indent=2)

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

    def custom(self, message: str, level: str, color: str) -> None:
        self.log(message, level, color)
