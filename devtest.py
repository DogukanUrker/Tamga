from tamga import Tamga
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
SMP_MAIL = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
tamga = Tamga(
    logToFile=True,
    logToJSON=True,
    logToConsole=True,
    logToMongo=True,
    logToSQL=True,
    logToAPI=True,
    sendMail=True,
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
)
startTime = datetime.now()
tamga.info("This is an info message!")
tamga.warning("This is a warning!")
tamga.error("This is an error!")
tamga.success("This is a success message!")
tamga.debug("This is a debug message!")
tamga.critical("This is a critical message!")
tamga.database("This is a database message!")
tamga.mail("This is a mail message!")
tamga.metric("This is a metric message!")
tamga.trace("This is a trace message!")
tamga.custom("This is a custom message!", "CUSTOM", "orange")
endTime = datetime.now()
print(f"Time taken: {endTime - startTime}")
