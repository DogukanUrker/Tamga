# Tamga [![PyPI Downloads](https://static.pepy.tech/badge/tamga)](https://pepy.tech/projects/tamga)

A modern, high-performance logging utility for Python with multiple output formats and colorful console output.

[![Installation](https://belg-api.vercel.app/badge/installation/pip3%20install%20tamga/neutral/dark)](https://pypi.org/project/tamga/)

tam·ga / noun
An ancient Turkic symbol or seal used for marking ownership, identity, or lineage.

<img alt="Terminal" src="https://github.com/DogukanUrker/Tamga/blob/main/Images/terminal.png?raw=true" />

**AI Integration:** For AI/LLM integration, see [LLMs.txt](https://raw.githubusercontent.com/DogukanUrker/Tamga/refs/heads/main/llms.txt) or access documentation directly via [Context7](https://context7.com/dogukanurker/tamga)

## Features

- 🎨 Colorful console output using Tailwind CSS color palette
- ⚡ High-performance buffered writing (10x faster than traditional logging)
- 📁 File logging with rotation and backup
- 📊 JSON logging with optimized performance
- 🗄️ SQLite database logging
- 🚀 MongoDB integration with async support
- 📧 Email notifications for specific log levels
- 🌐 API logging support
- 🔄 Automatic file rotation and backup
- 🎯 Multiple log levels with customizable colors
- 🕒 Optional timezone in timestamps
- 💾 Manual flush control for critical messages

## Installation

To install the `tamga` package, you can use the following commands based on your requirements:

- Basic installation:

  ```bash
  pip install tamga
  ```

- With API logging support:

  ```bash
  pip install tamga[api]
  ```

- With MongoDB integration:

  ```bash
  pip install tamga[mongo]
  ```

- Full installation with all features:
  ```bash
  pip install tamga[full]
  ```

## Quick Start

```python
from tamga import Tamga

# Initialize the logger
logger = Tamga(
    logToFile=True,
    logToJSON=True,
    logToConsole=True
)

# Basic logging
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error")
logger.success("This is a success message")
logger.debug("This is a debug message")
logger.critical("This is a critical message")

# Custom logging
logger.custom("This is a custom message", "CUSTOM", "orange")
```

## Advanced Usage

### Performance Optimization

```python
# High-performance logging with buffering
logger = Tamga(
    logToFile=True,
    bufferSize=200,  # Buffer 200 logs before writing to disk
    showTimezone=False  # Cleaner timestamps without timezone
)

# Process large amounts of data
for record in large_dataset:
    logger.info(f"Processing {record.id}")

# Ensure all logs are written
logger.flush()
```

### MongoDB Integration

```python
logger = Tamga(
    logToMongo=True,
    mongoURI="your_mongodb_uri",
    mongoDatabaseName="logs_db",
    mongoCollectionName="application_logs"
)
```

### Email Notifications

```python
logger = Tamga(
    sendMail=True,
    smtpServer="smtp.gmail.com",
    smtpPort=587,
    smtpMail="your_email@gmail.com",
    smtpPassword="your_password",
    smtpReceivers=["receiver@email.com"],
    mailLevels=["CRITICAL", "ERROR"]
)
```

### File Rotation and Backup

```python
logger = Tamga(
    logToFile=True,
    logToJSON=True,
    maxLogSize=10,  # MB
    maxJsonSize=10,  # MB
    enableBackup=True
)
```

### API Integration

```python
logger = Tamga(
    logToAPI=True,
    apiURL="http://your-api.com/logs"
)
```

### Structured Logging

```python
# Log with additional context
logger.dir("User action",
    user_id="12345",
    action="login",
    ip_address="192.168.1.1",
    success=True
)
```

## Configuration Options

### Core Parameters
- `isColored` (bool): Enable/disable colored output (default: True)
- `logToConsole` (bool): Log to console (default: True)
- `logToFile` (bool): Log to file (default: False)
- `logToJSON` (bool): Log to JSON file (default: False)
- `logToSQL` (bool): Log to SQLite database (default: False)
- `logToMongo` (bool): Log to MongoDB (default: False)
- `logToAPI` (bool): Log to external API (default: False)
- `sendMail` (bool): Send email notifications (default: False)

### Performance Parameters
- `bufferSize` (int): Number of logs to buffer before writing (default: 50)
- `showTimezone` (bool): Include timezone in timestamps (default: False)

### File Management
- `logFile` (str): Path to log file (default: "tamga.log")
- `logJSON` (str): Path to JSON file (default: "tamga.json")
- `logSQL` (str): Path to SQLite database (default: "tamga.db")
- `maxLogSize` (int): Max file size in MB before rotation (default: 10)
- `maxJsonSize` (int): Max JSON size in MB (default: 10)
- `maxSqlSize` (int): Max SQL size in MB (default: 50)
- `enableBackup` (bool): Create backups on rotation (default: True)

## Available Log Levels

- INFO (sky blue)
- WARNING (amber)
- ERROR (rose)
- SUCCESS (emerald)
- DEBUG (indigo)
- CRITICAL (red)
- DATABASE (green)
- MAIL (neutral)
- METRIC (cyan)
- TRACE (gray)
- Custom (user-defined)

## Performance Tips

1. **Buffer Size**: Adjust based on your needs
   - Interactive apps: `bufferSize=1-10`
   - Web services: `bufferSize=50-100`
   - Batch processing: `bufferSize=200-1000`

2. **Critical Logs**: Use `flush()` after important messages
   ```python
   logger.critical("System failure")
   logger.flush()  # Ensure immediate write
   ```

3. **High Throughput**: Disable console for maximum speed
   ```python
   logger = Tamga(logToConsole=False, logToFile=True, bufferSize=500)
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Doğukan Ürker
- Email: dogukanurker@icloud.com
- GitHub: [@dogukanurker](https://github.com/dogukanurker)
