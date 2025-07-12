"""
Modern templates for Tamga Apprise notifications
Supports HTML, Markdown, and Text formats
Uses the existing color system for different log levels
"""

import re
from typing import Dict, Tuple

from ..constants import COLOR_PALETTE, LOG_EMOJIS, LOG_LEVELS


def get_level_color(level: str) -> str:
    """Get hex color for log level using existing color system."""
    color_name = LOG_LEVELS.get(level, "purple")
    rgb = COLOR_PALETTE.get(color_name, (168, 85, 247))
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def get_level_emoji(level: str) -> str:
    """Get emoji for log level."""
    return LOG_EMOJIS.get(level, "📝")


def parse_message_with_data(message: str) -> Tuple[str, Dict[str, str]]:
    """
    Parse message to extract base message and key-value data.

    Args:
        message: Message that may contain key-value data (e.g., "User login | user_id=123, action='login'")

    Returns:
        Tuple of (base_message, key_value_dict)
    """
    if " | " not in message:
        return message, {}

    parts = message.split(" | ", 1)
    base_message = parts[0]
    data_part = parts[1]

    data_dict = {}
    pattern = r"(\w+)=([^,]+?)(?=,\s*\w+=|$)"
    matches = re.findall(pattern, data_part)

    for key, value in matches:
        value = value.strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')):
            value = value[1:-1]
        data_dict[key] = value

    return base_message, data_dict


def create_html_template(message: str, level: str, date: str, time: str) -> str:
    """Create modern HTML template for notifications."""
    color = get_level_color(level)
    rgb = COLOR_PALETTE.get(LOG_LEVELS.get(level, "purple"), (168, 85, 247))
    light_bg = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.1)"
    emoji = get_level_emoji(level)

    base_message, data = parse_message_with_data(message)

    data_rows = ""
    if data:
        data_rows = """
                    <!-- Data Section -->
                    <div style="padding: 0 28px 32px 28px;">
                        <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; border-left: 4px solid {color};">
                            <div style="margin-bottom: 12px;">
                                <span style="color: #6b7280; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                                    Additional Data
                                </span>
                            </div>
                            <div style="display: grid; gap: 8px;">
                                {data_items}
                            </div>
                        </div>
                    </div>""".format(
            color=color,
            data_items="".join(
                [
                    f"""
                                <div style="display: flex; justify-content: space-between; padding: 6px 0;">
                                    <span style="color: #374151; font-size: 14px; font-weight: 500;">{key}:</span>
                                    <span style="color: #6b7280; font-size: 14px; font-family: 'SF Mono', 'Monaco', monospace;">{value}</span>
                                </div>"""
                    for key, value in data.items()
                ]
            ),
        )

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
                            {base_message}
                        </p>
                    </div>

                    {data_rows}

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


def create_markdown_template(message: str, level: str, date: str, time: str) -> str:
    """Create markdown template for notifications."""
    emoji = get_level_emoji(level)

    base_message, data = parse_message_with_data(message)

    data_section = ""
    if data:
        data_section = "\n\n### 📊 Additional Data\n\n"
        data_section += "| Key | Value |\n|-----|-------|\n"
        for key, value in data.items():
            data_section += f"| **{key}** | `{value}` |\n"

    return f"""## {emoji} {level} Notification

**Message:** {base_message}
{data_section}
---
**Date:** {date}
**Time:** {time}

*Powered by [Tamga Logger](https://tamga.vercel.app)*"""


def create_text_template(message: str, level: str, date: str, time: str) -> str:
    """Create plain text template for notifications."""
    emoji = get_level_emoji(level)

    base_message, data = parse_message_with_data(message)

    data_section = ""
    if data:
        data_section = "\n\n📊 ADDITIONAL DATA:\n"
        data_section += "-" * 40 + "\n"
        max_key_length = max(len(key) for key in data.keys()) if data else 0
        for key, value in data.items():
            data_section += f"{key.ljust(max_key_length)} : {value}\n"

    return f"""
{emoji} {level} NOTIFICATION

{base_message}
{data_section}
{date} • {time}
"""


def format_notification(
    message: str, level: str, date: str, time: str, format_type: str = "text"
) -> str:
    """
    Format notification message based on the specified format type.

    Args:
        message: The log message (may contain key-value data)
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
