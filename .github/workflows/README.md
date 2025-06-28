# 🚀 Tamga Test Suite - Manual Trigger Guide

## How to Manually Run Tests

### 1. Navigate to Actions Tab
Go to your repository → Actions → Select "🧪 Tamga Test Suite"

### 2. Click "Run workflow"
You'll see a dropdown with these options:

## 📋 Manual Run Options

### Test Type Selection
Choose which tests to run:
- **`all`** - Run complete test suite (default)
- **`core`** - Core functionality tests only
- **`performance`** - Performance benchmarks only
- **`integration`** - Integration tests only
- **`colors`** - Color utility tests only
- **`time`** - Time utility tests only
- **`security`** - Security scanning only
- **`quick`** - Quick smoke tests (2 tests)

### Python Version
- **Leave empty** - Tests all versions (3.8-3.13)
- **Select specific** - Tests only that version

### Operating System
- **Leave empty** - Tests on all OS (Ubuntu, Windows, macOS)
- **Select specific** - Tests only on that OS

### Additional Options
- **Enable coverage** - Generate coverage reports (default: true)
- **Verbose output** - Show detailed test output (default: false)

## 🎯 Example Scenarios

### Quick Debug Run
```
Test type: quick
Python: 3.11
OS: ubuntu-latest
Coverage: false
Verbose: true
```
→ Runs 2 quick tests on Ubuntu with Python 3.11

### Performance Testing
```
Test type: performance
Python: (empty)
OS: ubuntu-latest
Coverage: false
Verbose: false
```
→ Runs performance benchmarks on Ubuntu with all Python versions

### Debug Color Issues
```
Test type: colors
Python: 3.11
OS: windows-latest
Coverage: true
Verbose: true
```
→ Tests color utilities on Windows with detailed output

### Full Integration Test
```
Test type: integration
Python: (empty)
OS: (empty)
Coverage: true
Verbose: false
```
→ Runs integration tests on all platforms and Python versions

### Single Platform Test
```
Test type: all
Python: 3.12
OS: macos-latest
Coverage: true
Verbose: false
```
→ Full test suite on macOS with Python 3.12

## 🔄 Automatic Triggers

The workflow also runs automatically when:
- You push changes to `tamga/` directory
- You push changes to `tests/` directory
- You modify `pyproject.toml` or requirements files
- Someone opens a PR with changes to these files

## 📊 Viewing Results

After the run:
1. Click on the workflow run
2. Check the summary for quick overview
3. Click on specific jobs for detailed logs
4. Download artifacts if generated
5. View coverage reports in Codecov (if enabled)

## 💡 Pro Tips

1. **Debugging failures**: Use verbose mode + single Python/OS combo
2. **Quick validation**: Use "quick" test type for fast feedback
3. **Performance regression**: Compare benchmark results between runs
4. **Coverage gaps**: Enable coverage to find untested code
5. **Platform issues**: Test specific OS when users report platform bugs

## 🚨 Troubleshooting

- **Tests fail on specific OS**: Select that OS only and enable verbose
- **Performance seems slow**: Run performance tests with benchmarks
- **Coverage missing**: Ensure coverage is enabled and tests aren't skipped
- **Security warnings**: Run security test type to see detailed output

## 📈 Test Metrics

The workflow provides:
- ✅ Pass/fail status for each test
- 📊 Coverage percentage (when enabled)
- ⚡ Performance benchmark results
- 🔒 Security scan results
- 📝 Detailed logs for debugging

## 🖥️ Command Line Triggers

You can also trigger tests from your terminal using GitHub CLI:

### Using Shell Script (Linux/macOS)
```bash
# Make executable
chmod +x .github/scripts/trigger-tests.sh

# Run all tests
./.github/scripts/trigger-tests.sh

# Run specific tests
./.github/scripts/trigger-tests.sh performance 3.11 ubuntu-latest false false
```

### Using PowerShell (Windows)
```powershell
# Run all tests
.\.github\scripts\trigger-tests.ps1

# Run specific tests
.\.github\scripts\trigger-tests.ps1 -TestType performance -PythonVersion 3.11
```

### Using Python (Cross-platform)
```bash
# Run all tests
python .github/scripts/trigger_tests.py

# Run quick tests
python .github/scripts/trigger_tests.py quick

# Run with specific config
python .github/scripts/trigger_tests.py performance 3.11 ubuntu-latest true false
```
