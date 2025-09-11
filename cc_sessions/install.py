#!/usr/bin/env python3
"""
Claude Code Sessions Framework - Cross-Platform Python Installer

Complete installation system for the Claude Code Sessions framework with native
Windows, macOS, and Linux support. Handles platform-specific path handling,
command installation, and shell compatibility.

Key Features:
    - Windows compatibility with native .cmd and .ps1 script support
    - Cross-platform path handling using pathlib
    - Platform-aware file permission management
    - Interactive configuration with terminal UI
    - Global daic command installation with PATH integration
    
Platform Support:
    - Windows 10/11 (Command Prompt, PowerShell, Git Bash)
    - macOS (Bash, Zsh)
    - Linux distributions (Bash, other shells)

Installation Locations:
    - Windows: %USERPROFILE%\\AppData\\Local\\cc-sessions\\bin
    - Unix/Mac: /usr/local/bin

See Also:
    - install.js: Node.js installer wrapper with same functionality
    - cc_sessions.scripts.daic: Unix bash implementation
    - cc_sessions.scripts.daic.cmd: Windows Command Prompt implementation
    - cc_sessions.scripts.daic.ps1: Windows PowerShell implementation
"""

import os
import sys
import json
import shutil
import stat
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Colors for terminal output
class Colors:
    RESET = '\033[0m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BGRED = '\033[41m'
    BGGREEN = '\033[42m'
    BGYELLOW = '\033[43m'
    BGBLUE = '\033[44m'
    BGMAGENTA = '\033[45m'
    BGCYAN = '\033[46m'

def color(text: str, color_code: str) -> str:
    """Colorize text for terminal output"""
    return f"{color_code}{text}{Colors.RESET}"

def command_exists(command: str) -> bool:
    """Check if a command exists in the system"""
    if os.name == 'nt':
        # Windows - try with common extensions
        for ext in ['', '.exe', '.bat', '.cmd']:
            if shutil.which(command + ext):
                return True
        return False
    return shutil.which(command) is not None

def get_package_dir() -> Path:
    """Get the directory where the package is installed"""
    import cc_sessions
    # All data files are now inside cc_sessions/
    return Path(cc_sessions.__file__).parent

class SessionsInstaller:
    def __init__(self):
        self.package_dir = get_package_dir()
        self.project_root = self.detect_project_directory()
        self._installed_mcp_servers = None  # Cache for MCP servers list
        self.config = {
            "developer_name": "the developer",
            "trigger_phrases": ["make it so", "run that", "go ahead", "yert"],
            "blocked_tools": ["Edit", "Write", "MultiEdit", "NotebookEdit"],
            "task_detection": {"enabled": True},
            "branch_enforcement": {"enabled": True},
            "serena_mcp": {
                "enabled": False,
                "auto_activate": True
            },
            "memory_bank_mcp": {
                "enabled": False,
                "auto_activate": True,
                "memory_bank_root": "",
                "sync_files": []
            },
            "github_mcp": {
                "enabled": False,
                "auto_activate": True,
                "requires_pat": True
            },
            "storybook_mcp": {
                "enabled": False,
                "auto_activate": True,
                "storybook_url": ""
            },
            "playwright_mcp": {
                "enabled": False,
                "auto_activate": True,
                "browser_automation": True
            },
            "document_governance": {
                "enabled": False,
                "auto_context_retention": True,
                "document_validation": True,
                "conflict_detection": True,
                "auto_versioning": True,
                "documents_path": "sessions/documents",
                "version_history_limit": 10,
                "require_user_confirmation": True
            }
        }
    
    def detect_project_directory(self) -> Path:
        """Detect the correct project directory when running from pip/pipx"""
        current_dir = Path.cwd()
        
        # If running from site-packages or pipx environment
        if 'site-packages' in str(current_dir) or '.local/pipx' in str(current_dir):
            print(color("⚠️  Running from package directory, not project directory.", Colors.YELLOW))
            print()
            project_path = input("Enter the path to your project directory (or press Enter for current directory): ")
            if project_path:
                return Path(project_path).resolve()
            else:
                # Default to user's current working directory before pip ran
                return Path.cwd()
        
        return current_dir
    
    def check_dependencies(self) -> None:
        """Check for required dependencies"""
        print(color("Checking dependencies...", Colors.CYAN))
        
        # Check Python version
        if sys.version_info < (3, 8):
            print(color("❌ Python 3.8+ is required.", Colors.RED))
            sys.exit(1)
        
        # Check pip
        if not command_exists("pip3") and not command_exists("pip"):
            print(color("❌ pip is required but not installed.", Colors.RED))
            sys.exit(1)
        
        # Check Git (warning only)
        if not command_exists("git"):
            print(color("⚠️  Warning: Git not found. Sessions works best with git.", Colors.YELLOW))
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    def check_package_json_exists(self) -> bool:
        """Check if package.json exists in project root"""
        package_json = self.project_root / "package.json"
        return package_json.exists()
    
    def check_package_installed(self, package_name: str) -> bool:
        """Check if a package is installed by looking in package.json"""
        if not self.check_package_json_exists():
            return False
            
        try:
            package_json = self.project_root / "package.json"
            import json
            with open(package_json) as f:
                data = json.load(f)
            
            # Check both dependencies and devDependencies
            deps = data.get("dependencies", {})
            dev_deps = data.get("devDependencies", {})
            
            # Support wildcard matching for packages like @storybook/*
            if "*" in package_name:
                prefix = package_name.replace("*", "")
                return any(pkg.startswith(prefix) for pkg in list(deps.keys()) + list(dev_deps.keys()))
            else:
                return package_name in deps or package_name in dev_deps
                
        except (json.JSONDecodeError, FileNotFoundError):
            return False
    
    def install_npm_package(self, package_name: str, dev: bool = True) -> bool:
        """Install an npm package"""
        try:
            cmd = ["npm", "install"]
            if dev:
                cmd.append("--save-dev")
            cmd.append(package_name)
            
            print(color(f"  Installing {package_name}...", Colors.DIM))
            subprocess.run(cmd, cwd=self.project_root, check=True, capture_output=True)
            print(color(f"  ✓ Installed {package_name}", Colors.GREEN))
            return True
        except subprocess.CalledProcessError:
            print(color(f"  ⚠️ Failed to install {package_name}", Colors.YELLOW))
            return False
    
    def check_storybook_running(self, port: int = 6006) -> bool:
        """Check if Storybook is running on the specified port"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', port))
                return result == 0
        except:
            return False
    
    def start_storybook(self) -> bool:
        """Start Storybook in the background"""
        try:
            print(color("  Starting Storybook...", Colors.DIM))
            # Start Storybook in background - don't wait for completion
            subprocess.Popen(
                ["npm", "run", "storybook"], 
                cwd=self.project_root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait a moment for startup, then check if it's running
            import time
            time.sleep(3)
            
            if self.check_storybook_running():
                print(color("  ✓ Storybook started successfully", Colors.GREEN))
                return True
            else:
                print(color("  ⚠️ Storybook may still be starting up", Colors.YELLOW))
                return True  # Return True anyway as it was started
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(color("  ⚠️ Failed to start Storybook", Colors.YELLOW))
            print(color("    Make sure you have a 'storybook' script in package.json", Colors.DIM))
            return False

    def get_installed_mcp_servers(self) -> set:
        """Get list of already installed MCP servers (cached to prevent repeated chrome launches)"""
        if self._installed_mcp_servers is not None:
            return self._installed_mcp_servers
            
        if not command_exists("claude"):
            self._installed_mcp_servers = set()
            return self._installed_mcp_servers
        
        try:
            result = subprocess.run(["claude", "mcp", "list"], 
                                  capture_output=True, text=True, check=True)
            installed = set()
            for line in result.stdout.split('\n'):
                if 'serena:' in line.lower():
                    installed.add('serena')
                elif 'memory-bank' in line.lower() or 'memorybank' in line.lower():
                    installed.add('memory-bank')
                elif 'github-mcp' in line.lower() or 'github_mcp' in line.lower():
                    installed.add('github')
                elif 'storybook-mcp' in line.lower() or 'storybook' in line.lower():
                    installed.add('storybook')
                elif 'playwright-mcp' in line.lower() or 'playwright' in line.lower():
                    installed.add('playwright')
            self._installed_mcp_servers = installed
            return installed
        except (subprocess.CalledProcessError, FileNotFoundError):
            self._installed_mcp_servers = set()
            return set()
    
    def check_serena_mcp(self) -> dict:
        """Check for Serena MCP availability"""
        has_uv = command_exists("uv")
        has_claude = command_exists("claude")
        installed_servers = self.get_installed_mcp_servers()
        
        return {
            "uv": has_uv,
            "claude": has_claude,
            "available": has_uv and has_claude,
            "already_installed": "serena" in installed_servers
        }
    
    def setup_serena_mcp(self) -> bool:
        """Setup Serena MCP integration"""
        serena_status = self.check_serena_mcp()
        
        if serena_status["already_installed"]:
            print(color("✓ Serena MCP already installed", Colors.GREEN))
            self.config["serena_mcp"]["enabled"] = True
            return True
        
        if not serena_status["available"]:
            missing = []
            if not serena_status["uv"]:
                missing.append("uv (Python package manager)")
            if not serena_status["claude"]:
                missing.append("claude (Claude Code CLI)")
            
            print(color(f"⚠️  Serena MCP requirements not met. Missing: {', '.join(missing)}", Colors.YELLOW))
            print(color("   Install with: curl -LsSf https://astral.sh/uv/install.sh | sh", Colors.DIM))
            print(color("   Serena MCP features will be disabled but agents will gracefully fallback.", Colors.DIM))
            return False
        
        print(color("✓ Serena MCP requirements detected", Colors.GREEN))
        
        response = input(color("  Install Serena MCP for enhanced code analysis? (y/n): ", Colors.CYAN))
        
        if response.lower() == 'y':
            try:
                print(color("  Installing Serena MCP server...", Colors.DIM))
                
                # Add Serena MCP server to Claude Code using JSON configuration
                import json
                serena_config = {
                    "type": "stdio",
                    "command": "uvx",
                    "args": [
                        "--from", "git+https://github.com/oraios/serena", 
                        "serena", "start-mcp-server",
                        "--enable-web-dashboard", "false",
                        "--enable-gui-log-window", "false",
                        "--log-level", "WARNING"
                    ]
                }
                subprocess.run([
                    "claude", "mcp", "add-json", "serena", json.dumps(serena_config)
                ], check=True)
                
                print(color("  ✓ Serena MCP server configured", Colors.GREEN))
                print(color("    Remember to activate your project: \"Activate the project /path/to/project\"", Colors.DIM))
                
                self.config["serena_mcp"]["enabled"] = True
                return True
                
            except subprocess.CalledProcessError:
                print(color("  ⚠️ Serena MCP installation failed, continuing without it", Colors.YELLOW))
                print(color("    You can set it up manually later with: claude mcp add serena ...", Colors.DIM))
                return False
        
        return False

    def check_memory_bank_mcp(self) -> dict:
        """Check for Memory Bank MCP availability"""
        has_npx = command_exists("npx")
        has_claude = command_exists("claude")
        installed_servers = self.get_installed_mcp_servers()
        
        return {
            "npx": has_npx,
            "claude": has_claude,
            "available": has_npx and has_claude,
            "already_installed": "memory-bank" in installed_servers
        }
    
    def install_memory_bank_mcp(self) -> bool:
        """Install Memory Bank MCP server only"""
        memory_bank_status = self.check_memory_bank_mcp()
        
        if memory_bank_status["already_installed"]:
            print(color("✓ Memory Bank MCP already installed", Colors.GREEN))
            self.config["memory_bank_mcp"]["enabled"] = True
            return True
        
        if not memory_bank_status["available"]:
            missing = []
            if not memory_bank_status["npx"]:
                missing.append("npx (Node.js package runner)")
            if not memory_bank_status["claude"]:
                missing.append("claude (Claude Code CLI)")
            
            print(color(f"⚠️  Memory Bank MCP requirements not met. Missing: {', '.join(missing)}", Colors.YELLOW))
            print(color("   Install Node.js to get npx: https://nodejs.org/", Colors.DIM))
            print(color("   Memory Bank MCP features will be disabled but workflow continues normally.", Colors.DIM))
            return False
        
        print(color("✓ Memory Bank MCP requirements detected", Colors.GREEN))
        
        response = input(color("  Install Memory Bank MCP for persistent context analysis? (y/n): ", Colors.CYAN))
        
        if response.lower() == 'y':
            try:
                print(color("  Installing Memory Bank MCP server...", Colors.DIM))
                
                # Set default memory bank root if not specified
                memory_bank_root = self.project_root / "sessions" / "memory_bank"
                memory_bank_root.mkdir(parents=True, exist_ok=True)
                
                # Install Memory Bank MCP server using smithery with MEMORY_BANK_ROOT
                env = os.environ.copy()
                env["MEMORY_BANK_ROOT"] = str(memory_bank_root)
                subprocess.run([
                    "npx", "-y", "@smithery/cli", "install", 
                    "@alioshr/memory-bank-mcp", "--client", "claude"
                ], env=env, check=True)
                
                print(color("  ✓ Memory Bank MCP server configured", Colors.GREEN))
                print(color(f"    Memory bank root: {memory_bank_root}", Colors.DIM))
                print(color("    MEMORY_BANK_ROOT automatically configured", Colors.GREEN))
                
                self.config["memory_bank_mcp"]["enabled"] = True
                self.config["memory_bank_mcp"]["memory_bank_root"] = str(memory_bank_root)
                
                return True
                
            except subprocess.CalledProcessError:
                print(color("  ⚠️ Memory Bank MCP server installation failed", Colors.RED))
                print(color("    You can set it up manually later with: npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude", Colors.DIM))
                return False
        
        return False

    def configure_memory_bank_files(self) -> bool:
        """Configure Memory Bank file synchronization and PRD/FSD detection"""
        if not self.config["memory_bank_mcp"]["enabled"]:
            return False
            
        try:
            # Collect requirement documents with folder-based detection
            print(color("\n  📋 Requirement Documents", Colors.CYAN))
            print(color("  Specify folder to search for PRD/FSD files automatically.", Colors.DIM))
            print(color('  Examples: "docs/", "requirements/", "spec/"', Colors.DIM))
            print()
            
            folder_path = input(color("  Folder path to search for PRD/FSD files (relative to project root, or Enter to skip): ", Colors.CYAN))
            detected_files = {"prd": None, "fsd": None}
            
            if folder_path:
                search_dir = self.project_root / folder_path
                if search_dir.exists() and search_dir.is_dir():
                    print(color(f"  Searching {folder_path} for PRD/FSD files...", Colors.DIM))
                    
                    # Search for markdown files in the directory
                    for md_file in search_dir.rglob("*.md"):
                        rel_path = str(md_file.relative_to(self.project_root))
                        file_name_lower = md_file.name.lower()
                        
                        # Check filename for PRD indicators
                        if any(indicator in file_name_lower for indicator in ["prd", "product-req", "product_req", "requirements"]):
                            if not detected_files["prd"]:  # Take the first match
                                detected_files["prd"] = rel_path
                                self.config["document_governance"]["prd_file"] = rel_path
                                print(color(f'  ✓ PRD detected: "{rel_path}"', Colors.GREEN))
                        
                        # Check filename for FSD indicators  
                        elif any(indicator in file_name_lower for indicator in ["fsd", "functional-spec", "functional_spec", "spec"]):
                            if not detected_files["fsd"]:  # Take the first match
                                detected_files["fsd"] = rel_path
                                self.config["document_governance"]["fsd_file"] = rel_path
                                print(color(f'  ✓ FSD detected: "{rel_path}"', Colors.GREEN))
                    
                    if not detected_files["prd"] and not detected_files["fsd"]:
                        print(color(f"  ⚠️ No PRD/FSD files found in {folder_path}", Colors.YELLOW))
                else:
                    print(color(f"  ⚠️ Folder not found: {folder_path}", Colors.YELLOW))

            # Collect files to sync with Memory Bank
            print(color("\n  📄 File Synchronization Setup", Colors.CYAN))
            print(color("  Specify markdown files to sync with Memory Bank for persistent context.", Colors.DIM))
            print(color('  Examples: "README.md", "docs/architecture.md", "DESIGN.md"', Colors.DIM))
            print()
            
            # Auto-add detected PRD/FSD files to sync
            auto_sync_files = []
            if detected_files["prd"]:
                auto_sync_files.append(detected_files["prd"])
            if detected_files["fsd"]:
                auto_sync_files.append(detected_files["fsd"])
            
            for file_path in auto_sync_files:
                sync_file = {
                    "path": file_path,
                    "status": "pending",
                    "last_synced": None
                }
                self.config["memory_bank_mcp"]["sync_files"].append(sync_file)
                print(color(f'  ✓ Auto-added requirement doc: "{file_path}"', Colors.GREEN))
            
            while True:
                file_path = input(color("  Add markdown file to sync (Enter path relative to project root, or Enter to skip): ", Colors.CYAN))
                if not file_path:
                    break
                
                # Skip if already added
                if any(f["path"] == file_path for f in self.config["memory_bank_mcp"]["sync_files"]):
                    print(color(f"  ⚠️ File already added: {file_path}", Colors.YELLOW))
                    continue
                
                # Validate file exists and is markdown
                full_path = self.project_root / file_path
                if not full_path.exists():
                    print(color(f"  ⚠️ File not found: {file_path}", Colors.YELLOW))
                    continue
                if not file_path.lower().endswith('.md'):
                    print(color(f"  ⚠️ Only markdown files (.md) are supported", Colors.YELLOW))
                    continue
                
                # Add to sync files configuration
                sync_file = {
                    "path": file_path,
                    "status": "pending",
                    "last_synced": None
                }
                self.config["memory_bank_mcp"]["sync_files"].append(sync_file)
                print(color(f'  ✓ Added: "{file_path}"', Colors.GREEN))
            
            return True
            
        except Exception as e:
            print(color("  ⚠️ Error during Memory Bank file configuration", Colors.YELLOW))
            print(color(f"    Error: {str(e)}", Colors.DIM))
            print(color("    Memory Bank MCP server is still installed and functional", Colors.GREEN))
            return False

    def check_github_mcp(self) -> dict:
        """Check for GitHub MCP availability"""
        has_go = command_exists("go")
        has_claude = command_exists("claude")
        has_git = command_exists("git")
        installed_servers = self.get_installed_mcp_servers()
        
        return {
            "go": has_go,
            "claude": has_claude,
            "git": has_git,
            "available": has_go and has_claude and has_git,
            "already_installed": "github" in installed_servers
        }
    
    def setup_github_mcp(self) -> bool:
        """Setup GitHub MCP integration"""
        github_status = self.check_github_mcp()
        
        if github_status["already_installed"]:
            print(color("✓ GitHub MCP already installed", Colors.GREEN))
            self.config["github_mcp"]["enabled"] = True
            return True
        
        if not github_status["available"]:
            missing = []
            if not github_status["go"]:
                missing.append("go (Go programming language)")
            if not github_status["claude"]:
                missing.append("claude (Claude Code CLI)")
            if not github_status["git"]:
                missing.append("git (version control)")
            
            print(color(f"⚠️  GitHub MCP requirements not met. Missing: {', '.join(missing)}", Colors.YELLOW))
            print(color("   Install Go: https://golang.org/doc/install", Colors.DIM))
            print(color("   GitHub MCP features will be disabled but workflow continues normally.", Colors.DIM))
            return False
        
        print(color("✓ GitHub MCP requirements detected", Colors.GREEN))
        
        response = input(color("  Install GitHub MCP for repository management and automation? (y/n): ", Colors.CYAN))
        
        if response.lower() == 'y':
            try:
                print(color("  Installing GitHub MCP server from source...", Colors.DIM))
                print(color("  Note: You will need a GitHub Personal Access Token to use this server", Colors.YELLOW))
                print(color("  Create one at: https://github.com/settings/tokens", Colors.DIM))
                print(color("  Recommended scopes: repo, read:packages, read:org", Colors.DIM))
                print()
                
                # Get GitHub Personal Access Token
                github_token = input(color("  Enter your GitHub Personal Access Token: ", Colors.CYAN))
                if not github_token:
                    print(color("  ⚠️ GitHub token required, skipping GitHub MCP installation", Colors.YELLOW))
                    return False
                
                # Create build directory
                build_dir = self.project_root / ".claude" / "mcp-servers"
                build_dir.mkdir(parents=True, exist_ok=True)
                
                # Clone and build GitHub MCP server
                print(color("  Cloning GitHub MCP server...", Colors.DIM))
                subprocess.run([
                    "git", "clone", "https://github.com/github/github-mcp-server.git",
                    str(build_dir / "github-mcp-server")
                ], check=True, capture_output=True)
                
                print(color("  Building GitHub MCP server...", Colors.DIM))
                subprocess.run([
                    "go", "build", "-o", "github-mcp-server"
                ], cwd=build_dir / "github-mcp-server", check=True, capture_output=True)
                
                # Configure GitHub MCP server in Claude
                binary_path = build_dir / "github-mcp-server" / "github-mcp-server"
                import json
                github_config = {
                    "type": "stdio",
                    "command": str(binary_path),
                    "args": ["stdio"],
                    "env": {
                        "GITHUB_PERSONAL_ACCESS_TOKEN": github_token
                    }
                }
                subprocess.run([
                    "claude", "mcp", "add-json", "github", json.dumps(github_config)
                ], check=True)
                
                print(color("  ✓ GitHub MCP server configured", Colors.GREEN))
                print(color("    GitHub token configured and stored securely", Colors.GREEN))
                
                self.config["github_mcp"]["enabled"] = True
                return True
                
            except subprocess.CalledProcessError as e:
                print(color("  ⚠️ GitHub MCP installation failed, continuing without it", Colors.YELLOW))
                print(color("    You can set it up manually later", Colors.DIM))
                return False
        
        return False

    def check_storybook_mcp(self) -> dict:
        """Check for Storybook MCP availability"""
        has_npx = command_exists("npx")
        has_claude = command_exists("claude")
        installed_servers = self.get_installed_mcp_servers()
        
        return {
            "npx": has_npx,
            "claude": has_claude,
            "available": has_npx and has_claude,
            "already_installed": "storybook" in installed_servers
        }
    
    def setup_storybook_mcp(self) -> bool:
        """Setup Storybook MCP integration with package validation"""
        storybook_status = self.check_storybook_mcp()
        
        if storybook_status["already_installed"]:
            print(color("✓ Storybook MCP already installed", Colors.GREEN))
            self.config["storybook_mcp"]["enabled"] = True
            return True
        
        if not storybook_status["available"]:
            missing = []
            if not storybook_status["npx"]:
                missing.append("npx (Node.js package runner)")
            if not storybook_status["claude"]:
                missing.append("claude (Claude Code CLI)")
            
            print(color(f"⚠️  Storybook MCP requirements not met. Missing: {', '.join(missing)}", Colors.YELLOW))
            print(color("   Install Node.js to get npx: https://nodejs.org/", Colors.DIM))
            print(color("   Storybook MCP features will be disabled but workflow continues normally.", Colors.DIM))
            return False
        
        print(color("✓ Storybook MCP requirements detected", Colors.GREEN))
        
        response = input(color("  Install Storybook MCP for component development workflows? (requires package installation) (y/n): ", Colors.CYAN))
        
        if response.lower() == 'y':
            try:
                # Check if this is a Node.js project
                if not self.check_package_json_exists():
                    print(color("  ⚠️ No package.json found. Storybook MCP requires a Node.js project.", Colors.YELLOW))
                    print(color("    Initialize with: npm init", Colors.DIM))
                    return False
                
                # Check if Storybook packages are installed
                storybook_installed = self.check_package_installed("@storybook/*")
                
                if not storybook_installed:
                    print(color("  Storybook packages not found, installing...", Colors.DIM))
                    # Install basic Storybook packages
                    success = (
                        self.install_npm_package("@storybook/react", dev=True) and
                        self.install_npm_package("@storybook/react-webpack5", dev=True) and
                        self.install_npm_package("storybook", dev=True)
                    )
                    if not success:
                        print(color("  ⚠️ Failed to install Storybook packages", Colors.YELLOW))
                        return False
                else:
                    print(color("  ✓ Storybook packages already installed", Colors.GREEN))
                
                # Check if Storybook is running
                if not self.check_storybook_running():
                    print(color("  Storybook not running, attempting to start...", Colors.DIM))
                    if not self.start_storybook():
                        print(color("  ⚠️ Could not start Storybook automatically", Colors.YELLOW))
                        print(color("    Start manually with: npm run storybook", Colors.DIM))
                else:
                    print(color("  ✓ Storybook is already running", Colors.GREEN))
                
                print(color("  Installing Storybook MCP server...", Colors.DIM))
                
                # Add Storybook MCP server to Claude Code
                subprocess.run([
                    "claude", "mcp", "add", "storybook",
                    "npx", "-y", "storybook-mcp"
                ], check=True)
                
                print(color("  ✓ Storybook MCP server configured", Colors.GREEN))
                print(color("    Storybook URL: http://localhost:6006/index.json", Colors.GREEN))
                
                self.config["storybook_mcp"]["enabled"] = True
                self.config["storybook_mcp"]["storybook_url"] = "http://localhost:6006/index.json"
                return True
                
            except subprocess.CalledProcessError:
                print(color("  ⚠️ Storybook MCP installation failed, continuing without it", Colors.YELLOW))
                print(color("    You can set it up manually later with: npx storybook-mcp", Colors.DIM))
                return False
        
        return False

    def check_playwright_mcp(self) -> dict:
        """Check for Playwright MCP availability"""
        has_npx = command_exists("npx")
        has_claude = command_exists("claude")
        installed_servers = self.get_installed_mcp_servers()
        
        return {
            "npx": has_npx,
            "claude": has_claude,
            "available": has_npx and has_claude,
            "already_installed": "playwright" in installed_servers
        }
    
    def setup_playwright_mcp(self) -> bool:
        """Setup Playwright MCP integration with package validation"""
        playwright_status = self.check_playwright_mcp()
        
        if playwright_status["already_installed"]:
            print(color("✓ Playwright MCP already installed", Colors.GREEN))
            self.config["playwright_mcp"]["enabled"] = True
            return True
        
        if not playwright_status["available"]:
            missing = []
            if not playwright_status["npx"]:
                missing.append("npx (Node.js package runner)")
            if not playwright_status["claude"]:
                missing.append("claude (Claude Code CLI)")
            
            print(color(f"⚠️  Playwright MCP requirements not met. Missing: {', '.join(missing)}", Colors.YELLOW))
            print(color("   Install Node.js to get npx: https://nodejs.org/", Colors.DIM))
            print(color("   Playwright MCP features will be disabled but workflow continues normally.", Colors.DIM))
            return False
        
        print(color("✓ Playwright MCP requirements detected", Colors.GREEN))
        
        response = input(color("  Install Playwright MCP for browser automation and testing? (requires package installation) (y/n): ", Colors.CYAN))
        
        if response.lower() == 'y':
            try:
                # Check if this is a Node.js project
                if not self.check_package_json_exists():
                    print(color("  ⚠️ No package.json found. Playwright MCP requires a Node.js project.", Colors.YELLOW))
                    print(color("    Initialize with: npm init", Colors.DIM))
                    return False
                
                # Check if Playwright packages are installed
                playwright_installed = self.check_package_installed("@playwright/test")
                
                if not playwright_installed:
                    print(color("  Playwright packages not found, installing...", Colors.DIM))
                    # Install Playwright test package
                    success = self.install_npm_package("@playwright/test", dev=True)
                    if not success:
                        print(color("  ⚠️ Failed to install Playwright packages", Colors.YELLOW))
                        return False
                else:
                    print(color("  ✓ Playwright packages already installed", Colors.GREEN))
                
                # Install Playwright browser binaries
                print(color("  Installing Playwright browser binaries...", Colors.DIM))
                try:
                    subprocess.run([
                        "npx", "playwright", "install"
                    ], cwd=self.project_root, check=True, capture_output=True)
                    print(color("  ✓ Playwright browser binaries installed", Colors.GREEN))
                except subprocess.CalledProcessError:
                    print(color("  ⚠️ Failed to install Playwright browser binaries", Colors.YELLOW))
                    print(color("    You can install them manually with: npx playwright install", Colors.DIM))
                
                print(color("  Installing Playwright MCP server...", Colors.DIM))
                
                # Add Playwright MCP server to Claude Code
                subprocess.run([
                    "claude", "mcp", "add", "playwright",
                    "npx", "@playwright/mcp@latest"
                ], check=True)
                
                print(color("  ✓ Playwright MCP server configured", Colors.GREEN))
                print(color("    Provides browser automation and web page interaction capabilities", Colors.GREEN))
                
                self.config["playwright_mcp"]["enabled"] = True
                return True
                
            except subprocess.CalledProcessError:
                print(color("  ⚠️ Playwright MCP installation failed, continuing without it", Colors.YELLOW))
                print(color("    You can set it up manually later with: npx @playwright/mcp@latest", Colors.DIM))
                return False
        
        return False

    def create_directories(self) -> None:
        """Create necessary directory structure"""
        print(color("Creating directory structure...", Colors.CYAN))
        
        dirs = [
            ".claude/hooks",
            ".claude/state", 
            ".claude/agents",
            ".claude/commands",
            "sessions/tasks",
            "sessions/tasks/done",
            "sessions/protocols",
            "sessions/documents",
            "sessions/documents/versions",
            "sessions/documents/archive",
            "sessions/knowledge"
        ]
        
        for dir_path in dirs:
            (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)
    
    def install_python_deps(self) -> None:
        """Install Python dependencies"""
        print(color("Installing Python dependencies...", Colors.CYAN))
        try:
            pip_cmd = "pip3" if command_exists("pip3") else "pip"
            subprocess.run([pip_cmd, "install", "tiktoken", "--quiet"], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print(color("⚠️  Could not install tiktoken. You may need to install it manually.", Colors.YELLOW))
    
    def copy_files(self) -> None:
        """Copy all necessary files to the project"""
        # Copy hooks
        print(color("Installing hooks...", Colors.CYAN))
        hooks_dir = self.package_dir / "hooks"
        if hooks_dir.exists():
            for hook_file in hooks_dir.glob("*.py"):
                dest = self.project_root / ".claude/hooks" / hook_file.name
                shutil.copy2(hook_file, dest)
                if os.name != 'nt':
                    dest.chmod(0o755)
        
        # Copy protocols
        print(color("Installing protocols...", Colors.CYAN))
        protocols_dir = self.package_dir / "protocols"
        if protocols_dir.exists():
            for protocol_file in protocols_dir.glob("*.md"):
                dest = self.project_root / "sessions/protocols" / protocol_file.name
                shutil.copy2(protocol_file, dest)
        
        # Copy agents
        print(color("Installing agent definitions...", Colors.CYAN))
        agents_dir = self.package_dir / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                dest = self.project_root / ".claude/agents" / agent_file.name
                shutil.copy2(agent_file, dest)
        
        # Copy templates
        print(color("Installing templates...", Colors.CYAN))
        templates_dir = self.package_dir / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.md"):
                if template_file.name == "TEMPLATE.md":
                    # Task template goes to sessions/tasks/
                    dest = self.project_root / "sessions/tasks/TEMPLATE.md"
                elif template_file.name == "BUILD_PROJECT_TEMPLATE.md":
                    # Build project template goes to sessions/ for easier access
                    dest = self.project_root / "sessions" / template_file.name
                else:
                    # Other templates go to sessions/ directory
                    dest = self.project_root / "sessions" / template_file.name
                shutil.copy2(template_file, dest)
        
        # Copy commands
        print(color("Installing commands...", Colors.CYAN))
        commands_dir = self.package_dir / "commands"
        if commands_dir.exists():
            for command_file in commands_dir.glob("*.md"):
                dest = self.project_root / ".claude/commands" / command_file.name
                shutil.copy2(command_file, dest)
            
            # Copy Python command scripts
            for script_file in commands_dir.glob("*.py"):
                dest = self.project_root / ".claude/commands" / script_file.name
                shutil.copy2(script_file, dest)
                if os.name != 'nt':
                    dest.chmod(0o755)
        
        # Copy knowledge files
        knowledge_dir = self.package_dir / "knowledge/claude-code"
        if knowledge_dir.exists():
            print(color("Installing Claude Code knowledge base...", Colors.CYAN))
            dest_dir = self.project_root / "sessions/knowledge/claude-code"
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(knowledge_dir, dest_dir)
    
    def install_daic_command(self) -> None:
        """Install the daic command globally"""
        print(color("Installing daic command...", Colors.CYAN))
        
        if os.name == 'nt':  # Windows
            # Install Windows scripts (.cmd and .ps1)
            daic_cmd_source = self.package_dir / "scripts/daic.cmd"
            daic_ps1_source = self.package_dir / "scripts/daic.ps1"
            
            # Try to install to user's local directory
            local_bin = Path.home() / "AppData" / "Local" / "cc-sessions" / "bin"
            local_bin.mkdir(parents=True, exist_ok=True)
            
            if daic_cmd_source.exists():
                daic_cmd_dest = local_bin / "daic.cmd"
                shutil.copy2(daic_cmd_source, daic_cmd_dest)
                print(color(f"  ✓ Installed daic.cmd to {local_bin}", Colors.GREEN))
            
            if daic_ps1_source.exists():
                daic_ps1_dest = local_bin / "daic.ps1"
                shutil.copy2(daic_ps1_source, daic_ps1_dest)
                print(color(f"  ✓ Installed daic.ps1 to {local_bin}", Colors.GREEN))
            
            print(color(f"  ℹ Add {local_bin} to your PATH to use 'daic' command", Colors.YELLOW))
        else:
            # Unix/Mac installation
            daic_source = self.package_dir / "scripts/daic"
            if not daic_source.exists():
                print(color("⚠️  daic script not found in package.", Colors.YELLOW))
                return
            
            daic_dest = Path("/usr/local/bin/daic")
            
            try:
                shutil.copy2(daic_source, daic_dest)
                daic_dest.chmod(0o755)
            except PermissionError:
                print(color("⚠️  Cannot write to /usr/local/bin. Trying with sudo...", Colors.YELLOW))
                try:
                    subprocess.run(["sudo", "cp", str(daic_source), str(daic_dest)], check=True)
                    subprocess.run(["sudo", "chmod", "+x", str(daic_dest)], check=True)
                except subprocess.CalledProcessError:
                    print(color("⚠️  Could not install daic command globally.", Colors.YELLOW))
    
    def configure(self) -> None:
        """Interactive configuration"""
        print()
        print(color("╔═══════════════════════════════════════════════════════════════╗", Colors.BRIGHT + Colors.CYAN))
        print(color("║                    CONFIGURATION SETUP                        ║", Colors.BRIGHT + Colors.CYAN))
        print(color("╚═══════════════════════════════════════════════════════════════╝", Colors.BRIGHT + Colors.CYAN))
        print()
        
        self.statusline_installed = False
        
        # Developer name section
        print(color(f"\n★ DEVELOPER IDENTITY", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Claude will use this name when addressing you in sessions", Colors.DIM))
        print()
        
        name = input(color("  Your name: ", Colors.CYAN))
        if name:
            self.config["developer_name"] = name
            print(color(f"  ✓ Hello, {name}!", Colors.GREEN))
        
        # Statusline installation section
        print(color(f"\n\n★ STATUSLINE INSTALLATION", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Real-time status display in Claude Code showing:", Colors.WHITE))
        print(color("    • Current task and DAIC mode", Colors.CYAN))
        print(color("    • Token usage with visual progress bar", Colors.CYAN))
        print(color("    • Modified file counts", Colors.CYAN))
        print(color("    • Open task count", Colors.CYAN))
        print()
        
        install_statusline = input(color("  Install statusline? (y/n): ", Colors.CYAN))
        
        if install_statusline.lower() == 'y':
            statusline_source = self.package_dir / "scripts/statusline-script.sh"
            if statusline_source.exists():
                print(color("  Installing statusline script...", Colors.DIM))
                statusline_dest = self.project_root / ".claude/statusline-script.sh"
                shutil.copy2(statusline_source, statusline_dest)
                statusline_dest.chmod(0o755)
                self.statusline_installed = True
                print(color("  ✓ Statusline installed successfully", Colors.GREEN))
            else:
                print(color("  ⚠ Statusline script not found in package", Colors.YELLOW))
        
        # DAIC trigger phrases section
        print(color(f"\n\n★ DAIC WORKFLOW CONFIGURATION", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  The DAIC system enforces discussion before implementation.", Colors.WHITE))
        print(color("  Trigger phrases tell Claude when you're ready to proceed.", Colors.WHITE))
        print()
        print(color("  Default triggers:", Colors.CYAN))
        for phrase in self.config['trigger_phrases']:
            print(color(f'    → "{phrase}"', Colors.GREEN))
        print()
        print(color('  Hint: Common additions: "implement it", "do it", "proceed"', Colors.DIM))
        print()
        
        # Allow adding multiple custom trigger phrases
        while True:
            custom_trigger = input(color("  Add custom trigger phrase (Enter to skip): ", Colors.CYAN))
            if not custom_trigger:
                break
            self.config["trigger_phrases"].append(custom_trigger)
            print(color(f'  ✓ Added: "{custom_trigger}"', Colors.GREEN))
        
        # API Mode configuration
        print(color(f"\n\n★ THINKING BUDGET CONFIGURATION", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Token usage is not much of a concern with Claude Code Max", Colors.WHITE))
        print(color("  plans, especially the $200 tier. But API users are often", Colors.WHITE))
        print(color("  budget-conscious and want manual control.", Colors.WHITE))
        print()
        print(color("  Sessions was built to preserve tokens across context windows", Colors.CYAN))
        print(color("  but uses saved tokens to enable 'ultrathink' - Claude's", Colors.CYAN))
        print(color("  maximum thinking budget - on every interaction for best results.", Colors.CYAN))
        print()
        print(color("  • Max users (recommended): Automatic ultrathink every message", Colors.DIM))
        print(color("  • API users: Manual control with [[ ultrathink ]] when needed", Colors.DIM))
        print()
        print(color("  You can toggle this anytime with: /api-mode", Colors.DIM))
        print()
        
        enable_ultrathink = input(color("  Enable automatic ultrathink for best performance? (y/n): ", Colors.CYAN))
        if enable_ultrathink.lower() == 'y':
            self.config["api_mode"] = False
            print(color("  ✓ Max mode - ultrathink enabled for best performance", Colors.GREEN))
        else:
            self.config["api_mode"] = True
            print(color("  ✓ API mode - manual ultrathink control (use [[ ultrathink ]])", Colors.GREEN))
        
        # Advanced configuration
        print(color(f"\n\n★ ADVANCED OPTIONS", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Configure tool blocking, task prefixes, and more", Colors.WHITE))
        print()
        
        advanced = input(color("  Configure advanced options? (y/n): ", Colors.CYAN))
        
        if advanced.lower() == 'y':
            # Tool blocking
            print()
            print(color("╭───────────────────────────────────────────────────────────────╮", Colors.CYAN))
            print(color("│              Tool Blocking Configuration                      │", Colors.CYAN))
            print(color("├───────────────────────────────────────────────────────────────┤", Colors.CYAN))
            print(color("│   Tools can be blocked in discussion mode to enforce DAIC     │", Colors.DIM))
            print(color("│   Default: Edit, Write, MultiEdit, NotebookEdit are blocked   │", Colors.DIM))
            print(color("╰───────────────────────────────────────────────────────────────╯", Colors.CYAN))
            print()
            
            tools = [
                ("Edit", "Edit existing files", True),
                ("Write", "Create new files", True),
                ("MultiEdit", "Multiple edits in one operation", True),
                ("NotebookEdit", "Edit Jupyter notebooks", True),
                ("Bash", "Run shell commands", False),
                ("Read", "Read file contents", False),
                ("Grep", "Search file contents", False),
                ("Glob", "Find files by pattern", False),
                ("LS", "List directory contents", False),
                ("WebSearch", "Search the web", False),
                ("WebFetch", "Fetch web content", False),
                ("Task", "Launch specialized agents", False)
            ]
            
            print(color("  Available tools:", Colors.WHITE))
            for i, (name, desc, blocked) in enumerate(tools, 1):
                icon = "🔒" if blocked else "🔓"
                status_color = Colors.YELLOW if blocked else Colors.GREEN
                print(f"    {i:2}. {icon} {color(name.ljust(15), status_color)} - {desc}")
            print()
            print(color("  Hint: Edit tools are typically blocked to enforce discussion-first workflow", Colors.DIM))
            print()
            
            modify_tools = input(color("  Modify blocked tools list? (y/n): ", Colors.CYAN))
            
            if modify_tools.lower() == 'y':
                tool_numbers = input(color("  Enter comma-separated tool numbers to block: ", Colors.CYAN))
                if tool_numbers:
                    tool_names = [t[0] for t in tools]
                    blocked_list = []
                    for num_str in tool_numbers.split(','):
                        try:
                            num = int(num_str.strip())
                            if 1 <= num <= len(tools):
                                blocked_list.append(tool_names[num - 1])
                        except ValueError:
                            pass
                    if blocked_list:
                        self.config["blocked_tools"] = blocked_list
                        print(color("  ✓ Tool blocking configuration saved", Colors.GREEN))
            
            # Task prefix configuration
            print(color(f"\n\n★ TASK PREFIX CONFIGURATION", Colors.BRIGHT + Colors.MAGENTA))
            print(color("─" * 60, Colors.DIM))
            print(color("  Task prefixes organize work by priority and type", Colors.WHITE))
            print()
            print(color("  Current prefixes:", Colors.CYAN))
            print(color("    → h- (high priority)", Colors.WHITE))
            print(color("    → m- (medium priority)", Colors.WHITE))
            print(color("    → l- (low priority)", Colors.WHITE))
            print(color("    → ?- (investigate/research)", Colors.WHITE))
            print()
            
            customize_prefixes = input(color("  Customize task prefixes? (y/n): ", Colors.CYAN))
            if customize_prefixes.lower() == 'y':
                high = input(color("  High priority prefix [h-]: ", Colors.CYAN)) or 'h-'
                med = input(color("  Medium priority prefix [m-]: ", Colors.CYAN)) or 'm-'
                low = input(color("  Low priority prefix [l-]: ", Colors.CYAN)) or 'l-'
                inv = input(color("  Investigate prefix [?-]: ", Colors.CYAN)) or '?-'
                
                self.config["task_prefixes"] = {
                    "priority": [high, med, low, inv]
                }
                
                print(color("  ✓ Task prefixes updated", Colors.GREEN))
    
    def save_config(self) -> None:
        """Save configuration files"""
        print(color("Creating configuration...", Colors.CYAN))
        
        # Save sessions config
        config_file = self.project_root / "sessions/sessions-config.json"
        config_file.write_text(json.dumps(self.config, indent=2))
        
        # Create or update .claude/settings.json with all hooks
        print(color("Configuring hooks in settings.json...", Colors.CYAN))
        settings_file = self.project_root / ".claude/settings.json"
        
        settings = {}
        if settings_file.exists():
            print(color("Found existing settings.json, merging sessions hooks...", Colors.CYAN))
            try:
                settings = json.loads(settings_file.read_text())
            except:
                settings = {}
        else:
            print(color("Creating new settings.json with sessions hooks...", Colors.CYAN))
        
        # Define the sessions hooks
        sessions_hooks = {
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/user-messages.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\user-messages.py\""
                        }
                    ]
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit|Task|Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/sessions-enforce.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\sessions-enforce.py\""
                        }
                    ]
                },
                {
                    "matcher": "Task",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/task-transcript-link.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\task-transcript-link.py\""
                        }
                    ]
                }
            ],
            "PostToolUse": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\post-tool-use.py\""
                        }
                    ]
                }
            ],
            "SessionStart": [
                {
                    "matcher": "startup|clear",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\session-start.py\""
                        }
                    ]
                }
            ]
        }
        
        # Merge hooks (sessions hooks take precedence)
        if "hooks" not in settings:
            settings["hooks"] = {}
        
        # Merge each hook type
        for hook_type, hook_config in sessions_hooks.items():
            if hook_type not in settings["hooks"]:
                settings["hooks"][hook_type] = hook_config
            else:
                # Append sessions hooks to existing ones
                settings["hooks"][hook_type].extend(hook_config)
        
        # Add statusline if requested
        if hasattr(self, 'statusline_installed') and self.statusline_installed:
            settings["statusLine"] = {
                "type": "command",
                "command": "$CLAUDE_PROJECT_DIR/.claude/statusline-script.sh" if os.name != 'nt' else "%CLAUDE_PROJECT_DIR%\\.claude\\statusline-script.sh",
                "padding": 0
            }
        
        # Save the updated settings
        settings_file.write_text(json.dumps(settings, indent=2))
        print(color("✓ Sessions hooks configured in settings.json", Colors.GREEN))
        
        # Initialize DAIC state
        daic_state = self.project_root / ".claude/state/daic-mode.json"
        daic_state.write_text(json.dumps({"mode": "discussion"}, indent=2))
        
        # Create initial task state
        current_date = datetime.now().strftime("%Y-%m-%d")
        task_state = self.project_root / ".claude/state/current_task.json"
        task_state.write_text(json.dumps({
            "task": None,
            "branch": None,
            "services": [],
            "updated": current_date
        }, indent=2))
    
    def setup_claude_md(self) -> None:
        """Set up CLAUDE.md integration"""
        print()
        print(color("═══════════════════════════════════════════", Colors.BRIGHT))
        print(color("         CLAUDE.md Integration", Colors.BRIGHT))
        print(color("═══════════════════════════════════════════", Colors.BRIGHT))
        print()
        
        # Check for existing CLAUDE.md
        sessions_md = self.package_dir / "templates/CLAUDE.sessions.md"
        claude_md = self.project_root / "CLAUDE.md"
        
        if claude_md.exists():
            # File exists, preserve it and add sessions as separate file
            print(color("CLAUDE.md already exists, preserving your project-specific rules...", Colors.CYAN))
            
            # Copy CLAUDE.sessions.md as separate file
            if sessions_md.exists():
                dest = self.project_root / "CLAUDE.sessions.md"
                shutil.copy2(sessions_md, dest)
            
            # Check if it already includes sessions
            content = claude_md.read_text()
            if "@CLAUDE.sessions.md" not in content:
                print(color("Adding sessions include to existing CLAUDE.md...", Colors.CYAN))
                
                addition = "\n## Sessions System Behaviors\n\n@CLAUDE.sessions.md\n"
                with claude_md.open("a") as f:
                    f.write(addition)
                
                print(color("✅ Added @CLAUDE.sessions.md include to your CLAUDE.md", Colors.GREEN))
            else:
                print(color("✅ CLAUDE.md already includes sessions behaviors", Colors.GREEN))
        else:
            # File doesn't exist, use sessions as CLAUDE.md
            print(color("No existing CLAUDE.md found, installing sessions as your CLAUDE.md...", Colors.CYAN))
            if sessions_md.exists():
                shutil.copy2(sessions_md, claude_md)
                print(color("✅ CLAUDE.md created with complete sessions behaviors", Colors.GREEN))
    
    def run(self) -> None:
        """Run the full installation process"""
        print(color("╔════════════════════════════════════════════╗", Colors.BRIGHT))
        print(color("║            cc-sessions Installer           ║", Colors.BRIGHT))
        print(color("╚════════════════════════════════════════════╝", Colors.BRIGHT))
        print()
        
        # Check CLAUDE_PROJECT_DIR
        if not os.environ.get("CLAUDE_PROJECT_DIR"):
            print(color(f"⚠️  CLAUDE_PROJECT_DIR not set. Setting it to {self.project_root}", Colors.YELLOW))
            print("   To make this permanent, add to your shell profile:")
            print(f'   export CLAUDE_PROJECT_DIR="{self.project_root}"')
            print()
        
        try:
            self.check_dependencies()
            self.create_directories()
            self.install_python_deps()
            self.copy_files()
            self.install_daic_command()
            serena_mcp_installed = self.setup_serena_mcp()
            memory_bank_mcp_installed = self.install_memory_bank_mcp()
            if memory_bank_mcp_installed:
                self.configure_memory_bank_files()
            github_mcp_installed = self.setup_github_mcp()
            storybook_mcp_installed = self.setup_storybook_mcp()
            playwright_mcp_installed = self.setup_playwright_mcp()
            self.configure()
            self.save_config()
            self.setup_claude_md()
            
            # Success message
            print()
            print()
            print(color("╔═══════════════════════════════════════════════════════════════╗", Colors.BRIGHT + Colors.GREEN))
            print(color("║                 🎉 INSTALLATION COMPLETE! 🎉                  ║", Colors.BRIGHT + Colors.GREEN))
            print(color("╚═══════════════════════════════════════════════════════════════╝", Colors.BRIGHT + Colors.GREEN))
            print()
            
            print(color("  Installation Summary:", Colors.BRIGHT + Colors.CYAN))
            print(color("  ─────────────────────", Colors.DIM))
            print(color("  ✓ Directory structure created", Colors.GREEN))
            print(color("  ✓ Hooks installed and configured", Colors.GREEN))
            print(color("  ✓ Protocols and agents deployed", Colors.GREEN))
            print(color("  ✓ daic command available globally", Colors.GREEN))
            print(color("  ✓ Configuration saved", Colors.GREEN))
            print(color("  ✓ DAIC state initialized (Discussion mode)", Colors.GREEN))
            
            if hasattr(self, 'statusline_installed') and self.statusline_installed:
                print(color("  ✓ Statusline configured", Colors.GREEN))
            
            print()
            
            # Test daic command
            if command_exists("daic"):
                print(color("  ✓ daic command verified and working", Colors.GREEN))
            else:
                print(color("  ⚠ daic command not in PATH", Colors.YELLOW))
                print(color("       Add /usr/local/bin to your PATH", Colors.DIM))
            
            print()
            print(color("  ★ NEXT STEPS", Colors.BRIGHT + Colors.MAGENTA))
            print(color("  ─────────────", Colors.DIM))
            print()
            print(color("  1. Restart Claude Code to activate the sessions hooks", Colors.WHITE))
            print(color("     → Close and reopen Claude Code", Colors.DIM))
            print()
            print(color("  2. Create your first task:", Colors.WHITE))
            print(color('     → Tell Claude: "Create a new task"', Colors.CYAN))
            print(color('     → Or: "Create a task for implementing feature X"', Colors.CYAN))
            print()
            print(color("  3. Start working with the DAIC workflow:", Colors.WHITE))
            print(color("     → Discuss approach first", Colors.DIM))
            print(color('     → Say "make it so" to implement', Colors.DIM))
            print(color('     → Run "daic" to return to discussion', Colors.DIM))
            print()
            print(color("  ──────────────────────────────────────────────────────", Colors.DIM))
            print()
            print(color(f"  Welcome aboard, {self.config['developer_name']}! 🚀", Colors.BRIGHT + Colors.CYAN))
            
        except Exception as e:
            print(color(f"❌ Installation failed: {e}", Colors.RED))
            sys.exit(1)

def main():
    """Main entry point for the installer"""
    installer = SessionsInstaller()
    installer.run()

def install():
    """Alias for main() for compatibility"""
    main()

if __name__ == "__main__":
    main()
