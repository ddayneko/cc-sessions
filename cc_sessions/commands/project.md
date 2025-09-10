---
allowed-tools: Bash(python3:*), Bash(echo:*)
argument-hint: "create [name] | list [name?] | work [name] [step] | complete [name] [step] | status [name] | parse [name]"
description: Manage complex multi-step projects with implementation plans and step tracking
---

!`python3 "$CLAUDE_PROJECT_DIR/.claude/commands/project.py" $ARGUMENTS && echo "Project command completed successfully." || echo "Project command failed. Check your arguments and try again."`