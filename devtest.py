from tamga import Tamga
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
tamga = Tamga(
    logToFile=True,
    logToJSON=True,
    logToConsole=True,
    logToMongo=False,
    logToSQL=True,
    mongoURI=MONGO_URI,
    logFile="tamga2.log",
    logJSON="tamga2.json",
    logSQL="tamga.db",
    sqlTable="logs2",
)
startTime = datetime.now()
tamga.info("This is an info message!")
tamga.warning("This is a warning!")
tamga.error("This is an error!")
tamga.success("This is a success message!")
tamga.debug("This is a debug message!")
tamga.critical("This is a critical message!")
tamga.database("This is a database message!")
tamga.custom("This is a custom message!", "CUSTOM", "orange")
endTime = datetime.now()
print(f"Time taken: {endTime - startTime}")
