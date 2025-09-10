#!/usr/bin/env python3
"""Test script to debug Serena MCP setup issues"""

import subprocess
import shutil

def command_exists(command: str) -> bool:
    """Check if a command exists in the system"""
    return shutil.which(command) is not None

def check_serena_mcp() -> dict:
    """Check for Serena MCP availability"""
    has_uv = command_exists("uv")
    has_claude = command_exists("claude")
    
    print(f"UV available: {has_uv}")
    print(f"Claude available: {has_claude}")
    
    return {
        "uv": has_uv,
        "claude": has_claude,
        "available": has_uv and has_claude
    }

def test_serena_install():
    """Test the Serena MCP installation command"""
    serena_status = check_serena_mcp()
    
    if not serena_status["available"]:
        missing = []
        if not serena_status["uv"]:
            missing.append("uv (Python package manager)")
        if not serena_status["claude"]:
            missing.append("claude (Claude Code CLI)")
        
        print(f"❌ Serena MCP requirements not met. Missing: {', '.join(missing)}")
        return False
    
    print("✅ Requirements met, testing Serena MCP installation...")
    
    try:
        # Test the actual command that's failing
        cmd = [
            "claude", "mcp", "add", "serena", 
            "uvx", "--from", "git+https://github.com/oraios/serena", 
            "serena", "start-mcp-server"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Command succeeded!")
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with return code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except FileNotFoundError as e:
        print(f"❌ Command not found: {e}")
        return False

if __name__ == "__main__":
    print("Testing Serena MCP setup...")
    print("-" * 50)
    test_serena_install()