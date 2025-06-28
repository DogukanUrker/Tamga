#!/usr/bin/env python3
"""
Monitor Tamga test runs using GitHub CLI
Shows recent test runs with their status and configuration

Usage:
    python monitor_tests.py [--watch] [--limit N]
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List


class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    GRAY = "\033[90m"
    RESET = "\033[0m"


def get_status_icon(status: str) -> str:
    """Get colored icon for workflow status."""
    icons = {
        "completed": f"{Colors.GREEN}✅{Colors.RESET}",
        "success": f"{Colors.GREEN}✅{Colors.RESET}",
        "failure": f"{Colors.RED}❌{Colors.RESET}",
        "cancelled": f"{Colors.GRAY}⏹️{Colors.RESET}",
        "in_progress": f"{Colors.YELLOW}🔄{Colors.RESET}",
        "queued": f"{Colors.BLUE}⏳{Colors.RESET}",
    }
    return icons.get(status.lower(), "❓")


def get_recent_runs(limit: int = 10) -> List[Dict]:
    """Get recent workflow runs."""
    try:
        cmd = [
            "gh",
            "run",
            "list",
            "--workflow=test-tamga.yaml",
            f"--limit={limit}",
            "--json=databaseId,status,conclusion,createdAt,displayTitle,event",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"{Colors.RED}Error getting runs: {result.stderr}{Colors.RESET}")
            return []
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        return []


def format_time_ago(timestamp: str) -> str:
    """Format timestamp as 'X minutes/hours/days ago'."""
    try:
        # Parse ISO format timestamp
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        diff = now - dt

        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "just now"
    except Exception:
        return timestamp


def display_runs(runs: List[Dict]):
    """Display workflow runs in a nice format."""
    if not runs:
        print("No recent test runs found.")
        return

    print(f"\n{Colors.BLUE}📊 Recent Tamga Test Runs{Colors.RESET}")
    print("=" * 70)

    for run in runs:
        status = run.get("conclusion") or run.get("status", "unknown")
        icon = get_status_icon(status)

        # Parse display title to extract test type if it's a manual run
        title = run.get("displayTitle", "")
        event = run.get("event", "")

        # Time formatting
        created = format_time_ago(run.get("createdAt", ""))

        # Build output line
        print(f"{icon} {title[:50]:<50} {Colors.GRAY}{created:>10}{Colors.RESET}")

        # Show trigger type for manual runs
        if event == "workflow_dispatch":
            print(f"   {Colors.GRAY}↳ Manual trigger{Colors.RESET}")

    print("=" * 70)
    print(f"\n{Colors.GRAY}View details: gh run view <run-id>{Colors.RESET}")


def watch_runs(interval: int = 30, limit: int = 5):
    """Watch for new test runs continuously."""
    print(
        f"{Colors.BLUE}👀 Watching for Tamga test runs (refresh every {interval}s)...{Colors.RESET}"
    )
    print(f"{Colors.GRAY}Press Ctrl+C to stop{Colors.RESET}")

    try:
        while True:
            # Clear screen (works on most terminals)
            print("\033[2J\033[H", end="")

            runs = get_recent_runs(limit)
            display_runs(runs)

            # Show in-progress count
            in_progress = sum(1 for r in runs if r.get("status") == "in_progress")
            if in_progress > 0:
                print(
                    f"\n{Colors.YELLOW}🔄 {in_progress} run(s) in progress{Colors.RESET}"
                )

            print(
                f"\n{Colors.GRAY}Last updated: {datetime.now().strftime('%H:%M:%S')}{Colors.RESET}"
            )

            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{Colors.GRAY}Stopped watching.{Colors.RESET}")


def main():
    """Main entry point."""
    args = sys.argv[1:]

    # Parse arguments
    watch = "--watch" in args or "-w" in args

    # Get limit
    limit = 10
    for i, arg in enumerate(args):
        if arg in ("--limit", "-l") and i + 1 < len(args):
            try:
                limit = int(args[i + 1])
            except ValueError:
                print(f"{Colors.RED}Invalid limit value{Colors.RESET}")
                return 1

    # Show help
    if "-h" in args or "--help" in args:
        print(__doc__)
        print("\nOptions:")
        print("  --watch, -w     Watch for new runs continuously")
        print("  --limit N, -l N Set number of runs to show (default: 10)")
        return 0

    # Execute
    if watch:
        watch_runs(limit=limit)
    else:
        runs = get_recent_runs(limit)
        display_runs(runs)

    return 0


if __name__ == "__main__":
    sys.exit(main())
