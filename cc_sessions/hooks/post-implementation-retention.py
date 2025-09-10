#!/usr/bin/env python3
"""Post-implementation context retention hook for preserving implementation outcomes."""
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from shared_state import get_project_root, get_task_state, check_daic_mode_bool

def load_config():
    """Load document governance configuration."""
    project_root = get_project_root()
    config_file = project_root / "sessions" / "sessions-config.json"
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get("document_governance", {})
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    return {"enabled": False, "auto_context_retention": True}

def check_memory_bank_available():
    """Check if Memory Bank MCP is available."""
    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "memory-bank" in result.stdout.lower()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return False

def analyze_implementation_outcome(tool_name, tool_input):
    """Analyze what was implemented and gather outcome data."""
    outcome_data = {
        "tool_used": tool_name,
        "timestamp": datetime.now().isoformat(),
        "files_modified": [],
        "implementation_type": "unknown"
    }
    
    # Extract file information from tool input
    if tool_name in ["Edit", "MultiEdit"]:
        file_path = tool_input.get("file_path", "")
        if file_path:
            outcome_data["files_modified"].append(file_path)
            outcome_data["implementation_type"] = "code_modification"
    elif tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        if file_path:
            outcome_data["files_modified"].append(file_path)
            outcome_data["implementation_type"] = "file_creation"
    elif tool_name == "NotebookEdit":
        notebook_path = tool_input.get("notebook_path", "")
        if notebook_path:
            outcome_data["files_modified"].append(notebook_path)
            outcome_data["implementation_type"] = "notebook_modification"
    
    # Determine if this is a significant implementation step
    if outcome_data["files_modified"]:
        outcome_data["significant"] = True
    else:
        outcome_data["significant"] = False
    
    return outcome_data

def preserve_implementation_context(outcome_data):
    """Preserve implementation outcome to Memory Bank."""
    if not check_memory_bank_available():
        return False
    
    try:
        project_root = get_project_root()
        project_name = project_root.name
        task_state = get_task_state()
        
        # Create implementation outcome file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = task_state.get("task", "unknown")
        outcome_filename = f"implementation_{task_name}_{timestamp}.md"
        
        # Format outcome data
        outcome_content = f"""# Implementation Outcome - {task_name}

**Generated:** {outcome_data['timestamp']}
**Task:** {task_name}
**Branch:** {task_state.get("branch", "unknown")}
**Tool Used:** {outcome_data['tool_used']}
**Implementation Type:** {outcome_data['implementation_type']}

## Files Modified
{chr(10).join(f"- {file}" for file in outcome_data['files_modified']) if outcome_data['files_modified'] else "No files modified"}

## Implementation Details
This implementation step was completed as part of task {task_name}.

### Changes Made
- Tool: {outcome_data['tool_used']}
- Timestamp: {outcome_data['timestamp']}
- Significance: {'High' if outcome_data['significant'] else 'Low'}

## Next Steps
Implementation outcome preserved for future reference and context continuity.

## Git Context
Current branch: {task_state.get("branch", "unknown")}
"""
        
        # Write outcome to Memory Bank context
        outcome_file = project_root / "sessions" / "memory_bank" / project_name / "implementations" / outcome_filename
        outcome_file.parent.mkdir(parents=True, exist_ok=True)
        outcome_file.write_text(outcome_content)
        
        return True
    except Exception as e:
        print(f"Warning: Could not preserve implementation context: {e}", file=sys.stderr)
        return False

def check_task_completion():
    """Check if the current task appears to be completed."""
    try:
        # Check if we're switching back to discussion mode
        discussion_mode = check_daic_mode_bool()
        if discussion_mode:
            return True
            
        # Additional completion indicators could be added here
        return False
    except:
        return False

def preserve_final_task_context():
    """Preserve comprehensive task completion context."""
    if not check_memory_bank_available():
        return False
    
    try:
        project_root = get_project_root()
        project_name = project_root.name
        task_state = get_task_state()
        
        # Create final task context file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = task_state.get("task", "unknown")
        final_filename = f"task_completion_{task_name}_{timestamp}.md"
        
        # Gather git status for completion context
        try:
            git_status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            modified_files = git_status.stdout.strip().split('\n') if git_status.stdout.strip() else []
        except:
            modified_files = ["Could not determine git status"]
        
        # Format final context
        final_content = f"""# Task Completion Context - {task_name}

**Completed:** {datetime.now().isoformat()}
**Task:** {task_name}
**Branch:** {task_state.get("branch", "unknown")}

## Task Summary
Task {task_name} has been completed.

## Final Git Status
{chr(10).join(f"- {file}" for file in modified_files) if modified_files and modified_files != [""] else "No pending changes"}

## Services Modified
{chr(10).join(f"- {service}" for service in task_state.get("services", [])) if task_state.get("services") else "No services specified"}

## Completion Timestamp
{datetime.now().isoformat()}

## Context Preservation
This document marks the completion of task {task_name} and preserves the final state for future reference.

## Recommendations
- Review changes before committing
- Update related documentation if necessary
- Consider integration testing if appropriate
"""
        
        # Write final context to Memory Bank
        final_file = project_root / "sessions" / "memory_bank" / project_name / "completions" / final_filename
        final_file.parent.mkdir(parents=True, exist_ok=True)
        final_file.write_text(final_content)
        
        return True
    except Exception as e:
        print(f"Warning: Could not preserve final task context: {e}", file=sys.stderr)
        return False

def main():
    """Main post-implementation hook function."""
    try:
        # Load input from stdin
        input_data = json.load(sys.stdin)
        
        # Get configuration
        config = load_config()
        
        if not config.get("enabled", False) or not config.get("auto_context_retention", True):
            return
        
        # Extract tool information
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        
        # Check if this is an implementation tool
        implementation_tools = ["Edit", "Write", "MultiEdit", "NotebookEdit"]
        
        if tool_name in implementation_tools:
            # Analyze and preserve implementation outcome
            outcome_data = analyze_implementation_outcome(tool_name, tool_input)
            
            if outcome_data["significant"]:
                preserve_implementation_context(outcome_data)
        
        # Check for task completion indicators
        if tool_name == "Bash" and "daic" in str(tool_input):
            # Task likely completing, preserve final context
            preserve_final_task_context()
        
        # Check for other completion indicators
        elif check_task_completion():
            preserve_final_task_context()
            
    except json.JSONDecodeError:
        pass
    except Exception as e:
        print(f"Post-implementation retention hook error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()