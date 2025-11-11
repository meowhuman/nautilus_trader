---
model: claude-haiku-4-5-20251001
description: Interactive guide to create custom slash commands - helps design and structure new commands for any use case
argument-hint: [COMMAND_NAME] [BRIEF_DESCRIPTION]
allowed-tools: Read, Write, Bash
---

# Purpose

Help users design, plan, and create new custom slash commands for ANY project or workflow. This guide provides:

- **Command structure overview** - YAML frontmatter + Markdown sections
- **Reference examples** - Real-world patterns from existing commands
- **Template sections** - Copy-paste ready structure for new commands
- **Best practices** - Design principles for effective commands
- **Project-agnostic approach** - Works with any tool, language, or workflow

Use this helper to create commands that automate workflows, integrate tools, or solve problems specific to your project.

## Quick Start

1. **Plan your command**: What problem does it solve?
2. **Choose a name**: Keep it descriptive (e.g., `/test-deploy`, `/audit-logs`, `/format-code`)
3. **Define arguments**: What inputs does the command need?
4. **Follow the structure**: Use the template sections below
5. **Test and refine**: Validate with real usage

## Command Structure Overview

Every custom command needs these components:

### 1. YAML Frontmatter (Required)

```yaml
---
model: claude-haiku-4-5-20251001
description: One-line description of what the command does
argument-hint: [ARG1] [ARG2] [ARG3]
allowed-tools: Bash, Read, Write, Grep, Glob
---
```

**Fields**:
- `model`: Claude model to use (recommended: claude-haiku-4-5-20251001 for speed)
- `description`: Brief explanation of command purpose
- `argument-hint`: Parameters the command accepts (in brackets)
- `allowed-tools`: Which tools the command can use

### 2. Core Sections (Recommended)

| Section | Purpose | Example |
|---------|---------|---------|
| **Purpose** | What does the command do? Why use it? | "Automate testing and deployment process" |
| **Variables** | Key variables and their values | `PROJECT_DIR=$1`, `BUILD_TYPE=$2` |
| **Instructions** | How to use; key guidelines | "Validates prerequisites before proceeding" |
| **Workflow** | Step-by-step process (numbered) | "1. Validate inputs", "2. Build project", etc. |
| **Report** | Output format after completion | What information to display to user |
| **Error Handling** | What can go wrong? How to fix? | Common issues and solutions |
| **Examples** | Real usage scenarios | Different use cases |
| **Troubleshooting** | Detailed problem-solving guide | Step-by-step recovery procedures |

## Reference Examples

### Example 1: setup_claude_prompt.md

**Purpose**: Set up Claude Code configuration in any project

**Structure**:
- Purpose & rationale
- Variables (file paths, defaults)
- Instructions (how command should behave)
- Workflow (validation → copy → customize → verify)
- Report (clear status format)
- Error handling (comprehensive table)
- Examples (multiple use cases)
- Troubleshooting (detailed recovery)

**Key Features**:
✓ Handles both new and existing configurations
✓ Validates prerequisites before proceeding
✓ Provides clear next steps
✓ Supports customization per project

### Example 2: git-fork-and-setup.md

**Purpose**: Automate GitHub workflow for ANY forked project

**Structure**:
- Purpose (works with multiple projects)
- Variables (UPSTREAM_REPO parameter for flexibility)
- Instructions (step-by-step GitHub operations)
- Workflow (auth → fork → commit → push)
- Report (project-specific summary)
- Error handling (GitHub-specific issues)
- Examples (multiple different projects)
- Usage patterns (various development workflows)

**Key Features**:
✓ Generic design (accepts project as parameter)
✓ Auto-detects and validates inputs
✓ Comprehensive error messages
✓ Multiple real-world examples

## Template Structure

Use this template to create a new custom command:

```markdown
---
model: claude-haiku-4-5-20251001
description: [ONE-LINE DESCRIPTION]
argument-hint: [ARG1] [ARG2]
allowed-tools: Bash, Read, Write
---

# Purpose

[2-3 sentences explaining what the command does]
[Why would someone use this?]

## Variables

\`\`\`
VAR1: $1 (description)
VAR2: $2 (description)
CONFIG_FILE: path/to/config
\`\`\`

## Instructions

- [Key guideline 1]
- [Key guideline 2]
- [Validation approach]

## Workflow

### 1. Validate Prerequisites

Check that:
- [Prerequisite 1]
- [Prerequisite 2]

Report status and error if any fails.

### 2. [Main Step 1]

Do [action]. Display: "[status message]"

### 3. [Main Step 2]

Do [action]. Display: "[status message]"

### 4. Report Success

Follow the Report section format below.

## Report

After successful completion:

\`\`\`
=== Command Complete ===

✓ Section 1:
  Item 1: [value]
  Item 2: [value]

✓ Section 2:
  Item 1: [value]
  Item 2: [value]

✓ Next Steps:
  1. [Action 1]
  2. [Action 2]
\`\`\`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Error message" | Why it happens | How to fix it |

## Examples

### Example 1: [Scenario]

\`\`\`bash
/command-name "argument"
\`\`\`

Result: [What happens]

### Example 2: [Different scenario]

\`\`\`bash
/command-name "different" "args"
\`\`\`

Result: [What happens]

## Troubleshooting

### "Specific Error"

1. **Check X**: \`command to run\`
2. **Verify Y**: Look for Z
3. **Fix**: Run \`recovery command\`

## Summary

The \`/command-name\` command provides:

✓ [Feature 1]
✓ [Feature 2]
✓ [Feature 3]

Use whenever you need to [primary use case].
```

## Design Principles

### 1. **Clear Purpose**
- One command = one job
- Solves a specific problem
- Name clearly indicates function

### 2. **Flexible Arguments**
- Accept parameters for customization
- Use $1, $2, $3 for positional arguments
- Validate arguments before proceeding

### 3. **Robust Validation**
- Check prerequisites early
- Provide helpful error messages
- Suggest solutions, not just problems

### 4. **Clear Workflow**
- Number steps 1, 2, 3...
- Each step has clear input/output
- Easy to follow and debug

### 5. **Comprehensive Examples**
- Show basic usage
- Show advanced usage
- Show different scenarios

### 6. **Helpful Error Handling**
- List common issues with solutions
- Provide recovery procedures
- Help users diagnose problems

## Creation Checklist

When creating a new custom command:

- [ ] **Name**: Chosen a descriptive command name
- [ ] **Purpose**: Written clear purpose statement
- [ ] **Arguments**: Defined required/optional parameters
- [ ] **Variables**: Listed all key variables
- [ ] **Workflow**: Planned numbered steps
- [ ] **Validation**: Identified prerequisites to check
- [ ] **Report**: Designed output format
- [ ] **Errors**: Listed possible failures & solutions
- [ ] **Examples**: Provided 2-3 real usage examples
- [ ] **Troubleshooting**: Added recovery procedures
- [ ] **Test**: Verified command works as designed

## Project-Agnostic Design

To make commands work across projects:

✓ **Use parameters** - Accept project/file paths as arguments
✓ **Auto-detect** - Identify configuration from current context
✓ **Validate inputs** - Check arguments before proceeding
✓ **Generic messages** - Reference variables, not hardcoded values
✓ **Examples** - Show usage with different projects
✓ **Error guidance** - Adapt help based on context

### Example: Generic vs Hardcoded

❌ **Hardcoded (Bad)**:
```markdown
### 4. Build nautilus_trader

Run: `cargo build -p nautilus_trader`
```

✓ **Generic (Good)**:
```markdown
### 4. Build Project

Extract PROJECT_NAME from $1
Run: `cargo build -p {$PROJECT_NAME}`
Display: "Building $PROJECT_NAME..."
```

## Common Command Types

### Type 1: Build/Deploy Commands
- Purpose: Automate build and deployment
- Arguments: Project name, environment, config file
- Workflow: Validate → Build → Test → Deploy
- Examples: `/deploy-staging`, `/build-release`, `/run-tests`

### Type 2: Data Processing Commands
- Purpose: Transform or analyze data
- Arguments: Input file, output format, options
- Workflow: Read input → Process → Validate → Output
- Examples: `/convert-logs`, `/analyze-metrics`, `/format-data`

### Type 3: Setup/Configuration Commands
- Purpose: Initialize or configure systems
- Arguments: Project path, config name, template
- Workflow: Validate → Create → Configure → Verify
- Examples: `/setup-env`, `/init-db`, `/configure-ci`

### Type 4: Integration Commands
- Purpose: Connect to external systems
- Arguments: API key, endpoint, data source
- Workflow: Auth → Connect → Execute → Report
- Examples: `/sync-github`, `/upload-s3`, `/notify-slack`

### Type 5: Utility Commands
- Purpose: Automate routine tasks
- Arguments: File paths, options, filters
- Workflow: Input → Process → Output
- Examples: `/cleanup-cache`, `/backup-data`, `/generate-report`

## Real-World Examples to Reference

### setup_claude_prompt.md
Location: `.claude/commands/km-selection/setup_claude_prompt.md`

Learn about:
- Multi-step workflows
- Configuration management
- User interaction and choices
- Comprehensive verification
- Clear next steps

### git-fork-and-setup.md
Location: `.claude/commands/km-selection/git-fork-and-setup.md`

Learn about:
- Generic project handling
- Parameter parsing
- External tool integration
- Fork/clone operations
- Multi-project examples

## Tips for Effective Commands

1. **Start Simple**: Basic version first, then add features
2. **Test Thoroughly**: Try with different inputs and edge cases
3. **Document Well**: Clear explanations help users understand
4. **Provide Examples**: Show real-world usage scenarios
5. **Plan Error Cases**: Anticipate what can go wrong
6. **Make it Reusable**: Design for multiple projects/contexts
7. **Update After Use**: Refine based on actual usage feedback

## Command Naming Convention

Good command names:
- `/setup-env` - Clear what it does
- `/deploy-staging` - Action + target
- `/generate-report` - Verb + object
- `/sync-github` - Action + service
- `/backup-database` - Action + resource

Avoid:
- `/do-stuff` - Too vague
- `/helper123` - Not descriptive
- `/x` - Too short
- `/my-special-thing` - Too specific

## Next Steps

1. **Identify your need**: What problem needs solving?
2. **Plan the workflow**: Write down the steps
3. **Choose your name**: Make it descriptive
4. **Copy the template**: Use the structure provided
5. **Fill in sections**: Purpose, Variables, Workflow, etc.
6. **Add examples**: Show real usage
7. **Test it**: Run and validate
8. **Refine**: Improve based on testing
9. **Document**: Add to your project's command directory
10. **Share**: Help others use it

## Getting Help

For reference implementations:
- Check `.claude/commands/km-selection/` for existing patterns
- Look at `setup_claude_prompt.md` for configuration patterns
- Look at `git-fork-and-setup.md` for generic project patterns
- Review other `.md` files in `.claude/commands/` for inspiration

## Summary

Creating custom commands:

✓ **Flexible**: Work across projects and workflows
✓ **Documented**: Clear purpose and usage
✓ **Robust**: Handle errors gracefully
✓ **Practical**: Solve real problems
✓ **Reusable**: Design for multiple use cases

Use this guide to create commands that make your development workflow faster, safer, and more consistent!

## Template Quick Copy

Save this filename as: `.claude/commands/km-selection/your-command-name.md`

```markdown
---
model: claude-haiku-4-5-20251001
description: [Your command description]
argument-hint: [ARG1] [ARG2]
allowed-tools: Bash, Read, Write
---

# Purpose

[What does this command do?]

## Variables

\`\`\`
VAR1: $1 (description)
VAR2: $2 (description)
\`\`\`

## Instructions

- [Guideline 1]
- [Guideline 2]

## Workflow

### 1. [Step Name]

[Action and validation]

## Report

✓ Status displayed after completion

## Error Handling

| Error | Solution |
|-------|----------|
| Issue | Fix |

## Examples

\`\`\`bash
/your-command arg1 arg2
\`\`\`

## Troubleshooting

### "Problem"

Solution steps here.

## Summary

The command provides clear value for your workflow.
```

Start creating! 🚀
