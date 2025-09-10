# Playwright MCP Integration Guide

## Overview

The cc-sessions framework integrates with Playwright MCP to provide comprehensive end-to-end testing, browser automation, and web application interaction capabilities. This integration enables automated testing workflows, screenshot capture, and comprehensive web element interaction for quality assurance and development testing.

## Architecture

### Core Components

**1. Playwright Testing Agent** (`cc_sessions/agents/playwright.md`)
- Specialized agent for end-to-end testing, browser automation, and web page interaction
- Provides comprehensive testing capabilities, screenshot capture, and web element interaction
- Automated test generation and quality assurance workflows

**2. Browser Automation Integration**
- Cross-browser testing capabilities (Chromium, Firefox, Safari)
- Automated user interaction simulation and testing
- Screenshot and visual regression testing
- Web application debugging and analysis

**3. Installation Integration**
- Both Python and Node.js installers detect and configure Playwright MCP
- Optional installation during setup process
- Automatic Claude Code MCP server configuration

## Installation Methods

### Automatic (Recommended)
During cc-sessions installation:
1. Installer detects `playwright` installation and `claude` commands
2. Offers optional Playwright MCP installation
3. Configures MCP server automatically with browser automation capabilities
4. Updates configuration with `playwright_mcp.enabled: true`

### Manual Installation
```bash
# Prerequisites: Install Playwright
npm install -D @playwright/test
npx playwright install

# Add Playwright MCP server to Claude Code
claude mcp add playwright [playwright-mcp-server-command]

# Update sessions configuration
# Edit sessions/sessions-config.json:
{
  "playwright_mcp": {
    "enabled": true,
    "auto_activate": true,
    "browser_automation": true,
    "default_browser": "chromium",
    "headless": true
  }
}
```

## Available Tools

### Core Playwright MCP Tools
- `mcp__playwright__navigate` - Navigate to web pages and URLs
- `mcp__playwright__screenshot` - Capture screenshots of pages or elements
- `mcp__playwright__click` - Click on web elements and buttons
- `mcp__playwright__type` - Type text into input fields and forms
- `mcp__playwright__get_by_role` - Locate elements by ARIA role
- `mcp__playwright__get_by_text` - Find elements by visible text content
- `mcp__playwright__wait_for_selector` - Wait for elements to appear/disappear
- `mcp__playwright__evaluate` - Execute JavaScript in browser context

### Agent Integration
**Playwright Testing Agent:**
- End-to-end test automation and execution
- Visual regression testing and screenshot comparison
- Web application debugging and analysis
- Cross-browser compatibility testing

**Context-Gathering Agent Enhancement:**
- Web application analysis and feature documentation
- User interface component discovery and mapping
- Application flow analysis and user journey mapping

## Usage Patterns

### End-to-End Testing Workflow
Before Playwright MCP:
```markdown
1. Manual test execution and validation
2. Separate screenshot and visual testing tools
3. Limited browser automation integration
4. Manual debugging of web application issues
```

With Playwright MCP:
```markdown
1. Automated end-to-end test generation and execution
2. Integrated visual regression testing with screenshots
3. Cross-browser automated testing capabilities
4. AI-assisted web application debugging and analysis
5. Comprehensive user interaction simulation
```

### Automated Testing and Debugging
```bash
# Traditional approach
Manual test writing → Manual execution → Manual screenshot comparison

# Playwright MCP approach
navigate("http://app.local") →
screenshot("homepage") →
click("login-button") →
type("username", "testuser") →
wait_for_selector("dashboard") →
screenshot("post-login")
```

## Configuration

### Project Configuration (`sessions/sessions-config.json`)
```json
{
  "playwright_mcp": {
    "enabled": true,
    "auto_activate": true,
    "browser_automation": true,
    "default_browser": "chromium",
    "headless": true,
    "screenshot_path": "./screenshots",
    "video_recording": false
  }
}
```

### Playwright Configuration Requirements
```
project/
├── playwright.config.ts (or .js)
├── tests/
│   └── example.spec.ts
├── package.json (with playwright dependencies)
└── test-results/ (generated)
```

## Graceful Fallback

The integration enhances rather than replaces existing testing workflows:

### When Playwright MCP Available
- Automated browser testing and interaction
- Screenshot capture and visual regression testing
- Cross-browser compatibility validation
- AI-assisted test generation and debugging

### When Playwright MCP Unavailable
- Full fallback to manual testing workflows
- Traditional test execution continues
- No loss of core development functionality
- Clear indication: "Playwright MCP unavailable - using manual testing"

## Benefits

### For Quality Assurance
- **Automation**: Automated end-to-end test generation and execution
- **Coverage**: Cross-browser testing across multiple environments
- **Visual Testing**: Screenshot comparison and visual regression detection
- **Debugging**: AI-assisted analysis of test failures and application issues

### for Web Development
- **Validation**: Automated user interface and interaction validation
- **Documentation**: Living documentation through automated testing
- **Regression**: Early detection of functionality regressions
- **Performance**: Automated performance and accessibility testing

### For Development Workflow
- **Integration**: Seamless integration between development and testing
- **Quality Gates**: Automated quality assurance in development pipeline
- **Efficiency**: Reduced manual testing overhead and faster feedback
- **Insight**: Better understanding of application behavior and user flows

## Troubleshooting

### Common Issues

**1. "Playwright MCP requirements not met"**
- Install Playwright: `npm install -D @playwright/test`
- Install browsers: `npx playwright install`
- Ensure Claude Code CLI is available: `claude --version`

**2. "Browser launch failed"**
- Check browser installation: `npx playwright install chromium`
- Verify system dependencies (Linux): Install browser dependencies
- Check headless configuration for server environments

**3. "Element not found or timeout"**
- Increase timeout values in configuration
- Use more specific selectors or wait conditions
- Check for dynamic content loading and timing issues

### Debug Steps
1. Verify MCP server status: `claude mcp list`
2. Test browser launch: `npx playwright test --headed`
3. Check element selectors: Use browser developer tools
4. Review sessions configuration: `cat sessions/sessions-config.json`

## Best Practices

### Test Development
- Use semantic selectors (role, text) over CSS selectors when possible
- Implement proper wait conditions for dynamic content
- Organize tests with clear descriptions and grouping
- Maintain test data and fixtures for consistent testing

### Browser Automation
- Use appropriate browser contexts for isolation
- Configure timeouts based on application performance characteristics
- Implement screenshot comparison for visual regression testing
- Use headless mode for CI/CD pipeline integration

### Integration
- Enable Playwright MCP during installation for best testing experience
- Configure appropriate browser and automation settings
- Framework supports existing Playwright configurations
- Provides clear feedback about test execution and results

## Future Enhancements

### Planned Integrations
- Integration with CI/CD pipelines for automated testing
- Advanced visual regression testing with AI-powered comparison
- Performance testing and monitoring integration
- Accessibility testing automation and validation

### Extensibility
The Playwright MCP infrastructure supports integration with other testing frameworks and provides a foundation for comprehensive quality assurance workflows in the cc-sessions framework.