---
description: Build the codebase based on the plan and report changes using git diff.
argument-hint: [path-to-plan]
allowed-tools: Read, Write, Bash, MultiEdit
model: claude-sonnet-4-5-20250929
---

# Build Agent: Implementation and Reporting

## Variables

PATH_TO_PLAN: $ARGUMENTS

## Workflow

1. If no 'PATH_TO_PLAN' is provided, **STOP** immediately and ask the user to provide it.
2. Read the plan at '$PATH_TO_PLAN'. **Think hard** about the plan and implement it into the codebase using your code generation/editing tools.

## Report

1. Summarize the work you've just done in a concise bullet point list.
2. Report the files and total lines changed with the Bash command: **'git diff --stat'**.
3. Provide a detailed **git diff report** for all changed files in the required format.