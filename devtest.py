from tamga import Tamga
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
tamga = Tamga(
    logToFile=True,
    logToJSON=True,
    logToConsole=True,
    logToMongo=True,
    mongoURI=MONGO_URI,
)
print("\n")
tamga.info("This is an info message!")
print("\n")
tamga.warning("This is a warning!")
print("\n")
tamga.error("This is an error!")
print("\n")
tamga.success("This is a success message!")
print("\n")
tamga.debug("This is a debug message!")
print("\n")
tamga.critical("This is a critical message!")
print("\n")
tamga.database("This is a database message!")
print("\n")
tamga.custom("This is a custom message!", "CUSTOM", "orange")
print("\n")
