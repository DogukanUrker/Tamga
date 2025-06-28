#!/bin/bash
# Trigger Tamga tests manually using GitHub CLI
# Requires: gh (GitHub CLI) installed and authenticated

# Default values
TEST_TYPE="${1:-all}"
PYTHON_VERSION="${2:-}"
OS="${3:-}"
COVERAGE="${4:-true}"
VERBOSE="${5:-false}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Triggering Tamga Test Suite${NC}"
echo -e "${YELLOW}Configuration:${NC}"
echo "  Test Type: $TEST_TYPE"
echo "  Python: ${PYTHON_VERSION:-all versions}"
echo "  OS: ${OS:-all platforms}"
echo "  Coverage: $COVERAGE"
echo "  Verbose: $VERBOSE"
echo ""

# Build the JSON payload
INPUTS=$(jq -n \
  --arg tt "$TEST_TYPE" \
  --arg pv "$PYTHON_VERSION" \
  --arg os "$OS" \
  --arg cov "$COVERAGE" \
  --arg verb "$VERBOSE" \
  '{
    test_type: $tt,
    python_version: $pv,
    os: $os,
    enable_coverage: ($cov == "true"),
    verbose: ($verb == "true")
  }')

# Trigger the workflow
echo -e "${BLUE}Triggering workflow...${NC}"
gh workflow run "test-tamga.yaml" --json --raw-field inputs="$INPUTS"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Workflow triggered successfully!${NC}"
    echo ""
    echo "View runs at: https://github.com/dogukanurker/tamga/actions/workflows/test-tamga.yaml"

    # Optional: Wait and show the run URL
    sleep 3
    echo ""
    echo "Latest run:"
    gh run list --workflow=test-tamga.yaml --limit=1
else
    echo -e "${RED}❌ Failed to trigger workflow${NC}"
    exit 1
fi
