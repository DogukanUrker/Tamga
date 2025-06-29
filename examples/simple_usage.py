# Simple Usage Example for Tamga

from tamga import Tamga

# Create a logger with default settings
logger = Tamga()

# Log messages at various levels
logger.info("Application started")
logger.success("User registration successful")
logger.warning("Disk space is running low")
logger.error("Failed to connect to database")
logger.critical("System outage detected")
logger.debug("Debugging variable x=42")

# Structured logging with key-value pairs
logger.dir(
    "User login event",
    user_id="abc123",
    action="login",
    ip_address="192.168.1.10",
    success=True,
)

# Custom log level and color
logger.custom("Payment received", "PAYMENT", "green")

# Force flush buffered logs (optional)
logger.flush()
