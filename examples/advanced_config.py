# Tamga / examples / advanced_config.py
# Example: Advanced Tamga Logger Configuration

import os

from tamga import Tamga

# Advanced logger setup for production-like environments
logger = Tamga(
    # File logging with rotation and backup
    file_output=True,
    json_path="logs/app.log",
    max_log_size=50,  # 50 MB max file size
    enable_backup=True,  # Enable backup on rotation
    # JSON logging for log aggregation
    json_output=True,
    log_json="logs/app.json",
    max_json_size_mb=50,
    # SQLite logging for analytics
    sql_output=True,
    sql_path="logs/app.db",
    sql_table_name="logs",
    max_sql_size_mb=100,
    # Performance
    buffer_size=200,  # Large buffer for high throughput
    console_output=False,  # Disable console for speed
    # MongoDB for centralized logging
    mongo_output=bool(os.getenv("MONGO_URI")),
    mongo_uri=os.getenv("MONGO_URI", ""),
    # Multi-service notifications for critical events
    notify_services=[
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
    notify_levels=["CRITICAL", "ERROR"],
    notify_title="🚨 {appname} Alert: {level}",
    notify_format="markdown",  # text, html, markdown
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
