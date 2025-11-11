---
model: claude-haiku-4-5-20251001
description: Automated GitHub fork authentication, setup, and commit workflow (auth, fork, commit, push) - works with any project
argument-hint: [UPSTREAM_REPO] [COMMIT_MESSAGE]
allowed-tools: Bash
---

# Purpose

Automate the complete GitHub fork workflow for ANY project in one command: authenticate with GitHub CLI, create fork if needed, update remote URL, stage changes, commit with message, and push to personal fork.

Supports ANY upstream repository (e.g., `nautechsystems/nautilus_trader`, `torvalds/linux`, `facebook/react`, etc.).

## Variables

```
GH_CLI: gh (GitHub CLI)
UPSTREAM_REPO: $1 (owner/repo - e.g., nautechsystems/nautilus_trader)
COMMIT_MESSAGE: $2 (user-provided message)
FORK_OWNER: auto-detected from gh auth status (your GitHub account)
PROJECT_NAME: auto-extracted from UPSTREAM_REPO (e.g., nautilus_trader)
FORK_OWNER_NAME: auto-extracted from UPSTREAM_REPO (e.g., nautechsystems)
REMOTE_URL: https://github.com/{your-username}/{project-name}.git
BRANCH: develop (default branch, can be customized)
```

## Instructions

- This is a streamlined workflow command that handles GitHub auth, fork creation, and git operations
- Validates GitHub CLI is installed and user is authenticated
- Checks for fork existence; creates if missing
- Handles branch divergence automatically with rebase
- Safe: validates all steps before proceeding
- Works from the project root directory

## Workflow

### 1. Validate Prerequisites

Check that:
- GitHub CLI (`gh`) is installed: `which gh`
- User is authenticated: `gh auth status`
- Current directory is a git repository: `[ -d .git ]`
- Commit message is provided (non-empty)

Report status and error if any prerequisite fails.

### 2. Get GitHub Authentication Status

Run `gh auth status` and parse output:
- Display: "✓ Authenticated as: [username]"
- Extract active account name for confirmation
- Error if not authenticated (guide user to run `gh auth login`)

### 3. Extract Project Information

Parse the UPSTREAM_REPO argument ($1):
- Format: `owner/repo` (e.g., `nautechsystems/nautilus_trader`)
- Extract PROJECT_NAME: `repo` portion
- Extract FORK_OWNER_NAME: `owner` portion
- Construct fork URL: `https://github.com/{your-username}/{project-name}.git`
- Display: "⏳ Setting up fork for: {UPSTREAM_REPO}"

### 4. Check Fork Existence

Try to access the fork:
```bash
gh repo view {username}/{project-name} --json url
```

If fork exists:
- Display: "✓ Fork found: https://github.com/{username}/{project-name}"
- Proceed to step 5

If fork doesn't exist:
- Display: "⚠️ Fork not found, creating fork of {UPSTREAM_REPO}..."
- Run: `gh repo fork {upstream-owner}/{project-name} --clone=false`
- Wait for completion
- Display: "✓ Fork created: https://github.com/{username}/{project-name}"
- Proceed to step 5

### 5. Update Git Remote

Check current remote:
```bash
git remote -v | grep origin
```

Extract current remote project name and validate it matches the target:
```bash
CURRENT_REMOTE=$(git remote get-url origin)
```

If remote is not the personal fork:
- Display: "Updating remote URL to personal fork..."
- Run: `git remote set-url origin https://github.com/{username}/{project-name}.git`
- Display: "✓ Remote updated to: https://github.com/{username}/{project-name}.git"

If remote is already correct:
- Display: "✓ Remote already configured: {CURRENT_REMOTE}"

### 6. Fetch Latest Changes

```bash
git fetch origin
```

This ensures we have the latest remote state before attempting to push.

### 7. Stage Changes

Run: `git add .`

Display progress:
```bash
STAGED_COUNT=$(git diff --cached --name-only | wc -l)
echo "✓ Staged $STAGED_COUNT files for commit"
```

### 8. Commit Changes

Run:
```bash
git commit -m "[COMMIT_MESSAGE]"
```

Where COMMIT_MESSAGE is provided by user ($1).

Display:
- "✓ Committed: [COMMIT_MESSAGE]"
- Show commit hash: `git log --oneline -1`

### 9. Handle Branch Divergence

Check if push will fail due to branch divergence:
```bash
git push -u origin develop --dry-run 2>&1 | grep -q "divergent"
```

If divergence detected:
- Display: "⚠️ Branch divergence detected, rebasing..."
- Run: `git pull --rebase origin develop`
- Display: "✓ Rebased successfully"

If no divergence:
- Display: "✓ Branch in sync"

### 10. Push to Fork

Run: `git push -u origin develop`

Display:
- "✓ Pushed to: https://github.com/{username}/{project-name}"
- Show branch info: `git log --oneline origin/develop -1`

### 11. Report Success

Follow the Report section format below.

## Report

After successful completion, provide information in this format:

```
=== Git Fork Workflow Complete ===

✓ Project Identified:
  Upstream: {UPSTREAM_REPO}
  Project name: {PROJECT_NAME}
  Fork owner: {username}

✓ GitHub Authentication:
  Account: {username}
  Status: Authenticated

✓ Fork Status:
  Source: {UPSTREAM_REPO}
  Fork URL: https://github.com/{username}/{project-name}
  Status: Ready

✓ Remote Configuration:
  URL: https://github.com/{username}/{project-name}.git
  Branch: develop

✓ Changes Committed:
  Files staged: [N]
  Commit message: {COMMIT_MESSAGE}
  Commit hash: [HASH]

✓ Push Status:
  Branch: develop
  Status: Pushed successfully
  Remote: origin/develop

✓ Next Steps:
  1. View your fork: https://github.com/{username}/{project-name}
  2. Create pull request to upstream (optional): {UPSTREAM_REPO}
  3. Continue development on this branch

Ready to proceed!
```

## Error Handling

If validation fails at any step:

```
✗ Git Workflow Failed!

Error: [Description]
  [Context/suggestion]

To fix:
- [Action 1]
- [Action 2]

Or check: gh auth status
```

Possible errors:

| Error | Cause | Solution |
|-------|-------|----------|
| "GitHub CLI not found" | `gh` not installed | Install GitHub CLI: `brew install gh` |
| "Not authenticated to GitHub" | User not logged in | Run: `gh auth login` |
| "Fork not found and creation failed" | Insufficient permissions | Check GitHub account permissions |
| "No upstream repo provided" | Empty $1 argument | Provide upstream repo: `/git-fork-and-setup owner/repo "your message"` |
| "No commit message provided" | Empty $2 argument | Provide commit message: `/git-fork-and-setup owner/repo "your message"` |
| "Not in a git repository" | Not a git project directory | Navigate to git repo: `cd /path/to/repo` |
| "Remote update failed" | Permission issue | Check GitHub credentials: `gh auth status` |
| "Push rejected due to divergence" | Branch mismatch | Rebase handled automatically; retry if fails |
| "Authentication token expired" | Credentials stale | Re-authenticate: `gh auth login` |

## Workflow Integration

**Typical usage after development**:

```bash
# Make your changes
echo "new feature" > file.txt

# Commit and push everything to your fork
/git-fork-and-setup nautechsystems/nautilus_trader "feat: add new feature"

# Or with more detailed message
/git-fork-and-setup torvalds/linux "fix(driver): resolve timeout issue

Add retry logic for transient failures.
Fixes #456"
```

**With other Claude Code commands**:

```bash
# Plan → Build → Commit
/plan "Add feature X"
# ... make changes ...
/build
# ... tests pass ...
/git-fork-and-setup owner/project "feat: implement feature X"
```

**Flexible project identification**:

```bash
# Works with ANY upstream project
/git-fork-and-setup nautechsystems/nautilus_trader "feat: add module"
/git-fork-and-setup torvalds/linux "fix: kernel module"
/git-fork-and-setup facebook/react "feat: add hook"
/git-fork-and-setup kubernetes/kubernetes "feat: add controller"
```

## Examples

### Example 1: Nautilus Trader Fork

```bash
# In your nautilus_trader fork directory
/git-fork-and-setup nautechsystems/nautilus_trader "feat: add authentication module"
```

Result:
- Identifies upstream project: `nautechsystems/nautilus_trader`
- Authenticates with GitHub
- Creates fork if missing
- Stages all changes
- Commits with message "feat: add authentication module"
- Pushes to your personal fork: `https://github.com/{username}/nautilus_trader`
- Displays success with fork URL

### Example 2: Linux Kernel Contribution

```bash
# In your linux fork directory
/git-fork-and-setup torvalds/linux "fix(driver): resolve timeout issue

Increase driver timeout from 5s to 10s.
Add retry logic for transient failures.
Refs #456"
```

Result:
- Identifies upstream: `torvalds/linux`
- All changes committed with detailed message
- Visible in git log with full description
- Ready for pull request to torvalds/linux

### Example 3: React Fork Contribution

```bash
# In your react fork directory
/git-fork-and-setup facebook/react "refactor: extract custom hook

- Move hook logic to separate file
- Update imports in dependent components
- Add comprehensive tests"
```

Result:
- All changed files staged automatically
- Multi-line commit message preserved
- Pushed to your fork: `https://github.com/{username}/react`
- Ready to create PR to facebook/react

## Usage Patterns

**After Feature Development**:
```bash
# Develop feature for any project
# Test locally
# Then commit and push to your fork
/git-fork-and-setup owner/project "feat: add dashboard widget"
```

**Hotfix Workflow**:
```bash
# Fix bug in upstream project
# Test fix
# Commit and push immediately
/git-fork-and-setup torvalds/linux "fix: critical kernel issue"
```

**Documentation Updates**:
```bash
# Update docs in your fork
/git-fork-and-setup facebook/react "docs: update hooks documentation"
```

**Code Refactoring**:
```bash
# Refactor in any project
/git-fork-and-setup kubernetes/kubernetes "refactor: extract controller logic"
```

**Dependencies Update**:
```bash
# Update deps in your fork
/git-fork-and-setup nautechsystems/nautilus_trader "chore: update dependencies"
```

## Troubleshooting

### "GitHub CLI not found"

1. **Install GitHub CLI**:
   ```bash
   brew install gh
   ```

2. **Verify installation**:
   ```bash
   gh --version
   ```

### "Not authenticated"

1. **Login with GitHub**:
   ```bash
   gh auth login
   ```

2. **Choose HTTPS protocol** when prompted
3. **Paste your personal access token**

4. **Verify authentication**:
   ```bash
   gh auth status
   ```

### "Fork not found and creation failed"

1. **Check GitHub account**:
   ```bash
   gh api user
   ```

2. **Verify account has permission to fork**:
   - Public repos can be forked
   - Private repos may have restrictions

3. **Create fork manually**:
   - Go to: `https://github.com/{upstream-owner}/{project-name}`
   - Example: `https://github.com/torvalds/linux`
   - Click "Fork" button
   - Then retry: `/git-fork-and-setup upstream-owner/project "your message"`

### "Permission denied when pushing"

1. **Check authentication**:
   ```bash
   gh auth status
   ```

2. **Refresh credentials**:
   ```bash
   gh auth login
   ```

3. **Verify fork URL**:
   ```bash
   git remote -v
   ```

### "Branch divergence error"

This is handled automatically by the command:
- Command detects divergence
- Automatically rebases your commits
- Retries push

If issue persists:
```bash
git pull --rebase origin develop
git push -u origin develop
```

### "Missing arguments"

Command requires two arguments: UPSTREAM_REPO and COMMIT_MESSAGE

❌ Wrong:
```bash
/git-fork-and-setup
/git-fork-and-setup "feat: add new feature"
```

✓ Correct:
```bash
/git-fork-and-setup nautechsystems/nautilus_trader "feat: add new feature"
/git-fork-and-setup torvalds/linux "fix: kernel module"
/git-fork-and-setup owner/project "your commit message"
```

## Integration with CLAUDE.md

This command follows the Git workflow defined in `CLAUDE.md`:

- **Commit Format**: Supports conventional commit types (feat, fix, docs, etc.)
- **Branch Strategy**: Works with `develop` branch as defined in standards
- **Automation**: Streamlines the manual git workflow for efficiency
- **Security**: Uses authenticated GitHub CLI instead of credentials in config

## Advanced Usage

### Integration with Pre-commit Hooks

If you have pre-commit hooks configured:
```bash
/git "feat: add feature"
# Hooks may modify files (formatting, linting)
# If modified, script will:
#   1. Detect modified files
#   2. Stage again
#   3. Commit with same message (auto-amended)
#   4. Push normally
```

### With Custom Commit Message Format

```bash
/git "feat(core): implement new algorithm

This adds a new sorting algorithm that
improves performance by 40% for large datasets.

Benchmarks:
- Old: 5.2s for 1M items
- New: 3.1s for 1M items

Closes #789"
```

Message is preserved exactly as provided in the log.

## Summary

The `/git-fork-and-setup` command provides:

✓ **Project Flexibility**: Works with ANY upstream GitHub repository (not limited to one project)
✓ **Auto-Identification**: Automatically identifies and validates the upstream project
✓ **Convenience**: One-command git workflow automation for multiple projects
✓ **Safety**: Validates all prerequisites before proceeding
✓ **Flexibility**: Accepts custom commit messages with multi-line support
✓ **Intelligence**: Handles fork creation and branch divergence automatically
✓ **Transparency**: Clear status updates at each step showing project information
✓ **Compliance**: Follows project's CLAUDE.md git standards
✓ **Recovery**: Helpful error messages and troubleshooting for any project

Use whenever you need to commit and push changes to your personal fork of ANY project:
- `nautechsystems/nautilus_trader` (trading platform)
- `torvalds/linux` (kernel)
- `facebook/react` (web framework)
- `kubernetes/kubernetes` (container orchestration)
- Any other GitHub project you fork!
