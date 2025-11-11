# Python Project Setup with UV and Claude Code Hooks

## Prerequisites
- `uv` package manager installed
- Python 3.11+ installed
- Claude Code CLI

## Setup Steps

### 1. Create Project Structure
```
project_name/
├── .venv/          # Virtual environment (created automatically)
├── .claude/         # Claude Code configuration
│   ├── settings.json
│   ├── commands/
│   └── hooks/
├── docs/           # Documentation
├── src/            # Source code
├── tests/          # Test files
├── .gitignore      # Git ignore rules
├── README.md       # Project documentation
├── pyproject.toml  # Project configuration
└── CLAUDE.md       # Claude Code instructions
```

### 2. Create pyproject.toml
Create a `pyproject.toml` file with:
- Project metadata (name, version, description)
- Build system configuration (hatchling)
- Dependencies and dev dependencies
- Tool configurations (black, isort, mypy, pytest)
- Python version requirements
- **Important**: Update GitHub URLs in `[project.urls]` section to point to correct repository

### 3. Create README.md
Create a basic `README.md` file with:
- Project description
- Setup instructions
- Development workflow commands

### 4. Set Up Environment Variables
Copy and configure environment variables:
```bash
cp .env.sample .env
```
Edit `.env` file to add your API keys:
- `OPENAI_API_KEY` - for OpenAI models and TTS
- `ANTHROPIC_API_KEY` - for Claude models
- `ELEVENLABS_API_KEY` - for premium TTS
- `ENGINEER_NAME` - for personalized notifications (default: "Teri")

**Note**: Without API keys, the system will use offline alternatives (pyttsx3 for TTS).

### 5. Create Local Settings
Create local Claude Code settings (personal configuration):
```bash
# Create basic local settings
cat > .claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "outputStyle": "default"
}
EOF
```

**Purpose of settings.local.json:**
- **Personal permissions**: MCP tool access permissions
- **Local preferences**: Output styles, editor settings
- **Machine-specific config**: Paths, local tools
- **Developer preferences**: Personal workflow settings

**Important**: This file is in .gitignore and should NOT be committed to version control.

### 6. Set Up Claude Code Hooks
Configure Claude Code hooks for automation:

#### Shebang Settings
All hooks files must use:
```bash
#!/usr/bin/env uv run python
```

#### File Permissions
Ensure all hook files have execute permissions:
```bash
chmod +x .claude/hooks/*.py
```

#### Available Hook Types
- **PreToolUse** - Before tool execution
- **PostToolUse** - After tool execution
- **Notification** - Event notifications
- **Stop** - Session end
- **SubagentStop** - Subagent termination
- **UserPromptSubmit** - User prompt submission
- **PreCompact** - Before context compression
- **SessionStart** - Session start

#### Best Practices
- Use consistent shebang: `#!/usr/bin/env uv run python`
- Include proper error handling in hooks
- Log important events to `logs/` directory
- Keep hooks fast to avoid blocking

### 5. Run UV Sync
```bash
uv sync
```
This will:
- Create a virtual environment in `.venv/`
- Install the project in development mode
- Install all dependencies from `pyproject.toml`
- Set up Claude Code hooks environment

### 6. Verify Installation
Check if the virtual environment was created:
```bash
ls -la .venv/
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Test Claude Code hooks:
```bash
# Check hook files have correct shebang
head -1 .claude/hooks/*.py

# Check file permissions
ls -la .claude/hooks/*.py
```

Test voice output (Samantha voice - macOS high quality):
```bash
# Test the enhanced pyttsx3 with automatic voice selection
./.claude/hooks/utils/tts/pyttsx3_tts.py "Hello Teri, setup complete!"
```

**Note**: The system automatically selects Samantha (US English female voice) on macOS for high-quality voice output.

## Notes

- The `uv sync` command automatically creates the `.venv/` directory
- No need to manually create virtual environments with `python -m venv`
- The project is installed in editable mode, so changes to source code are immediately available
- All dependencies defined in `pyproject.toml` are automatically installed
- Claude Code hooks enhance development workflow with automation

## Troubleshooting

### UV Sync Issues
If `uv sync` fails, check:
1. `pyproject.toml` exists and is valid
2. `README.md` exists (if specified in pyproject.toml)
3. No conflicting `.venv` directory exists
4. Python version meets requirements in pyproject.toml

### Hooks Issues
If hooks don't work:
1. Check shebang is correct: `#!/usr/bin/env uv run python`
2. Verify execute permissions: `chmod +x .claude/hooks/*.py`
3. Ensure virtual environment is set up: `uv sync`
4. Check `.claude/settings.json` configuration

### Common Errors
- `No such file or directory` → Check shebang and file permissions
- `ModuleNotFoundError` → Run `uv sync` to ensure dependencies
- `Permission denied` → Set execute permissions on hook files