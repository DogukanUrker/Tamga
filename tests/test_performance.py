"""
Performance benchmarks for Tamga logger
"""

import tempfile

import pytest

from tamga import Tamga


class TestPerformance:
    """Performance benchmarks for different logging scenarios"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.mark.benchmark(group="console")
    def test_console_logging_performance(self, benchmark):
        """Benchmark console logging performance"""
        logger = Tamga(logToConsole=True, isColored=False)

        def log_messages():
            for i in range(100):
                logger.info(f"Message {i}")

        benchmark(log_messages)

    @pytest.mark.benchmark(group="console")
    def test_colored_console_performance(self, benchmark):
        """Benchmark colored console logging performance"""
        logger = Tamga(logToConsole=True, isColored=True)

        def log_messages():
            for i in range(100):
                logger.info(f"Colored message {i}")

        benchmark(log_messages)

    @pytest.mark.benchmark(group="file")
    def test_file_logging_buffered(self, benchmark, temp_dir):
        """Benchmark buffered file logging"""
        logger = Tamga(
            logToFile=True,
            logToConsole=False,
            logFile=f"{temp_dir}/perf_buffered.log",
            bufferSize=100,
        )

        def log_messages():
            for i in range(1000):
                logger.info(f"Buffered message {i}")
            logger.flush()

        benchmark(log_messages)

    @pytest.mark.benchmark(group="file")
    def test_file_logging_unbuffered(self, benchmark, temp_dir):
        """Benchmark unbuffered file logging"""
        logger = Tamga(
            logToFile=True,
            logToConsole=False,
            logFile=f"{temp_dir}/perf_unbuffered.log",
            bufferSize=1,
        )

        def log_messages():
            for i in range(100):
                logger.info(f"Unbuffered message {i}")

        benchmark(log_messages)

    @pytest.mark.benchmark(group="json")
    def test_json_logging_performance(self, benchmark, temp_dir):
        """Benchmark JSON logging performance"""
        logger = Tamga(
            logToJSON=True,
            logToConsole=False,
            logJSON=f"{temp_dir}/perf.json",
            bufferSize=50,
        )

        def log_messages():
            for i in range(500):
                logger.info(f"JSON message {i}")
            logger.flush()

        benchmark(log_messages)

    @pytest.mark.benchmark(group="sql")
    def test_sql_logging_performance(self, benchmark, temp_dir):
        """Benchmark SQLite logging performance"""
        logger = Tamga(
            logToSQL=True,
            logToConsole=False,
            logSQL=f"{temp_dir}/perf.db",
        )

        def log_messages():
            for i in range(100):
                logger.info(f"SQL message {i}")

        benchmark(log_messages)

    @pytest.mark.benchmark(group="multi")
    def test_multiple_outputs_performance(self, benchmark, temp_dir):
        """Benchmark logging to multiple outputs"""
        logger = Tamga(
            logToConsole=False,
            logToFile=True,
            logToJSON=True,
            logToSQL=True,
            logFile=f"{temp_dir}/multi.log",
            logJSON=f"{temp_dir}/multi.json",
            logSQL=f"{temp_dir}/multi.db",
            bufferSize=50,
        )

        def log_messages():
            for i in range(100):
                logger.info(f"Multi-output message {i}")
            logger.flush()

        benchmark(log_messages)

    @pytest.mark.benchmark(group="levels")
    def test_different_log_levels_performance(self, benchmark):
        """Benchmark different log levels"""
        logger = Tamga(logToConsole=False, logToFile=False)

        def log_all_levels():
            for i in range(50):
                logger.info(f"Info {i}")
                logger.warning(f"Warning {i}")
                logger.error(f"Error {i}")
                logger.debug(f"Debug {i}")
                logger.critical(f"Critical {i}")

        benchmark(log_all_levels)

    @pytest.mark.benchmark(group="buffer")
    def test_buffer_size_impact(self, benchmark, temp_dir):
        """Benchmark impact of different buffer sizes"""
        buffer_sizes = [1, 10, 50, 100, 500]

        for buffer_size in buffer_sizes:
            logger = Tamga(
                logToFile=True,
                logToConsole=False,
                logFile=f"{temp_dir}/buffer_{buffer_size}.log",
                bufferSize=buffer_size,
            )

            def log_with_buffer():
                for i in range(1000):
                    logger.info(f"Buffer test {i}")
                logger.flush()

            # Tag the benchmark with buffer size
            benchmark.extra_info["buffer_size"] = buffer_size
            benchmark(log_with_buffer)

    @pytest.mark.benchmark(group="structured")
    def test_structured_logging_performance(self, benchmark):
        """Benchmark structured logging with dir()"""
        logger = Tamga(logToConsole=False, logToFile=False)

        def log_structured():
            for i in range(100):
                logger.dir(
                    "User action",
                    user_id=f"user_{i}",
                    action="login",
                    ip=f"192.168.1.{i}",
                    timestamp=i,
                    success=i % 2 == 0,
                )

        benchmark(log_structured)
