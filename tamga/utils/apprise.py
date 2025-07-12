"""
Modern templates for Tamga Apprise notifications
Supports HTML, Markdown, and Text formats
Uses the existing color system for different log levels
"""

from ..constants import COLOR_PALETTE, LOG_EMOJIS, LOG_LEVELS


def get_level_color(level: str) -> str:
    """Get hex color for log level using existing color system."""
    color_name = LOG_LEVELS.get(level, "purple")
    rgb = COLOR_PALETTE.get(color_name, (168, 85, 247))
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def get_level_emoji(level: str) -> str:
    """Get emoji for log level."""
    return LOG_EMOJIS.get(level, "📝")


def create_html_template(
    message: str, level: str, date: str, time: str, data: dict = None
) -> str:
    """Create modern HTML template for notifications."""
    color = get_level_color(level)
    rgb = COLOR_PALETTE.get(LOG_LEVELS.get(level, "purple"), (168, 85, 247))
    light_bg = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.1)"
    emoji = get_level_emoji(level)

    data_section = ""
    if data:
        data_rows = ""
        for key, value in data.items():
            data_rows += f"""
                <tr>
                    <td style="padding: 8px 12px; border-bottom: 1px solid #f0f0f0; font-weight: 600; color: #374151; text-align: left;">{key}</td>
                    <td style="padding: 8px 12px; border-bottom: 1px solid #f0f0f0; color: #6b7280; text-align: left;">{value}</td>
                </tr>
            """

        data_section = f"""
            <!-- Structured Data -->
            <div style="padding: 0 28px 24px 28px;">
                <h3 style="margin: 0 0 16px 0; color: #374151; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
                    📊 Data
                </h3>
                <table style="width: 100%; border-collapse: collapse; border-radius: 8px; overflow: hidden; border: 1px solid #e5e7eb;">
                    {data_rows}
                </table>
            </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{emoji} Tamga - {level} Notification</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
        <div style="background-color: #f5f5f5; padding: 40px 20px;">
            <div style="max-width: 560px; margin: 0 auto;">

                <!-- Card -->
                <div style="border: 1px solid #e5e5e5; border-radius: 12px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04); overflow: hidden;">

                    <!-- Header with light background -->
                    <div style="padding: 24px 28px; background: {light_bg}; border-bottom: 1px solid #e5e5e5;">
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td>
                                    <span style="color: {color}; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
                                        ● {level}
                                    </span>
                                </td>
                                <td align="right">
                                    <span style="color: #525252; font-size: 13px; font-weight: 500;">
                                        {date} • {time}
                                    </span>
                                </td>
                            </tr>
                        </table>
                    </div>

                    <!-- Body -->
                    <div style="padding: 32px 28px;">
                        <p style="margin: 0; color: #000000; font-size: 18px; line-height: 1.6; font-weight: 500; text-align: center;">
                            {message}
                        </p>
                    </div>

                    {data_section}

                    <!-- Footer -->
                    <div style="padding: 20px 28px; border-top: 1px solid #f0f0f0; background: #fafafa;">
                        <p style="margin: 0; text-align: center; color: #737373; font-size: 13px;">
                            Powered by <a href="https://tamga.vercel.app" style="color: {color}; text-decoration: none; font-weight: 600;">Tamga</a>
                        </p>
                    </div>

                </div>

            </div>
        </div>
    </body>
    </html>
    """.strip()


def create_markdown_template(
    message: str, level: str, date: str, time: str, data: dict = None
) -> str:
    """Create markdown template for notifications."""
    emoji = get_level_emoji(level)

    data_section = ""
    if data:
        data_section = "\n\n**📊 Data:**\n"
        for key, value in data.items():
            data_section += f"- **{key}:** `{value}`\n"

    return f"""## {emoji} {level} Notification

**Message:** {message}
{data_section}
---
**Date:** {date}
**Time:** {time}

*Powered by [Tamga Logger](https://tamga.vercel.app)*"""


def create_text_template(
    message: str, level: str, date: str, time: str, data: dict = None
) -> str:
    """Create plain text template for notifications."""
    emoji = get_level_emoji(level)

    data_section = ""
    if data:
        data_section = "\n\n📊 DATA:\n"
        for key, value in data.items():
            data_section += f"  {key}: {value}\n"

    return f"""
{emoji} {level} NOTIFICATION

{message}
{data_section}
{date} • {time}
""".strip()


def format_notification(
    message: str,
    level: str,
    date: str,
    time: str,
    format_type: str = "text",
    data: dict = None,
) -> str:
    """
    Format notification message based on the specified format type.

    Args:
        message: The log message
        level: The log level
        date: The date string
        time: The time string
        format_type: The format type ('html', 'markdown', or 'text')
        data: Optional structured data dictionary

    Returns:
        Formatted message string
    """
    format_type = format_type.lower()

    if format_type == "html":
        return create_html_template(message, level, date, time, data)
    elif format_type == "markdown":
        return create_markdown_template(message, level, date, time, data)
    else:
        return create_text_template(message, level, date, time, data)
