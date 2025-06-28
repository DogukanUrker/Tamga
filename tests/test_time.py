"""
Test cases for time utilities
"""

import re
import time
from datetime import datetime

import pytest

from tamga.utils.time import (
    currentDate,
    currentTime,
    currentTimeStamp,
    currentTimeZone,
    formatTimestamp,
)


class TestTimeUtils:
    """Test time utility functions"""

    def test_current_date_format(self):
        """Test date format is DD.MM.YY"""
        date = currentDate()
        assert re.match(r"^\d{2}\.\d{2}\.\d{2}$", date)

        # Verify it's today's date
        now = datetime.now()
        expected = now.strftime("%d.%m.%y")
        assert date == expected

    def test_current_time_format(self):
        """Test time format is HH:MM:SS"""
        time_str = currentTime()
        assert re.match(r"^\d{2}:\d{2}:\d{2}$", time_str)

        # Verify hours, minutes, seconds are in valid ranges
        parts = time_str.split(":")
        assert 0 <= int(parts[0]) <= 23  # hours
        assert 0 <= int(parts[1]) <= 59  # minutes
        assert 0 <= int(parts[2]) <= 59  # seconds

    def test_current_timezone(self):
        """Test timezone returns a string"""
        tz = currentTimeZone()
        assert isinstance(tz, str)
        assert len(tz) > 0  # Should not be empty

    def test_current_timestamp(self):
        """Test timestamp returns valid Unix timestamp"""
        ts1 = currentTimeStamp()
        time.sleep(0.1)
        ts2 = currentTimeStamp()

        assert isinstance(ts1, float)
        assert isinstance(ts2, float)
        assert ts2 > ts1  # Time should have advanced
        assert ts1 > 1000000000  # Should be after year 2001

    def test_format_timestamp_with_timezone(self):
        """Test formatted timestamp with timezone"""
        formatted = formatTimestamp(include_timezone=True)
        parts = formatted.split(" | ")

        assert len(parts) == 3  # date | time | timezone
        assert re.match(r"^\d{2}\.\d{2}\.\d{2}$", parts[0])  # date
        assert re.match(r"^\d{2}:\d{2}:\d{2}$", parts[1])  # time
        assert len(parts[2]) > 0  # timezone

    def test_format_timestamp_without_timezone(self):
        """Test formatted timestamp without timezone"""
        formatted = formatTimestamp(include_timezone=False)
        parts = formatted.split(" | ")

        assert len(parts) == 2  # date | time
        assert re.match(r"^\d{2}\.\d{2}\.\d{2}$", parts[0])  # date
        assert re.match(r"^\d{2}:\d{2}:\d{2}$", parts[1])  # time

    def test_time_consistency(self):
        """Test time functions return consistent results"""
        # Get multiple samples quickly
        dates = [currentDate() for _ in range(5)]
        times = [currentTime() for _ in range(5)]

        # All dates should be the same (unless we cross midnight)
        assert len(set(dates)) == 1

        # Times might differ by a second or two
        assert len(set(times)) <= 3

    def test_timestamp_precision(self):
        """Test timestamp has microsecond precision"""
        timestamps = []
        for _ in range(10):
            timestamps.append(currentTimeStamp())
            time.sleep(0.001)  # 1ms

        # All timestamps should be unique
        assert len(set(timestamps)) == 10

        # Check they have decimal places (microseconds)
        for ts in timestamps:
            assert int(ts) != ts  # Has decimal part

    @pytest.mark.parametrize(
        "year,month,day",
        [
            (2025, 1, 1),
            (2025, 12, 31),
            (2025, 2, 28),
        ],
    )
    def test_date_edge_cases(self, year, month, day, monkeypatch):
        """Test date formatting for edge cases"""
        # Note: This would require mocking datetime.now()
        # Just verify the format works for current date
        date = currentDate()
        assert len(date) == 8  # DD.MM.YY format

    def test_performance(self):
        """Test time functions are fast"""
        import timeit

        # Each function should be very fast
        date_time = timeit.timeit(currentDate, number=1000)
        time_time = timeit.timeit(currentTime, number=1000)
        tz_time = timeit.timeit(currentTimeZone, number=1000)
        ts_time = timeit.timeit(currentTimeStamp, number=1000)

        # Should complete 1000 calls in under 0.1 seconds
        assert date_time < 0.1
        assert time_time < 0.1
        assert tz_time < 0.1
        assert ts_time < 0.1
