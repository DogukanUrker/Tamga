#!/usr/bin/env python3
"""
Trigger Tamga tests manually using GitHub CLI
Cross-platform script that works on Windows, macOS, and Linux

Requirements:
- gh (GitHub CLI) installed and authenticated
- Python 3.6+

Usage:
    python trigger_tests.py [test_type] [python_version] [os] [coverage] [verbose]

Examples:
    python trigger_tests.py quick
    python trigger_tests.py performance 3.11 ubuntu-latest
    python trigger_tests.py all "" "" true true
"""

import json
import subprocess
import sys
import time


# ANSI color codes
class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"


def trigger_workflow(
    test_type: str = "all",
    python_version: str = "",
    os: str = "",
    coverage: bool = True,
    verbose: bool = False,
) -> bool:
    """Trigger the Tamga test workflow with specified parameters."""

    print(f"{Colors.BLUE}🚀 Triggering Tamga Test Suite{Colors.RESET}")
    print(f"{Colors.YELLOW}Configuration:{Colors.RESET}")
    print(f"  Test Type: {test_type}")
    print(f"  Python: {python_version or 'all versions'}")
    print(f"  OS: {os or 'all platforms'}")
    print(f"  Coverage: {coverage}")
    print(f"  Verbose: {verbose}")
    print()

    # Build inputs
    inputs = {
        "test_type": test_type,
        "python_version": python_version,
        "os": os,
        "enable_coverage": coverage,
        "verbose": verbose,
    }

    inputs_json = json.dumps(inputs)

    # Trigger workflow
    print(f"{Colors.BLUE}Triggering workflow...{Colors.RESET}")

    try:
        cmd = [
            "gh",
            "workflow",
            "run",
            "test-tamga.yaml",
            "--raw-field",
            f"inputs={inputs_json}",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Workflow triggered successfully!{Colors.RESET}")
            print()
            print(
                "View runs at: https://github.com/dogukanurker/tamga/actions/workflows/test-tamga.yaml"
            )

            # Wait and show latest run
            time.sleep(3)
            print("\nLatest run:")
            subprocess.run(
                ["gh", "run", "list", "--workflow=test-tamga.yaml", "--limit=1"]
            )

            return True
        else:
            print(f"{Colors.RED}❌ Failed to trigger workflow{Colors.RESET}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except FileNotFoundError:
        print(f"{Colors.RED}❌ GitHub CLI (gh) not found!{Colors.RESET}")
        print("Please install GitHub CLI: https://cli.github.com/")
        return False
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        return False


def parse_bool(value: str) -> bool:
    """Parse string to boolean."""
    return value.lower() in ("true", "yes", "1", "on")


def main():
    """Main entry point."""
    # Parse command line arguments
    args = sys.argv[1:]

    test_type = args[0] if len(args) > 0 else "all"
    python_version = args[1] if len(args) > 1 else ""
    os = args[2] if len(args) > 2 else ""
    coverage = parse_bool(args[3]) if len(args) > 3 else True
    verbose = parse_bool(args[4]) if len(args) > 4 else False

    # Show help if requested
    if test_type in ("-h", "--help", "help"):
        print(__doc__)
        print("\nAvailable test types:")
        print("  - all: Run complete test suite")
        print("  - core: Core functionality tests")
        print("  - performance: Performance benchmarks")
        print("  - integration: Integration tests")
        print("  - colors: Color utility tests")
        print("  - time: Time utility tests")
        print("  - security: Security scanning")
        print("  - quick: Quick smoke tests")
        return 0

    # Trigger the workflow
    success = trigger_workflow(test_type, python_version, os, coverage, verbose)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
