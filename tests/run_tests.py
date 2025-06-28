#!/usr/bin/env python
"""
Test runner for Tamga logger
Run all tests or specific test categories
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a command and return exit code"""
    print(f"\n{'=' * 60}")
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)
    return subprocess.call(cmd)


def main():
    """Main test runner"""
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "all"

    # Change to project root
    project_root = Path(__file__).parent.parent  # noqa F841

    exit_code = 0

    if test_type in ["all", "core"]:
        # Run core tests
        exit_code |= run_command(
            [sys.executable, "-m", "pytest", "tests/test_core.py", "-v", "--tb=short"]
        )

    if test_type in ["all", "performance", "perf"]:
        # Run performance tests
        exit_code |= run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_performance.py",
                "-v",
                "--benchmark-only",
                "--tb=short",
            ]
        )

    if test_type in ["all", "integration", "int"]:
        # Run integration tests
        exit_code |= run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_integration.py",
                "-v",
                "--tb=short",
            ]
        )

    if test_type in ["all", "coverage", "cov"]:
        # Run with coverage
        exit_code |= run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "-v",
                "--cov=tamga",
                "--cov-report=term-missing",
                "--cov-report=html",
                "--tb=short",
            ]
        )
        print("\nCoverage report generated in htmlcov/index.html")

    if test_type == "quick":
        # Quick smoke test
        exit_code |= run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_core.py::TestCoreLogging::test_console_logging",
                "tests/test_core.py::TestCoreLogging::test_all_log_levels",
                "-v",
                "--tb=short",
            ]
        )

    if test_type not in [
        "all",
        "core",
        "performance",
        "perf",
        "integration",
        "int",
        "coverage",
        "cov",
        "quick",
    ]:
        print(f"\nUnknown test type: {test_type}")
        print(
            "\nUsage: python run_tests.py [all|core|performance|integration|coverage|quick]"
        )
        print("\nOptions:")
        print("  all         - Run all tests (default)")
        print("  core        - Run core functionality tests")
        print("  performance - Run performance benchmarks")
        print("  integration - Run integration tests")
        print("  coverage    - Run all tests with coverage report")
        print("  quick       - Run quick smoke tests")
        return 1

    print(f"\n{'=' * 60}")
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
