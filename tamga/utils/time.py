"""
Time utilities for Tamga logger
"""

from datetime import datetime
from time import tzname

_DATE_FORMAT = "%d.%m.%y"
_TIME_FORMAT = "%H:%M:%S"


def current_date() -> str:
    """Get current date in DD.MM.YY format."""
    return datetime.now().strftime(_DATE_FORMAT)


def current_time() -> str:
    """Get current time in HH:MM:SS format."""
    return datetime.now().strftime(_TIME_FORMAT)


def current_timezone() -> str:
    """Get current timezone abbreviation."""
    return tzname[0]


def current_timestamp() -> float:
    """Get current Unix timestamp."""
    return datetime.now().timestamp()


def format_timestamp(include_timezone: bool = True) -> str:
    """
    Format complete timestamp string.

    Args:
        include_timezone: Whether to include timezone in output

    Returns:
        Formatted timestamp string
    """
    parts = [current_date(), current_time()]
    if include_timezone:
        parts.append(current_timezone())
    return " | ".join(parts)
