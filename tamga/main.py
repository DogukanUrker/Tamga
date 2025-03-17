import asyncio
import json
import os
import sqlite3
from datetime import datetime




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
    ):
        """
        Initialize Tamga with optional file and JSON logging.

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
        """

        self.maxLevelWidth = max(len(level) for level in self.LOG_LEVELS)

        self.isColored = isColored
        self.logToFile = logToFile
        self.logToJSON = logToJSON
        self.logToConsole = logToConsole
        self.logToMongo = logToMongo
        self.logToSQL = logToSQL
        self.logToAPI = logToAPI
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
        self.sendMail = sendMail
        self.mailLevels = mailLevels
        self.apiURL = apiURL
        self.maxLogSize = maxLogSize
        self.maxJsonSize = maxJsonSize
        self.maxSqlSize = maxSqlSize
        self.enableBackup = enableBackup

        global client
        client = None

        global mailClient
        mailClient = None

        if self.logToMongo:
            try:
                import motor.motor_asyncio
                client = motor.motor_asyncio.AsyncIOMotorClient(
                    self.mongoURI, tls=True, tlsAllowInvalidCertificates=True
                )
                client = client[mongoDatabaseName][mongoCollectionName]
                self._writeToConsole("Connected to MongoDB", "TAMGA", "lime")
            except Exception as e:
                self.critical(f"TAMGA: Failed to connect to MongoDB: {e}")

        if self.logToJSON and not os.path.exists(self.logJSON):
            with open(self.logJSON, "w", encoding="utf-8") as file:
                json.dump([], file)

        if self.logToFile and not os.path.exists(self.logFile):
            with open(self.logFile, "w", encoding="utf-8") as file:
                file.write("")

        if self.logToSQL and not os.path.exists(self.logSQL):
            with open(self.logSQL, "w", encoding="utf-8") as file:
                file.write("")
            conn = sqlite3.connect(self.logSQL)
            c = conn.cursor()

            c.execute(
                f"CREATE TABLE IF NOT EXISTS {self.sqlTable} (level TEXT, message TEXT, date TEXT, time TEXT, timezone TEXT, timestamp REAL)"
            )

        if self.sendMail:
            mailClient = Mail(
                serverAddress=self.smtpServer,
                portNumber=self.smtpPort,
                userName=self.smtpMail,
                userPassword=self.smtpPassword,
                senderEmail=self.smtpMail,
                receiverEmails=self.smtpReceivers,
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

        if self.sendMail:
            self._sendMail(message, level)

        if self.logToAPI:
            self._writeToAPI(message, level)

        if self.logToMongo:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self._writeToMongo(message, level, client))
            else:
                loop.run_until_complete(self._writeToMongo(message, level, client))

        return None

    def _checkFileSize(self, filePath: str, maxSizeMB: int) -> bool:
        """Check if file size exceeds the maximum size limit."""
        if not os.path.exists(filePath):
            return False
        return (os.path.getsize(filePath) / (1024 * 1024)) >= maxSizeMB

    def _createBackup(self, filePath: str) -> None:
        """Create a backup of the file with timestamp."""
        if not os.path.exists(filePath):
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backupPath = f"{filePath}.{timestamp}.bak"
        try:
            import shutil

            shutil.copy2(filePath, backupPath)
        except Exception as e:
            self.critical(f"Failed to create backup: {e}")

    def _handleFileRotation(self, filePath: str, maxSizeMB: int) -> None:
        """Handle file rotation when size limit is reached."""
        if self._checkFileSize(filePath, maxSizeMB):
            if self.enableBackup:
                self._createBackup(filePath)
            if filePath.endswith(".json"):
                with open(filePath, "w", encoding="utf-8") as f:
                    json.dump([], f)
            elif filePath.endswith(".db"):
                conn = sqlite3.connect(filePath)
                c = conn.cursor()
                c.execute(f"DELETE FROM {self.sqlTable}")
                conn.commit()
                conn.close()
            else:
                open(filePath, "w", encoding="utf-8").close()

    def _writeToFile(self, message: str, level: str) -> None:
        """Write log entry to file."""
        self._handleFileRotation(self.logFile, self.maxLogSize)
        with open(self.logFile, "a", encoding="utf-8") as file:
            file.write(
                f"[{currentDate()} | {currentTime()} | {currentTimeZone()}] {level}: {message}\n"
            )
        return None

    def _writeToJSON(self, message: str, level: str) -> None:
        """Write log entry to JSON file."""
        self._handleFileRotation(self.logJSON, self.maxJsonSize)
        logEntry = {
            "level": level,
            "message": message,
            "date": currentDate(),
            "time": currentTime(),
            "timezone": currentTimeZone(),
            "timestamp": currentTimeStamp(),
        }

        with open(self.logJSON, "r", encoding="utf-8") as file:
            logs = json.load(file)

        logs.append(logEntry)

        with open(self.logJSON, "w", encoding="utf-8") as file:
            json.dump(logs, file, ensure_ascii=False, indent=2)

        return None

    def _writeToConsole(self, message: str, level: str, color: str) -> None:
        """Write formatted log entry to console."""

        if not self.isColored:
            print(
                f"[{currentDate()} | {currentTime()} | {currentTimeZone()}]  {level:<{self.maxLevelWidth}}  {message}"
            )
            return None

        prefix = (
            f"{Color.text('gray')}["
            f"{Color.endCode}{Color.text('indigo')}{currentDate()}"
            f"{Color.endCode} {Color.text('gray')}|"
            f"{Color.endCode} {Color.text('violet')}{currentTime()}"
            f"{Color.text('gray')} |"
            f"{Color.endCode} {Color.text('purple')}{currentTimeZone()}"
            f"{Color.text('gray')}]"
            f"{Color.endCode}"
        )

        levelSTR = (
            f"{Color.background(color)}"
            f"{Color.style('bold')}"
            f" {level:<{self.maxLevelWidth}} "
            f"{Color.endCode}"
        )

        print(f"{prefix} {levelSTR} {Color.text(color)}{message}{Color.endCode}")

        return None

    def _sendMail(self, message: str, level: str) -> None:
        if level in self.mailLevels:
            mailClient.sendMail(
                emailSubject=f"TAMGA: {level} Log - {currentDate()}",
                messageContent=message,
                logLevel=level,
            )
        return None

    def _writeToAPI(self, message: str, level: str) -> None:
        import requests
        requests.post(
            self.apiURL,
            json={
                "level": level,
                "message": message,
                "date": currentDate(),
                "time": currentTime(),
                "timezone": currentTimeZone(),
                "timestamp": currentTimeStamp(),
            },
        )
        return None

    def _writeToSQL(self, message: str, level: str) -> None:
        """Write log entry to SQL database."""
        self._handleFileRotation(self.logSQL, self.maxSqlSize)
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
        if not self.sendMail:
            self.critical("TAMGA: Mail logging is not enabled!")

    def metric(self, message: str) -> None:
        self.log(message, "METRIC", "cyan")

    def trace(self, message: str) -> None:
        self.log(message, "TRACE", "gray")

    def custom(self, message: str, level: str, color: str) -> None:
        self.log(message, level, color)

    def dir(self, message: str, **kwargs) -> None:
        if kwargs:
            strJSON = json.dumps(kwargs, ensure_ascii=False)
            formatted = strJSON.replace('"', "'")
            logMessage = f"{message} | {formatted}"
        else:
            logMessage = message

        self.log(logMessage, "DIR", "yellow")
