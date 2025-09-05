---
project: [project-name]
status: pending
created: YYYY-MM-DD
description: [Brief project description]
repository: [git-repository-url-if-applicable]
---

# [Project Title]

## Project Overview
[Comprehensive description of what this build project aims to accomplish]

## Goals and Success Criteria
- [ ] Primary objective 1
- [ ] Primary objective 2
- [ ] Primary objective 3

## Architecture Overview
[High-level description of the system architecture, components, and their relationships]

## Implementation Phases
This project is organized into phases, each containing numbered steps:

### Phase 1: [Phase Name]
- Steps 1.1 - 1.x: [Brief description of this phase]
- Files: `plan/01-phase-name.md`

### Phase 2: [Phase Name]  
- Steps 2.1 - 2.x: [Brief description of this phase]
- Files: `plan/02-phase-name.md`

### Phase 3: [Phase Name]
- Steps 3.1 - 3.x: [Brief description of this phase]  
- Files: `plan/03-phase-name.md`

## Dependencies and Prerequisites
- [ ] Required tools and software
- [ ] Environment setup requirements
- [ ] External service dependencies
- [ ] Knowledge or documentation prerequisites

## Risk Assessment
**High Risk:**
- [Risk 1]: [Mitigation strategy]

**Medium Risk:**
- [Risk 2]: [Mitigation strategy]

**Low Risk:**
- [Risk 3]: [Monitoring approach]

## Resources and References
- [Documentation links]
- [API references]
- [Design documents]
- [External tools and libraries]

## Project Notes
[Any additional context, constraints, or special considerations]

---

## Quick Start

1. **Initialize project tracking:**
   ```bash
   /build-project parse [project-name]
   ```

2. **View available steps:**
   ```bash
   /build-project list [project-name]
   ```

3. **Start working on a step:**
   ```bash
   /build-project work [project-name] 1.1
   ```

4. **Complete a step:**
   ```bash
   /build-project complete [project-name] 1.1
   ```

5. **Check progress:**
   ```bash
   /build-project status [project-name]
   ```

---

## Implementation Plan Files

Create detailed implementation plans in the `plan/` directory following this structure:

### File: `plan/01-foundation.md`
```markdown
# Phase 1: Foundation

## 1.1 Environment Setup
**Implementation:**
- Install required dependencies
- Configure development environment  
- Set up project structure

**Validation:**
- [ ] All dependencies installed successfully
- [ ] Development server starts without errors
- [ ] Project structure matches specification

## 1.2 Database Configuration
**Implementation:**
- Set up database connection
- Create initial schema
- Configure connection pooling

**Validation:**
- [ ] Database connection established
- [ ] Schema created successfully
- [ ] Connection pool configured and tested
```

### File: `plan/02-core-features.md`
```markdown
# Phase 2: Core Features

## 2.1 User Authentication
**Implementation:**
- Implement authentication system
- Set up session management
- Create user registration flow

**Validation:**
- [ ] Users can register successfully
- [ ] Login/logout works correctly
- [ ] Sessions persist across requests
- [ ] Security tests pass

## 2.2 API Endpoints
**Implementation:**
- Create REST API endpoints
- Implement request validation
- Add error handling

**Validation:**
- [ ] All endpoints respond correctly
- [ ] Input validation works
- [ ] Error responses are properly formatted
- [ ] API tests pass
```

Continue this pattern for additional phases and steps as needed.