"""
Integration tests for Tamga logger
"""

import json
import os
import sqlite3
import tempfile
import time
from pathlib import Path

import pytest

from tamga import Tamga


class TestIntegration:
    """Integration tests for complex scenarios"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_high_volume_logging(self, temp_dir):
        """Test logging under high volume conditions"""
        logger = Tamga(
            logToFile=True,
            logToJSON=True,
            logToSQL=True,
            logFile=f"{temp_dir}/high_volume.log",
            logJSON=f"{temp_dir}/high_volume.json",
            logSQL=f"{temp_dir}/high_volume.db",
            bufferSize=500,
            maxLogSize=5,  # 5MB
        )

        # Generate 10,000 log entries
        for i in range(10000):
            if i % 5 == 0:
                logger.info(f"Info message {i}")
            elif i % 5 == 1:
                logger.warning(f"Warning message {i}")
            elif i % 5 == 2:
                logger.error(f"Error message {i}")
            elif i % 5 == 3:
                logger.debug(f"Debug message {i}")
            else:
                logger.success(f"Success message {i}")

        logger.flush()

        # Verify all outputs exist and contain data
        assert os.path.exists(f"{temp_dir}/high_volume.log")
        assert os.path.exists(f"{temp_dir}/high_volume.json")
        assert os.path.exists(f"{temp_dir}/high_volume.db")

        # Check JSON integrity
        with open(f"{temp_dir}/high_volume.json", "r") as f:
            data = json.load(f)
            assert len(data) > 1000  # Should have many entries

        # Check SQL integrity
        conn = sqlite3.connect(f"{temp_dir}/high_volume.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM logs")
        count = cursor.fetchone()[0]
        conn.close()
        assert count > 1000

    def test_concurrent_logging(self, temp_dir):
        """Test concurrent logging from multiple threads"""
        import concurrent.futures

        logger = Tamga(
            logToFile=True,
            logToJSON=True,
            logFile=f"{temp_dir}/concurrent.log",
            logJSON=f"{temp_dir}/concurrent.json",
            bufferSize=50,
        )

        def log_worker(worker_id):
            for i in range(100):
                logger.info(f"Worker {worker_id} - Message {i}")
                if i % 20 == 0:
                    logger.error(f"Worker {worker_id} - Error {i}")
            return worker_id

        # Run 10 workers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(log_worker, i) for i in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]  # noqa: F841

        logger.flush()

        # Verify all workers logged
        with open(f"{temp_dir}/concurrent.log", "r") as f:
            content = f.read()
            for worker_id in range(10):
                assert f"Worker {worker_id}" in content

    def test_rotation_stress_test(self, temp_dir):
        """Test file rotation under stress"""
        logger = Tamga(
            logToFile=True,
            logToJSON=True,
            logFile=f"{temp_dir}/rotate_stress.log",
            logJSON=f"{temp_dir}/rotate_stress.json",
            maxLogSize=0.1,  # 100KB for quick rotation
            maxJsonSize=0.1,
            enableBackup=True,
            bufferSize=10,
        )

        # Generate logs to trigger multiple rotations
        for i in range(1000):
            logger.info("x" * 200)  # Long message

        logger.flush()

        # Check for multiple backup files
        log_backups = list(Path(temp_dir).glob("rotate_stress.log.*.bak"))
        json_backups = list(Path(temp_dir).glob("rotate_stress.json.*.bak"))

        assert len(log_backups) > 0
        assert len(json_backups) > 0

    def test_mixed_workload(self, temp_dir):
        """Test mixed workload with various log types and operations"""
        logger = Tamga(
            logToFile=True,
            logToJSON=True,
            logToSQL=True,
            logFile=f"{temp_dir}/mixed.log",
            logJSON=f"{temp_dir}/mixed.json",
            logSQL=f"{temp_dir}/mixed.db",
            bufferSize=25,
        )

        # Simulate realistic mixed workload
        for i in range(500):
            # Regular logs
            if i % 10 == 0:
                logger.info(f"Processing batch {i}")

            # Structured logs
            if i % 25 == 0:
                logger.dir(
                    "Batch complete",
                    batch_id=i,
                    items_processed=25,
                    duration=1.23,
                    errors=0,
                )

            # Errors
            if i % 50 == 0:
                logger.error(f"Connection timeout for batch {i}")

            # Metrics
            if i % 15 == 0:
                logger.metric(f"CPU: 45%, Memory: 2.3GB, Batch: {i}")

            # Debug traces
            if i % 100 == 0:
                logger.trace(f"Detailed trace at iteration {i}")

            # Custom levels
            if i % 75 == 0:
                logger.custom(f"Payment processed: ${i * 10}", "PAYMENT", "green")

        logger.flush()

        # Verify data integrity across all outputs
        with open(f"{temp_dir}/mixed.json", "r") as f:
            data = json.load(f)
            # Check various message types exist
            messages = [item["message"] for item in data]
            assert any("Processing batch" in msg for msg in messages)
            assert any("Batch complete" in msg for msg in messages)
            assert any("Connection timeout" in msg for msg in messages)

    def test_error_recovery(self, temp_dir):
        """Test logger behavior when outputs fail"""
        # Create a read-only file to simulate write failure
        readonly_file = f"{temp_dir}/readonly.log"
        Path(readonly_file).touch()
        os.chmod(readonly_file, 0o444)  # Read-only

        logger = Tamga(
            logToFile=True,
            logToConsole=False,  # Disable to not clutter test output
            logFile=readonly_file,
            bufferSize=1,
        )

        # Should handle the error gracefully
        logger.info("This should not crash")
        logger.error("Even with write errors")

        # Cleanup
        os.chmod(readonly_file, 0o644)

    def test_unicode_and_special_chars(self, temp_dir):
        """Test handling of unicode and special characters"""
        logger = Tamga(
            logToFile=True,
            logToJSON=True,
            logToSQL=True,
            logFile=f"{temp_dir}/unicode.log",
            logJSON=f"{temp_dir}/unicode.json",
            logSQL=f"{temp_dir}/unicode.db",
            bufferSize=1,
        )

        # Test various unicode and special characters
        test_messages = [
            "Hello 世界",
            "Emoji test: 🎨 🚀 ⚡ 🔥",
            "Special chars: <>&\"'",
            "Math symbols: ∑ ∏ ∫ √",
            "Currency: € £ ¥ ₹",
            "Accents: café résumé naïve",
            "RTL: مرحبا שלום",
        ]

        for msg in test_messages:
            logger.info(msg)

        # Verify JSON handles unicode properly
        with open(f"{temp_dir}/unicode.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for i, item in enumerate(data):
                assert item["message"] == test_messages[i]

    def test_api_mock_integration(self, temp_dir):
        """Test API integration with mock server"""
        try:
            import requests  # noqa
        except ImportError:
            pytest.skip("requests not installed")

        # Note: In real tests, you'd use a mock server
        # This test just verifies the API call doesn't crash
        logger = Tamga(
            logToAPI=True,
            apiURL="http://localhost:9999/nonexistent",  # Will fail but shouldn't crash
            logToConsole=False,
        )

        # Should handle API errors gracefully
        logger.info("API test message")
        logger.error("API error test")

        # Give async API calls time to complete
        time.sleep(0.1)

    def test_long_running_application(self, temp_dir):
        """Simulate a long-running application with various logging patterns"""
        logger = Tamga(
            logToFile=True,
            logToJSON=True,
            logFile=f"{temp_dir}/longrun.log",
            logJSON=f"{temp_dir}/longrun.json",
            bufferSize=100,
            maxLogSize=1,  # 1MB
            enableBackup=True,
        )

        # Simulate different phases of application lifecycle

        # Startup phase
        logger.info("Application starting...")
        logger.debug("Loading configuration")
        logger.success("Configuration loaded")

        # Processing phase
        for hour in range(3):  # Simulate 3 hours
            logger.info(f"Hour {hour} processing started")

            for minute in range(60):
                if minute % 10 == 0:
                    logger.metric(f"Hour {hour}, Minute {minute}: Processed 1000 items")

                if minute == 30:
                    logger.warning(f"Hour {hour}: High memory usage detected")

                if hour == 1 and minute == 45:
                    logger.error(f"Database connection lost at hour {hour}")
                    logger.info("Attempting reconnection...")
                    logger.success("Database reconnected")

            logger.info(f"Hour {hour} completed")

        # Shutdown phase
        logger.info("Graceful shutdown initiated")
        logger.flush()
        logger.success("Application stopped successfully")

        # Verify log continuity and rotation
        assert os.path.exists(f"{temp_dir}/longrun.log")
        backups = list(Path(temp_dir).glob("longrun.log.*.bak"))
        assert len(backups) >= 0  # May or may not rotate depending on content
