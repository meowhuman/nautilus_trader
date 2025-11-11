---
name: Project Setup Manager
description: Replicates the .claude directory structure from the multi-agent observability project template. Use when setting up a new project with Claude Code hooks, agents, skills, commands, and observability features, or when the user asks to setup project .claude configuration.
---

# Project Setup Manager

This skill manages the setup of new projects with the complete `.claude` configuration from the multi-agent observability template. It copies the entire structure including hooks, agents, skills, commands, output styles, and settings.

## Instructions

### Overview

This skill replicates the `.claude` directory structure documented in [reference_structure.md](docs/reference_structure.md). The template includes:

- **Hooks**: Event-driven scripts for observability and lifecycle management
- **Agents**: Custom agent definitions for specialized tasks
- **Skills**: Reusable capabilities (worktree management, video processing, etc.)
- **Commands**: Slash commands for common workflows
- **Output Styles**: Formatting templates for agent responses
- **Status Lines**: Custom CLI status displays
- **Settings**: Centralized configuration with hook registrations

### Prerequisites

Before running this skill, ensure:

1. **Target project exists** with a git repository
2. **Source template is accessible** at:
   `/Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude`
3. **uv is installed** for Python dependency management (if using hooks)
4. **Git is configured** (for worktree-related features)

### Workflow

#### Step 1: Verify Source Template

First, confirm the template directory exists and is accessible:

```bash
ls -la /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude
```

This should show:
- `agents/` directory
- `commands/` directory
- `hooks/` directory
- `output-styles/` directory
- `skills/` directory
- `status_lines/` directory
- `settings.json` file

#### Step 2: Determine Target Project

Identify where to copy the configuration. Use `$CLAUDE_PROJECT_DIR` or the current working directory:

```bash
echo "Target: $CLAUDE_PROJECT_DIR/.claude"
```

#### Step 3: Handle Existing Configuration

**If `.claude` directory already exists** in the target project:

1. Ask the user what to do:
   - **Merge**: Keep existing files, add missing ones from template
   - **Replace**: Back up current `.claude` to `.claude.backup`, then copy template
   - **Abort**: Don't modify existing configuration

2. For merge strategy:
   ```bash
   # Copy only missing directories/files
   # User can manually review conflicts
   ```

3. For replace strategy:
   ```bash
   mv .claude .claude.backup.$(date +%Y%m%d-%H%M%S)
   ```

**If `.claude` directory does NOT exist**:

Proceed directly to copying the template (Step 4).

#### Step 4: Copy Template Structure

Copy the complete `.claude` directory from the template to the target project:

```bash
# Full copy approach
cp -r /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude "$CLAUDE_PROJECT_DIR/"
```

**Important**: This copies the entire structure including:
- All hook scripts and utilities
- All agent definitions
- All skills (including this one)
- All commands
- All output styles
- Status line scripts
- settings.json with hook registrations

#### Step 5: Update Path References (Optional)

If the user wants to customize paths in `settings.json`:

1. Read current settings:
   ```bash
   cat .claude/settings.json
   ```

2. The template uses `$CLAUDE_PROJECT_DIR` which automatically resolves to the project root. No changes needed unless user requests specific customizations.

3. If custom paths are needed, update using the `/convert_paths_absolute` command or manual editing.

#### Step 6: Verify Installation

Check that all components are in place:

```bash
# Verify directory structure
ls -la .claude/

# Count total files (should be ~84 files/directories)
find .claude -type f -o -type d | wc -l

# Verify settings.json is valid JSON
cat .claude/settings.json | python3 -m json.tool > /dev/null && echo "✓ Valid JSON"

# Check that key hooks exist
ls .claude/hooks/{pre_tool_use,post_tool_use,send_event}.py
```

#### Step 7: Configure Source App Identifier (Optional)

The template uses `--source-app cc-hook-multi-agent-obvs` in all `send_event.py` calls. Users may want to customize this:

1. Ask if they want to keep the default or use a custom source app name
2. If customizing, update all occurrences in `settings.json`:
   ```bash
   # Example: Replace with custom name
   sed -i.bak 's/cc-hook-multi-agent-obvs/my-custom-app/g' .claude/settings.json
   ```

#### Step 8: Test Basic Functionality

Verify the setup works:

1. **Test status line**:
   ```bash
   uv run .claude/status_lines/status_line_main.py
   ```
   Should display project status without errors.

2. **Test a simple hook**:
   ```bash
   echo '{"event_type": "test"}' | uv run .claude/hooks/send_event.py --source-app test --event-type Test
   ```
   Should execute without errors.

3. **List available commands**:
   ```bash
   ls .claude/commands/*.md
   ```
   Should show all slash commands.

4. **Verify skills are discoverable**:
   ```bash
   ls .claude/skills/*/SKILL.md
   ```
   Should list all skill definitions.

#### Step 9: Commit to Version Control

If the target project uses git, commit the new configuration:

```bash
git add .claude/
git commit -m "Add Claude Code multi-agent observability configuration

- Hooks for lifecycle events and observability
- Custom agents for specialized tasks
- Skills for worktree management, video processing, etc.
- Slash commands for common workflows
- Output styles and status line customization"
```

### Customization After Setup

After the basic setup, users may want to:

1. **Modify hook behavior**:
   - Edit individual hook scripts in `.claude/hooks/`
   - Add/remove hooks from `settings.json`
   - Adjust `--summarize` flags or other parameters

2. **Add custom agents**:
   - Create new files in `.claude/agents/`
   - Reference them in code or skills

3. **Create custom commands**:
   - Add `.md` files to `.claude/commands/`
   - Use frontmatter for metadata if needed

4. **Customize skills**:
   - Modify existing skills in `.claude/skills/`
   - Create new skills using the meta-skill

5. **Adjust output styles**:
   - Edit styles in `.claude/output-styles/`
   - Create new formatting templates

6. **Configure observability**:
   - Update `send_event.py` destinations
   - Modify summarization prompts
   - Add custom event types

### Handling Specific User Requests

**If user says**: "Use the default template exactly as is"
→ Skip all customization steps, just copy and verify

**If user says**: "I want to customize [specific aspect]"
→ Complete the base setup first, then help with specific customizations

**If user says**: "Only copy [specific parts]"
→ Instead of copying everything, selectively copy requested components:
```bash
# Example: Only copy hooks
cp -r /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude/hooks .claude/

# Create minimal settings.json with just those hooks
```

**If user says**: "Update my existing setup with new features"
→ Use merge strategy, compare differences, add only new files/features

## Examples

### Example 1: Full Setup for New Project

User request:
```
Set up my new project with the Claude Code configuration
```

You would:

1. Verify the source template exists:
   ```bash
   ls /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude
   ```

2. Check if target has existing `.claude`:
   ```bash
   ls $CLAUDE_PROJECT_DIR/.claude 2>/dev/null
   ```

3. If not exists, copy the complete template:
   ```bash
   cp -r /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude $CLAUDE_PROJECT_DIR/
   ```

4. Verify the installation:
   ```bash
   find .claude -type f | wc -l
   ls .claude/settings.json
   ```

5. Test status line:
   ```bash
   uv run .claude/status_lines/status_line_main.py
   ```

6. Inform the user:
   - ✓ Copied complete .claude configuration
   - ✓ Includes hooks, agents, skills, commands, output styles
   - ✓ settings.json configured with all hooks
   - ✓ Ready to use

### Example 2: Setup with Custom Source App Name

User request:
```
Set up the .claude config but use 'my-project' as the source app identifier
```

You would:

1. Copy the complete template (as in Example 1)

2. Update the source app name in settings.json:
   ```bash
   cd $CLAUDE_PROJECT_DIR
   sed -i.bak 's/cc-hook-multi-agent-obvs/my-project/g' .claude/settings.json
   ```

3. Verify the changes:
   ```bash
   grep "source-app" .claude/settings.json | head -3
   ```

4. Confirm all occurrences were updated:
   ```bash
   grep -c "my-project" .claude/settings.json
   ```

5. Clean up backup:
   ```bash
   rm .claude/settings.json.bak
   ```

### Example 3: Merge with Existing Configuration

User request:
```
I already have some .claude files. Add the missing pieces from the template.
```

You would:

1. Check what already exists:
   ```bash
   ls -la .claude/
   ```

2. Identify missing directories:
   ```bash
   # Example output shows they have commands/ but missing hooks/
   ```

3. Copy only missing directories:
   ```bash
   cp -r /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude/hooks .claude/
   cp -r /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude/agents .claude/
   # ... etc for each missing directory
   ```

4. For settings.json, ask user if they want to:
   - Keep their current settings.json (manual merge needed)
   - Replace with template settings.json
   - Review differences first

5. If reviewing differences:
   ```bash
   diff .claude/settings.json /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude/settings.json
   ```

6. Help user manually merge any conflicting files

### Example 4: Only Install Specific Components

User request:
```
Just copy the hooks and the status line setup
```

You would:

1. Create .claude directory if it doesn't exist:
   ```bash
   mkdir -p .claude
   ```

2. Copy only requested components:
   ```bash
   cp -r /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude/hooks .claude/
   cp -r /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude/status_lines .claude/
   ```

3. Extract relevant parts of settings.json:
   - Read the template settings.json
   - Create a minimal settings.json with only hooks and statusLine sections
   - Write to .claude/settings.json

4. Verify:
   ```bash
   ls .claude/hooks/*.py
   ls .claude/status_lines/*.py
   cat .claude/settings.json
   ```

5. Test the components:
   ```bash
   uv run .claude/status_lines/status_line_main.py
   echo '{}' | uv run .claude/hooks/send_event.py --source-app test --event-type Test
   ```

### Example 5: Update Existing Setup with New Features

User request:
```
Update my .claude config with any new hooks or skills from the template
```

You would:

1. List current files:
   ```bash
   find .claude -type f | sort > /tmp/current_files.txt
   ```

2. List template files:
   ```bash
   find /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude -type f | sed 's|.*/.claude/|.claude/|' | sort > /tmp/template_files.txt
   ```

3. Find new files in template:
   ```bash
   comm -13 /tmp/current_files.txt /tmp/template_files.txt
   ```

4. Show the user what's new and ask if they want to add these files

5. Copy new files selectively:
   ```bash
   # For each new file
   cp /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude/path/to/new/file .claude/path/to/new/file
   ```

6. Check for updated files (compare file modification times or hashes):
   ```bash
   # For files that exist in both, check if template is newer
   ```

7. Offer to update modified files (with backup)

## Advanced Usage

### Scripted Setup for Multiple Projects

Create a setup script that automates the process:

```bash
#!/bin/bash
# setup_claude_config.sh

TEMPLATE="/Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude"
TARGET="${1:-.}"
SOURCE_APP="${2:-cc-hook-multi-agent-obvs}"

# Copy template
cp -r "$TEMPLATE" "$TARGET/"

# Customize source app if provided
if [ "$SOURCE_APP" != "cc-hook-multi-agent-obvs" ]; then
  sed -i.bak "s/cc-hook-multi-agent-obvs/$SOURCE_APP/g" "$TARGET/.claude/settings.json"
  rm "$TARGET/.claude/settings.json.bak"
fi

# Verify
echo "✓ Setup complete for $TARGET"
echo "✓ Source app: $SOURCE_APP"
```

### Maintaining Multiple Project Variants

If you maintain different variants (dev/prod, different features):

1. Keep the base template as the source of truth
2. Document customizations in each project's CLAUDE.md
3. Use git branches for different configuration variants
4. Consider creating project-specific skills for unique needs

## Troubleshooting

**Issue**: Hooks don't execute after setup
- **Check**: Verify `settings.json` paths use `$CLAUDE_PROJECT_DIR`
- **Check**: Ensure hook scripts have correct permissions
- **Check**: Test hooks individually with `uv run`

**Issue**: Skills not discoverable
- **Check**: Verify SKILL.md files have proper YAML frontmatter
- **Check**: Ensure skills are in `.claude/skills/` directory
- **Check**: Validate YAML with a linter

**Issue**: Commands not available
- **Check**: Verify `.md` files are in `.claude/commands/`
- **Check**: Use `/help` to list available commands
- **Check**: Check for syntax errors in command files

**Issue**: Path errors in settings.json
- **Check**: Use `/convert_paths_absolute` command
- **Check**: Manually verify `$CLAUDE_PROJECT_DIR` resolves correctly
- **Check**: Use absolute paths as fallback

## Summary

This skill provides a streamlined way to replicate the multi-agent observability project's `.claude` configuration. It:

- Copies the complete template structure
- Handles existing configurations (merge/replace)
- Supports customization (source app names, selective components)
- Verifies installation correctness
- Provides troubleshooting guidance

The template includes production-ready hooks, agents, skills, and commands that provide:
- Event-driven observability
- Multi-agent coordination
- Workflow automation
- Extensible architecture

Use this skill whenever you need to set up a new project with Claude Code's advanced features, or when you want to standardize configuration across multiple projects.
