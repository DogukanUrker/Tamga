from .utils.colors import Color
from .utils.time import currentDate, currentTime, currentTimeZone, currentTimeStamp
import json
import os


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
    }

    def __init__(self, logToFile: bool = False, logToJSON: bool = False):
        """
        Initialize Tamga with optional file and JSON logging.

        Args:
            logToFile: Enable logging to a file (default: False)
            logToJSON: Enable logging to a JSON file (default: False)
        """
        self.logToFile = logToFile
        self.logToJSON = logToJSON

        # Initialize JSON file with empty array if it doesn't exist
        if self.logToJSON and not os.path.exists("tamga.json"):
            with open("tamga.json", "w") as logFile:
                json.dump([], logFile)

        print(f"{Color.text('indigo')}Tamga class is imported{Color.endCode}")

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

        self._writeToConsole(message, level, color)

    def _writeToFile(self, message: str, level: str) -> None:
        """Write log entry to file."""
        with open("tamga.log", "a") as logFile:
            logFile.write(
                f"[{currentDate()} | {currentTime()} | {currentTimeZone()}] {level}: {message}\n"
            )

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

    def custom(self, message: str, level: str, color: str) -> None:
        self.log(message, level, color)
