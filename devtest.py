from tamga import Tamga
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
SMP_MAIL = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def testBackupFeature():
    tamga = Tamga(
        logToFile=True,
        logToJSON=True,
        logToConsole=True,
        logToMongo=False,
        logToSQL=True,
        logToAPI=True,
        sendMail=False,
        mongoURI=MONGO_URI,
        mongoDatabaseName="tamga",
        mongoCollectionName="logs",
        logFile="tamga.log",
        logJSON="tamga.json",
        logSQL="tamga.db",
        sqlTable="logs",
        smtpServer="smtp.gmail.com",
        smtpPort=587,
        smtpMail=SMP_MAIL,
        smtpPassword=SMTP_PASSWORD,
        smtpReceivers=["dogukanurker@icloud.com"],
        mailLevels=["MAIL"],
        apiURL="http://127.0.0.1:5000/api/log",
        # Set small file size limits to test backup feature
        maxLogSize=0.001,  # 100KB for log file
        maxJsonSize=1,  # 100KB for JSON file
        maxSqlSize=1,  # 100KB for SQL file
        enableBackup=True,
    )

    print("Starting backup feature test...")
    print("Writing logs to trigger backup...")

    # Generate logs until backup is triggered
    for i in range(1000):
        tamga.info(
            f"Test log message {i} with some extra content to increase file size quickly. This is a longer message to help reach the file size limit faster."
        )
        tamga.error(
            f"Test error message {i} with additional content for file size increase."
        )
        tamga.warning(
            f"Test warning message {i} with more content to make the file grow."
        )

        backupFiles = [f for f in os.listdir(".") if f.endswith(".bak")]
        if backupFiles:
            print("\nBackup files created:")
            for backup in backupFiles:
                print(f"- {backup}")
            break

        time.sleep(0.1)

        if i % 10 == 0:
            print(f"Progress: {i} logs written", end="\r")


def main():
    startTime = datetime.now()

    print("=== Testing Backup Feature ===")
    testBackupFeature()

    endTime = datetime.now()
    print(f"\nTotal time taken: {endTime - startTime}")


if __name__ == "__main__":
    main()
