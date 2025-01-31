# Tamga [![PyPI Downloads](https://static.pepy.tech/badge/tamga)](https://pepy.tech/projects/tamga)

A modern, logging utility for Python with multiple output formats and colorful console output.    

tam·ga / noun      
An ancient Turkic symbol or seal used for marking ownership, identity, or lineage.

<img alt="Terminal" src="https://github.com/DogukanUrker/Tamga/blob/main/Images/terminal.png?raw=true" />


## Features

- 🎨 Colorful console output using Tailwind CSS color palette
- 📁 File logging with rotation and backup
- 📊 JSON logging with size limits and backup
- 🗄️ SQLite database logging
- 🚀 MongoDB integration
- 📧 Email notifications for specific log levels
- 🌐 API logging support
- 🔄 Automatic file rotation and backup
- 🎯 Multiple log levels with customizable colors

## Installation

```bash
pip install tamga
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Doğukan Ürker
- Email: dogukanurker@icloud.com
- GitHub: [@dogukanurker](https://github.com/dogukanurker) 
