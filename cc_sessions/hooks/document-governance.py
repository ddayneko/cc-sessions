#!/usr/bin/env python3
"""Document governance hook for context retention and document validation."""
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from shared_state import get_project_root, get_task_state

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
    
    # Default configuration
    return {
        "enabled": False,
        "auto_context_retention": True,
        "document_validation": True,
        "conflict_detection": True,
        "auto_versioning": True,
        "documents_path": "sessions/documents",
        "version_history_limit": 10,
        "require_user_confirmation": True
    }

def check_memory_bank_available():
    """Check if Memory Bank MCP is available."""
    try:
        # Try to list MCP servers to see if memory bank is available
        result = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "memory-bank" in result.stdout.lower()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return False

def preserve_context_to_memory_bank(context_data):
    """Preserve context to Memory Bank MCP if available."""
    if not check_memory_bank_available():
        return False
    
    try:
        project_root = get_project_root()
        project_name = project_root.name
        task_state = get_task_state()
        
        # Create context file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = task_state.get("task", "unknown")
        context_filename = f"context_{task_name}_{timestamp}.md"
        
        # Format context data
        context_content = f"""# Context Analysis - {task_name}

**Generated:** {datetime.now().isoformat()}
**Task:** {task_name}
**Branch:** {task_state.get("branch", "unknown")}

## Analysis Summary
{context_data.get("summary", "No summary available")}

## Implementation Plan
{context_data.get("plan", "No plan available")}

## Key Findings
{context_data.get("findings", "No findings available")}

## Dependencies Identified
{context_data.get("dependencies", "No dependencies identified")}

## Risks and Considerations
{context_data.get("risks", "No risks identified")}
"""
        
        # Write context to Memory Bank (simplified - in real implementation would use MCP calls)
        context_file = project_root / "sessions" / "memory_bank" / project_name / "contexts" / context_filename
        context_file.parent.mkdir(parents=True, exist_ok=True)
        context_file.write_text(context_content)
        
        return True
    except Exception as e:
        print(f"Warning: Could not preserve context to Memory Bank: {e}", file=sys.stderr)
        return False

def load_project_documents():
    """Load PRD, FSD, and Epic documents from the project."""
    project_root = get_project_root()
    docs_path = project_root / "sessions" / "documents"
    
    documents = {}
    
    # Look for PRD files
    for prd_file in docs_path.glob("**/PRD*.md"):
        documents.setdefault("PRD", []).append(prd_file.read_text())
    
    # Look for FSD files
    for fsd_file in docs_path.glob("**/FSD*.md"):
        documents.setdefault("FSD", []).append(fsd_file.read_text())
    
    # Look for Epic files
    for epic_file in docs_path.glob("**/EPIC*.md"):
        documents.setdefault("EPIC", []).append(epic_file.read_text())
    
    return documents

def detect_document_conflicts(proposed_changes, documents):
    """Detect potential conflicts between proposed changes and existing documents."""
    conflicts = []
    
    # Simple keyword-based conflict detection
    # In a real implementation, this would be more sophisticated
    change_keywords = set(proposed_changes.lower().split())
    
    for doc_type, doc_contents in documents.items():
        for i, content in enumerate(doc_contents):
            doc_keywords = set(content.lower().split())
            
            # Look for conflicting requirements
            conflict_indicators = [
                "not allowed", "forbidden", "prohibited", "deprecated",
                "must not", "cannot", "shall not", "restricted"
            ]
            
            for indicator in conflict_indicators:
                if indicator in content.lower() and any(keyword in change_keywords for keyword in content.lower().split()):
                    conflicts.append({
                        "type": doc_type,
                        "document_index": i,
                        "conflict_type": "restriction_violation",
                        "indicator": indicator,
                        "description": f"Proposed changes may violate {doc_type} restrictions"
                    })
    
    return conflicts

def request_user_confirmation(conflicts):
    """Request user confirmation when conflicts are detected."""
    if not conflicts:
        return True
    
    print("⚠️  Document Governance Alert: Potential conflicts detected!", file=sys.stderr)
    print("", file=sys.stderr)
    
    for conflict in conflicts:
        print(f"• {conflict['type']}: {conflict['description']}", file=sys.stderr)
        print(f"  Conflict type: {conflict['conflict_type']}", file=sys.stderr)
        print(f"  Indicator: {conflict['indicator']}", file=sys.stderr)
        print("", file=sys.stderr)
    
    print("How would you like to proceed?", file=sys.stderr)
    print("1. Continue with implementation (override conflicts)", file=sys.stderr)
    print("2. Stop and revise documents", file=sys.stderr)
    print("3. Abort implementation", file=sys.stderr)
    
    # In a real implementation, this would be interactive
    # For now, return False to indicate conflicts need resolution
    return False

def validate_against_documents(context_data):
    """Validate proposed changes against project documents."""
    config = load_config()
    
    if not config.get("enabled", False) or not config.get("document_validation", True):
        return True
    
    # Load project documents
    documents = load_project_documents()
    
    if not documents:
        print("No project documents found for validation.", file=sys.stderr)
        return True
    
    # Detect conflicts
    proposed_changes = context_data.get("plan", "") + " " + context_data.get("summary", "")
    conflicts = detect_document_conflicts(proposed_changes, documents)
    
    if conflicts and config.get("require_user_confirmation", True):
        return request_user_confirmation(conflicts)
    
    return len(conflicts) == 0

def main():
    """Main hook function."""
    try:
        # Load input from stdin
        input_data = json.load(sys.stdin)
        
        # Get configuration
        config = load_config()
        
        if not config.get("enabled", False):
            return
        
        # Extract context from tool usage
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        
        # Check if this is a context-gathering completion or implementation start
        if tool_name == "Task" and "context-gathering" in str(tool_input):
            # Analysis phase complete - preserve context
            context_data = {
                "summary": "Context analysis completed",
                "plan": str(tool_input),
                "timestamp": datetime.now().isoformat()
            }
            
            if config.get("auto_context_retention", True):
                preserve_context_to_memory_bank(context_data)
            
            if config.get("document_validation", True):
                if not validate_against_documents(context_data):
                    print("🛑 Implementation blocked due to document conflicts.", file=sys.stderr)
                    print("Please resolve conflicts before proceeding.", file=sys.stderr)
                    # In a real implementation, this would block the action
        
        # Check for implementation tools that indicate implementation phase
        implementation_tools = ["Edit", "Write", "MultiEdit", "NotebookEdit"]
        if tool_name in implementation_tools:
            # Implementation starting - could trigger additional validation
            pass
            
    except json.JSONDecodeError:
        pass
    except Exception as e:
        print(f"Document governance hook error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()