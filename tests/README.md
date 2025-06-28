# Tamga Test Suite

[![Test Suite](https://github.com/dogukanurker/tamga/actions/workflows/test-tamga.yaml/badge.svg)](https://github.com/dogukanurker/tamga/actions/workflows/test-tamga.yaml)

## Overview

Comprehensive test suite for the Tamga logger covering:
- ✅ Core functionality
- ⚡ Performance benchmarks
- 🔗 Integration tests
- 🎨 Color utilities
- 🕒 Time utilities
- 🔒 Security checks

## Running Tests Locally

### Quick Start

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio pytest-benchmark

# Run all tests
pytest

# Run with coverage
pytest --cov=tamga --cov-report=term-missing

# Run specific test file
pytest tests/test_core.py -v
```

### Using the Test Runner

```bash
# Run all tests
python tests/run_tests.py

# Run only core tests
python tests/run_tests.py core

# Run performance benchmarks
python tests/run_tests.py performance

# Run integration tests
python tests/run_tests.py integration

# Run with coverage report
python tests/run_tests.py coverage

# Quick smoke test
python tests/run_tests.py quick
```

## Test Categories

### Core Tests (`test_core.py`)
- Console logging (colored and plain)
- All log levels (INFO, WARNING, ERROR, etc.)
- File, JSON, and SQL logging
- Buffer functionality
- File rotation
- Thread safety
- Custom log levels
- Structured logging with `dir()`

### Performance Tests (`test_performance.py`)
- Console logging speed
- Buffered vs unbuffered file writes
- JSON logging performance
- SQL logging benchmarks
- Multi-output performance
- Buffer size impact
- Structured logging overhead

### Integration Tests (`test_integration.py`)
- High-volume logging (10,000+ entries)
- Concurrent logging from multiple threads
- File rotation stress testing
- Mixed workload scenarios
- Error recovery
- Unicode and special characters
- Long-running application simulation

### Color Tests (`test_colors.py`)
- All color codes validation
- Text and background colors
- Style codes (bold, italic, etc.)
- Color consistency
- RGB value verification

### Time Tests (`test_time.py`)
- Date/time format validation
- Timezone handling
- Timestamp precision
- Performance benchmarks

## Running in CI/CD

The test suite runs automatically on:
- Push to `tamga/**` directory
- Pull requests affecting Tamga code
- Multiple Python versions (3.8-3.13)
- Multiple OS (Ubuntu, Windows, macOS)

### Manual Triggers in GitHub Actions

You can manually run tests with custom configurations:

1. Go to Actions tab → "🧪 Tamga Test Suite" → "Run workflow"
2. Select options:
   - **Test type**: all, core, performance, integration, colors, time, security, quick
   - **Python version**: Leave empty for all or select specific (3.8-3.13)
   - **OS**: Leave empty for all or select specific platform
   - **Coverage**: Enable/disable coverage reporting
   - **Verbose**: Enable/disable detailed output

Example scenarios:
- Quick debug: `test_type=quick, python=3.11, os=ubuntu-latest`
- Performance only: `test_type=performance, os=ubuntu-latest`
- Windows issues: `test_type=all, os=windows-latest, verbose=true`

See [.github/workflows/README.md](../.github/workflows/README.md) for detailed guide.

## Test Configuration

### `pytest.ini`
- Configures test discovery
- Sets markers for test categories
- Configures output format

### `conftest.py`
- Pytest configuration
- Custom markers setup
- Path configuration

## Coverage Goals

- Aim for >90% code coverage
- Focus on critical paths
- Test error conditions
- Verify thread safety

## Writing New Tests

1. Place tests in `tests/test_*.py`
2. Use descriptive test names
3. Group related tests in classes
4. Use fixtures for setup/teardown
5. Add docstrings explaining test purpose

Example:
```python
class TestNewFeature:
    """Test the new amazing feature"""

    @pytest.fixture
    def logger(self, temp_dir):
        """Create logger with test config"""
        return Tamga(logFile=f"{temp_dir}/test.log")

    def test_feature_works(self, logger):
        """Test that feature does what it should"""
        logger.amazing_feature("test")
        assert logger.is_amazing == True
```

## Debugging Failed Tests

1. Run with verbose output: `pytest -vv`
2. Show full traceback: `pytest --tb=long`
3. Run specific test: `pytest tests/test_core.py::TestCoreLogging::test_console_logging`
4. Use pytest debugging: `pytest --pdb`
5. Check test artifacts in temp directories

## Performance Benchmarking

```bash
# Run benchmarks
pytest tests/test_performance.py --benchmark-only

# Save benchmark results
pytest tests/test_performance.py --benchmark-save=baseline

# Compare with baseline
pytest tests/test_performance.py --benchmark-compare=baseline
```

## Notes

- MongoDB and Email tests are skipped (require credentials)
- API tests use mock endpoints
- File operations use temporary directories
- Tests clean up after themselves
- Thread-safe tests use proper synchronization
