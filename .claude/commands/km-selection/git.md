---
model: claude-haiku-4-5-20251001
description: Automated GitHub authentication, fork creation, and git workflow (auth, fork, commit, push)
argument-hint: [COMMIT_MESSAGE]
allowed-tools: Bash
---

# Purpose

Automate the complete GitHub workflow in one command: authenticate with GitHub CLI, create fork if needed, update remote URL, stage changes, commit with message, and push to personal fork.

## Variables

```
GH_CLI: gh (GitHub CLI)
FORK_SOURCE: nautechsystems/nautilus_trader (upstream project)
FORK_OWNER: meowhuman (your GitHub account)
COMMIT_MESSAGE: $1 (user-provided message)
REMOTE_URL: https://github.com/meowhuman/nautilus_trader.git
BRANCH: develop (default branch)
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

### 3. Determine Fork Ownership

- Extract GitHub username from `gh auth status`
- Construct fork URL: `https://github.com/{username}/nautilus_trader.git`
- Display fork URL for confirmation

### 4. Check Fork Existence

Try to access the fork:
```bash
gh repo view {username}/nautilus_trader --json url
```

If fork exists:
- Display: "✓ Fork found: [URL]"
- Proceed to step 5

If fork doesn't exist:
- Display: "⚠️ Fork not found, creating..."
- Run: `gh repo fork nautechsystems/nautilus_trader --clone=false`
- Wait for completion
- Display: "✓ Fork created: [URL]"
- Proceed to step 5

### 5. Update Git Remote

Check current remote:
```bash
git remote -v | grep origin
```

If remote is not the personal fork:
- Display: "Updating remote URL to personal fork..."
- Run: `git remote set-url origin https://github.com/{username}/nautilus_trader.git`
- Display: "✓ Remote updated"

If remote is already correct:
- Display: "✓ Remote already configured correctly"

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
- "✓ Pushed to: https://github.com/{username}/nautilus_trader"
- Show branch info: `git log --oneline origin/develop -1`

### 11. Report Success

Follow the Report section format below.

## Report

After successful completion, provide information in this format:

```
=== Git Workflow Complete ===

✓ GitHub Authentication:
  Account: {username}
  Status: Authenticated

✓ Fork Status:
  Owner: {username}
  Source: nautechsystems/nautilus_trader
  Fork URL: https://github.com/{username}/nautilus_trader

✓ Remote Configuration:
  URL: https://github.com/{username}/nautilus_trader.git
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
  1. View your fork: https://github.com/{username}/nautilus_trader
  2. Create pull request to upstream (optional)
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
| "No commit message provided" | Empty $1 argument | Provide commit message: `/git "your message"` |
| "Not in a git repository" | Not a git project directory | Navigate to git repo: `cd /path/to/repo` |
| "Remote update failed" | Permission issue | Check GitHub credentials: `gh auth status` |
| "Push rejected due to divergence" | Branch mismatch | Rebase handled automatically; retry if fails |
| "Authentication token expired" | Credentials stale | Re-authenticate: `gh auth login` |

## Workflow Integration

**Typical usage after development**:

```bash
# Make your changes
echo "new feature" > file.txt

# Commit and push everything
/git "feat: add new feature"

# Or with more detailed message
/git "feat(module): add new feature

Implement X functionality to improve Y.
Fixes #123"
```

**With other Claude Code commands**:

```bash
# Plan → Build → Commit
/plan "Add feature X"
# ... make changes ...
/build
# ... tests pass ...
/git "feat: implement feature X"
```

## Examples

### Example 1: Simple Feature Commit

```bash
/git "feat: add authentication module"
```

Result:
- Authenticates with GitHub
- Creates fork if missing
- Stages all changes
- Commits with message "feat: add authentication module"
- Pushes to personal fork
- Displays success with fork URL

### Example 2: Bug Fix with Details

```bash
/git "fix(api): resolve timeout issue

Increase default timeout from 5s to 10s.
Add retry logic for transient failures.
Refs #456"
```

Result:
- All changes committed with detailed message
- Visible in git log with full description
- Ready for pull request

### Example 3: Multiple File Commit

```bash
# After modifying several files
/git "refactor: reorganize project structure

- Move utilities to utils/ directory
- Update imports in dependent modules
- Add missing docstrings"
```

Result:
- All changed files staged automatically
- Multi-line commit message preserved
- Pushed to fork in one operation

## Usage Patterns

**After Feature Development**:
```bash
# Develop feature
# Test locally
# Then commit and push
/git "feat: add dashboard widget"
```

**Hotfix Workflow**:
```bash
# Fix bug
# Test fix
# Commit immediately
/git "fix: critical production issue"
```

**Documentation Updates**:
```bash
/git "docs: update API documentation"
```

**Code Refactoring**:
```bash
/git "refactor: extract common functions"
```

**Dependencies Update**:
```bash
/git "chore: update dependencies"
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
   - Go to: https://github.com/nautechsystems/nautilus_trader
   - Click "Fork" button
   - Then retry: `/git "your message"`

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

### "Commit message not provided"

Command requires a commit message argument:

❌ Wrong:
```bash
/git
```

✓ Correct:
```bash
/git "feat: add new feature"
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

The `/git` command provides:

✓ **Convenience**: One-command git workflow automation
✓ **Safety**: Validates all prerequisites before proceeding
✓ **Flexibility**: Accepts custom commit messages
✓ **Intelligence**: Handles fork creation and branch divergence
✓ **Transparency**: Clear status updates at each step
✓ **Compliance**: Follows project's CLAUDE.md git standards
✓ **Recovery**: Helpful error messages and troubleshooting

Use whenever you need to commit and push changes to your personal fork of the project.
