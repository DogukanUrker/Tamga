# Tamga [![PyPI Downloads](https://static.pepy.tech/badge/tamga)](https://pepy.tech/projects/tamga)

A modern, high-performance logging utility for Python with multiple output formats and colorful console output.

[![Installation](https://belg-api.vercel.app/badge/installation/pip3%20install%20tamga/neutral/dark)](https://pypi.org/project/tamga/)

**🤖 AI Integration:** For AI/LLM integration, see [LLMs.txt](https://raw.githubusercontent.com/DogukanUrker/Tamga/refs/heads/main/llms.txt) or access documentation directly via [Context7](https://context7.com/dogukanurker/tamga)

> **tam·ga** */ˈtæmɡə/* · noun
> An ancient Turkic symbol or seal used for marking ownership, identity, or lineage.

<img alt="Terminal" src="https://github.com/DogukanUrker/Tamga/blob/main/Images/terminal.png?raw=true" />

## ✨ Features

- 🎨 **Beautiful Console Output** - Colorful, formatted logs using Tailwind CSS colors
- ⚡ **High Performance** - Buffered writing system (10x faster than traditional logging)
- 📊 **Multiple Outputs** - Console, file, JSON, SQLite, MongoDB
- 🔄 **Automatic Rotation** - File size management with backup support
- 🧵 **Thread-Safe** - Safe for multi-threaded applications
- 🔔 **Notifications** - Multi-service notifications via [Apprise](https://github.com/caronc/apprise) (Discord, Slack, Email, SMS, and more)
- 🔍 **Structured Logging** - Key-value data support for all log levels plus pretty printing with `dir()` method

## 🚀 Quick Start

See [`examples/simple_usage.py`](./examples/simple_usage.py) for a full script.

```python
from tamga import Tamga

# Create logger with default settings
logger = Tamga()

# Log messages
logger.info("Application started")
logger.warning("Memory usage at 85%")
logger.error("Failed to connect to API")
logger.success("User registered successfully")
logger.debug("Cache initialized with 1000 entries")

# Log with key-value data (all levels support this)
logger.info("User login", user_id=123, ip="192.168.1.1", success=True)
logger.error("API failed", endpoint="/api/users", status_code=500)
```

## 🧑‍💻 Examples

See [`examples/`](./examples) for ready-to-run scripts:

- `simple_usage.py` — basic logging
- `fastapi_webapp.py` — FastAPI integration
- `advanced_config.py` — production config
- `high_performance.py` — high-speed big data logging demo


## 📦 Installation

```bash
pip install tamga                    # Basic installation
pip install tamga[mongo]             # With MongoDB support
pip install tamga[notifications]     # With notification support
pip install tamga[all]              # All features
```

## 🎯 Usage Examples

### Basic Configuration
```python
logger = Tamga(
    # Display settings
    colored_output=True,        # Colored output
    show_time=True,         # Include timestamp
    show_timezone=False,    # Include timezone

    # Output destinations
    file_output=True,        # Log to file
    file_path="app.log",     # Log file path
    buffer_size=50,         # Buffer size for performance
)
```

### Key-Value Logging
```python
# All log levels now support key-value data
logger.info("User login", user_id=123, ip="192.168.1.1", success=True)
logger.warning("High memory usage", current_mb=7680, total_mb=8192, percentage=93.75)
logger.error("API request failed", endpoint="/api/users", status_code=500, retry_count=3)
logger.success("Payment processed", transaction_id="TXN-789", amount=99.99, currency="USD")
logger.debug("Cache statistics", hits=1250, misses=45, hit_rate=0.965)
```

### Pretty Printing Objects
```python
# Use dir() for beautiful formatting of complex objects
user_profile = {
    "id": 456,
    "username": "johndoe",
    "profile": {
        "name": "John Doe",
        "email": "john@example.com",
        "verified": True
    },
    "roles": ["user", "premium", "beta_tester"]
}
logger.dir(user_profile, "User profile loaded")
```

### Production Setup
```python
logger = Tamga(
    # File rotation
    file_output=True,
    max_file_size_mb=50,         # 50MB max file size
    enable_backup=True,     # Create backups

    # Performance
    buffer_size=200,        # Larger buffer for production
    console_output=False,    # Disable console for speed

    # External services
    mongo_output=True,
    mongo_uri="mongodb://...",

    # Multi-service notifications
    notify_services=[
        "discord://webhook_id/webhook_token",
        "slack://tokenA/tokenB/tokenC/#alerts",
        "mailto://user:pass@smtp.gmail.com:587/?to=alerts@company.com",
        "twilio://SID:Token@+1234567890/+0987654321",
    ],
    notify_levels=["CRITICAL", "ERROR", "NOTIFY"],
)
```

## 📋 Log Levels

| Level | Color | Method | Use Case |
|-------|-------|---------|----------|
| INFO | Sky | `logger.info()` | General information |
| WARNING | Amber | `logger.warning()` | Warning messages |
| ERROR | Rose | `logger.error()` | Error messages |
| SUCCESS | Emerald | `logger.success()` | Success messages |
| DEBUG | Indigo | `logger.debug()` | Debug information |
| CRITICAL | Red | `logger.critical()` | Critical issues |
| DATABASE | Green | `logger.database()` | Database operations |
| NOTIFY | Purple | `logger.notify()` | Send notifications |
| METRIC | Cyan | `logger.metric()` | Performance metrics |
| TRACE | Gray | `logger.trace()` | Detailed trace info |
| DIR | Yellow | `logger.dir()` | Structured key-value data |
| CUSTOM | Any | `logger.custom()` | Custom levels |

**Note**: All log levels support key-value data through keyword arguments. The `dir()` method is specifically designed for pretty printing complex objects.

## 🔧 Advanced Features

### Notifications
```python
# Configure notification services (supports 80+ services via Apprise)
logger = Tamga(
    notify_services=[
        "discord://webhook_id/webhook_token",
        "slack://tokenA/tokenB/tokenC/#channel",
    ],
    notify_levels=["CRITICAL", "ERROR", "NOTIFY"],
    notify_title="{appname}: {level} Alert",
    notify_format="markdown",  # text, markdown, or html
)

# Send notification with structured data
logger.notify(
    "Payment received from user #123",
    user_id="123",
    amount=299.99,
    currency="USD",
    payment_method="stripe"
)

# Critical logs also trigger notifications with structured data
logger.critical(
    "Database connection lost",
    host="db.production.internal",
    port=5432,
    error="Connection timeout after 30s"
)
```

### Custom Log Levels
```python
logger.custom("Deploy completed", "DEPLOY", "purple")
logger.custom("Payment received", "PAYMENT", "green")
```

### Buffer Control
```python
# Force write all buffered logs
logger.flush()
```

### File Rotation
When log files reach `max_file_size_mb`, Tamga automatically:
- Creates timestamped backups (if enabled)
- Clears the original file
- Continues logging seamlessly

## 📊 Performance

Tamga uses a buffered writing system that delivers significantly faster performance compared to traditional logging. The buffering mechanism provides optimal throughput for high-volume logging scenarios while maintaining thread safety.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/tamga/)
- [GitHub Repository](https://github.com/DogukanUrker/Tamga)
- [Documentation](https://tamga.vercel.app/)
- [Bug Reports](https://github.com/DogukanUrker/Tamga/issues)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/DogukanUrker">Doğukan Ürker</a>
</p>
