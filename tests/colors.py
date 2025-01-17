import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
from tamga.utils.colors import Color


class ColorTests(unittest.TestCase):
    """
    Test cases for Color class functionality
    """

    def setUp(self):
        self.testMessage = "Test Message"
        self.availableColors = Color.getColorList()

    def testTextColors(self):
        """Test all available text colors"""
        for colorName in self.availableColors:
            colorCode = Color.text(colorName)
            # Test if color code is generated
            self.assertTrue(colorCode.startswith("\033[38"))
            # Test if color can be applied and reset
            coloredText = f"{colorCode}{self.testMessage}{Color.endCode}"
            self.assertTrue(coloredText.endswith(Color.endCode))

    def testBackgroundColors(self):
        """Test all available background colors"""
        for colorName in self.availableColors:
            colorCode = Color.background(colorName)
            # Test if color code is generated
            self.assertTrue(colorCode.startswith("\033[48"))
            # Test if color can be applied and reset
            coloredText = f"{colorCode}{self.testMessage}{Color.endCode}"
            self.assertTrue(coloredText.endswith(Color.endCode))

    def testInvalidColor(self):
        """Test behavior with invalid color name"""
        invalidColorName = "nonexistentColor"
        self.assertEqual(Color.text(invalidColorName), "")
        self.assertEqual(Color.background(invalidColorName), "")

    def testColorDemonstration(self):
        """Demonstrate all colors in action"""
        for colorName in self.availableColors:
            # Print text colors
            print(f"{Color.text(colorName)}Text in {colorName}{Color.endCode}")
            # Print background colors
            print(
                f"{Color.background(colorName)}Background in {colorName}{Color.endCode}"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
