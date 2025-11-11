# Claude Code Multi-Agent Observability Project Structure Reference

This document captures the complete `.claude` directory structure for the multi-agent observability project. Use this as a reference when setting up new projects with the same configuration.

## Directory Structure

```
.claude/
├── agents/                          # Custom agent definitions
│   ├── create_worktree_subagent.md
│   ├── docs-scraper.md
│   ├── fetch-docs-haiku45.md
│   ├── fetch-docs-sonnet45.md
│   ├── meta-agent.md
│   ├── scout-report-suggest-fast.md
│   └── scout-report-suggest.md
│
├── commands/                        # Slash commands
│   ├── bench/                      # Benchmarking commands
│   │   ├── find_and_summarize.md
│   │   ├── load_ai_docs.md
│   │   └── plan_new_feature.md
│   ├── build.md
│   ├── convert_paths_absolute.md
│   ├── create_worktree_prompt.md
│   ├── list_worktrees_prompt.md
│   ├── load_ai_docs.md
│   ├── prime.md
│   ├── quick-plan.md
│   ├── remove_worktree_prompt.md
│   ├── start.md
│   └── t_metaprompt_workflow.md
│
├── hooks/                          # Event hooks
│   ├── examples/
│   │   └── hitl_example.py
│   ├── utils/
│   │   ├── llm/
│   │   │   ├── anth.py            # Anthropic LLM integration
│   │   │   └── oai.py             # OpenAI LLM integration
│   │   ├── tts/
│   │   │   ├── elevenlabs_tts.py
│   │   │   ├── openai_tts.py
│   │   │   └── pyttsx3_tts.py
│   │   ├── constants.py
│   │   ├── hitl.py                # Human-in-the-loop utilities
│   │   ├── model_extractor.py
│   │   └── summarizer.py
│   ├── notification.py
│   ├── post_tool_use.py
│   ├── pre_compact.py
│   ├── pre_tool_use.py
│   ├── send_event.py
│   ├── session_end.py
│   ├── session_start.py
│   ├── stop.py
│   ├── subagent_stop.py
│   ├── test_hitl.py
│   └── user_prompt_submit.py
│
├── output-styles/                  # Output formatting styles
│   ├── bullet-points.md
│   ├── genui.md
│   ├── html-structured.md
│   ├── markdown-focused.md
│   ├── observable-tools-diffs-tts.md
│   ├── observable-tools-diffs.md
│   ├── table-based.md
│   ├── tts-summary-base.md
│   ├── tts-summary.md
│   ├── ultra-concise.md
│   └── yaml-structured.md
│
├── skills/                         # Agent skills
│   ├── create-worktree-skill/
│   │   └── SKILL.md
│   ├── meta-skill/
│   │   ├── SKILL.md
│   │   └── docs/
│   │       ├── blog_equipping_agents_with_skills.md
│   │       ├── claude_code_agent_skills.md
│   │       └── claude_code_agent_skills_overview.md
│   ├── project-setup/              # This skill
│   │   ├── SKILL.md
│   │   └── docs/
│   │       └── reference_structure.md
│   ├── video-processor/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── video_processor.py
│   └── worktree-manager-skill/
│       ├── SKILL.md
│       ├── EXAMPLES.md
│       ├── OPERATIONS.md
│       ├── REFERENCE.md
│       └── TROUBLESHOOTING.md
│
├── status_lines/                   # Status line scripts
│   └── status_line_main.py
│
└── settings.json                   # Main configuration file
```

## Key Components

### 1. Agents (`agents/`)
Custom agent definitions that extend Claude Code's capabilities with specialized behaviors:
- **create_worktree_subagent**: Creates isolated git worktrees
- **docs-scraper**: Fetches and formats documentation
- **fetch-docs-haiku45/sonnet45**: Model-specific doc fetching for benchmarking
- **meta-agent**: Creates new agent configurations
- **scout-report-suggest**: Analyzes codebase and suggests improvements

### 2. Commands (`commands/`)
Slash commands that expand to full prompts:
- **Worktree management**: create, list, remove worktree operations
- **Documentation**: load_ai_docs for fetching external docs
- **Planning**: quick-plan, build for project management
- **Benchmarking**: bench/ subdirectory for performance testing
- **Utilities**: convert_paths_absolute, t_metaprompt_workflow

### 3. Hooks (`hooks/`)
Event-driven scripts that execute during Claude Code lifecycle:
- **Tool hooks**: pre_tool_use.py, post_tool_use.py
- **Session hooks**: session_start.py, session_end.py
- **Event tracking**: send_event.py (broadcasts to observability system)
- **Lifecycle hooks**: stop.py, subagent_stop.py, pre_compact.py
- **User interaction**: user_prompt_submit.py, notification.py
- **Utilities**: summarizer, model_extractor, TTS integrations, LLM clients

### 4. Output Styles (`output-styles/`)
Predefined formatting templates for agent responses:
- **Structured formats**: yaml-structured, html-structured, table-based
- **Concise formats**: ultra-concise, bullet-points
- **Observability**: observable-tools-diffs, observable-tools-diffs-tts
- **Documentation**: markdown-focused
- **Audio**: tts-summary, tts-summary-base
- **UI**: genui

### 5. Skills (`skills/`)
Reusable capabilities that Claude can load on-demand:
- **worktree-manager-skill**: Comprehensive git worktree operations
- **video-processor**: Video conversion and transcription
- **meta-skill**: Creates new skills
- **create-worktree-skill**: Simplified worktree creation
- **project-setup**: This skill for replicating project structure

### 6. Status Lines (`status_lines/`)
Custom status line displays for the CLI interface

### 7. Settings (`settings.json`)
Central configuration for:
- Status line configuration
- Hook registrations for all lifecycle events
- Command paths using `$CLAUDE_PROJECT_DIR` variable

## Configuration Philosophy

This setup implements a **multi-agent observability system** with:

1. **Event Broadcasting**: All hooks call `send_event.py` to broadcast events
2. **Summarization**: Many hooks use `--summarize` flag for concise reporting
3. **Extensibility**: Modular design allows adding new hooks, agents, skills
4. **Source Identification**: Uses `--source-app cc-hook-multi-agent-obvs` for tracking
5. **Progressive Enhancement**: Core functionality works without optional components

## Dependencies

All Python scripts use `uv run` for dependency management, ensuring:
- Consistent environment across executions
- PEP 723 inline dependencies where applicable
- No global Python package conflicts

## Usage Pattern

When this structure is replicated:
1. Hooks automatically activate based on `settings.json`
2. Skills are discovered and loaded on-demand
3. Commands become available via `/command-name`
4. Agents can be invoked via Task tool
5. Output styles can be selected by user
6. Status line displays project-specific info
