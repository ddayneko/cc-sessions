# Storybook MCP Integration Guide

## Overview

The cc-sessions framework integrates with Storybook MCP to provide component-driven development workflows, automated story generation, and comprehensive UI component analysis. This integration enables seamless interaction with Storybook instances, component documentation generation, and design system maintenance.

## Architecture

### Core Components

**1. Storybook Development Agent** (`cc_sessions/agents/storybook.md`)
- Specialized agent for Storybook-based component development workflows
- Provides component analysis, story generation, and Storybook integration management
- Automated component documentation and design system maintenance

**2. Component-Driven Development Integration**
- Analyze existing Storybook components and stories
- Generate new stories based on component analysis
- Maintain design system consistency and documentation
- Integrate component development with broader application architecture

**3. Installation Integration**
- Both Python and Node.js installers detect and configure Storybook MCP
- Optional installation during setup process
- Automatic Claude Code MCP server configuration

## Installation Methods

### Automatic (Recommended)
During cc-sessions installation:
1. Installer detects existing Storybook installation and `claude` commands
2. Offers optional Storybook MCP installation
3. Configures MCP server automatically with project's Storybook instance
4. Updates configuration with `storybook_mcp.enabled: true`

### Manual Installation
```bash
# Prerequisites: Existing Storybook installation
npm install @storybook/cli

# Add Storybook MCP server to Claude Code
claude mcp add storybook [storybook-mcp-server-command]

# Update sessions configuration
# Edit sessions/sessions-config.json:
{
  "storybook_mcp": {
    "enabled": true,
    "auto_activate": true,
    "storybook_url": "http://localhost:6006"
  }
}
```

## Available Tools

### Core Storybook MCP Tools
- `mcp__storybook__getComponentList` - List all available Storybook components
- `mcp__storybook__getComponentsProps` - Analyze component properties and interfaces
- `mcp__storybook__getStory` - Retrieve specific story details and configuration
- `mcp__storybook__createStory` - Generate new stories based on component analysis
- `mcp__storybook__updateStory` - Modify existing story configurations
- `mcp__storybook__validateStory` - Validate story consistency and best practices

### Agent Integration
**Storybook Development Agent:**
- Component analysis and documentation generation
- Story creation and maintenance workflows
- Design system consistency validation
- Component prop analysis and type checking

**Context-Gathering Agent Enhancement:**
- Include Storybook components in architectural analysis
- Understand component relationships and usage patterns
- Analyze design system implementation and consistency

## Usage Patterns

### Component-Driven Development Workflow
Before Storybook MCP:
```markdown
1. Manual component analysis from source code
2. Separate Storybook story creation process  
3. Limited visibility into component usage patterns
4. Manual design system consistency checking
```

With Storybook MCP:
```markdown
1. Automated component analysis from running Storybook
2. AI-assisted story generation based on component props
3. Comprehensive component usage and relationship mapping
4. Automated design system consistency validation
5. Integrated component documentation workflow
```

### Story Generation and Maintenance
```bash
# Traditional approach
Manual story creation → Manual prop documentation → Manual testing

# Storybook MCP approach  
getComponentsProps("Button") → Analyze component interface →
createStory("Button", variants_based_on_props) → 
validateStory("Button", consistency_check)
```

## Configuration

### Project Configuration (`sessions/sessions-config.json`)
```json
{
  "storybook_mcp": {
    "enabled": true,
    "auto_activate": true,
    "storybook_url": "http://localhost:6006",
    "build_command": "npm run build-storybook",
    "dev_command": "npm run storybook"
  }
}
```

### Storybook Integration Requirements
```
project/
├── .storybook/
│   └── main.js (or main.ts)
├── src/
│   └── components/
│       └── Button/
│           ├── Button.tsx
│           └── Button.stories.tsx
└── package.json (with storybook scripts)
```

## Graceful Fallback

The integration enhances rather than replaces existing component development:

### When Storybook MCP Available
- Automated component analysis and story generation
- Design system consistency validation
- Component relationship mapping
- Integrated documentation workflows

### When Storybook MCP Unavailable
- Full fallback to manual component analysis
- Traditional story creation workflows continue
- No loss of core development functionality
- Clear indication: "Storybook MCP unavailable - using manual component analysis"

## Benefits

### For Component Development
- **Automation**: Automated story generation based on component analysis
- **Consistency**: Design system validation and consistency checking
- **Documentation**: Integrated component documentation workflows
- **Analysis**: Deep understanding of component relationships and usage

### For Design Systems
- **Validation**: Automated design token and component consistency checking
- **Documentation**: Living documentation generation from component analysis
- **Patterns**: Identification of design patterns and inconsistencies
- **Maintenance**: Streamlined design system maintenance workflows

### For Development Workflow
- **Integration**: Seamless integration between component development and broader architecture
- **Quality**: Automated validation of component best practices
- **Efficiency**: Reduced manual work in story creation and maintenance
- **Insight**: Better understanding of component ecosystem and relationships

## Troubleshooting

### Common Issues

**1. "Storybook MCP requirements not met"**
- Ensure Storybook is installed: `npm list @storybook/cli`
- Verify Storybook is running: Check configured storybook_url
- Ensure Claude Code CLI is available: `claude --version`

**2. "Cannot connect to Storybook instance"**
- Check if Storybook server is running: `npm run storybook`
- Verify storybook_url in configuration is correct
- Check firewall settings and port accessibility

**3. "Component analysis failed"**
- Ensure components are properly exported in Storybook
- Verify story files follow Storybook conventions
- Check for TypeScript/prop-types configuration issues

### Debug Steps
1. Verify MCP server status: `claude mcp list`
2. Test Storybook connection: Visit configured storybook_url in browser
3. Check component exports: `getComponentList()`
4. Review sessions configuration: `cat sessions/sessions-config.json`

## Best Practices

### Component Development
- Follow Storybook naming conventions for consistent analysis
- Use TypeScript or prop-types for clear component interfaces
- Maintain comprehensive component documentation in stories
- Implement design tokens for consistent theming

### Story Management
- Use descriptive story names and categories
- Include comprehensive component variants in stories
- Document component usage patterns and best practices
- Maintain story consistency across design system

### Integration
- Enable Storybook MCP during installation for best experience
- Configure appropriate Storybook URL and build commands
- Framework works with existing Storybook configurations
- Provides clear feedback about component analysis results

## Future Enhancements

### Planned Integrations
- Visual regression testing integration with component stories
- Design token validation and synchronization
- Component usage analytics and optimization suggestions
- Integration with design tools (Figma, Sketch) for design-to-code workflows

### Extensibility
The Storybook MCP infrastructure supports integration with other design system tools and provides a foundation for comprehensive component-driven development workflows in the cc-sessions framework.