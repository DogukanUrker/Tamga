# Tamga / examples / advanced_config.py
# Example: Advanced Tamga Logger Configuration

import os

from tamga import Tamga

# Advanced logger setup for production-like environments
logger = Tamga(
    # File logging with rotation and backup
    logToFile=True,
    logFile="logs/app.log",
    maxLogSize=50,  # 50 MB max file size
    enableBackup=True,  # Enable backup on rotation
    # JSON logging for log aggregation
    logToJSON=True,
    logJSON="logs/app.json",
    maxJsonSize=50,
    # SQLite logging for analytics
    logToSQL=True,
    logSQL="logs/app.db",
    sqlTable="logs",
    maxSqlSize=100,
    # Performance
    bufferSize=200,  # Large buffer for high throughput
    logToConsole=False,  # Disable console for speed
    # MongoDB for centralized logging
    logToMongo=bool(os.getenv("MONGO_URI")),
    mongoURI=os.getenv("MONGO_URI", ""),
    # Multi-service notifications for critical events
    notifyServices=[
        # Discord webhook for dev team
        os.getenv("DISCORD_WEBHOOK", "discord://webhook_id/webhook_token"),
        # Slack for ops team
        os.getenv("SLACK_WEBHOOK", "slack://tokenA/tokenB/tokenC/#alerts"),
        # Email notifications
        f"mailto://{os.getenv('ALERT_EMAIL', 'ops@company.com')}",
        # SMS for critical issues
        os.getenv("TWILIO_SMS", "twilio://SID:Token@+1234567890/+0987654321"),
    ]
    if os.getenv("NOTIFICATIONS_ENABLED")
    else [],
    notifyLevels=["CRITICAL", "ERROR", "NOTIFY"],
    notifyTitle="🚨 {appname} Alert: {level}",
    notifyFormat="markdown",
)

# Example log events
logger.info("Advanced logger initialized")
logger.success("Service started successfully")
logger.warning("Cache miss rate above threshold")
logger.error("Failed to process payment")
logger.critical("Database connection lost")
logger.notify("New premium subscription purchased!")

# Structured logging for business events
logger.dir(
    "User action",
    user_id="user_456",
    action="purchase",
    item="Pro Plan",
    amount=99.99,
    currency="USD",
    success=True,
)

# Custom log level and color
logger.custom("Deploy completed", "DEPLOY", "purple")

# Force flush buffered logs (important before shutdown)
logger.flush()
