"""
Color utilities for Tamga logger using Tailwind CSS palette
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from ..constants import COLOR_PALETTE


class ColorType(Enum):
    """ANSI color type enumeration."""

    TEXT = "text"
    BACKGROUND = "background"


@dataclass(frozen=True)
class ColorCode:
    """
    Immutable dataclass to store ANSI color codes.
    """

    code: str
    color_type: ColorType


class Color:
    """
    Terminal color handler using Tailwind CSS color palette.
    Provides methods for text colors, background colors, and text styles.
    """

    end_code: str = "\033[0m"

    _color_palette: Dict[str, Tuple[int, int, int]] = COLOR_PALETTE

    _style_codes: Dict[str, str] = {
        "bold": "\033[1m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "strikethrough": "\033[9m",
    }

    @classmethod
    def _generate_color_code(
        cls, color_name: str, color_type: ColorType
    ) -> Optional[ColorCode]:
        """
        Generate ANSI color code for given color name and type.

        Args:
            color_name: Name of the color from palette
            color_type: Type of color (text or background)

        Returns:
            ColorCode object or None if color not found
        """
        rgb_values = cls._color_palette.get(color_name)
        if not rgb_values:
            return None

        prefix = "38" if color_type == ColorType.TEXT else "48"
        r, g, b = rgb_values
        code = f"\033[{prefix};2;{r};{g};{b}m"

        return ColorCode(code, color_type)

    @classmethod
    def text(cls, color_name: str) -> str:
        """
        Get ANSI code for text color.

        Args:
            color_name: Name of the color

        Returns:
            ANSI escape code string, empty if color not found
        """
        color_code = cls._generate_color_code(color_name, ColorType.TEXT)
        return color_code.code if color_code else ""

    @classmethod
    def background(cls, color_name: str) -> str:
        """
        Get ANSI code for background color.

        Args:
            color_name: Name of the color

        Returns:
            ANSI escape code string, empty if color not found
        """
        color_code = cls._generate_color_code(color_name, ColorType.BACKGROUND)
        return color_code.code if color_code else ""

    @classmethod
    def style(cls, style_name: str) -> str:
        """
        Get ANSI code for text style.

        Args:
            style_name: Name of the style (bold, italic, underline, strikethrough)

        Returns:
            ANSI escape code string, empty if style not found
        """
        return cls._style_codes.get(style_name, "")

    @classmethod
    def get_color_list(cls) -> List[str]:
        """
        Get list of all available color names.

        Returns:
            List of color names
        """
        return list(cls._color_palette.keys())

    @classmethod
    def is_color_supported(cls, color_name: str) -> bool:
        """
        Check if a color name is supported.

        Args:
            color_name: Name of the color to check

        Returns:
            True if color is supported, False otherwise
        """
        return color_name in cls._color_palette
