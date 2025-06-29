# Tamga / examples / high_performance.py
# Example: High-Performance Logging with Tamga (Big Data Logging Demo)
#
# This script demonstrates Tamga's speed by logging a massive number of entries.
# For best results, run with console output disabled and a large buffer size.

import time

from tamga import Tamga

NUM_LOGS = 1_000_000  # One million log entries

logger = Tamga(
    logToFile=True,
    logFile="biglog.log",
    maxLogSize=100,  # 100 MB max file size
    logToConsole=False,  # Disable console for max speed
    bufferSize=10_000,  # Large buffer for throughput
)

print(f"Logging {NUM_LOGS:,} entries...")

start = time.time()
for i in range(NUM_LOGS):
    logger.info(f"Big log entry #{i + 1}")
    # Optionally, flush every N logs to avoid memory buildup in real scenarios
    # if (i + 1) % 100_000 == 0:
    #     logger.flush()

elapsed = time.time() - start

print(f"Done. Logged {NUM_LOGS:,} entries in {elapsed:.2f} seconds.")
print(f"Throughput: {NUM_LOGS / elapsed:,.0f} logs/sec")

# Tip: Try increasing NUM_LOGS or bufferSize for even higher throughput.
# For benchmarking, compare with Python's built-in logging for reference.
