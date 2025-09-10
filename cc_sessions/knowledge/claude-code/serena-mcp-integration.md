# Serena MCP Integration Guide

## Overview

The cc-sessions framework integrates with [Serena MCP](https://github.com/oraios/serena) to provide enhanced semantic code analysis capabilities. This integration transforms context-gathering from text-based pattern matching to precise symbol-level analysis.

## Architecture

### Core Components

**1. Semantic Analysis Agent** (`cc_sessions/agents/semantic-analysis.md`)
- Dedicated agent for precise code analysis using Serena MCP tools
- Provides symbol-level precision for dependency mapping
- Gracefully falls back to text-based analysis when unavailable

**2. Enhanced Context-Gathering Agent** (`cc_sessions/agents/context-gathering.md`)
- Updated with Serena MCP tools for hybrid analysis approach
- Combines semantic precision with traditional text search
- Maintains full backward compatibility

**3. Installation Integration**
- Both Python and Node.js installers detect and configure Serena MCP
- Optional installation during setup process
- Automatic Claude Code MCP server configuration

## Installation Methods

### Automatic (Recommended)
During cc-sessions installation:
1. Installer detects `uv` and `claude` commands
2. Offers optional Serena MCP installation
3. Configures MCP server automatically: `claude mcp add serena uvx --from git+https://github.com/oraios/serena serena start-mcp-server`
4. Updates configuration with `serena_mcp.enabled: true`

### Manual Installation
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add Serena MCP server to Claude Code
claude mcp add serena uvx --from git+https://github.com/oraios/serena serena start-mcp-server

# Update sessions configuration
# Edit sessions/sessions-config.json:
{
  "serena_mcp": {
    "enabled": true,
    "auto_activate": true
  }
}
```

## Available Tools

### Core Serena MCP Tools
- `mcp__serena__find_symbol` - Locate exact symbol definitions
- `mcp__serena__find_referencing_symbols` - Map all symbol dependencies
- `mcp__serena__get_symbol_definition` - Get complete symbol definitions
- `mcp__serena__list_symbols` - List all symbols in a file
- `mcp__serena__insert_after_symbol` - Surgical code insertions

### Agent Integration
**Semantic Analysis Agent:**
- Specialized for pure semantic operations
- Focused on architecture analysis and dependency mapping
- Provides structured reports on code relationships

**Context-Gathering Agent:**
- Hybrid approach: semantic first, text expansion
- Uses semantic analysis to guide targeted research
- Cross-validates findings between approaches

## Usage Patterns

### Context Gathering Enhancement
Before Serena MCP:
```markdown
1. Grep for component patterns across codebase
2. Read entire files to understand relationships
3. Text-based pattern matching for dependencies
4. High token usage, potential for missing relationships
```

With Serena MCP:
```markdown
1. find_symbol("target_component") → exact location
2. find_referencing_symbols("target_component") → precise dependencies
3. Semantic understanding of architectural relationships
4. Targeted text search for business logic context
5. Lower token usage, higher accuracy
```

### Dependency Analysis
```bash
# Traditional approach
grep -r "UserAuth" src/ | head -20

# Semantic approach  
find_symbol("UserAuth") → src/auth/user.py:45
find_referencing_symbols("UserAuth") → [
  src/controllers/login.py:12,
  src/middleware/auth.py:8,
  src/services/session.py:23
]
```

## Configuration

### Project Configuration (`sessions/sessions-config.json`)
```json
{
  "serena_mcp": {
    "enabled": true,
    "auto_activate": true
  }
}
```

### Project Activation
After Serena MCP installation, activate your project:
```bash
# In Claude Code, tell Claude:
"Activate the project /path/to/your/project"
```

## Graceful Fallback

The integration is designed to enhance rather than replace existing functionality:

### When Serena MCP Available
- Enhanced precision in dependency mapping
- Reduced token usage through targeted analysis
- Better architectural understanding
- IDE-like code navigation

### When Serena MCP Unavailable
- Full fallback to text-based analysis
- No loss of functionality
- Agents continue to provide comprehensive context
- Clear indication in output: "Semantic analysis unavailable - using text search"

## Benefits

### For Context Gathering
- **Precision**: Exact symbol locations vs. text pattern matching
- **Efficiency**: Targeted analysis vs. reading entire files  
- **Accuracy**: True dependency relationships vs. assumptions
- **Architecture**: Understanding WHY relationships exist

### For Code Review
- **Security**: Symbol-level flow analysis for vulnerability detection
- **Impact**: Precise understanding of change implications
- **Patterns**: Semantic consistency analysis vs. text patterns

### For Development Workflow
- **Token Efficiency**: Reduced context window usage
- **Speed**: Faster analysis with targeted operations
- **Quality**: Better understanding of existing codebase
- **Integration**: Seamless enhancement of existing agents

## Troubleshooting

### Common Issues

**1. "Serena MCP requirements not met"**
- Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Ensure Claude Code CLI is available: `claude --version`

**2. "Semantic analysis unavailable"**
- Check if Serena MCP server is configured: `claude mcp list`
- Verify project activation: Tell Claude "Activate the project /path/to/project"

**3. "Symbol not found"**
- Ensure project is indexed (may take time for large codebases)
- Try alternative symbol names or broader text search
- Check if symbol exists in currently activated project

### Debug Steps
1. Verify MCP server status: `claude mcp list`
2. Check project activation status in Claude Code
3. Test with simple symbol: `find_symbol("main")`
4. Review sessions configuration: `cat sessions/sessions-config.json`

## Best Practices

### Agent Usage
- Use semantic-analysis agent for pure architectural analysis
- Use enhanced context-gathering for comprehensive task context
- Start with semantic analysis, expand with text search
- Cross-validate findings between both approaches

### Performance
- Let Serena MCP index large codebases before first use
- Use specific symbol names rather than broad patterns
- Combine semantic precision with contextual text analysis

### Integration
- Enable during installation for best experience
- Manual setup available for existing installations  
- Framework works fully with or without integration
- Provides clear feedback about availability and usage

## Future Enhancements

### Planned Integrations
- Code review agent semantic security analysis
- Service boundary detection via symbol analysis
- Automatic task scoping based on semantic dependencies
- Enhanced refactoring support with impact analysis

### Extensibility
The semantic analysis infrastructure supports additional MCP integrations beyond Serena, providing a foundation for other IDE-like capabilities in the cc-sessions framework.