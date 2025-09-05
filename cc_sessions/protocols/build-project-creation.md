# Build Project Creation Protocol

## Overview
This protocol manages the creation and tracking of large build projects using structured implementation plan files. Build projects differ from regular tasks by supporting multi-file plans with numbered steps in x.x format (e.g., 1.11, 2.4) and step-by-step validation.

## Build Project Directory Structure

Build projects are stored in `sessions/build-projects/` with this structure:
```
sessions/build-projects/
├── project-name/
│   ├── plan/                    # Implementation plan files  
│   │   ├── 01-foundation.md     # Phase files with numbered steps
│   │   ├── 02-core-features.md
│   │   └── 03-integration.md
│   ├── state.json              # Project tracking state
│   └── README.md               # Project overview
```

## Implementation Plan Format

Each plan file must follow this structure:

```markdown
# Phase Name

## 1.1 Step Title
**Implementation:**
- Detailed implementation instructions
- Code examples or patterns
- File locations and changes needed

**Validation:**
- [ ] Specific validation criteria
- [ ] Tests to run
- [ ] Expected outcomes

## 1.2 Next Step Title
...
```

## Step Numbering System

- **Major version** (1, 2, 3): Represents phases or major components
- **Minor version** (.1, .2, .3): Individual steps within that phase
- Examples: 1.1, 1.2, 2.1, 2.2, 3.1, 3.2
- Steps can be worked on non-sequentially but dependencies should be noted

## Creating a Build Project

### 1. Initialize Project Structure

```bash
# Create project directory
mkdir sessions/build-projects/[project-name]
mkdir sessions/build-projects/[project-name]/plan

# Copy template
cp cc_sessions/templates/BUILD_PROJECT_TEMPLATE.md sessions/build-projects/[project-name]/README.md
```

### 2. Project State Initialization

Create `sessions/build-projects/[project-name]/state.json`:
```json
{
  "project": "project-name",
  "status": "pending",
  "created": "2025-01-15",
  "current_step": null,
  "completed_steps": [],
  "active_branch": null,
  "plan_files": [],
  "total_steps": 0,
  "completion_percentage": 0
}
```

### 3. Plan File Processing

The build project parser agent will:
1. Scan all `.md` files in the `plan/` directory
2. Extract numbered steps in x.x format  
3. Parse implementation and validation sections
4. Update project state with discovered steps
5. Calculate completion percentage

## Working on Build Project Steps

### Step Selection Process

1. **List Available Steps**:
   ```bash
   /build-project list [project-name]
   ```

2. **Select Step to Work On**:
   ```bash  
   /build-project work [project-name] [step-number]
   ```

3. **System Actions**:
   - Creates git branch: `build-project/[project-name]/step-[step-number]`
   - Updates current task state to reference the step
   - Provides step implementation details and validation criteria
   - Tracks step as "in-progress"

### Step Completion Process

1. **Mark Step Complete**:
   ```bash
   /build-project complete [project-name] [step-number]
   ```

2. **System Actions**:
   - Runs validation criteria if specified
   - Updates project state with completed step
   - Recalculates completion percentage
   - Optionally merges branch or prompts for merge

## State Management

### Project State Schema

```json
{
  "project": "string",           // Project name
  "status": "pending|active|completed|blocked",
  "created": "YYYY-MM-DD",       // Creation date
  "updated": "YYYY-MM-DD",       // Last update
  "current_step": "1.2",         // Currently active step
  "completed_steps": ["1.1"],    // Array of completed step numbers
  "active_branch": "build-project/name/step-1-2",
  "plan_files": ["01-phase.md"], // Discovered plan files
  "total_steps": 12,             // Total steps across all plan files
  "completion_percentage": 8.3,  // Calculated completion
  "step_details": {              // Parsed step information
    "1.1": {
      "title": "Setup Foundation",
      "file": "01-foundation.md",
      "implementation": "...",
      "validation": ["criteria1", "criteria2"],
      "status": "completed",
      "completed_date": "2025-01-15"
    },
    "1.2": {
      "title": "Configure Database", 
      "file": "01-foundation.md",
      "implementation": "...",
      "validation": ["criteria1"],
      "status": "in-progress",
      "started_date": "2025-01-16"
    }
  }
}
```

### Integration with Current Task State

When working on a build project step, update `.claude/state/current_task.json`:
```json
{
  "task": "build-project:project-name:1.2",
  "branch": "build-project/project-name/step-1-2", 
  "services": ["extracted-from-step-details"],
  "updated": "2025-01-15",
  "build_project": {
    "project": "project-name",
    "step": "1.2",
    "step_title": "Configure Database"
  }
}
```

## CLI Commands

### Available Commands

- `/build-project create [name]` - Initialize new build project
- `/build-project list` - Show all build projects
- `/build-project list [name]` - Show steps for specific project
- `/build-project work [name] [step]` - Start working on specific step
- `/build-project complete [name] [step]` - Mark step as completed
- `/build-project status [name]` - Show project progress
- `/build-project parse [name]` - Re-parse plan files for changes

### Command Integration

Commands are implemented as markdown files in `cc_sessions/commands/` and processed by the existing command system during installation.

## Validation System

### Automatic Validation

When completing a step, the system can:
1. Parse validation criteria from the step definition
2. Execute validation commands (tests, checks, etc.)
3. Report validation results
4. Block completion if validation fails

### Validation Criteria Format

In plan files:
```markdown
**Validation:**
- [ ] Run tests: `npm test`  
- [ ] Check configuration: `config-check.sh`
- [ ] Verify API endpoint: `curl http://localhost:3000/health`
- [ ] Manual verification: Database tables created correctly
```

## DAIC Integration

Build project steps integrate with DAIC methodology:
- **Discussion**: Review step implementation details before starting
- **Alignment**: Use trigger phrases to begin step work  
- **Implementation**: Execute step with proper branch context
- **Check**: Run validation criteria before marking complete

## Hook Integration

Existing hooks are extended to support build project context:
- Branch enforcement validates against build project branch patterns
- Current task detection recognizes build project step format
- Tool blocking respects build project workflow phases

## Migration from Tasks

Existing complex tasks can be converted to build projects:
1. Create build project structure
2. Break task into numbered steps across plan files
3. Add implementation and validation details
4. Migrate work log to project state tracking

## Best Practices

### Plan File Organization
- Keep phases focused and cohesive
- Number steps logically within phases
- Include clear validation criteria for each step
- Reference external documentation and patterns

### Step Granularity
- Each step should be 1-4 hours of focused work
- Steps should have clear completion criteria
- Avoid steps that are too small (< 30 minutes) or large (> 1 day)
- Include validation that can be automated where possible

### Branch Management
- Each step gets its own branch for isolation
- Branches follow pattern: `build-project/[name]/step-[number]`
- Consider step dependencies when merging
- Clean up completed step branches periodically

## Error Handling

### Common Issues
- **Plan file parse errors**: Validate markdown format and step numbering
- **Step dependency conflicts**: Check for logical step ordering
- **Validation failures**: Review criteria and fix implementation
- **State synchronization**: Re-parse project files if state becomes inconsistent

### Recovery Procedures
- Re-parsing plan files updates project state
- Manual state editing for complex recovery scenarios
- Branch cleanup commands for orphaned step branches
- Project state reset and re-initialization options