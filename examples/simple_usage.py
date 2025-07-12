# Simple Usage Example for Tamga

from tamga import Tamga

# Create a logger with default settings
logger = Tamga()

# Optional: Add notifications (requires pip install tamga[notifications])
# logger = Tamga(
#     notify_services=["discord://webhook_id/webhook_token"],
#     notify_levels=["CRITICAL", "ERROR"]
# )

# Log messages at various levels
logger.info("Application started")
logger.success("User registration successful")
logger.warning("Disk space is running low")
logger.error("Failed to connect to database")
logger.critical("System outage detected")
logger.debug("Debugging variable x=42")
logger.info("User login event", user_id="abc123", ip="192.168.1.10", success=True)
logger.warning("High memory usage", current_mb=7680, total_mb=8192, percentage=93.75)
logger.error(
    "API request failed", endpoint="/api/users", status_code=500, retry_count=3
)
logger.success(
    "Payment processed", transaction_id="TXN-789", amount=99.99, currency="USD"
)
logger.debug("Cache statistics", hits=1250, misses=45, hit_rate=0.965)

# Custom log level with data
logger.custom(
    "Payment received",
    "PAYMENT",
    "green",
    amount=150.00,
    method="stripe",
    customer_id="CUST-123",
)

user_profile = {
    "id": 456,
    "username": "johndoe",
    "profile": {
        "name": "John Doe",
        "email": "john@example.com",
        "verified": True,
        "created_at": "2024-01-15",
    },
    "preferences": {
        "theme": "dark",
        "notifications": {"email": True, "push": False, "sms": True},
        "language": "en",
    },
    "roles": ["user", "premium", "beta_tester"],
}

# Pretty print the complex object
logger.dir(user_profile, "User profile loaded")

# Pretty print a list
active_connections = [
    {"id": 1, "ip": "192.168.1.100", "port": 8080, "status": "active"},
    {"id": 2, "ip": "192.168.1.101", "port": 8081, "status": "active"},
    {"id": 3, "ip": "192.168.1.102", "port": 8082, "status": "idle"},
]
logger.dir(active_connections, "Current connections")

# Notification with structured data
logger.notify(
    "New premium subscription purchased!",
    customer_id="CUST-789",
    plan="enterprise",
    monthly_value=999.99,
    contract_length_months=12,
)

# Force flush buffered logs (optional)
logger.flush()
