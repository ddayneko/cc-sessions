# Serena MCP Integration with cc-sessions

## Overview

This guide provides detailed instructions for setting up and using the [Serena MCP](https://github.com/oraios/serena) server with the cc-sessions npm package. Serena MCP enhances cc-sessions with semantic code analysis capabilities, transforming basic text-based pattern matching into precise symbol-level analysis for superior code understanding.

## What is Serena MCP?

Serena MCP is a Model Context Protocol server that provides IDE-like semantic analysis for codebases. When integrated with cc-sessions, it enables:

- **Precise Symbol Location**: Find exact definitions instead of text pattern matches
- **Dependency Mapping**: Understand true architectural relationships between components  
- **Surgical Code Operations**: Make targeted insertions and modifications
- **Enhanced Context Gathering**: Reduce token usage while increasing analysis accuracy
- **Architecture Understanding**: Gain insights into WHY code relationships exist

## Installation Methods

### Method 1: Automatic Installation (Recommended)

The easiest way is to install cc-sessions with automatic Serena MCP integration:

```bash
# Install globally via npm
npm install -g cc-sessions

# Or install temporarily 
npx cc-sessions
```

During installation, the cc-sessions installer will:
1. Detect if `uv` and `claude` commands are available
2. Offer optional Serena MCP installation
3. Automatically configure the MCP server in Claude Code
4. Update your sessions configuration

### Method 2: Manual Installation

If you already have cc-sessions installed or want manual control:

#### Step 1: Install Prerequisites

**Install uv (Python package manager):**
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Alternative: via pip
pip install uv
```

**Verify Claude Code CLI is installed:**
```bash
claude --version
```

#### Step 2: Add Serena MCP Server

```bash
# Add the MCP server to Claude Code
claude mcp add serena sh -c "uvx --from git+https://github.com/oraios/serena serena start-mcp-server"
```

#### Step 3: Configure cc-sessions

Edit your `sessions/sessions-config.json` file:

```json
{
  "serena_mcp": {
    "enabled": true,
    "auto_activate": true
  }
}
```

#### Step 4: Activate Your Project

In Claude Code, tell Claude to activate your project:
```
"Activate the project /path/to/your/project"
```

## Verification

Verify your installation works correctly:

### Check MCP Server Status
```bash
claude mcp list
```

You should see `serena` in the list of configured servers.

### Test Basic Functionality

In Claude Code, ask Claude to test the integration:
```
"Can you test if Serena MCP is working? Try finding a symbol in this project."
```

### Run Test Script

You can also run the included test scripts:

```bash
# Test current setup
python test_serena_fixed.py

# Debug any issues
python test_serena.py
```

## Available Features

### Enhanced Agents

With Serena MCP enabled, cc-sessions provides two enhanced agents:

**1. Semantic Analysis Agent**
- Pure semantic operations for architecture analysis
- Precise dependency mapping and relationship understanding
- Surgical code modifications with symbol-level precision

**2. Enhanced Context-Gathering Agent**  
- Hybrid approach: semantic analysis first, then targeted text search
- Dramatically reduced token usage
- Higher accuracy in understanding code relationships

### MCP Tools Available

- `mcp__serena__find_symbol` - Locate exact symbol definitions
- `mcp__serena__find_referencing_symbols` - Map all dependencies of a symbol
- `mcp__serena__get_symbol_definition` - Get complete symbol definitions with context
- `mcp__serena__list_symbols` - List all symbols in a file
- `mcp__serena__insert_after_symbol` - Make surgical code insertions

## Usage Examples

### Example 1: Finding a Component

**Without Serena MCP:**
```bash
# Claude would run something like:
grep -r "UserAuth" src/ | head -20
# Then read entire files to understand relationships
```

**With Serena MCP:**
```bash
# Claude uses semantic analysis:
find_symbol("UserAuth") → src/auth/user.py:45
find_referencing_symbols("UserAuth") → [
  src/controllers/login.py:12,
  src/middleware/auth.py:8, 
  src/services/session.py:23
]
# Precise locations, no need to read entire files
```

### Example 2: Context Gathering for a Task

When you create a task that involves modifying authentication:

**Traditional approach:**
- Grep for auth-related patterns across codebase
- Read many entire files to understand relationships
- High token usage, potential to miss connections

**With Serena MCP:**
- Find exact auth component locations
- Map all dependencies semantically
- Understand architectural relationships
- Targeted text search only for business logic context
- Much lower token usage, higher accuracy

### Example 3: Code Review Enhancement

**Traditional:**
- Text-based pattern matching for code review
- Manual analysis of potential security issues
- Assumptions about code relationships

**With Serena MCP:**
- Symbol-level security flow analysis
- Precise understanding of data flow
- True dependency impact analysis
- Semantic consistency checking

## Troubleshooting

### Common Issues

#### "Serena MCP requirements not met"

**Symptoms:** Installation fails with missing requirements message

**Solutions:**
1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Ensure Claude Code CLI is available: `claude --version`
3. Restart your terminal after installing uv
4. On Windows, ensure PATH is updated for uv

#### "Semantic analysis unavailable"

**Symptoms:** Claude reports fallback to text-based analysis

**Solutions:**
1. Check MCP server status: `claude mcp list`
2. Verify project activation: Tell Claude "Activate the project /path/to/project"
3. Restart Claude Code
4. Check if Serena MCP server is running properly

#### "Symbol not found"

**Symptoms:** Serena MCP can't locate symbols you know exist

**Solutions:**
1. Wait for project indexing (may take time for large codebases)
2. Try alternative symbol names or patterns
3. Verify the symbol exists in the currently activated project
4. Use broader text search as fallback

#### Claude MCP Add Command Fails

**Symptoms:** `claude mcp add` command returns errors

**Solutions:**

Try alternative command formats:

```bash
# Method 1: Direct uvx command 
claude mcp add serena uvx --from git+https://github.com/oraios/serena serena start-mcp-server

# Method 2: Shell wrapper (recommended)
claude mcp add serena sh -c "uvx --from git+https://github.com/oraios/serena serena start-mcp-server"

# Method 3: Test basic uvx functionality first
uvx --from git+https://github.com/oraios/serena serena --help
```

### Debug Steps

1. **Check prerequisites:**
   ```bash
   which uv        # Should show path to uv
   claude --version # Should show Claude Code version
   ```

2. **Verify MCP server:**
   ```bash
   claude mcp list  # Should show serena in list
   ```

3. **Test basic functionality:**
   ```bash
   python test_serena_fixed.py
   ```

4. **Check project activation:**
   In Claude Code: "What project is currently activated?"

5. **Review configuration:**
   ```bash
   cat sessions/sessions-config.json | grep serena_mcp
   ```

## Platform-Specific Notes

### Windows
- Use PowerShell or Command Prompt
- The installer creates both `.cmd` and `.ps1` versions of daic command
- uv installation may require PATH refresh

### macOS
- Works with Terminal, iTerm2, and other standard terminals
- Supports both Bash and Zsh shells
- May require `xcode-select --install` for some dependencies

### Linux
- Tested on major distributions
- Requires Python 3.8+ 
- May need to install build tools for some dependencies

## Benefits Summary

### For Developers
- **Faster Analysis**: Precise symbol-level operations vs text searching
- **Better Understanding**: True architectural relationships vs assumptions
- **Token Efficiency**: Reduced context window usage
- **Higher Quality**: More accurate code analysis and suggestions

### For AI Workflows
- **Enhanced Precision**: Exact locations instead of pattern matching
- **Improved Context**: Better understanding of code relationships
- **Reduced Errors**: Less confusion from similar-looking code patterns
- **Graceful Fallback**: Full functionality even when MCP unavailable

## Getting Help

### Documentation
- [cc-sessions GitHub Repository](https://github.com/GWUDCAP/cc-sessions)
- [Serena MCP Repository](https://github.com/oraios/serena)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

### Support
- Report issues at: https://github.com/GWUDCAP/cc-sessions/issues
- Include your platform, installation method, and error messages
- Provide output from test scripts when possible

### Community
- Share usage patterns and tips in GitHub discussions
- Contribute improvements to documentation and code
- Help others with setup and configuration issues

# Memory Bank MCP Integration

## Overview

Memory Bank MCP provides persistent context storage and analysis capabilities that complement cc-sessions with long-term memory across development sessions. This integration enables document consistency validation, historical context preservation, and intelligent content management.

## What is Memory Bank MCP?

Memory Bank MCP is a centralized service for managing memory banks across multiple projects. Key capabilities include:

- **Persistent Context Storage**: Maintain project context across sessions
- **Document Management**: Store and retrieve PRD, FSD, and other critical documents
- **Multi-Project Support**: Isolated memory banks for different projects
- **Remote Accessibility**: Centralized access to memory bank files
- **Type-Safe Operations**: Secure read/write operations with validation

## Installation Methods

### Method 1: Automatic Installation (Recommended)

Memory Bank MCP installation is included in the cc-sessions installation process:

```bash
# During cc-sessions installation, when prompted:
Install Memory Bank MCP for persistent context analysis? (y/n): y
```

The installer will:
1. Check for `npx` and `claude` availability
2. Install Memory Bank MCP server using Smithery
3. Create default memory bank directory structure
4. Configure the MCP server in Claude Code

### Method 2: Manual Installation

**Prerequisites:**
- Node.js (for npx)
- Claude Code CLI

**Installation:**
```bash
# Install Memory Bank MCP server
npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude

# Verify installation
claude mcp list
```

**Configuration:**
1. Set environment variable (optional):
   ```bash
   export MEMORY_BANK_ROOT="/path/to/memory/banks"
   ```

2. Update `sessions/sessions-config.json`:
   ```json
   {
     "memory_bank_mcp": {
       "enabled": true,
       "auto_activate": true,
       "memory_bank_root": "/path/to/sessions/memory_bank"
     }
   }
   ```

## Available Tools

### Memory Bank MCP Tools
- `mcp__memory_bank__read_file` - Read memory bank files
- `mcp__memory_bank__write_file` - Write new memory bank files
- `mcp__memory_bank__update_file` - Update existing memory bank files
- `mcp__memory_bank__list_projects` - List available projects
- `mcp__memory_bank__list_files` - List files within projects

### Enhanced Agent Capabilities

**Context-Gathering Agent Enhancement:**
- Historical context retrieval from previous sessions
- PRD/FSD document alignment validation
- Persistent context storage for future sessions
- Multi-session continuity for complex tasks

## Usage Examples

### Example 1: Project Context Preservation

When working on a task, Memory Bank MCP automatically:
```bash
# Claude checks for existing project context
list_projects() → ["my-app", "api-service"]
list_files("my-app") → ["PRD.md", "FSD.md", "architecture.md"]

# Retrieves relevant documents
read_file("my-app", "PRD.md") → Product requirements
read_file("my-app", "FSD.md") → Functional specifications

# Validates new changes against existing documents
# Stores updated context for future sessions
write_file("my-app", "task_context_auth.md", comprehensive_analysis)
```

### Example 2: Document Consistency Validation

**Before implementing changes:**
- Memory Bank retrieves PRD and FSD documents
- Context-gathering agent validates proposed changes against requirements
- Ensures implementation aligns with documented specifications

**During implementation:**
- Changes are cross-referenced with stored architectural decisions
- Historical context prevents repeating resolved issues
- Maintains consistency across development sessions

### Example 3: Session Continuity

**Starting a new session:**
```bash
# Memory Bank provides immediate context restoration
"I'm working on authentication. What context do you have?"

# Claude retrieves:
- Previous analysis from memory_bank/my-app/auth_context.md
- Requirements from memory_bank/my-app/PRD.md
- Architecture decisions from memory_bank/my-app/architecture.md
```

## Configuration Options

### Project Structure

Memory Bank creates organized project structures:
```
sessions/memory_bank/
├── project-name/
│   ├── PRD.md                 # Product Requirements Document
│   ├── FSD.md                 # Functional Specification Document  
│   ├── architecture.md        # Architectural decisions
│   ├── task_contexts/         # Task-specific context files
│   └── decisions/             # Historical decisions and rationale
```

### Configuration Parameters

**sessions-config.json:**
```json
{
  "memory_bank_mcp": {
    "enabled": true,
    "auto_activate": true,
    "memory_bank_root": "sessions/memory_bank",
    "project_name": "my-project",
    "auto_preserve_context": true,
    "document_validation": true
  }
}
```

## Benefits for cc-sessions

### Enhanced Context Management
- **Session Continuity**: Context preserved across sessions
- **Document Alignment**: Changes validated against PRD/FSD
- **Historical Memory**: Previous decisions and analysis available
- **Multi-Project Support**: Isolated contexts for different projects

### Improved Development Workflow
- **Reduced Ramp-up**: Immediate context restoration
- **Consistency Enforcement**: Automated validation against requirements
- **Knowledge Preservation**: Critical decisions and rationale stored
- **Collaborative Memory**: Shared context across team members

## Troubleshooting

### Common Issues

#### "Memory Bank MCP requirements not met"
**Solutions:**
1. Install Node.js: https://nodejs.org/
2. Ensure Claude Code CLI is available: `claude --version`
3. Check npx availability: `npx --version`

#### "Memory Bank server not found"
**Solutions:**
1. Verify MCP server installation: `claude mcp list`
2. Reinstall if missing:
   ```bash
   npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude
   ```

#### "Project context not found"
**Solutions:**
1. Initialize project context:
   ```bash
   # In Claude Code:
   "Initialize Memory Bank for this project"
   ```
2. Verify memory bank root directory exists
3. Check project name configuration

#### "Memory bank access denied"
**Solutions:**
1. Check directory permissions for memory_bank_root
2. Verify MEMORY_BANK_ROOT environment variable
3. Ensure Claude Code has access to the memory bank directory

### Debug Steps

1. **Check MCP server status:**
   ```bash
   claude mcp list | grep memory-bank
   ```

2. **Verify memory bank directory:**
   ```bash
   ls -la sessions/memory_bank/
   ```

3. **Test basic functionality:**
   In Claude Code: "List all projects in Memory Bank"

4. **Check configuration:**
   ```bash
   cat sessions/sessions-config.json | grep memory_bank_mcp
   ```

## Integration with Other MCP Servers

### Memory Bank + Serena MCP

When both are available:
- **Serena** provides semantic analysis and precise symbol mapping
- **Memory Bank** provides persistent context and document validation
- **Combined**: Comprehensive analysis with long-term memory and validation

### Workflow Enhancement

1. **Context Gathering**: Memory Bank retrieves historical context
2. **Semantic Analysis**: Serena provides precise code analysis
3. **Validation**: Changes validated against stored requirements
4. **Preservation**: Updated context stored for future sessions

---

# Document Governance Integration

## Overview

The Document Governance system builds on Memory Bank MCP to provide comprehensive document-driven development with automated context retention, document validation, and version management. This integration ensures all code changes align with project requirements while maintaining complete development history.

## Key Features

### Automated Context Retention
- **Pre-Implementation**: Context automatically preserved to Memory Bank after analysis completion
- **Post-Implementation**: Implementation outcomes stored for future reference
- **Task Completion**: Final task context captured with git status and completion details

### Document Consistency Validation
- **PRD/FSD/Epic Integration**: All changes validated against project documentation
- **Conflict Detection**: Identifies when proposed changes violate existing requirements
- **User Confirmation Flows**: Interactive prompts when conflicts are detected
- **Implementation Blocking**: Prevents non-compliant changes from proceeding

### Automated Document Versioning
- **Version Management**: Automatic version increments with change tracking
- **History Preservation**: Maintains configurable version history (default: 10 versions)
- **Archive System**: Organized storage in `sessions/documents/versions/`
- **Change Logging**: Automatic change log entries with timestamps and descriptions

## Document Structure

### Project Documents Location
```
sessions/documents/
├── PRD.md                 # Product Requirements Document
├── FSD.md                 # Functional Specification Document
├── EPIC_*.md              # Story epics and user stories
├── versions/              # Version history archive
│   ├── PRD_v1.0_20250909_143022.md
│   ├── FSD_v2.1_20250909_143045.md
│   └── ...
└── archive/               # Long-term document storage
```

### Document Templates
- **PRD Template**: Standardized Product Requirements format
- **FSD Template**: Technical Functional Specification format  
- **Epic Template**: User story and epic documentation format

## Configuration

### Document Governance Settings
```json
{
  "document_governance": {
    "enabled": true,
    "auto_context_retention": true,
    "document_validation": true,
    "conflict_detection": true,
    "auto_versioning": true,
    "documents_path": "sessions/documents",
    "version_history_limit": 10,
    "require_user_confirmation": true
  }
}
```

## Workflow Integration

### Development Lifecycle
1. **Analysis Phase**: Context-gathering agent validates against existing documents
2. **Conflict Detection**: System identifies potential requirement violations
3. **User Confirmation**: Interactive resolution when conflicts detected
4. **Implementation Phase**: Changes proceed with context retention
5. **Completion Phase**: Final context and outcomes preserved to Memory Bank

### Document Updates
1. **Conflict Resolution**: When changes require document updates
2. **Version Creation**: Automatic versioning of revised documents
3. **Memory Bank Update**: New document context stored for future reference
4. **History Preservation**: Previous versions archived with full traceability

## Benefits

### Development Quality
- **Requirement Alignment**: Ensures all changes align with documented requirements
- **Context Continuity**: Complete development history preserved across sessions
- **Knowledge Preservation**: Critical decisions and rationale stored permanently
- **Team Coordination**: Shared context and documentation for collaboration

### Process Improvement
- **Automated Compliance**: Document validation without manual oversight
- **Version Control**: Comprehensive document history with change tracking
- **Conflict Prevention**: Early detection prevents costly requirement drift
- **Audit Trail**: Complete traceability from requirements to implementation

## Usage Examples

### Document Validation Workflow
```bash
# During analysis phase
Claude: "Analyzing proposed authentication changes..."
System: "⚠️ Document conflicts detected!"
System: "PRD restriction: 'OAuth2 only - password auth prohibited'"
System: "Proposed change: 'Add username/password login'"
User: "Update PRD to allow hybrid authentication"
System: "Creating PRD v2.0 with hybrid auth requirements"
```

### Context Preservation
```bash
# Automatic context retention
Analysis Complete → Memory Bank: context_auth-task_20250909.md
Implementation Done → Memory Bank: implementation_auth-task_20250909.md
Task Complete → Memory Bank: task_completion_auth-task_20250909.md
```

## Commands and Tools

### Document Versioning Commands
```bash
# Create new document version
python cc_sessions/hooks/document-versioning.py version PRD.md "Added hybrid auth"

# View document history
python cc_sessions/hooks/document-versioning.py history PRD.md

# Restore previous version
python cc_sessions/hooks/document-versioning.py restore PRD.md 1.0
```

### Memory Bank Integration
- **Context Storage**: `sessions/memory_bank/{project}/contexts/`
- **Implementation Records**: `sessions/memory_bank/{project}/implementations/`
- **Task Completions**: `sessions/memory_bank/{project}/completions/`

---

# GitHub MCP Integration

## Overview

GitHub MCP provides comprehensive repository management, issue tracking, pull request automation, and CI/CD workflow intelligence. This integration enables cc-sessions to interact directly with GitHub repositories, analyze code changes, manage issues, and automate development workflows.

## What is GitHub MCP?

GitHub MCP is a sophisticated GitHub integration system designed for AI-driven development workflows. Key capabilities include:

- **Repository Management**: Browse repositories, search code, analyze commits, and understand project structure
- **Issue & PR Automation**: Create, update, and manage issues and pull requests with AI assistance
- **CI/CD Intelligence**: Monitor GitHub Actions workflows, analyze build failures, manage releases
- **Code Analysis**: Review security findings, Dependabot alerts, code patterns, and comprehensive insights
- **Team Collaboration**: Access discussions, manage notifications, analyze team activity

## Installation Methods

### Method 1: Automatic Installation (Recommended)

GitHub MCP installation is included in the cc-sessions installation process:

```bash
# During cc-sessions installation, when prompted:
Install GitHub MCP for repository management and automation? (y/n): y
```

The installer will:
1. Check for Docker and Claude Code CLI availability
2. Install GitHub MCP server using Docker
3. Configure the MCP server in Claude Code
4. Guide you through Personal Access Token setup

### Method 2: Manual Installation

**Prerequisites:**
- Docker (container runtime)
- Claude Code CLI
- GitHub Personal Access Token

**Installation:**
```bash
# Add GitHub MCP server to Claude Code
claude mcp add github docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server

# Verify installation
claude mcp list | grep github
```

**Configuration:**
1. Create GitHub Personal Access Token at: https://github.com/settings/tokens
2. Recommended scopes: `repo`, `read:packages`, `read:org`
3. Set environment variable: `GITHUB_PERSONAL_ACCESS_TOKEN=your_token`

## Available Tools

### GitHub MCP Tools
- `mcp__github__get_repo` - Retrieve repository information and metadata
- `mcp__github__list_issues` - List and filter repository issues
- `mcp__github__get_issue` - Get detailed issue information
- `mcp__github__list_pull_requests` - List and filter pull requests
- `mcp__github__get_pull_request` - Get detailed PR information and changes
- `mcp__github__search_repositories` - Search across GitHub repositories
- `mcp__github__get_file_contents` - Retrieve specific file contents from repositories
- `mcp__github__list_commits` - List and analyze repository commits
- `mcp__github__get_workflow_runs` - Monitor GitHub Actions workflow execution

### Enhanced Agent Capabilities

**Context-Gathering Agent Enhancement:**
- Repository analysis and project structure understanding
- Issue tracking and requirement gathering from GitHub issues
- Pull request analysis for implementation context
- Workflow and CI/CD pipeline analysis

**Semantic Analysis Agent Enhancement:**
- Cross-repository code analysis and symbol mapping
- Pull request code review and analysis
- Commit history analysis for architectural decisions
- Integration with local semantic analysis for comprehensive understanding

## Usage Examples

### Example 1: Repository Analysis During Context Gathering

```bash
# Claude analyzes repository structure and recent activity
get_repo("owner/repository") → Repository metadata and structure
list_commits("owner/repository", limit=10) → Recent development activity
list_issues("owner/repository", state="open") → Current project requirements

# Results integrated into comprehensive context analysis
```

### Example 2: Issue-Driven Development Workflow

```bash
# User references GitHub issue in task creation
get_issue("owner/repository", issue_number) → Issue requirements and discussion
get_pull_request("owner/repository", pr_number) → Related implementation context
search_repositories("specific functionality") → Similar implementations across projects
```

### Example 3: CI/CD and Workflow Intelligence

```bash
# Monitor and analyze build pipeline status
get_workflow_runs("owner/repository") → Recent workflow executions
get_file_contents("owner/repository", ".github/workflows/ci.yml") → CI configuration analysis
list_commits("owner/repository", sha="branch") → Changes affecting build status
```

## Configuration Options

### Authentication Setup
Update `sessions/sessions-config.json`:
```json
{
  "github_mcp": {
    "enabled": true,
    "auto_activate": true,
    "requires_pat": true,
    "default_owner": "your-org-or-username",
    "rate_limit_enabled": true
  }
}
```

### Environment Variables
- `GITHUB_PERSONAL_ACCESS_TOKEN`: Required for API access
- `GITHUB_API_URL`: Optional, defaults to GitHub.com API
- `GITHUB_RATE_LIMIT`: Optional rate limiting configuration

## Benefits for cc-sessions

### Enhanced Development Workflow
- **Repository Integration**: Seamless connection between local development and GitHub
- **Issue Tracking**: Automatic context gathering from GitHub issues and discussions
- **PR Analysis**: Comprehensive pull request analysis and review assistance
- **Workflow Monitoring**: Real-time visibility into CI/CD pipeline status

### Improved Context Quality
- **Project Understanding**: Deep analysis of repository structure and development patterns
- **Requirement Traceability**: Link development tasks to GitHub issues and discussions
- **Implementation Insights**: Learn from existing codebases and implementation patterns
- **Team Collaboration**: Enhanced visibility into team development activities

---

# Storybook MCP Integration

## Overview

Storybook MCP provides specialized component development workflows, enabling seamless interaction with Storybook instances for component analysis, story management, and component-driven development practices. This integration bridges the gap between development and design systems.

## What is Storybook MCP?

Storybook MCP is a component-focused integration system designed for modern frontend development workflows. Key capabilities include:

- **Component Discovery**: Retrieve comprehensive component inventories from Storybook
- **Props Analysis**: Extract detailed component prop information and interfaces
- **Story Management**: Analyze and manage component stories and variations
- **Design System Integration**: Connect component development with design system practices
- **Component Documentation**: Automated analysis of component APIs and usage patterns

## Installation Methods

### Method 1: Automatic Installation (Recommended)

Storybook MCP installation is included in the cc-sessions installation process:

```bash
# During cc-sessions installation, when prompted:
Install Storybook MCP for component development workflows? (y/n): y
```

The installer will:
1. Check for Node.js/npx and Claude Code CLI availability
2. Install Storybook MCP server using npx
3. Configure the MCP server in Claude Code
4. Guide you through Storybook URL configuration

### Method 2: Manual Installation

**Prerequisites:**
- Node.js 18.0.0 or higher
- Claude Code CLI
- Running Storybook instance

**Installation:**
```bash
# Add Storybook MCP server to Claude Code
claude mcp add storybook npx -y storybook-mcp

# Verify installation
claude mcp list | grep storybook
```

**Configuration:**
Set environment variable pointing to your Storybook:
```bash
export STORYBOOK_URL=http://localhost:6006/index.json
```

## Available Tools

### Storybook MCP Tools
- `mcp__storybook__getComponentList` - Retrieve all components from Storybook instance
- `mcp__storybook__getComponentsProps` - Extract detailed component prop information

### Enhanced Agent Capabilities

**Dedicated Storybook Agent:**
- Component-driven development workflows
- Story generation and management
- Component analysis and documentation
- Design system maintenance and consistency
- Props interface analysis and validation

**Context-Gathering Agent Enhancement:**
- Component inventory analysis for UI-focused tasks
- Design system pattern recognition
- Component usage and dependency mapping

## Usage Examples

### Example 1: Component Analysis and Documentation

```bash
# Storybook agent analyzes component ecosystem
getComponentList() → Complete component inventory
getComponentsProps("ButtonComponent") → Detailed prop analysis and interface

# Results used for component development planning
```

### Example 2: Design System Audit

```bash
# Systematic analysis of component consistency
getComponentList() → All available components
# For each component:
getComponentsProps(componentName) → Props analysis
# Generate consistency report and recommendations
```

### Example 3: New Component Development

```bash
# Research similar components for patterns
getComponentList() → Existing component patterns
getComponentsProps("SimilarComponent") → Interface patterns to follow
# Create new component following established patterns
```

## Configuration Options

### Storybook Connection
Update `sessions/sessions-config.json`:
```json
{
  "storybook_mcp": {
    "enabled": true,
    "auto_activate": true,
    "storybook_url": "http://localhost:6006/index.json",
    "timeout": 30000,
    "retry_attempts": 3
  }
}
```

### Environment Variables
- `STORYBOOK_URL`: Required, points to Storybook index.json
- `STORYBOOK_TIMEOUT`: Optional connection timeout
- `CUSTOM_TOOLS`: Optional custom tool extensions

## Benefits for cc-sessions

### Component-Driven Development
- **Component Analysis**: Deep understanding of component APIs and patterns
- **Story Management**: Systematic approach to story creation and maintenance
- **Design System Integration**: Seamless connection with design system practices
- **Component Documentation**: Automated component interface documentation

### Enhanced Development Workflow
- **Pattern Recognition**: Learn from existing component implementations
- **Consistency Enforcement**: Maintain design system consistency across components
- **Component Discovery**: Easily find and analyze existing components
- **Interface Validation**: Ensure component APIs follow established patterns

---

# Playwright MCP Integration

## Overview

Playwright MCP provides comprehensive end-to-end testing, browser automation, and web page interaction capabilities. This integration enables cc-sessions to create robust test suites, automate user workflows, and ensure web application quality through systematic testing approaches.

## What is Playwright MCP?

Playwright MCP is a browser automation and testing integration system designed for comprehensive web application quality assurance. Key capabilities include:

- **Browser Automation**: Cross-browser testing and automation across Chromium, Firefox, and WebKit
- **Visual Testing**: Screenshot capture and visual regression testing
- **User Interaction Simulation**: Comprehensive form filling, clicking, and user journey automation
- **Accessibility Testing**: Role-based element interaction and accessibility validation
- **Performance Testing**: Page load monitoring and interaction response measurement

## Installation Methods

### Method 1: Automatic Installation (Recommended)

Playwright MCP installation is included in the cc-sessions installation process:

```bash
# During cc-sessions installation, when prompted:
Install Playwright MCP for browser automation and testing? (y/n): y
```

The installer will:
1. Check for Node.js/npx and Claude Code CLI availability
2. Install Playwright MCP server using npx
3. Configure the MCP server in Claude Code
4. Set up browser automation capabilities

### Method 2: Manual Installation

**Prerequisites:**
- Node.js (latest LTS recommended)
- Claude Code CLI

**Installation:**
```bash
# Add Playwright MCP server to Claude Code
claude mcp add playwright npx @playwright/mcp@latest

# Verify installation
claude mcp list | grep playwright
```

## Available Tools

### Playwright MCP Tools
- `mcp__playwright__navigate` - Navigate to URLs and manage page state
- `mcp__playwright__screenshot` - Capture page and element screenshots
- `mcp__playwright__click` - Simulate user clicks on elements
- `mcp__playwright__type` - Input text into form fields
- `mcp__playwright__get_by_role` - Find elements by accessibility role
- `mcp__playwright__get_by_text` - Locate elements by visible text
- `mcp__playwright__wait_for_selector` - Wait for elements to appear
- `mcp__playwright__evaluate` - Execute JavaScript in browser context

### Enhanced Agent Capabilities

**Dedicated Playwright Agent:**
- End-to-end test suite creation and management
- Visual regression testing workflows
- User journey validation and automation
- Performance monitoring and analysis
- Cross-browser compatibility testing

**Context-Gathering Agent Enhancement:**
- Application workflow analysis through browser interaction
- User interface structure understanding
- Interactive element discovery and mapping

## Usage Examples

### Example 1: End-to-End Test Creation

```bash
# Playwright agent creates comprehensive test suite
navigate("https://app.example.com") → Load application
click("button[data-testid='login']") → Simulate user interaction
type("input[name='email']", "user@example.com") → Fill form fields
screenshot() → Capture test evidence
```

### Example 2: Visual Regression Testing

```bash
# Systematic visual testing workflow
navigate("https://app.example.com/dashboard") → Load target page
wait_for_selector(".dashboard-content") → Ensure page loaded
screenshot({ fullPage: true }) → Capture baseline
# Compare with previous screenshots for regression detection
```

### Example 3: Accessibility and User Journey Testing

```bash
# Accessibility-focused testing approach
get_by_role("button", { name: "Submit" }) → Accessibility-compliant selection
get_by_text("Welcome back") → Content-based element location
evaluate("document.querySelector('h1').textContent") → Custom page analysis
```

## Configuration Options

### Browser and Testing Setup
Update `sessions/sessions-config.json`:
```json
{
  "playwright_mcp": {
    "enabled": true,
    "auto_activate": true,
    "browser_automation": true,
    "headless": true,
    "viewport": { "width": 1280, "height": 720 },
    "timeout": 30000
  }
}
```

### Testing Configuration
- **Browser Selection**: Chromium, Firefox, WebKit support
- **Device Emulation**: Mobile and tablet testing capabilities
- **Network Throttling**: Slow network and offline testing
- **Parallel Execution**: Multi-worker test execution

## Benefits for cc-sessions

### Comprehensive Testing Capabilities
- **End-to-End Coverage**: Complete user journey testing automation
- **Visual Quality Assurance**: Screenshot-based regression detection
- **Cross-Browser Validation**: Consistent behavior across browser engines
- **Performance Monitoring**: Page load and interaction performance tracking

### Enhanced Development Workflow
- **Quality Gates**: Automated testing integration in development workflows
- **Bug Reproduction**: Systematic reproduction of reported issues
- **Feature Validation**: Automated validation of new feature implementations
- **User Experience Assurance**: Comprehensive UX testing and validation

---

**Next Steps:** Once all MCP servers (Serena, Memory Bank, GitHub, Storybook, Playwright) and Document Governance are configured, experience a complete development workflow where code analysis is enhanced with semantic precision, repository management is seamlessly integrated, component development follows design system practices, comprehensive testing ensures quality, context is automatically preserved, and project knowledge is maintained across all development sessions.