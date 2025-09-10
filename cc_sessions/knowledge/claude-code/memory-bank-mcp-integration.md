# Memory Bank MCP Integration Guide

## Overview

The cc-sessions framework integrates with [Memory Bank MCP](https://github.com/alioshr/memory-bank-mcp) to provide persistent knowledge storage and cross-session context preservation. This integration enables long-term memory capabilities, allowing context and insights to be retained across multiple development sessions.

## Architecture

### Core Components

**1. Context-Gathering Agent Enhancement** (`cc_sessions/agents/context-gathering.md`)
- Enhanced with Memory Bank MCP tools for persistent context storage
- Stores project insights and architectural understanding for future sessions
- Retrieves relevant historical context during task startup

**2. Cross-Session Context Preservation**
- Maintains project knowledge across session boundaries  
- Preserves architectural decisions and implementation patterns
- Builds cumulative understanding of codebase evolution

**3. Installation Integration**
- Both Python and Node.js installers detect and configure Memory Bank MCP
- Optional installation during setup process
- Automatic Claude Code MCP server configuration

## Installation Methods

### Automatic (Recommended)
During cc-sessions installation:
1. Installer detects `npx` and `claude` commands
2. Offers optional Memory Bank MCP installation
3. Configures MCP server automatically: `claude mcp add memory-bank npx -y @alioshr/memory-bank-mcp`
4. Updates configuration with `memory_bank_mcp.enabled: true`

### Manual Installation
```bash
# Install via npx (requires Node.js)
npx -y @alioshr/memory-bank-mcp

# Add Memory Bank MCP server to Claude Code
claude mcp add memory-bank npx -y @alioshr/memory-bank-mcp

# Update sessions configuration
# Edit sessions/sessions-config.json:
{
  "memory_bank_mcp": {
    "enabled": true,
    "auto_activate": true,
    "memory_bank_root": ""
  }
}
```

## Available Tools

### Core Memory Bank MCP Tools
- `mcp__memory_bank__read_file` - Retrieve stored knowledge files
- `mcp__memory_bank__write_file` - Store new knowledge and insights
- `mcp__memory_bank__update_file` - Modify existing knowledge entries
- `mcp__memory_bank__list_projects` - List all tracked projects
- `mcp__memory_bank__list_files` - List knowledge files for a project

### Agent Integration
**Context-Gathering Agent:**
- Stores architectural insights and implementation patterns
- Retrieves relevant historical context during task setup
- Builds cumulative understanding of project evolution
- Cross-references current analysis with past findings

## Usage Patterns

### Context Preservation Across Sessions
Before Memory Bank MCP:
```markdown
1. Each session starts with limited context
2. Architectural insights lost between sessions
3. Repeated analysis of same components
4. No cumulative learning from project history
```

With Memory Bank MCP:
```markdown
1. Session starts with relevant historical context
2. Architectural understanding preserved and enhanced
3. Build upon previous insights and decisions
4. Cumulative knowledge growth across sessions
5. Avoid re-analyzing well-understood components
```

### Project Knowledge Building
```bash
# Traditional approach - ephemeral analysis
Context-gathering: Analyze UserAuth component
Session ends → insights lost

# Memory Bank approach - persistent learning
write_file("project_auth_architecture.md", analysis_results)
Next session: read_file("project_auth_architecture.md") → context restored
```

## Configuration

### Project Configuration (`sessions/sessions-config.json`)
```json
{
  "memory_bank_mcp": {
    "enabled": true,
    "auto_activate": true,
    "memory_bank_root": "/path/to/memory/storage"
  }
}
```

### Memory Storage Structure
```
memory_bank_root/
├── projects/
│   └── project_name/
│       ├── architecture.md
│       ├── implementation_patterns.md
│       ├── decisions.md
│       └── lessons_learned.md
```

## Graceful Fallback

The integration enhances rather than replaces existing functionality:

### When Memory Bank MCP Available
- Persistent context across sessions
- Cumulative project understanding
- Reduced redundant analysis
- Historical insight retrieval

### When Memory Bank MCP Unavailable
- Full fallback to session-based context only
- No loss of immediate functionality
- Agents continue to provide comprehensive context
- Clear indication: "Memory bank unavailable - using session-only context"

## Benefits

### For Context Gathering
- **Persistence**: Context preserved across session boundaries
- **Efficiency**: Avoid re-analyzing understood components
- **Learning**: Cumulative understanding growth over time
- **Consistency**: Maintain architectural decisions across sessions

### For Project Management
- **History**: Track evolution of implementation decisions
- **Patterns**: Identify recurring architectural patterns
- **Documentation**: Automatically build living project documentation
- **Onboarding**: Rich context for new team members or sessions

### For Development Workflow
- **Continuity**: Seamless context restoration between sessions
- **Insight**: Build upon previous analysis and decisions
- **Quality**: Consistent implementation patterns over time
- **Knowledge**: Preserve and share architectural understanding

## Troubleshooting

### Common Issues

**1. "Memory Bank MCP requirements not met"**
- Install Node.js and npm: Visit https://nodejs.org
- Ensure Claude Code CLI is available: `claude --version`

**2. "Memory storage unavailable"**
- Check if Memory Bank MCP server is configured: `claude mcp list`
- Verify npx can access the package: `npx @alioshr/memory-bank-mcp --version`

**3. "Failed to read/write memory files"**
- Check memory_bank_root directory permissions
- Ensure sufficient disk space for knowledge storage
- Verify file path accessibility

### Debug Steps
1. Verify MCP server status: `claude mcp list`
2. Test basic operations: `list_projects()`
3. Check storage directory: `ls $memory_bank_root`
4. Review sessions configuration: `cat sessions/sessions-config.json`

## Best Practices

### Knowledge Storage
- Store architectural insights and implementation patterns
- Document design decisions with reasoning
- Preserve lessons learned from implementation challenges
- Maintain project evolution history

### Session Management
- Review relevant memory files during task startup
- Update knowledge files when making architectural changes
- Use descriptive filenames for easy retrieval
- Regular cleanup of outdated information

### Integration
- Enable during installation for best experience
- Configure appropriate memory_bank_root location
- Framework works fully with or without integration
- Provides clear feedback about storage operations

## Future Enhancements

### Planned Integrations
- Automatic knowledge extraction from completed tasks
- Smart context retrieval based on current task similarity
- Cross-project pattern recognition and sharing
- Integration with team knowledge bases

### Extensibility
The persistent memory infrastructure supports integration with other knowledge management systems and provides a foundation for team-wide knowledge sharing in the cc-sessions framework.