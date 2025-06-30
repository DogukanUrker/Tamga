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
- 📊 **Multiple Outputs** - Console, file, JSON, SQLite, MongoDB, and notifications
- 🔄 **Automatic Rotation** - File size management with backup support
- 🧵 **Thread-Safe** - Safe for multi-threaded applications
- 📱 **80+ Notification Services** - Discord, Slack, Telegram, SMS, Email, and more via [Apprise](https://github.com/caronc/apprise)
- 🔍 **Structured Logging** - Key-value data support with `dir()` method

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
```

## 🧑‍💻 Examples

See [`examples/`](./examples) for ready-to-run scripts:

- `simple_usage.py` — basic logging
- `notifications.py` — 80+ notification services showcase
- `fastapi_webapp.py` — FastAPI integration
- `advanced_config.py` — production config
- `high_performance.py` — high-speed big data logging demo


## 📦 Installation

```bash
pip install tamga                    # Basic installation
pip install tamga[mongo]             # With MongoDB support
pip install tamga[all]               # With all optional dependencies
pip install tamga[notifications]     # With 80+ notification services
```

## 🎯 Usage Examples

### Basic Configuration
```python
logger = Tamga(
    # Display settings
    isColored=True,        # Colored output
    showTime=True,         # Include timestamp
    showTimezone=False,    # Include timezone

    # Output destinations
    logToFile=True,        # Log to file
    logFile="app.log",     # Log file path
    bufferSize=50,         # Buffer size for performance
)
```

### Structured Logging
```python
# Log with key-value data
logger.dir("User action",
    user_id="123",
    action="login",
    ip_address="192.168.1.1",
    success=True
)
```

### Production Setup
```python
logger = Tamga(
    # File rotation
    logToFile=True,
    maxLogSize=50,         # 50MB max file size
    enableBackup=True,     # Create backups

    # Performance
    bufferSize=200,        # Larger buffer for production
    logToConsole=False,    # Disable console for speed

    # External services
    logToMongo=True,
    mongoURI="mongodb://...",

    # Multi-service notifications (80+ services supported!)
    notifyServices=[
        "discord://webhook_id/webhook_token",      # Discord
        "slack://tokenA/tokenB/tokenC/#alerts",    # Slack
        "mailto://alerts@company.com",             # Email
        "twilio://SID:Token@+1234567890/+0987654321"  # SMS
    ],
    notifyLevels=["CRITICAL", "ERROR"],
    notifyFormat="markdown"
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
| NOTIFY | Purple | `logger.notify()` | Direct notifications |
| METRIC | Cyan | `logger.metric()` | Performance metrics |
| TRACE | Gray | `logger.trace()` | Detailed trace info |
| DIR | Yellow | `logger.dir()` | Structured key-value data |
| CUSTOM | Any | `logger.custom()` | Custom levels |

## 🔧 Advanced Features

### Notifications (80+ Services)
```python
# Multi-service notifications
logger = Tamga(
    notifyServices=[
        "discord://webhook_id/webhook_token",
        "slack://tokenA/tokenB/tokenC/#channel",
        "telegram://bottoken/chatid",
        "mailto://user:pass@gmail.com",
        "twilio://SID:Token@FromPhone/ToPhone"
    ]
)

# Direct notifications
logger.notify("Deployment completed!")
logger.notify("Critical alert!", title="🚨 Emergency")

# Auto-notify on specific levels
logger.critical("This will notify all services!")

# Notification with custom services (override defaults)
logger.notify(
    "Deployment to production completed!",
    title="🚀 Production Deploy",
    services=["discord://webhook", "slack://tokens"]
)
```

**Popular notification services:**
- **Discord**: `discord://webhook_id/webhook_token`
- **Slack**: `slack://tokenA/tokenB/tokenC/#channel`
- **Telegram**: `tgram://bottoken/ChatID`
- **SMS (Twilio)**: `twilio://SID:Token@FromPhone/ToPhone`
- **Email**: `mailto://user:pass@gmail.com`
- **Teams**: `msteams://TokenA/TokenB/TokenC`
- **Desktop**: `gnome://` (Linux), `macosx://` (macOS), `windows://` (Windows)

[See all 80+ supported services](https://github.com/caronc/apprise)

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
When log files reach `maxLogSize`, Tamga automatically:
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
