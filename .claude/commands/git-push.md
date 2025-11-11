---
description: Git add, commit with AI summary, and push
allowed-tools:
  - Bash(git status:*, git add:*, git commit:*, git push:*)
---

Execute the git-push Python script to stage all changes, generate an AI commit message, and push to remote.

Run the following command:

```bash
cd /Users/terivercheung/Documents/AI/CLI_setup/CLAUDE
uv run .claude/scripts/git-push.py
```

The script will:
1. Check for unstaged changes
2. Stage all changes with `git add .`
3. Generate a concise commit message using AI (OpenAI/Anthropic)
4. Commit with the generated message
5. Push to remote repository
6. Display summary with timestamp

**Features:**
- 🤖 AI-generated commit message following conventional commits
- 📊 Shows changes and summary with date/time
- 🔒 Safe git operations (only add, commit, push)
