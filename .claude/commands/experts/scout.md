---
description: Run multiple agents in parallel to scout the codebase for files needed to complete the task.
argument-hint: [user-prompt]
model: claude-haiku-4.5
allowed-tools: Bash, Task, Write
---

# Scout Agent: Parallel Codebase Search

## Purpose

Run a parallel agent workflow to quickly search the codebase for files needed to complete the 'USER_PROMPT'.

## Variables

USER_PROMPT: $1
SCALE: 5 # Number of parallel agents to run (Example)

## Instructions

- We are executing a parallel search using the **Task tool**.
- The subagents are **ONLY** to call the **Bash tool** to run agentic coding tools (gemini, opencode, claude, etc.).
- Instruct subagents to **ONLY** search the codebase and return a **structured list of files** with specific line ranges.
- **DO NOT** attempt to implement the task or call any search tools other than Bash.
- Use a **timeout of 3 minutes** for each agent's bash call.

## Workflow

> Run $SCALE number of agents in parallel to search the codebase.

1. Run TaskCommand('/call_bash_agent ["$USER_PROMPT"] [1-5]') 
   -> 'relevant_files_collection_path'

---

## Output Format (for relevant_files_collection_path)

The final output **MUST** be a structured bullet point list of files with line ranges:
- `<path to file> (offset: N, limit: M)`