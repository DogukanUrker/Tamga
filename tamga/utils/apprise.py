"""
Modern templates for Tamga Apprise notifications
Supports HTML, Markdown, and Text formats
Uses the existing color system for different log levels
"""

from ..constants import COLOR_PALLETTE, LOG_LEVELS


def get_level_color(level: str) -> str:
    """Get hex color for log level using existing color system."""
    color_name = LOG_LEVELS.get(level, "indigo")
    rgb = COLOR_PALLETTE.get(color_name, (99, 102, 241))
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def create_html_template(message: str, level: str, date: str, time: str) -> str:
    """Create modern HTML template for notifications."""
    color = get_level_color(level)
    rgb = COLOR_PALLETTE.get(LOG_LEVELS.get(level, "indigo"), (99, 102, 241))
    light_bg = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.1)"

    return f"""
<div style="max-width: 600px; margin: 0 auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">

    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); padding: 24px; text-align: center;">
        <h1 style="margin: 0; color: white; font-size: 20px; font-weight: 600; letter-spacing: 0.5px;">
            {level} NOTIFICATION
        </h1>
    </div>

    <div style="padding: 32px 24px;">
        <div style="background: {light_bg}; border-left: 4px solid {color}; padding: 20px; border-radius: 8px; margin-bottom: 24px;">
            <p style="margin: 0; font-size: 16px; line-height: 1.6; color: #2d3748; font-weight: 500;">
                {message}
            </p>
        </div>

        <div style="border-top: 1px solid #e2e8f0; padding-top: 16px; text-align: center;">
            <span style="color: #718096; font-size: 14px; font-weight: 600;">
                {date} | {time}
            </span>
        </div>
    </div>

    <div style="background: #f8fafc; padding: 16px 24px; text-align: center; border-top: 1px solid #e2e8f0;">
        <p style="margin: 0; color: #a0aec0; font-size: 12px;">
            Powered by <a href="https://tamga.vercel.app" style="font-weight: 600; color: {color}; text-decoration: none;">Tamga Logger</a>
        </p>
    </div>

</div>
    """.strip()


def create_markdown_template(message: str, level: str, date: str, time: str) -> str:
    """Create markdown template for notifications."""
    level_emoji = {
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "SUCCESS": "✅",
        "DEBUG": "🐛",
        "CRITICAL": "🚨",
        "DATABASE": "🗄️",
        "NOTIFY": "📢",
        "METRIC": "📊",
        "TRACE": "🔍",
    }

    emoji = level_emoji.get(level, "📝")

    return f"""## {emoji} {level} Notification

**Message:** {message}

---
**Date:** {date}
**Time:** {time}

*Powered by [Tamga Logger](https://tamga.vercel.app)*"""


def create_text_template(message: str, level: str, date: str, time: str) -> str:
    """Create plain text template for notifications."""
    # Shorter border for better compatibility with notification systems
    border = "=" * 25

    return f"""{border}
{level} NOTIFICATION
{border}

{message}

{date} | {time}
{border}"""


def format_notification(
    message: str, level: str, date: str, time: str, format_type: str = "text"
) -> str:
    """
    Format notification message based on the specified format type.

    Args:
        message: The log message
        level: The log level
        date: The date string
        time: The time string
        format_type: The format type ('html', 'markdown', or 'text')

    Returns:
        Formatted message string
    """
    format_type = format_type.lower()

    if format_type == "html":
        return create_html_template(message, level, date, time)
    elif format_type == "markdown":
        return create_markdown_template(message, level, date, time)
    else:
        return create_text_template(message, level, date, time)
