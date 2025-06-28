"""
Test cases for Color utilities
"""

import pytest

from tamga.utils.colors import Color


class TestColors:
    """Test color functionality"""

    def test_all_text_colors(self):
        """Test all available text colors generate valid codes"""
        for color_name in Color.get_color_list():
            color_code = Color.text(color_name)
            assert color_code.startswith("\033[38;2;")
            assert color_code.endswith("m")
            assert len(color_code) > 10

    def test_all_background_colors(self):
        """Test all available background colors generate valid codes"""
        for color_name in Color.get_color_list():
            color_code = Color.background(color_name)
            assert color_code.startswith("\033[48;2;")
            assert color_code.endswith("m")
            assert len(color_code) > 10

    def test_invalid_color_returns_empty(self):
        """Test invalid color names return empty string"""
        assert Color.text("nonexistent") == ""
        assert Color.background("invalid_color") == ""
        assert Color.text("") == ""
        assert Color.background(None) == ""

    def test_color_support_check(self):
        """Test color support checking"""
        assert Color.is_color_supported("red") == True  # noqa E712
        assert Color.is_color_supported("blue") == True  # noqa E712
        assert Color.is_color_supported("invalid") == False  # noqa E712
        assert Color.is_color_supported("") == False  # noqa E712

    def test_style_codes(self):
        """Test text style codes"""
        assert Color.style("bold") == "\033[1m"
        assert Color.style("italic") == "\033[3m"
        assert Color.style("underline") == "\033[4m"
        assert Color.style("strikethrough") == "\033[9m"
        assert Color.style("invalid") == ""

    def test_end_code(self):
        """Test reset/end code"""
        assert Color.endCode == "\033[0m"

    def test_color_list_completeness(self):
        """Test color list contains expected colors"""
        colors = Color.get_color_list()
        assert len(colors) > 20  # Should have many colors

        # Check some expected colors exist
        expected_colors = [
            "red",
            "blue",
            "green",
            "yellow",
            "purple",
            "orange",
            "pink",
            "gray",
            "cyan",
            "indigo",
        ]
        for color in expected_colors:
            assert color in colors

    def test_color_consistency(self):
        """Test color codes are consistent"""
        # Same color should always return same code
        red1 = Color.text("red")
        red2 = Color.text("red")
        assert red1 == red2

        bg_blue1 = Color.background("blue")
        bg_blue2 = Color.background("blue")
        assert bg_blue1 == bg_blue2

    def test_color_rgb_values(self):
        """Test specific color RGB values"""
        # Test a few known colors
        red_text = Color.text("red")
        assert "239;68;68" in red_text  # RGB for red-500

        blue_text = Color.text("blue")
        assert "59;130;246" in blue_text  # RGB for blue-500

    @pytest.mark.parametrize(
        "color,expected_rgb",
        [
            ("red", "239;68;68"),
            ("green", "34;197;94"),
            ("blue", "59;130;246"),
            ("yellow", "234;179;8"),
            ("purple", "168;85;247"),
        ],
    )
    def test_specific_color_values(self, color, expected_rgb):
        """Test specific color RGB values match expected"""
        color_code = Color.text(color)
        assert expected_rgb in color_code

    def test_combined_styling(self):
        """Test combining colors and styles"""
        test_text = "Hello World"

        # Bold red text
        styled = f"{Color.style('bold')}{Color.text('red')}{test_text}{Color.endCode}"
        assert styled.startswith("\033[1m\033[38;2;")
        assert styled.endswith(f"{test_text}\033[0m")

        # Blue background with white text
        styled = (
            f"{Color.background('blue')}{Color.text('gray')}{test_text}{Color.endCode}"
        )
        assert "\033[48;2;" in styled
        assert "\033[38;2;" in styled

    def test_visual_output(self, capsys):
        """Test visual output of colors (for manual verification)"""
        print("\n\nColor Palette Test:")
        print("=" * 50)

        for color in Color.get_color_list():
            # Text color
            print(f"{Color.text(color)}■■■ {color:<12}{Color.endCode} ", end="")
            # Background color
            print(f"{Color.background(color)}   {Color.endCode}")

        print("\nStyle Tests:")
        print(f"{Color.style('bold')}Bold text{Color.endCode}")
        print(f"{Color.style('italic')}Italic text{Color.endCode}")
        print(f"{Color.style('underline')}Underlined text{Color.endCode}")
        print(f"{Color.style('strikethrough')}Strikethrough text{Color.endCode}")

        # This test is mainly for visual verification
        captured = capsys.readouterr()
        assert "Color Palette Test:" in captured.out
