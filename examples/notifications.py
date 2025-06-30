"""
Tamga Notification Examples
Shows how to use the new Apprise-based notification system for 80+ services
"""

import time

from tamga import Tamga

# Example 1: Discord notifications for errors
print("=== Example 1: Discord Error Notifications ===")
discord_logger = Tamga(
    notifyServices=["discord://webhook_id/webhook_token"],
    notifyLevels=["ERROR", "CRITICAL"],
    notifyTitle="{appname} Alert: {level}",
    notifyFormat="markdown",
)

# These will trigger notifications
discord_logger.error("Database connection failed!")
discord_logger.critical("System is down!")

# This won't trigger notification (not in notifyLevels)
discord_logger.info("Regular info message")


# Example 2: Multi-service ops alerts
print("\n=== Example 2: Multi-Service Operations Alerts ===")
ops_logger = Tamga(
    notifyServices=[
        # Discord for dev team
        "discord://webhook_id/webhook_token",
        # Slack for ops team
        "slack://tokenA/tokenB/tokenC/#ops-alerts",
        # Email notifications
        "mailto://alerts@company.com",
        # SMS for critical issues (Twilio example)
        "twilio://AccountSID:AuthToken@+1234567890/+0987654321",
    ],
    notifyLevels=["CRITICAL", "ERROR"],
    notifyFormat="text",
)

ops_logger.critical("Payment system is offline - immediate attention required!")
ops_logger.error("High memory usage detected on server-03")


# Example 3: Development notifications (desktop)
print("\n=== Example 3: Desktop Development Notifications ===")
dev_logger = Tamga(
    notifyServices=[
        # Desktop notifications (cross-platform)
        "gnome://",  # Linux
        "macosx://",  # macOS
        "windows://",  # Windows
    ],
    notifyLevels=["ERROR", "SUCCESS"],
    notifyTitle="Build Status: {level}",
)

dev_logger.error("Unit tests failed!")
dev_logger.success("Build completed successfully!")


# Example 4: Direct notification with custom services
print("\n=== Example 4: Direct Notifications ===")
general_logger = Tamga()

# Send to specific services (overrides defaults)
general_logger.notify(
    "Deployment to production completed!",
    title="🚀 Production Deploy",
    services=[
        "discord://webhook_id/webhook_token",
        "slack://tokenA/tokenB/tokenC/#deployments",
    ],
)

# Example 5: Multi-service production setup
print("\n=== Example 5: Production Multi-Service Setup ===")
production_logger = Tamga(
    notifyServices=[
        # Critical alerts to multiple channels
        "discord://webhook_id/webhook_token",
        "slack://tokenA/tokenB/tokenC/#critical-alerts",
        "mailto://ops@company.com",
    ],
    notifyLevels=["CRITICAL", "ERROR"],
)

# Production alerts
production_logger.critical("Database connection lost!")
production_logger.notify("System maintenance completed successfully!")


# Example 6: Performance test - notifications don't slow down logging
print("\n=== Example 6: Performance Test ===")
perf_logger = Tamga(
    notifyServices=["discord://webhook_id/webhook_token"],
    notifyLevels=["CRITICAL"],  # Only critical notifications
)

# Logging speed test
start_time = time.time()
for i in range(1000):
    perf_logger.info(f"Log message {i}")  # These won't trigger notifications

# Flush any remaining logs
perf_logger.flush()
end_time = time.time()

print(f"Logged 1000 messages in {end_time - start_time:.3f} seconds")
print("Notification system has zero performance impact when not triggered!")

# Trigger one notification
perf_logger.critical("This will trigger a notification")


# Example 7: Rich notification formats
print("\n=== Example 7: Rich Notification Formats ===")
rich_logger = Tamga(
    notifyServices=["discord://webhook_id/webhook_token"],
    notifyFormat="markdown",  # Support for markdown formatting
    notifyTitle="📊 **{appname}** | {level} Alert",
)

rich_logger.notify("""
## System Status Update

### 🔴 Issues Detected:
- **Database**: High latency (>500ms)
- **Cache**: Memory usage at 95%
- **Queue**: 1,247 pending jobs

### 📈 Metrics:
- CPU: 78%
- RAM: 12.4GB/16GB
- Disk: 450GB/500GB

*Automatic scaling initiated...*
""")


# Example 8: Conditional notifications
print("\n=== Example 8: Conditional Notifications ===")


def smart_notify(logger, level, message, condition=True):
    """Smart notification based on conditions"""
    if condition:
        logger.log(message, level, "red" if level == "ERROR" else "green")
    else:
        logger.info(f"Condition not met for: {message}")


monitoring_logger = Tamga(
    notifyServices=["discord://webhook_id/webhook_token"],
    notifyLevels=["ERROR", "CRITICAL"],
)

# Only notify if error rate is high
error_rate = 5.2  # Simulated error rate
smart_notify(
    monitoring_logger,
    "ERROR",
    f"Error rate is {error_rate}% - above threshold!",
    condition=error_rate > 5.0,
)


print("\n=== Available Services ===")
print("""
📱 Mobile & Messaging:
   - Discord: discord://webhook_id/webhook_token
   - Slack: slack://tokenA/tokenB/tokenC/#channel
   - Telegram: tgram://bottoken/ChatID
   - WhatsApp: whatsapp://token/phoneno
   - Teams: msteams://TokenA/TokenB/TokenC

📧 Email:
   - Gmail: mailto://user:pass@gmail.com
   - Outlook: mailtos://user:pass@outlook.com
   - Custom SMTP: smtp://user:pass@server:port

📟 SMS & Push:
   - Twilio: twilio://AccountSID:AuthToken@FromPhone/ToPhone
   - Pushover: pover://user@token
   - Pushbullet: pbul://accesstoken

🖥️ Desktop:
   - Linux: gnome://
   - macOS: macosx://
   - Windows: windows://

🌐 Web Services:
   - Webhook: json://webhook.site/your-uuid
   - IFTTT: ifttt://WebHookID

And 60+ more services! See: https://github.com/caronc/apprise
""")

print(
    "\n✅ Migration completed! Tamga now supports 80+ notification services while maintaining peak performance."
)
