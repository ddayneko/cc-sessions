---
task: m-implement-build-project-tracking
branch: feature/implement-build-project-tracking
status: pending
created: 2025-01-15
modules: [install.js, install.py, protocols, agents, templates, commands]
---

# Build Project Tracking System

## Problem/Goal
Implement a comprehensive system for tracking larger build projects using .md formatted implementation plans. Users should be able to drop implementation plan files (possibly split into multiple files) and have cc-sessions automatically parse, track, and validate numbered steps in x.x format (e.g., 1.11, 2.4).

## Success Criteria
- [ ] System can detect and parse .md implementation plan files in user directory
- [ ] Process similar to "Create a task" but specifically for implementation plans
- [ ] Can identify and track numbered steps in x.x format (1.11, 2.4, etc.)
- [ ] Step completion tracking with persistent state
- [ ] Validation criteria parsing and execution for each step
- [ ] Integration with existing cc-sessions workflow and DAIC methodology
- [ ] Support for multi-file implementation plans
- [ ] CLI commands for managing implementation plans
- [ ] Status reporting and progress visualization
- [ ] Documentation for users on implementation plan format

## Context Manifest

### How the Current cc-sessions System Works: Task Management and Package Distribution

The cc-sessions framework is a sophisticated workflow management system built around the DAIC (Discussion-Alignment-Implementation-Check) methodology. Understanding its architecture is critical because the build project tracking system must integrate seamlessly with existing patterns while extending them to handle numbered step tracking.

**Installation and Package Distribution Flow:**

When users install cc-sessions via `pipx install cc-sessions` or `npm install -g cc-sessions`, they're getting a dual-installer system. The Python package (defined in `pyproject.toml`) provides the core installer via `cc_sessions.install:main` as a console script, while the Node.js package (`package.json`) wraps the same functionality for JavaScript environments. Both installers detect the user's project directory (avoiding site-packages/node_modules), create the necessary directory structure (`.claude/hooks`, `sessions/tasks`, `sessions/protocols`), and copy template files from the package's embedded resources.

The installation process is critical because it establishes the foundational patterns that build project tracking must follow. Files are copied from `cc_sessions/hooks/*.py`, `cc_sessions/protocols/*.md`, `cc_sessions/agents/*.md`, `cc_sessions/templates/*.md`, and `cc_sessions/commands/*.md` into the user's project. The installer also configures Claude Code hooks in `.claude/settings.json` using platform-specific command formats (Windows uses `python "%CLAUDE_PROJECT_DIR%\.claude\hooks\script.py"` while Unix uses `$CLAUDE_PROJECT_DIR/.claude/hooks/script.py`).

**Task Creation and Management System:**

The existing task system (defined in `cc_sessions/protocols/task-creation.md`) uses a structured approach with priority prefixes (`h-`, `m-`, `l-`, `?-`) and type prefixes (`implement-`, `fix-`, `refactor-`, etc.) that map to git branch patterns. Tasks can be either single files for focused work (`h-fix-auth-redirect.md`) or directories for complex multi-phase projects (`h-implement-auth/README.md`). Each task includes YAML frontmatter with fields: `task`, `branch`, `status`, `created`, and `modules` (array of affected services).

The critical state management happens through `.claude/state/current_task.json` which maintains the active task context with the exact structure:
```json
{
  "task": "task-name",        // NO path, NO .md extension  
  "branch": "feature/branch", // Git branch name
  "services": ["service1"],   // Array of affected services
  "updated": "2025-01-15"     // Current date
}
```

**Hook System and DAIC Enforcement:**

The enforcement mechanism operates through Claude Code's hook system. `cc_sessions/hooks/sessions-enforce.py` runs before Edit/Write/MultiEdit tools and blocks them in discussion mode unless specific trigger phrases are detected by `cc_sessions/hooks/user-messages.py`. The system maintains DAIC state in `.claude/state/daic-mode.json` with modes "discussion" or "implementation".

Branch enforcement is particularly sophisticated - the hook checks if the current git branch matches the expected task branch, handles submodule scenarios, and validates that files being edited belong to services listed in the task's `modules` array. This creates a disciplined workflow where developers must explicitly declare which components they're touching before the system allows edits.

**Agent System for Specialized Operations:**

The agent system (templates in `cc_sessions/agents/*.md`) delegates heavy operations to specialized contexts. Agents like `context-gathering`, `logging`, and `code-review` receive full conversation transcripts and operate in isolation, preventing context pollution in the main thread. Each agent has specific tools permissions and behavioral instructions defined in their markdown templates.

**CLI Command System:**

CLI commands are implemented as markdown files in `cc_sessions/commands/*.md` that use Claude Code's command system. For example, `/add-trigger` executes inline Python to modify `sessions/sessions-config.json`. The `daic` command (distributed as shell scripts for Unix and .cmd/.ps1 for Windows) toggles DAIC mode by importing `shared_state.py` from the hooks directory.

### For Build Project Tracking Implementation: Integration Points and Architecture

The build project tracking system needs to extend this architecture to handle implementation plans with numbered steps in x.x format, while maintaining compatibility with existing patterns.

**Step Parsing and State Management Integration:**

Since the existing system already manages task state through `.claude/state/current_task.json`, build project tracking will need a parallel state structure. The system should create `.claude/state/build_projects.json` to track active implementation plans, completed steps, and progress. Each implementation plan should map to a temporary task context, leveraging the existing branch enforcement and service tracking mechanisms.

The step parsing logic needs to extract numbered steps (1.11, 2.4, etc.) from implementation plan markdown files, along with their validation criteria and implementation instructions. This parsing should happen in a new agent (similar to `context-gathering`) that can read multiple files and build a comprehensive step registry.

**Protocol System Extension:**

A new protocol `cc_sessions/protocols/build-project-startup.md` should handle the workflow of detecting implementation plan files, parsing their structure, and presenting step selection to users. This protocol would be triggered similarly to how task creation works - through specific user phrases that get detected by the user-messages hook.

The existing task creation pattern of copying templates and updating state files provides the blueprint. Build project tracking should follow the same pattern but operate on a different file structure in a designated directory (perhaps `sessions/build-projects/`).

**Hook System Integration:**

The sessions-enforce.py hook already has sophisticated logic for task-based workflow enforcement. Build project tracking should extend this by adding build project context checking. When a user is working on a specific step, the system should validate that:
1. They're on the correct branch for the implementation plan
2. The files they're editing are relevant to the current step  
3. Step dependencies are satisfied before allowing work to begin

**CLI Command Extensions:**

New commands need to be added to `cc_sessions/commands/` for build project management:
- `/list-projects` - Show active implementation plans
- `/select-step` - Choose a specific step to work on  
- `/mark-step-complete` - Mark current step as finished
- `/validate-step` - Run validation criteria for current step
- `/project-status` - Show overall progress across all plans

**Agent System for Step Validation:**

A new agent `build-project-validation` should handle running validation criteria for completed steps. This agent would receive the step definition, implementation details, and project state, then execute validation logic and update progress tracking.

**Installation and Distribution:**

The new functionality must be packaged within the existing installer system. Templates for implementation plan structure should be added to `cc_sessions/templates/`, new protocols to `cc_sessions/protocols/`, and any new agents to `cc_sessions/agents/`. The pyproject.toml and package.json files already include the necessary glob patterns to package these resources.

### Technical Reference Details

#### Component Interfaces & Signatures

**Core State Management (extending shared_state.py):**
```python
def get_build_project_state() -> dict
def set_current_step(project_id: str, step: str)  
def mark_step_complete(project_id: str, step: str, validation_passed: bool)
def list_active_projects() -> list[dict]
```

**Step Parser (new module):**
```python
def parse_implementation_plan(file_path: Path) -> dict
def extract_numbered_steps(content: str) -> list[dict] 
def validate_step_format(step_number: str) -> bool
def get_step_dependencies(steps: list[dict]) -> dict[str, list[str]]
```

**Hook Integration (extending sessions-enforce.py):**
```python
def check_build_project_context(tool_input: dict) -> bool
def validate_step_file_access(file_path: str, current_step: str) -> bool
```

#### Data Structures

**Build Project State (.claude/state/build_projects.json):**
```json
{
  "active_projects": {
    "project-name": {
      "plan_files": ["path/to/plan1.md", "path/to/plan2.md"],
      "current_step": "1.11",
      "completed_steps": ["1.1", "1.10"], 
      "branch": "feature/implement-project-name",
      "created": "2025-01-15",
      "last_updated": "2025-01-15"
    }
  }
}
```

**Step Structure (parsed from markdown):**
```python
{
  "number": "1.11",
  "title": "Step title", 
  "description": "Implementation instructions",
  "validation_criteria": ["criteria1", "criteria2"],
  "dependencies": ["1.1", "1.10"],
  "files_to_modify": ["src/component.py", "tests/test_component.py"],
  "estimated_time": "2h"
}
```

#### Configuration Requirements

**New config in sessions/sessions-config.json:**
```json
{
  "build_projects": {
    "enabled": true,
    "plans_directory": "sessions/build-projects", 
    "auto_detect_plans": true,
    "step_validation_timeout": 300,
    "branch_prefix": "implement-"
  }
}
```

#### File Locations

- Implementation goes here: `cc_sessions/build_projects/` (new module)
- Step parser: `cc_sessions/build_projects/parser.py`
- State management: `cc_sessions/build_projects/state.py`  
- Hook extensions: `cc_sessions/hooks/build_project_hooks.py`
- New protocols: `cc_sessions/protocols/build-project-*.md`
- New agents: `cc_sessions/agents/build-project-*.md`
- New commands: `cc_sessions/commands/build-project-*.md`
- Templates: `cc_sessions/templates/BUILD_PROJECT_TEMPLATE.md`
- Tests: `tests/test_build_projects.py`

## Context Files
<!-- Updated by context-gathering agent -->
- @cc_sessions/install.py          # Python installer integration patterns
- @install.js                      # Node.js installer integration patterns  
- @cc_sessions/protocols/task-creation.md # Existing task creation workflow to extend
- @cc_sessions/hooks/sessions-enforce.py # DAIC enforcement and branch validation to extend
- @cc_sessions/hooks/shared_state.py # State management patterns to extend
- @cc_sessions/agents/context-gathering.md # Agent system patterns to replicate
- @cc_sessions/templates/TEMPLATE.md # Task template structure to adapt
- @cc_sessions/commands/add-trigger.md # CLI command implementation patterns
- @pyproject.toml                  # Python package configuration for distribution
- @package.json                    # Node.js package configuration for distribution

## User Notes
Implementation plan files should support:
- Numbered steps in x.x format (1.11, 2.4, etc.)
- Validation criteria per step
- Implementation instructions per step
- Multi-file plan support
- Integration with git branch management
- Step dependency tracking
- Progress persistence across sessions

Expected workflow:
1. User drops implementation plan .md files in designated directory
2. cc-sessions detects and parses plan structure
3. User can select specific step to work on
4. System creates appropriate task/branch context
5. Validation runs after step completion
6. Progress tracked and reported

## Work Log
- [2025-01-15] Task created, awaiting context gathering and implementation planning