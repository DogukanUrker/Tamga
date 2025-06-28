# Trigger Tamga tests manually using GitHub CLI (PowerShell version)
# Requires: gh (GitHub CLI) installed and authenticated

param(
    [string]$TestType = "all",
    [string]$PythonVersion = "",
    [string]$OS = "",
    [bool]$Coverage = $true,
    [bool]$Verbose = $false
)

# Colors
$Blue = "`e[34m"
$Green = "`e[32m"
$Yellow = "`e[33m"
$Reset = "`e[0m"

Write-Host "${Blue}🚀 Triggering Tamga Test Suite${Reset}"
Write-Host "${Yellow}Configuration:${Reset}"
Write-Host "  Test Type: $TestType"
Write-Host "  Python: $(if ($PythonVersion) { $PythonVersion } else { 'all versions' })"
Write-Host "  OS: $(if ($OS) { $OS } else { 'all platforms' })"
Write-Host "  Coverage: $Coverage"
Write-Host "  Verbose: $Verbose"
Write-Host ""

# Build the inputs
$inputs = @{
    test_type = $TestType
    python_version = $PythonVersion
    os = $OS
    enable_coverage = $Coverage
    verbose = $Verbose
} | ConvertTo-Json -Compress

# Trigger the workflow
Write-Host "${Blue}Triggering workflow...${Reset}"

try {
    gh workflow run "test-tamga.yaml" --raw-field inputs=$inputs

    Write-Host "${Green}✅ Workflow triggered successfully!${Reset}"
    Write-Host ""
    Write-Host "View runs at: https://github.com/dogukanurker/tamga/actions/workflows/test-tamga.yaml"

    # Wait a moment then show latest run
    Start-Sleep -Seconds 3
    Write-Host ""
    Write-Host "Latest run:"
    gh run list --workflow=test-tamga.yaml --limit=1
}
catch {
    Write-Host "❌ Failed to trigger workflow" -ForegroundColor Red
    exit 1
}
