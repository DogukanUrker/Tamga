from typing import Optional
from dataclasses import dataclass
from enum import Enum


class ColorType(Enum):
    TEXT = "text"
    BACKGROUND = "background"


@dataclass
class ColorCode:
    """
    Dataclass to store ANSI color codes for text and background using Tailwind CSS colors (color-500)
    """

    colorCode: str
    colorType: ColorType


class Color:
    """
    Modern implementation of Color class for terminal text and background colors
    using Tailwind CSS color palette (color-500)
    """

    endCode: str = "\033[0m"

    # Color codes dictionary using RGB values
    __colorPalette: dict = {
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

    @classmethod
    def __generateColorCode(
        cls, colorName: str, colorType: ColorType
    ) -> Optional[ColorCode]:
        """
        Private method to generate ANSI color code
        """
        if colorName not in cls.__colorPalette:
            return None

        rgbValues = cls.__colorPalette[colorName]
        prefixCode = "38" if colorType == ColorType.TEXT else "48"
        return ColorCode(
            f"\033[{prefixCode};2;{rgbValues[0]};{rgbValues[1]};{rgbValues[2]}m",
            colorType,
        )

    @classmethod
    def text(cls, colorName: str) -> str:
        """
        Get text color ANSI code
        """
        colorCode = cls.__generateColorCode(colorName, ColorType.TEXT)
        return colorCode.colorCode if colorCode else ""

    @classmethod
    def background(cls, colorName: str) -> str:
        """
        Get background color ANSI code
        """
        colorCode = cls.__generateColorCode(colorName, ColorType.BACKGROUND)
        return colorCode.colorCode if colorCode else ""

    @classmethod
    def getColorList(cls) -> list[str]:
        """
        Get list of all available color names
        """
        return list(cls.__colorPalette.keys())
