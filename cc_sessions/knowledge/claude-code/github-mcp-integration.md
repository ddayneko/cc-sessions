# GitHub MCP Integration Guide

## Overview

The cc-sessions framework integrates with [GitHub MCP](https://github.com/github/github-mcp-server) to provide comprehensive repository management, issue tracking, pull request automation, and CI/CD workflow intelligence. This integration enables direct GitHub interaction, automated development workflows, and seamless git operations through GitHub's API.

## Architecture

### Core Components

**1. Enhanced Agent Integration** (`cc_sessions/agents/`)
- **Context-Gathering Agent**: Repository analysis, issue tracking, and PR context integration
- **Code-Review Agent**: Automated PR creation, review management, and merge operations  
- **Semantic-Analysis Agent**: Cross-repository code analysis and git workflow automation

**2. Git Workflow Automation**
- Direct commit creation through GitHub API
- Automated pull request creation and management
- Branch operations and merge workflow automation
- CI/CD pipeline monitoring and analysis

**3. Installation Integration**
- Both Python and Node.js installers detect and configure GitHub MCP
- Docker-based MCP server deployment
- Automatic Claude Code MCP server configuration

## Installation Methods

### Automatic (Recommended)
During cc-sessions installation:
1. Installer detects `docker` and `claude` commands
2. Offers optional GitHub MCP installation
3. Configures MCP server automatically: `claude mcp add github docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server`
4. Updates configuration with `github_mcp.enabled: true`

### Manual Installation
```bash
# Prerequisites: Docker and GitHub Personal Access Token
docker pull ghcr.io/github/github-mcp-server

# Add GitHub MCP server to Claude Code
claude mcp add github docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server

# Set environment variable
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here

# Update sessions configuration
# Edit sessions/sessions-config.json:
{
  "github_mcp": {
    "enabled": true,
    "auto_activate": true,
    "requires_pat": true
  }
}
```

## Available Tools

### Repository & Information
- `mcp__github__get_repo` - Retrieve repository information and metadata
- `mcp__github__search_repositories` - Search across GitHub repositories
- `mcp__github__get_file_contents` - Retrieve specific file contents from repositories

### Issues & Pull Requests
- `mcp__github__list_issues` - List and filter repository issues
- `mcp__github__get_issue` - Get detailed issue information
- `mcp__github__list_pull_requests` - List and filter pull requests
- `mcp__github__get_pull_request` - Get detailed PR information and changes
- `mcp__github__create_pull_request` - Create new pull request
- `mcp__github__merge_pull_request` - Merge pull request with options
- `mcp__github__create_pull_request_review` - Create pull request review

### Git Workflow & Commits
- `mcp__github__list_commits` - List and analyze repository commits
- `mcp__github__create_commit` - Create commits directly via GitHub API
- `mcp__github__create_tree` - Create git tree for commit structure
- `mcp__github__create_blob` - Create git blob for file content
- `mcp__github__create_ref` - Create new branch references
- `mcp__github__update_ref` - Update branch references
- `mcp__github__merge` - Merge branches via API
- `mcp__github__push_files` - Push multiple file changes in single commit

### CI/CD & Actions
- `mcp__github__get_workflow_runs` - Monitor GitHub Actions workflow execution
- `mcp__github__trigger_workflow` - Trigger workflow dispatches

## Usage Patterns

### Context Gathering Enhancement
Before GitHub MCP:
```markdown
1. Limited to local repository analysis
2. No integration with GitHub issues or discussions
3. Manual PR review and analysis
4. Separate workflow for repository operations
```

With GitHub MCP:
```markdown
1. Repository analysis across entire GitHub ecosystem
2. Issue-driven development with automatic context
3. PR analysis and automated review workflows
4. Integrated development and deployment pipeline
5. Cross-repository pattern analysis and insights
```

### Automated Task Completion Workflow
```bash
# Traditional approach
Manual git operations → Manual PR creation → Manual review → Manual merge

# GitHub MCP approach  
create_pull_request("feature-branch", "main", "Task completion") →
create_pull_request_review("APPROVE") →
merge_pull_request("squash") →
update_ref("delete-branch")
```

## Configuration

### Project Configuration (`sessions/sessions-config.json`)
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

### Authentication Setup
1. Create GitHub Personal Access Token at: https://github.com/settings/tokens
2. Required scopes: `repo`, `read:packages`, `read:org`, `workflow`
3. Set environment variable: `GITHUB_PERSONAL_ACCESS_TOKEN=your_token`
4. Configure Docker environment for MCP server access

## Task Completion Integration

### Automated Workflow Option
Enhanced task-completion.md protocol includes GitHub MCP option:

**Step 1: Offer GitHub Workflow**
```
"Would you like to use GitHub MCP for automated PR creation and merge? (y/n)"
```

**Step 2: Create Pull Request**
```
create_pull_request({
  title: "[Task] Brief description from task file",
  body: "Summary of changes and task completion",
  base: "main", 
  head: "current-feature-branch"
})
```

**Step 3: User Review & Merge Options**
```
"Pull Request created: [PR_URL]
Would you like me to:
1. Auto-merge immediately (if no conflicts)  
2. Wait for manual review and then merge
3. Leave open for manual handling"
```

**Step 4: Automated Merge & Cleanup**
```
merge_pull_request(merge_method: "squash") →
update_ref(delete_branch: true) →
Pull latest main locally
```

## Graceful Fallback

The integration enhances rather than replaces existing git functionality:

### When GitHub MCP Available
- Automated PR creation and management
- Issue-driven development workflows
- Repository analysis across GitHub ecosystem
- CI/CD pipeline integration and monitoring

### When GitHub MCP Unavailable
- Full fallback to local git operations
- Traditional branch/merge workflows continue
- No loss of core development functionality
- Clear indication: "GitHub MCP unavailable - using local git workflow"

## Benefits

### For Context Gathering
- **Repository Integration**: Seamless connection between local development and GitHub
- **Issue Tracking**: Automatic context gathering from GitHub issues and discussions
- **PR Analysis**: Comprehensive pull request analysis and review assistance
- **Cross-Repository**: Pattern analysis across entire GitHub ecosystem

### For Code Review
- **Automated Reviews**: Create and manage PR reviews programmatically
- **Workflow Integration**: Connect code review with GitHub's review system
- **Team Collaboration**: Enhanced visibility into team development activities
- **Quality Gates**: Integrate review requirements with merge workflows

### For Development Workflow
- **Workflow Automation**: Complete development lifecycle through GitHub API
- **Pipeline Monitoring**: Real-time visibility into CI/CD pipeline status
- **Branch Management**: Automated branch creation, merging, and cleanup
- **Integration**: Unified workflow between local development and GitHub

## Troubleshooting

### Common Issues

**1. "GitHub MCP requirements not met"**
- Install Docker: https://docs.docker.com/get-docker/
- Ensure Claude Code CLI is available: `claude --version`
- Verify Docker daemon is running: `docker ps`

**2. "Authentication failed"**
- Create Personal Access Token with correct scopes
- Verify token is set: `echo $GITHUB_PERSONAL_ACCESS_TOKEN`
- Check token permissions and expiration

**3. "Rate limit exceeded"**
- GitHub API has rate limits (5000/hour for authenticated requests)
- Enable rate limiting in configuration
- Consider using GitHub Enterprise for higher limits

### Debug Steps
1. Verify MCP server status: `claude mcp list`
2. Test Docker container: `docker run --rm ghcr.io/github/github-mcp-server --version`
3. Validate token: Test basic API call with curl
4. Review sessions configuration: `cat sessions/sessions-config.json`

## Best Practices

### Authentication Security
- Use Personal Access Tokens with minimal required scopes
- Regularly rotate tokens and update environment variables
- Never commit tokens to repositories
- Use organization tokens for team workflows

### Workflow Integration
- Enable GitHub MCP during installation for seamless experience
- Configure default organization/owner for streamlined operations
- Use automated PR workflow for consistent development practices
- Monitor rate limits and optimize API usage

### Team Collaboration
- Standardize PR templates and review processes
- Use GitHub MCP for consistent code review workflows
- Integrate with team notification systems
- Document workflow customizations in project configuration

## Future Enhancements

### Planned Integrations
- GitHub Discussions integration for requirements gathering
- GitHub Projects integration for task management
- Advanced security scanning and vulnerability management
- Team analytics and development insights

### Extensibility
The GitHub MCP infrastructure supports additional GitHub API integrations and provides a foundation for enterprise development workflow automation in the cc-sessions framework.