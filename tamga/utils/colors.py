from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..constants import COLOR_PALLETTE


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

    __colorPalette: dict = COLOR_PALLETTE

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
    def style(cls, styleName: str) -> str:
        """
        Get text style ANSI code
        """
        styleCodes = {
            "bold": "\033[1m",
            "italic": "\033[3m",
            "underline": "\033[4m",
            "strikethrough": "\033[9m",
        }
        return styleCodes.get(styleName, "")

    @classmethod
    def getColorList(cls) -> list[str]:
        """
        Get list of all available color names
        """
        return list(cls.__colorPalette.keys())
