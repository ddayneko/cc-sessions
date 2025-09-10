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

# DuckDuckGo MCP Integration

## Overview

DuckDuckGo MCP provides web search and content retrieval capabilities that enhance cc-sessions with real-time knowledge gathering, troubleshooting support, and access to current best practices. This integration enables agents to research solutions, gather external documentation, and stay current with evolving technologies.

## What is DuckDuckGo MCP?

DuckDuckGo MCP is a sophisticated web search and content retrieval system designed specifically for AI and language models. Key capabilities include:

- **Intelligent Web Search**: Clean, structured search results through DuckDuckGo
- **Content Extraction**: Advanced webpage parsing and content retrieval
- **AI-Optimized Results**: Formatted specifically for AI consumption
- **Rate Limiting**: Built-in limits to ensure responsible usage
- **Ad-Free Results**: Clean results without advertising clutter

## Installation Methods

### Method 1: Automatic Installation (Recommended)

DuckDuckGo MCP installation is included in the cc-sessions installation process:

```bash
# During cc-sessions installation, when prompted:
Install DuckDuckGo MCP for web search and knowledge gathering? (y/n): y
```

The installer will:
1. Check for `npx` or `uv` availability along with Claude Code CLI
2. Install DuckDuckGo MCP server using preferred method (Smithery or uv)
3. Configure the MCP server in Claude Code
4. Set up rate limiting and usage guidelines

### Method 2: Manual Installation

**Prerequisites:**
- Node.js (for npx) OR uv (Python package manager)
- Claude Code CLI

**Installation Options:**

**Option A: Via Smithery (Recommended):**
```bash
# Install DuckDuckGo MCP server
npx -y @smithery/cli install @nickclyde/duckduckgo-mcp-server --client claude

# Verify installation
claude mcp list
```

**Option B: Via uv:**
```bash
# Install DuckDuckGo MCP server
claude mcp add ddg-search uvx duckduckgo-mcp-server

# Verify installation
claude mcp list
```

**Configuration:**
Update `sessions/sessions-config.json`:
```json
{
  "duckduckgo_mcp": {
    "enabled": true,
    "auto_activate": true,
    "rate_limit_enabled": true
  }
}
```

## Available Tools

### DuckDuckGo MCP Tools
- `mcp__duckduckgo__search` - Perform web searches with intelligent result formatting
- `mcp__duckduckgo__fetch_content` - Retrieve and parse webpage content

### Enhanced Agent Capabilities

**Context-Gathering Agent Enhancement:**
- External knowledge gathering for current best practices
- Technical research for known issues and solutions
- Documentation retrieval from official sources
- Industry standard validation and recommendations

**Semantic Analysis Agent Enhancement:**
- Research architectural patterns and design decisions
- Gather documentation for frameworks and libraries
- Find troubleshooting guides for specific technologies
- Validate approaches against current industry practices

## Usage Examples

### Example 1: Knowledge Gathering During Context Analysis

When creating a task context, DuckDuckGo MCP enables:
```bash
# Claude researches current best practices
search("React authentication patterns 2024") → Current industry standards
search("Node.js security best practices") → Latest security guidelines
fetch_content("https://docs.framework.com/auth") → Official documentation

# Results integrated into comprehensive context analysis
```

### Example 2: Troubleshooting and Problem Resolution

**During development issues:**
- Search for similar problems and solutions
- Retrieve official documentation for error messages
- Research current workarounds and fixes
- Validate proposed solutions against community knowledge

**Example workflow:**
```bash
# User encounters authentication error
search("OAuth2 token refresh error Node.js") → Common solutions
search("express-session secure configuration") → Security best practices
fetch_content("github.com/expressjs/session#readme") → Official documentation
```

### Example 3: Technology Research and Validation

**Before implementing new features:**
```bash
# Research implementation approaches
search("real-time notifications implementation patterns")
search("WebSocket vs Server-Sent Events 2024")
fetch_content("developer.mozilla.org/en-US/docs/Web/API/WebSocket")

# Validate against current standards and community consensus
```

## Rate Limits and Responsible Usage

### Built-in Rate Limits
- **Search Operations**: 30 requests per minute
- **Content Fetching**: 20 requests per minute
- **Automatic Queue Management**: Requests queued when limits approached
- **Intelligent Wait Times**: Automatic delays to respect limits

### Best Practices
- Use search for broad knowledge gathering
- Use content fetching for specific documentation
- Cache results when possible to minimize requests
- Focus searches on specific, relevant queries

## Configuration Options

### Rate Limiting Configuration

**sessions-config.json:**
```json
{
  "duckduckgo_mcp": {
    "enabled": true,
    "auto_activate": true,
    "rate_limit_enabled": true,
    "search_timeout": 30,
    "content_timeout": 60,
    "max_results": 10
  }
}
```

### Search Optimization
- **Specific Queries**: Better results than broad searches
- **Technology Context**: Include framework/language names
- **Current Year**: Add current year for up-to-date results
- **Problem Context**: Include error messages or specific issues

## Benefits for cc-sessions

### Enhanced Development Workflow
- **Real-Time Knowledge**: Access to current best practices and solutions
- **Problem Resolution**: Quick research for troubleshooting issues
- **Documentation Access**: Retrieve official docs and guides
- **Technology Validation**: Verify approaches against industry standards

### Improved Context Quality
- **External Validation**: Cross-reference internal analysis with external knowledge
- **Current Standards**: Ensure recommendations align with latest practices
- **Comprehensive Research**: Combine codebase analysis with external knowledge
- **Informed Decisions**: Make implementation choices based on complete information

## Troubleshooting

### Common Issues

#### "DuckDuckGo MCP requirements not met"
**Solutions:**
1. Install Node.js for npx: https://nodejs.org/
2. OR install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Ensure Claude Code CLI is available: `claude --version`

#### "DuckDuckGo MCP server not found"
**Solutions:**
1. Verify MCP server installation: `claude mcp list | grep ddg`
2. Reinstall using preferred method:
   ```bash
   # Smithery method
   npx -y @smithery/cli install @nickclyde/duckduckgo-mcp-server --client claude
   
   # OR uv method
   claude mcp add ddg-search uvx duckduckgo-mcp-server
   ```

#### "Search rate limit exceeded"
**Solutions:**
1. Wait for rate limit reset (limits reset every minute)
2. Use more specific search terms to reduce query volume
3. Cache search results to avoid repeated queries
4. Check rate_limit_enabled in configuration

#### "Content fetch timeout"
**Solutions:**
1. Try fetching from a different source
2. Increase content_timeout in configuration
3. Verify the target URL is accessible
4. Use search to find alternative documentation sources

### Debug Steps

1. **Check MCP server status:**
   ```bash
   claude mcp list | grep -E "(ddg|duckduckgo)"
   ```

2. **Test basic functionality:**
   In Claude Code: "Search for 'test query' using DuckDuckGo"

3. **Verify rate limiting:**
   Check that searches are properly queued and spaced

4. **Check configuration:**
   ```bash
   cat sessions/sessions-config.json | grep duckduckgo_mcp
   ```

## Integration with Other MCP Servers

### Complete MCP Ecosystem

When all MCP servers are available:
- **Serena MCP**: Precise semantic analysis and symbol mapping
- **Memory Bank MCP**: Persistent context and document validation  
- **DuckDuckGo MCP**: Real-time knowledge and external validation
- **Combined Power**: Comprehensive analysis with historical context, semantic precision, and current knowledge

### Enhanced Workflow

1. **Context Gathering**: Memory Bank retrieves historical context
2. **Semantic Analysis**: Serena provides precise code analysis
3. **External Research**: DuckDuckGo gathers current best practices
4. **Validation**: Changes validated against stored requirements and external standards
5. **Preservation**: Updated context with external research stored for future sessions

## Security and Privacy

### DuckDuckGo Privacy Benefits
- **No Tracking**: DuckDuckGo doesn't track searches or build user profiles
- **Private Results**: Search queries remain private
- **No Data Retention**: Search history not stored by DuckDuckGo
- **Secure Connections**: All searches performed over HTTPS

### Rate Limiting Security
- **Abuse Prevention**: Built-in limits prevent excessive usage
- **Resource Protection**: Protects against unintentional API abuse
- **Graceful Degradation**: System continues working when limits reached

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

**Next Steps:** Once all MCP servers (Serena, Memory Bank, DuckDuckGo) and Document Governance are configured, experience a complete document-driven development workflow where every change is validated against requirements, context is automatically preserved, and project knowledge is maintained across all development sessions.