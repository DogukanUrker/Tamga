# GitHub CLI Scripts for Tamga Tests

These scripts allow you to trigger and monitor Tamga tests from your command line using GitHub CLI.

## Prerequisites

1. Install GitHub CLI: https://cli.github.com/
2. Authenticate: `gh auth login`

## Available Scripts

### 🚀 Trigger Scripts

#### 🐧 Linux/macOS: `trigger-tests.sh`
```bash
# Make executable (first time only)
chmod +x trigger-tests.sh

# Usage
./trigger-tests.sh [test_type] [python_version] [os] [coverage] [verbose]

# Examples
./trigger-tests.sh                          # Run all tests
./trigger-tests.sh quick                    # Quick tests
./trigger-tests.sh performance 3.11         # Performance on Python 3.11
./trigger-tests.sh all "" windows-latest    # All tests on Windows
```

#### 🪟 Windows: `trigger-tests.ps1`
```powershell
# Usage
.\trigger-tests.ps1 [-TestType <type>] [-PythonVersion <version>] [-OS <os>] [-Coverage <bool>] [-Verbose <bool>]

# Examples
.\trigger-tests.ps1                                    # Run all tests
.\trigger-tests.ps1 -TestType quick                    # Quick tests
.\trigger-tests.ps1 -TestType performance -Verbose $true
```

#### 🐍 Cross-platform: `trigger_tests.py`
```bash
# Usage
python trigger_tests.py [test_type] [python_version] [os] [coverage] [verbose]

# Examples
python trigger_tests.py                      # Run all tests
python trigger_tests.py quick                # Quick tests
python trigger_tests.py performance 3.11 ubuntu-latest
python trigger_tests.py --help               # Show help
```

### 📊 Monitor Script: `monitor_tests.py`

Monitor recent test runs and their status:

```bash
# Show recent runs
python monitor_tests.py

# Watch for new runs (updates every 30s)
python monitor_tests.py --watch

# Show more runs
python monitor_tests.py --limit 20

# Watch with custom limit
python monitor_tests.py --watch --limit 5
```

## Test Types

- `all` - Complete test suite
- `core` - Core functionality
- `performance` - Performance benchmarks
- `integration` - Integration tests
- `colors` - Color utilities
- `time` - Time utilities
- `security` - Security scanning
- `quick` - Quick smoke tests

## Quick Commands Reference

```bash
# Trigger quick test on latest Python
python trigger_tests.py quick 3.13

# Watch test results
python monitor_tests.py --watch

# Check specific workflow run
gh run view <run-id>

# Download logs from failed run
gh run download <run-id>

# Re-run failed jobs
gh run rerun <run-id> --failed
```

## Notes

- Empty string `""` means "all" for python_version and os
- Coverage and verbose are boolean (true/false)
- Scripts will show the workflow URL after triggering
- You can check status with: `gh run list --workflow=test-tamga.yaml`
