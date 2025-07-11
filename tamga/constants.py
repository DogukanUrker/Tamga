"""
Constants for Tamga logger
"""

from typing import Dict, Tuple

# Tailwind CSS color palette (color-500 values)
COLOR_PALETTE: Dict[str, Tuple[int, int, int]] = {
    "slate": (100, 116, 139),
    "gray": (107, 114, 128),
    "zinc": (113, 113, 122),
    "neutral": (115, 115, 115),
    "stone": (120, 113, 108),
    "red": (239, 68, 68),
    "orange": (249, 115, 22),
    "amber": (245, 158, 11),
    "yellow": (234, 179, 8),
    "lime": (132, 204, 2),
    "green": (34, 197, 94),
    "emerald": (16, 185, 129),
    "teal": (20, 184, 166),
    "cyan": (6, 182, 212),
    "sky": (14, 165, 233),
    "blue": (59, 130, 246),
    "indigo": (99, 102, 241),
    "violet": (139, 92, 246),
    "purple": (168, 85, 247),
    "fuchsia": (217, 70, 239),
    "pink": (236, 73, 153),
    "rose": (244, 63, 94),
}

LOG_LEVELS: Dict[str, str] = {
    "INFO": "sky",
    "WARNING": "amber",
    "ERROR": "rose",
    "SUCCESS": "emerald",
    "DEBUG": "indigo",
    "CRITICAL": "red",
    "DATABASE": "green",
    "NOTIFY": "purple",
    "METRIC": "cyan",
    "TRACE": "gray",
    "DIR": "yellow",
}

LOG_EMOJIS: Dict[str, str] = {
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
    "DIR": "📝",
}
