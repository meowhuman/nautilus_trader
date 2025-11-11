---
model: claude-haiku-4-5-20251001
description: Fast setup of Claude Code configuration in any project directory
argument-hint: [TARGET_DIR] [SOURCE_APP_NAME]
allowed-tools: Bash
---

# Purpose

Set up the complete Claude Code configuration (`.claude` directory with ~68 files) in any project in 10 seconds. Works from any directory without requiring `.claude` to already exist.

## Variables

```
SCRIPT_LOCATION: ~/bin/setup-claude
CONFIG_SCRIPT: ~/bin/setup-claude-config.sh
TEMPLATE_LOCATION: /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude
TARGET_DIR: $1 (default: current directory ".")
SOURCE_APP: $2 (default: "cc-hook-multi-agent-obvs")
INSTALLATION: Alias in ~/.zshrc pointing to ~/bin/setup-claude
SHELL: zsh (or bash)
```

## Instructions

- This is a ONE-SHOT command that validates, copies, and verifies the complete configuration
- Handles both empty directories (fresh setup) and existing `.claude` directories (merge/replace)
- Customizes source app identifier for multi-tenant observability tracking
- Validates JSON and all required files after copying
- Safe: backs up existing `.claude` to `.claude.backup.TIMESTAMP` before replacing
- Fast: complete setup in ~10 seconds
- Works from anywhere: no dependency on current working directory

## Workflow

### 1. User Invokes Command

User runs from any directory:
```bash
setup-claude [TARGET_DIR] [SOURCE_APP_NAME]
```

Examples:
- `setup-claude` - Use current directory, default app name
- `setup-claude . my-project` - Current dir, custom app name
- `setup-claude /path/to/project` - Custom directory, default app name
- `setup-claude /path/to/project my-app` - Both custom

### 2. Parse and Validate Arguments

- Read TARGET_DIR from $1, default to "." (current directory)
- Read SOURCE_APP from $2, default to "cc-hook-multi-agent-obvs"
- Verify TARGET_DIR path is valid and accessible
- Display setup parameters to user

### 3. Verify Template Exists

- Check if TEMPLATE_LOCATION exists: `/Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude`
- Verify directory contains required subdirectories: agents, commands, hooks, output-styles, skills, status_lines
- Verify settings.json file exists in template
- Error if template is missing or incomplete

### 4. Verify Target Directory

- Check if TARGET_DIR exists
- Check if TARGET_DIR is writable: `[ -w "$TARGET_DIR" ]`
- Error if directory doesn't exist or isn't writable
- Success message when target is valid

### 5. Handle Existing .claude Directory

If TARGET_DIR/.claude already exists:
- Display warning: "Existing .claude directory found"
- Present user with three options:
  1. **Replace**: Back up current to `.claude.backup.$(date +%Y%m%d-%H%M%S)`, then copy template
  2. **Merge**: Keep existing files, copy only missing components from template
  3. **Abort**: Exit without making changes
- Read user choice (1-3)
- Execute selected action:
  - Replace: `mv TARGET_DIR/.claude TARGET_DIR/.claude.backup.TIMESTAMP && cp -r TEMPLATE TARGET_DIR/.claude`
  - Merge: Iterate through each component directory and copy missing files
  - Abort: Print "Setup aborted by user" and exit with error code

If TARGET_DIR/.claude does NOT exist:
- Skip this step, proceed directly to copying template

### 6. Copy Configuration

**Replace Mode (or new directory)**:
```bash
cp -r "$TEMPLATE_LOCATION" "$TARGET_DIR/.claude"
```

**Merge Mode**:
```bash
# For each component directory
mkdir -p "$TARGET_DIR/.claude/$dir"
cp -r "$TEMPLATE_LOCATION/$dir"/* "$TARGET_DIR/.claude/$dir/" 2>/dev/null || true
```

Verify copy succeeded: `[ -d "$TARGET_DIR/.claude" ] && [ -f "$TARGET_DIR/.claude/settings.json" ]`

### 7. Customize Source App Identifier

If SOURCE_APP is not the default "cc-hook-multi-agent-obvs":
- Use sed to replace all occurrences in settings.json:
  - macOS: `sed -i '' "s/cc-hook-multi-agent-obvs/$SOURCE_APP/g" "$TARGET_DIR/.claude/settings.json"`
  - Linux: `sed -i "s/cc-hook-multi-agent-obvs/$SOURCE_APP/g" "$TARGET_DIR/.claude/settings.json"`
- Verify replacement: `grep -c "$SOURCE_APP" "$TARGET_DIR/.claude/settings.json"` should show multiple matches
- Display: "Updated source app identifier to: $SOURCE_APP"

### 8. Verify Installation

Check all critical components:

**Directory Structure**:
- Count total files: `find "$TARGET_DIR/.claude" -type f | wc -l`
- Should show ~68 files
- Display count to user

**Required Files**:
- Check existence of:
  - `$TARGET_DIR/.claude/settings.json`
  - `$TARGET_DIR/.claude/hooks/pre_tool_use.py`
  - `$TARGET_DIR/.claude/hooks/post_tool_use.py`
  - `$TARGET_DIR/.claude/hooks/send_event.py`
  - `$TARGET_DIR/.claude/status_lines/status_line_main.py`
- Report: "✓ Found: [file]" or "✗ Missing: [file]"

**JSON Validation**:
- Validate settings.json: `python3 -m json.tool "$TARGET_DIR/.claude/settings.json" > /dev/null 2>&1`
- Report: "✓ settings.json is valid JSON" or error

**Component Verification**:
- Verify subdirectories exist: agents, commands, hooks, output-styles, skills, status_lines
- Report count of items in each: `ls -1 "$TARGET_DIR/.claude/agents" | wc -l` etc.

### 9. Show Next Steps

Display user-friendly instructions:

```
Next steps:
1. Navigate to the project: cd $TARGET_DIR
2. Initialize git if needed: git init
3. Test the status line: uv run .claude/status_lines/status_line_main.py
4. Commit the configuration: git add .claude/ && git commit -m "Add Claude Code configuration"

Available components:
  - Hooks: .claude/hooks/
  - Agents: .claude/agents/
  - Skills: .claude/skills/
  - Commands: .claude/commands/
  - Output styles: .claude/output-styles/
```

### 10. Report Success

Follow the Report section format below.

## Report

After successful setup, provide information in this format:

```
=== Claude Code Configuration Setup ===

✓ Setup Parameters:
  Template: /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude
  Target: $TARGET_DIR
  Source app: $SOURCE_APP

✓ Template Verification:
  Located at: $TEMPLATE_LOCATION
  Status: Found and valid

✓ Target Directory:
  Path: $TARGET_DIR
  Writable: Yes
  Status: Ready

✓ Configuration Copied:
  Method: [Replace/Merge/New Install]
  Total files: ~68
  Location: $TARGET_DIR/.claude

✓ Customization:
  Source app identifier: $SOURCE_APP
  Settings updated: Yes
  Occurrences replaced: [N]

✓ Installation Verified:
  settings.json: Valid JSON
  Key files: All present (5/5 critical files)
  Subdirectories: All present (6/6)
    - agents/ (7 files)
    - commands/ (13 files)
    - hooks/ (15 files)
    - output-styles/ (11 files)
    - skills/ (4+ files)
    - status_lines/ (1 file)

✓ Setup Complete!

Next Steps:
1. cd $TARGET_DIR
2. git init (if needed)
3. git add .claude/
4. git commit -m "Add Claude Code multi-agent configuration"

Available Components:
  ✓ Hooks: Event-driven observability
  ✓ Agents: Specialized task handlers
  ✓ Skills: Worktree manager, video processor, etc.
  ✓ Commands: Slash commands for workflows
  ✓ Output Styles: Response formatting templates
  ✓ Status Lines: Custom CLI displays
  ✓ Settings: Centralized hook configuration

Ready to use! Run: uv run .claude/status_lines/status_line_main.py
```

If backup was created during replace:

```
⚠️  Backup Created:
  Previous .claude backed up to: .claude.backup.$TIMESTAMP
  Keep for reference or restore: mv .claude.backup.$TIMESTAMP .claude
```

If merge mode was used:

```
ℹ️  Merge Mode:
  Kept existing .claude files
  Added missing components from template
  Note: Manual review recommended for conflicting configurations
```

## Error Handling

If validation fails at any step:

```
✗ Setup Failed!

Error: [Description]
  [Context/suggestion]

To fix:
- [Action 1]
- [Action 2]

Or run with full path: ~/bin/setup-claude $TARGET_DIR $SOURCE_APP
```

Possible errors:
- Template not found: "Template directory not found at TEMPLATE_LOCATION"
- Target not found: "Target directory not found: TARGET_DIR"
- Target not writable: "Target directory not writable: TARGET_DIR"
- JSON validation failed: "settings.json is invalid JSON"
- Copy failed: "Failed to copy .claude configuration"

## Integration with Alias

User has alias in `.zshrc`:
```bash
alias setup-claude='~/bin/setup-claude'
```

This points to wrapper script at `~/bin/setup-claude`, which calls `~/bin/setup-claude-config.sh`.

Both scripts must be:
- Executable: `chmod +x ~/bin/setup-claude*`
- In home directory bin: `~/bin/`
- Accessible from anywhere via alias

## Speed Optimization

The setup completes in ~10 seconds because:
- Uses native bash/cp (no node, no npm install)
- Single copy operation for all ~68 files
- Minimal validation (JSON check only)
- No network calls
- No compilation or build steps
- Single sed replace for source app customization

Timing breakdown:
- 1-2 sec: Verify template
- 1-2 sec: Verify target
- 4-5 sec: Copy ~68 files
- 1 sec: Customize source app
- 2-3 sec: Verify installation
- ~10 sec total

## Examples

### Example 1: Setup Current Directory with Default Name

```bash
cd /Users/terivercheung/Documents/MyProject
setup-claude
```

Result:
- Copies to: /Users/terivercheung/Documents/MyProject/.claude
- Source app: cc-hook-multi-agent-obvs (default)
- Ready immediately

### Example 2: Setup Different Directory with Custom App Name

```bash
setup-claude /Users/terivercheung/Documents/Obsidian obsidian-project
```

Result:
- Copies to: /Users/terivercheung/Documents/Obsidian/.claude
- Source app: obsidian-project
- All settings.json references updated
- Ready immediately

### Example 3: Merge with Existing Configuration

```bash
cd /path/to/existing/project
setup-claude
```

If .claude exists:
- User prompted: Replace/Merge/Abort
- Choose: 2 (Merge)
- Keeps existing files
- Adds missing components
- Ready for review

### Example 4: Script Usage (Non-Interactive)

```bash
# In a bash script
~/bin/setup-claude /path/to/project my-project-name
# Returns exit code 0 on success, 1 on failure
```

## Usage Patterns

**Personal Project**:
```bash
mkdir ~/my-ai-project
cd ~/my-ai-project
setup-claude . my-project
git init
git add .claude/
git commit -m "Add Claude Code configuration"
```

**Team/Startup Project**:
```bash
setup-claude /path/to/startup startup-name
cd /path/to/startup
git add .claude/
git commit -m "Add observability configuration"
git push
```

**Multiple Concurrent Projects**:
```bash
setup-claude ~/project1 proj1
setup-claude ~/project2 proj2
setup-claude ~/project3 proj3
# All have isolated, named configurations
```

**Development Environment**:
```bash
setup-claude . dev-env
# Use with: uv run .claude/status_lines/status_line_main.py
```

## Troubleshooting

If command not found after install:

1. **Verify alias exists**:
   ```bash
   grep "setup-claude" ~/.zshrc
   ```

2. **Reload shell**:
   ```bash
   exec zsh
   ```

3. **Use full path**:
   ```bash
   ~/bin/setup-claude /path/to/project
   ```

If template not found:

1. **Verify template exists**:
   ```bash
   ls /Users/terivercheung/Documents/AI/claude-code-hooks-multi-agent-observability/.claude
   ```

2. **Update script if moved**:
   ```bash
   # Edit ~/bin/setup-claude-config.sh, line 13:
   TEMPLATE_DIR="/new/path/.claude"
   ```

If JSON validation fails:

1. **Check file integrity**:
   ```bash
   cat .claude/settings.json | python3 -m json.tool
   ```

2. **Restore from backup** (if exists):
   ```bash
   rm -rf .claude
   mv .claude.backup.TIMESTAMP .claude
   ```

## Summary

The `setup-claude` command provides:

✓ **Speed**: 10 seconds for complete setup
✓ **Convenience**: Works from any directory
✓ **Safety**: Backs up existing configurations
✓ **Flexibility**: Merge or replace existing configs
✓ **Customization**: Per-project source app names
✓ **Verification**: Validates all components after copy
✓ **Documentation**: Clear next steps provided

Use whenever you need to quickly set up new projects with Claude Code's multi-agent observability system.
