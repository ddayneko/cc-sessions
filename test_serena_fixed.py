#!/usr/bin/env python3
"""Test script with corrected Serena MCP setup"""

import subprocess
import shutil

def test_serena_commands():
    """Test different command structures for Serena MCP"""
    
    # Test 1: Direct uvx command (what we want to run)
    print("Test 1: Direct uvx command")
    try:
        cmd1 = ["uvx", "--from", "git+https://github.com/oraios/serena", "serena", "--help"]
        result1 = subprocess.run(cmd1, check=True, capture_output=True, text=True, timeout=30)
        print("✅ Direct uvx works")
        print("Output:", result1.stdout[:200])
    except Exception as e:
        print(f"❌ Direct uvx failed: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 2: Correct claude mcp add syntax - pass uvx as the command with args
    print("Test 2: claude mcp add with corrected syntax")
    try:
        # The correct format should be:
        # claude mcp add <name> <command> [args...]
        # where uvx is the command and everything else are args
        cmd2 = [
            "claude", "mcp", "add", "serena-test",
            "uvx", "--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server"
        ]
        
        print(f"Running: {' '.join(cmd2)}")
        result2 = subprocess.run(cmd2, check=True, capture_output=True, text=True)
        print("✅ claude mcp add succeeded!")
        print("STDOUT:", result2.stdout)
        
        # Clean up the test server
        subprocess.run(["claude", "mcp", "remove", "serena-test"], capture_output=True)
        print("Cleaned up test server")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ claude mcp add failed with return code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
    
    print("\n" + "-"*50 + "\n")
    
    # Test 3: Alternative approach - use full uvx command as a single string
    print("Test 3: Alternative approach with shell command")
    try:
        # Sometimes MCP servers need to be added as shell commands
        cmd3 = [
            "claude", "mcp", "add", "serena-test2",
            "sh", "-c", "uvx --from git+https://github.com/oraios/serena serena start-mcp-server"
        ]
        
        print(f"Running: {' '.join(cmd3)}")
        result3 = subprocess.run(cmd3, check=True, capture_output=True, text=True)
        print("✅ Shell wrapper approach succeeded!")
        print("STDOUT:", result3.stdout)
        
        # Clean up
        subprocess.run(["claude", "mcp", "remove", "serena-test2"], capture_output=True)
        print("Cleaned up test server")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Shell wrapper failed with return code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)

if __name__ == "__main__":
    print("Testing different Serena MCP installation approaches...")
    print("=" * 60)
    test_serena_commands()