---
description: Creates a concise engineering implementation plan based on user requirements and saves it to specs directory.
argument-hint: [user-prompt] [documentation-urls] [relevant-files-collection-path]
allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit, Bash, Task
model: claude-sonnet-4-5-20250929
---

# Quick Plan with Documentation

## Variables

USER_PROMPT: $1
DOCUMENTATION_URLS: $2
RELEVANT_FILES_COLLECTION: $3
PLAN_OUTPUT_DIRECTORY: specs/
DOCUMENTATION_OUTPUT_DIRECTORY: 'ai_docs/'

## Instructions

- IMPORTANT: If any of $1, $2, or $3 is missing, STOP and ask the user to provide them.
- READ the '$RELEVANT_FILES_COLLECTION' file which contains a structured file list.
- With **Task**, in **parallel**, scrap each **DOCUMENTATION_URLS** with **firecrawl** (or webfetch). Save them to '$DOCUMENTATION_OUTPUT_DIRECTORY' and return the paths.
- **Think deeply (ultrathink)** about the best approach.
- **READ** the code snippets listed in the '$RELEVANT_FILES_COLLECTION' using the specified offset and limit values.

## Workflow

1. Analyze Requirements - **THINK HARD** and parse the $USER_PROMPT.
2. Scrap Documentation - With **Task**, in parallel, scrap $DOCUMENTATION_URLS and save the results.
3. Design Solution - Develop a technical approach including architecture decisions and implementation strategy, synthesizing code context and documentation.
4. Document Plan - Structure a comprehensive markdown document.
5. Generate Filename - Create a descriptive **kebab-case** filename.
6. Save & Report - Write the plan to '$PLAN_OUTPUT_DIRECTORY/<filename>.md'.

## Report

Provide a summary of the key components of the implementation plan.