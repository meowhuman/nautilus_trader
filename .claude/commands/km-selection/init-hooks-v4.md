---
description: Initializes Claude Code hooks with comprehensive setup validation and TTS configuration.
argument-hint: [project-directory]
allowed-tools: Read, Write, Bash, Glob, Grep
model: claude-haiku-4-5-20251001
---

# Claude Code Hooks Initialization v3

## Variables

PROJECT_DIR: ${1:-.}
CLAUDE_DIR: .claude
PYPROJECT_TOML: .claude/pyproject.toml
ENV_FILE: .env
ENV_SAMPLE: .env.sample
HOOKS_DIR: .claude/hooks
CLAUDE_MD: CLAUDE.md

## Architecture: Dual pyproject.toml

This initialization relies on **separate, isolated environments**:

**Root `pyproject.toml`** (Your Project)
- Contains application dependencies
- Manages project venv (`venv/` or `.venv`)
- Used for building and packaging your app

**`.claude/pyproject.toml`** (Hooks Only)
- Contains only hook-specific dependencies (elevenlabs, requests, python-dotenv)
- Manages isolated venv (`.claude/.venv`)
- Runs during Claude Code events (hooks execution)
- Does NOT interfere with your project dependencies

**Why separate?** ✅ No version conflicts, clean isolation, independent updates

## Instructions

- IMPORTANT: If $1 is not provided, use current directory (.).
- Validate all prerequisites before initialization.
- Check file existence (CLAUDE.md, .env, .env.sample, root `pyproject.toml`).
- Verify `.claude/pyproject.toml` exists for hook dependencies.
- Perform initialization steps in correct dependency order.
- Provide clear feedback for each step.
- Stop and report if any critical file is missing.

## Workflow

1. `Pre-flight Validation` - Check all required files exist
2. `Verify pyproject.toml` - Ensure project configuration is ready
3. `Setup Environment Files` - Create .env from .env.sample if needed
4. `Initialize Virtual Environment` - Run uv sync in .claude directory
5. `Configure Hook Permissions` - Make all hooks executable
6. `Setup Logs Directory` - Create logs directory from CLAUDE_HOOKS_LOG_DIR if configured
7. `Verify Setup` - Run post-initialization checks with logs validation
8. `Report Status` - Summarize initialization results

## Pre-flight Checks

```bash
#!/bin/bash
set -e

echo "=== Claude Code Hooks Initialization v3 ==="
echo ""
echo "📋 Pre-flight Validation..."
echo ""

# Check CLAUDE.md
if [ -f CLAUDE.md ]; then
    echo "✅ CLAUDE.md found"
else
    echo "❌ CLAUDE.md not found - required documentation missing"
    exit 1
fi

# Check .env.sample
if [ -f .env.sample ]; then
    echo "✅ .env.sample found"
else
    echo "❌ .env.sample not found - cannot configure environment"
    exit 1
fi

# Check .env exists
if [ -f .env ]; then
    echo "✅ .env found (already configured)"
else
    echo "⚠️ .env not found - will create from .env.sample"
fi

# Check root pyproject.toml (project config)
if [ -f pyproject.toml ]; then
    echo "✅ Root pyproject.toml found (project dependencies)"
else
    echo "⚠️  Root pyproject.toml not found - recommended for project setup"
fi

# Check .claude/pyproject.toml (hook dependencies)
if [ -f .claude/pyproject.toml ]; then
    echo "✅ .claude/pyproject.toml found (hook dependencies isolated)"
else
    echo "❌ .claude/pyproject.toml not found - hook config missing"
    exit 1
fi

# Check hooks directory
if [ -d .claude/hooks ]; then
    echo "✅ .claude/hooks directory found"
else
    echo "❌ .claude/hooks directory not found"
    exit 1
fi

echo ""
echo "✅ Pre-flight validation passed!"
```

## Environment Setup

```bash
#!/bin/bash

echo "📝 Setting up environment files..."

# Create .env from .env.sample if missing
if [ ! -f .env ]; then
    cp .env.sample .env
    echo "✅ .env created from .env.sample"
    echo "⚠️  IMPORTANT: Edit .env and add your API keys for TTS to work"
else
    echo "✅ .env already configured"
fi

echo ""
```

## Virtual Environment Initialization

```bash
#!/bin/bash

echo "🔧 Initializing virtual environment..."

# Verify pyproject.toml exists
if [ ! -f .claude/pyproject.toml ]; then
    echo "❌ .claude/pyproject.toml not found!"
    exit 1
fi

# Clean up corrupted .venv if it exists
if [ -d .claude/.venv ]; then
    echo "🧹 Removing corrupted .venv..."
    rm -rf .claude/.venv
    echo "✅ Removed corrupted virtual environment"
fi

# Run uv sync
cd .claude
uv sync
cd ..

echo "✅ Virtual environment initialized"
echo ""
```

## Hook Configuration

```bash
#!/bin/bash

echo "🔐 Configuring hook files..."

# Set executable permissions on all hook files
chmod +x .claude/hooks/*.py

echo "✅ All hook files are now executable"

# Verify shebang in hooks
echo ""
echo "📖 Verifying shebang headers..."
if grep -l "uv run python" .claude/hooks/*.py > /dev/null 2>&1; then
    echo "✅ Hooks shebang verified"
else
    echo "⚠️  Some hooks may have incorrect shebang - check manually"
fi

echo ""
```

## Logs Directory Setup

```bash
#!/bin/bash

echo "📁 Setting up logs directory..."

# Load environment variables
set -a
[ -f .env ] && source .env
set +a

# Create logs directory if CLAUDE_HOOKS_LOG_DIR is configured
if [ -n "$CLAUDE_HOOKS_LOG_DIR" ]; then
    mkdir -p "$CLAUDE_HOOKS_LOG_DIR"
    if [ -d "$CLAUDE_HOOKS_LOG_DIR" ]; then
        echo "✅ Logs directory created: $CLAUDE_HOOKS_LOG_DIR"
    else
        echo "❌ Failed to create logs directory: $CLAUDE_HOOKS_LOG_DIR"
        exit 1
    fi
else
    echo "⚠️  CLAUDE_HOOKS_LOG_DIR not set - logs may end up in default location"
fi

echo ""
```

## Post-initialization Verification

```bash
#!/bin/bash

echo "✔️  Verifying setup..."
echo ""

ERRORS=0

# Load environment variables for verification
set -a
[ -f .env ] && source .env
set +a

# Check all required files
echo "📋 File Status:"
[ -f CLAUDE.md ] && echo "  ✅ CLAUDE.md" || { echo "  ❌ CLAUDE.md"; ERRORS=$((ERRORS+1)); }
[ -f .env ] && echo "  ✅ .env" || echo "  ⚠️  .env created from .env.sample"
[ -f .env.sample ] && echo "  ✅ .env.sample" || { echo "  ❌ .env.sample"; ERRORS=$((ERRORS+1)); }
[ -f .claude/pyproject.toml ] && echo "  ✅ .claude/pyproject.toml" || { echo "  ❌ .claude/pyproject.toml"; ERRORS=$((ERRORS+1)); }
[ -d .claude/hooks ] && echo "  ✅ .claude/hooks/" || { echo "  ❌ .claude/hooks/"; ERRORS=$((ERRORS+1)); }

echo ""
echo "📁 Logs Configuration:"
if [ -n "$CLAUDE_HOOKS_LOG_DIR" ]; then
    if [ -d "$CLAUDE_HOOKS_LOG_DIR" ]; then
        echo "  ✅ CLAUDE_HOOKS_LOG_DIR is set and directory exists"
        echo "     Path: $CLAUDE_HOOKS_LOG_DIR"
    else
        echo "  ❌ CLAUDE_HOOKS_LOG_DIR path does not exist: $CLAUDE_HOOKS_LOG_DIR"
        ERRORS=$((ERRORS+1))
    fi
else
    echo "  ⚠️  CLAUDE_HOOKS_LOG_DIR not configured (logs may end up in default location)"
fi

echo ""
echo "🔒 Hook Permissions:"
if [ -x .claude/hooks/notification.py ]; then
    echo "  ✅ Hooks are executable"
else
    echo "  ❌ Hooks are not executable"
    ERRORS=$((ERRORS+1))
fi

echo ""
echo "🔌 Virtual Environment:"
if [ -d .claude/.venv ]; then
    echo "  ✅ Virtual environment exists"
else
    echo "  ⚠️  Virtual environment not found (may be in different location)"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 ✅ Initialization successful! Hooks are ready."
    echo ""
    echo "🎤 Testing TTS with Mina's greeting..."
    echo ""

    # Load environment variables for TTS test
    set -a
    [ -f .env ] && source .env
    set +a

    # Generate greeting with Mina's introduction
    GREETING=$(python3 << 'PYTHON_EOF'
import os
import json
import subprocess

api_key = os.getenv('OPENAI_API_KEY', '')

if api_key:
    try:
        result = subprocess.run([
            'curl', '-s', 'https://api.openai.com/v1/chat/completions',
            '-H', f'Authorization: Bearer {api_key}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({
                "model": "gpt-4o-mini",
                "max_tokens": 30,
                "messages": [{
                    "role": "user",
                    "content": "I am Mina, your voice guide. Generate a very short, casual welcome greeting (1 sentence max, under 20 words). Start with Hey or Hi, mention my name naturally. Be warm and friendly like greeting a friend. No mention of being AI."
                }]
            })
        ], capture_output=True, text=True, timeout=5)

        data = json.loads(result.stdout)
        greeting = data['choices'][0]['message']['content']
        if 'Mina' not in greeting:
            greeting = f"Hey, it's Mina. {greeting}"
        print(greeting)
    except Exception as e:
        print("Hey, it's Mina. Claude Code hooks are ready and listening!")
else:
    print("Hey, it's Mina. Claude Code hooks are ready and listening!")
PYTHON_EOF
)

    echo "📢 Mina says: $GREETING"
    echo ""

    # Test TTS
    TTS_WORKED=0

    # Try ElevenLabs first
    if grep -q "ELEVENLABS_API_KEY" .env 2>/dev/null && [ -n "$ELEVENLABS_API_KEY" ]; then
        echo "🎙️  Attempting ElevenLabs TTS..."
        if cd .claude && uv run hooks/utils/tts/elevenlabs_tts.py "$GREETING" 2>/dev/null; then
            echo "✅ ElevenLabs TTS test successful - Mina is speaking!"
            TTS_WORKED=1
            cd ..
        else
            cd ..
        fi
    fi

    # Fall back to macOS say if needed
    if [ $TTS_WORKED -eq 0 ]; then
        echo "🎙️  Using macOS say for TTS..."
        if say "$GREETING" 2>/dev/null; then
            echo "✅ TTS test successful - Mina is speaking!"
            TTS_WORKED=1
        fi
    fi

    if [ $TTS_WORKED -eq 0 ]; then
        echo "⚠️  TTS not available on this system"
    fi

    echo ""
else
    echo "⚠️  $ERRORS issue(s) detected - please review above"
    exit 1
fi

echo ""
```

## TTS Configuration

`API Priority (highest to lowest):`

1. `ElevenLabs` (Recommended)
   ```env
   ELEVENLABS_API_KEY=your-key-here
   ```
   - Highest quality voice synthesis
   - Get key: https://elevenlabs.io

2. `OpenAI`
   ```env
   OPENAI_API_KEY=your-key-here
   ```
   - Requires OpenAI account
   - Get key: https://platform.openai.com

3. `pyttsx3` (Default)
   - No API key required
   - Local text-to-speech
   - Lower quality but cost-free

`Optional Settings:`
```env
ENGINEER_NAME=Your Name    # For personalized notifications (30% chance)
```

## Troubleshooting

### Common Issues

| Error | Solution |
|-------|----------|
| `.env not found` | Run `cp .env.sample .env` and edit with API keys |
| `CLAUDE.md missing` | Ensure root directory has CLAUDE.md documentation |
| `pyproject.toml not found` | Verify `.claude/pyproject.toml` exists with correct configuration |
| `ModuleNotFoundError` | Run `cd .claude && uv sync && cd ..` to install dependencies |
| `No TTS audio` | Check `.env` has valid API keys for your chosen TTS service |
| `Permission denied` | Run `chmod +x .claude/hooks/*.py` to set executable permissions |
| `Logs directory not found` | Ensure `CLAUDE_HOOKS_LOG_DIR` is set in `.env` and the path exists |
| `Logs in wrong location` | Check that `CLAUDE_HOOKS_LOG_DIR` in `.env` points to the correct directory path |

### Verification Commands

```bash
# Check all required files
echo "=== Checking required files ===" && \
[ -f CLAUDE.md ] && echo "✅ CLAUDE.md" || echo "❌ CLAUDE.md" && \
[ -f .env ] && echo "✅ .env" || echo "⚠️ .env" && \
[ -f .env.sample ] && echo "✅ .env.sample" || echo "❌ .env.sample" && \
[ -d .claude/hooks ] && echo "✅ .claude/hooks" || echo "❌ .claude/hooks"

# Check API keys are configured
echo "=== Checking TTS API keys ===" && \
grep -q "ELEVENLABS_API_KEY" .env && echo "✅ ElevenLabs configured" || echo "⚠️ ElevenLabs not configured" && \
grep -q "OPENAI_API_KEY" .env && echo "✅ OpenAI configured" || echo "⚠️ OpenAI not configured"

# Verify hook permissions
echo "=== Checking hook permissions ===" && \
ls -la .claude/hooks/*.py | grep -c "x" && echo "✅ Hooks are executable" || echo "❌ Hooks need chmod +x"

# Test TTS directly
echo "=== Testing TTS ===" && \
uv run .claude/hooks/utils/tts/elevenlabs_tts.py "Test message"

# Check logs directory configuration
echo "=== Checking logs configuration ===" && \
set -a && [ -f .env ] && source .env && set +a && \
if [ -n "$CLAUDE_HOOKS_LOG_DIR" ]; then
    echo "✅ CLAUDE_HOOKS_LOG_DIR=$CLAUDE_HOOKS_LOG_DIR"
    if [ -d "$CLAUDE_HOOKS_LOG_DIR" ]; then
        echo "✅ Logs directory exists"
        ls -lad "$CLAUDE_HOOKS_LOG_DIR"
    else
        echo "❌ Logs directory does not exist - create it with: mkdir -p '$CLAUDE_HOOKS_LOG_DIR'"
    fi
else
    echo "⚠️ CLAUDE_HOOKS_LOG_DIR not set in .env"
fi
```

## Report

Upon successful initialization, report:
- ✅ All required files present and validated
- ✅ Virtual environment created with dependencies installed
- ✅ Hook files configured with correct permissions
- ✅ Logs directory configured and verified
- ✅ TTS system tested and ready for use
- ⚠️ Next steps: Verify `CLAUDE_HOOKS_LOG_DIR` is set in `.env` and logs directory exists
