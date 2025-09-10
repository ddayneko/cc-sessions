#!/usr/bin/env python3
"""Hook to offer GitHub MCP automated workflow when task completion is detected."""
import json
import sys
from pathlib import Path
from shared_state import get_project_root

def main():
    # Load input
    input_data = json.load(sys.stdin)
    prompt = input_data.get("prompt", "")
    
    # Keywords that suggest task completion
    completion_keywords = [
        "complete the task",
        "finish this task", 
        "mark it done",
        "task completion",
        "run task completion",
        "complete task"
    ]
    
    # Check if user is requesting task completion
    is_completion_request = any(keyword.lower() in prompt.lower() for keyword in completion_keywords)
    
    if is_completion_request:
        # Check if GitHub MCP is likely available (rough heuristic)
        project_root = get_project_root()
        config_file = project_root / "sessions" / "sessions-config.json"
        
        github_mcp_available = False
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    github_mcp_available = config.get("github_mcp", {}).get("enabled", False)
            except:
                pass
        
        if github_mcp_available:
            print("\n[GitHub Workflow] GitHub MCP is available for automated PR creation and merge.", file=sys.stderr)
            print("[GitHub Workflow] Consider using GitHub MCP workflow for cleaner merge process.", file=sys.stderr)
            sys.exit(2)  # Feed stderr back to Claude
    
    sys.exit(0)

if __name__ == "__main__":
    main()