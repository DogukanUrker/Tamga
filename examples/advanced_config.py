# Tamga / examples / advanced_config.py
# Example: Advanced Tamga Logger Configuration

import os

from tamga import Tamga

# Advanced logger setup for production-like environments
logger = Tamga(
    # File logging with rotation and backup
    file_output=True,
    file_path="logs/app.log",
    max_file_size_mb=50,  # 50 MB max file size
    enable_backup=True,  # Enable backup on rotation
    # JSON logging for log aggregation
    json_output=True,
    json_path="logs/app.json",
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

# Example log events with structured data
logger.info(
    "Advanced logger initialized", config_file="production.yaml", pid=os.getpid()
)
logger.success("Service started successfully", port=8080, workers=4, ssl_enabled=True)
logger.warning(
    "Cache miss rate above threshold", miss_rate=0.15, threshold=0.10, cache_size_mb=512
)
logger.error(
    "Failed to process payment",
    error_code="PAYMENT_DECLINED",
    transaction_id="TXN-12345",
    amount=199.99,
    retry_attempt=2,
)
logger.critical(
    "Database connection lost",
    host="db.production.internal",
    port=5432,
    error="Connection timeout after 30s",
    pool_size=20,
)

# Notification with structured data
logger.notify(
    "New premium subscription purchased!",
    customer_id="CUST-789",
    plan="enterprise",
    monthly_value=999.99,
    contract_length_months=12,
)

# Business metrics logging
logger.metric(
    "API performance",
    endpoint="/api/v2/users",
    avg_response_ms=45,
    p95_response_ms=125,
    requests_per_second=1250,
)

# Custom log level with business context
logger.custom(
    "Deployment completed",
    "DEPLOY",
    "purple",
    version="2.1.0",
    environment="production",
    region="us-east-1",
    deployment_time_seconds=180,
    rollback_enabled=True,
)

# Pretty print complex configuration
app_config = {
    "database": {
        "primary": {
            "host": "db-primary.prod",
            "port": 5432,
            "pool": {"min": 10, "max": 50},
        },
        "replica": {
            "host": "db-replica.prod",
            "port": 5432,
            "pool": {"min": 5, "max": 25},
        },
    },
    "cache": {
        "redis": {
            "nodes": ["redis-1:6379", "redis-2:6379", "redis-3:6379"],
            "cluster_mode": True,
            "ttl_seconds": 3600,
        }
    },
    "features": {"new_dashboard": True, "beta_api": False, "experimental_cache": True},
    "monitoring": {
        "metrics_enabled": True,
        "trace_sample_rate": 0.1,
        "log_level": "INFO",
    },
}

logger.dir(app_config, "Application configuration loaded")

# Force flush buffered logs (important before shutdown)
logger.flush()
