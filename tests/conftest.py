"""
Pytest configuration for Tamga tests
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import tamga
sys.path.insert(0, str(Path(__file__).parent.parent))


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "benchmark: mark test as a performance benchmark"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers"""
    for item in items:
        # Add integration marker to integration tests
        if "integration" in str(item.fspath):
            item.add_marker("integration")

        # Add performance marker to performance tests
        if "performance" in str(item.fspath):
            item.add_marker("performance")
