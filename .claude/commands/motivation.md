---
model: claude-haiku-4-5-20251001
description: Fast audio mindfulness message for Teri
argument-hint: [theme]
allowed-tools: Bash
---

# Purpose

Provide personalized, calming motivation messages inspired by yoga and mindfulness practices. Uses Claude's fast and cost-effective haiku model to generate thoughtful, encouraging messages for work, coding, or personal reflection.

## Variables

```
USER_NAME: "Teri" (hardcoded)
THEME: $1 (default: "focus")
ELEVENLABS_API_KEY: hardcoded in workflow
ELEVENLABS_VOICE_ID: hardcoded in workflow
```

## Available Themes

- `focus` - Concentration and deep work
- `calm` - Stress relief and tranquility
- `energy` - Motivation and vitality
- `balance` - Work-life harmony
- `creativity` - Flow and inspiration
- `gratitude` - Appreciation and presence
- `resilience` - Strength through challenges
- `mindfulness` - Present moment awareness

## Instructions

**STREAMLINED EXECUTION - NO TODO TRACKING, NO VERBOSE OUTPUT**

1. **Generate message instantly** - 1 short sentence only, personalized for Teri based on theme
2. **Call ElevenLabs API immediately** - No environment loading steps or validation
3. **Play audio silently** - No console output except minimal emoji
4. **Fast execution** - Skip all TodoWrite calls and verbose workflow steps

## Workflow

```bash
#!/bin/bash

# Get theme from argument or default to focus
THEME="${1:-focus}"

# Load environment variables
set -a
[ -f .env ] && source .env
set +a

# Get API key from environment
API_KEY="${ELEVENLABS_API_KEY}"
if [ -z "$API_KEY" ]; then
    echo "❌ ELEVENLABS_API_KEY not configured"
    exit 1
fi

# Define messages by theme
case "$THEME" in
    focus)
        MESSAGE="Teri, breathe deep and let your mind become still like mountain water."
        ;;
    calm)
        MESSAGE="Release the tension, Teri, and let peace flow through your work."
        ;;
    energy)
        MESSAGE="Feel the spark rising within you, Teri, ready to illuminate every task."
        ;;
    balance)
        MESSAGE="Find your center, Teri, where effort and ease dance in perfect harmony."
        ;;
    creativity)
        MESSAGE="Let your creativity flow freely, Teri, unbound and radiant like dawn light."
        ;;
    gratitude)
        MESSAGE="Pause and appreciate this moment, Teri, this gift of presence and purpose."
        ;;
    resilience)
        MESSAGE="You are stronger than any challenge, Teri, rooted and unshakeable."
        ;;
    mindfulness)
        MESSAGE="Be here now, Teri, where life truly happens in this precious breath."
        ;;
    *)
        MESSAGE="Breathe, Teri. You are exactly where you need to be."
        ;;
esac

# Use ElevenLabs TTS via uv run
cd .claude && \
uv run hooks/utils/tts/elevenlabs_tts.py "$MESSAGE" 2>/dev/null && \
cd .. && \
echo "🔊 $THEME"
```

**Console output:**
```
🔊 {THEME}
```

**That's it. Clean, simple, and effective.**

## Example Messages (1 sentence max)

**Focus Theme:**
"Teri, breathe deep and let your mind become still like mountain water."

**Calm Theme:**
"Release the tension, Teri, and let peace flow through your work."

**Energy Theme:**
"Feel the spark rising within you, Teri, ready to illuminate every task."

**Balance Theme:**
"Find your center, Teri, where effort and ease dance in perfect harmony."

## Error Handling

If API fails, show:
```
❌ Audio generation failed. Try again.
```

## Integration Benefits

- **Cost-effective**: Uses Claude Haiku (very affordable)
- **Fast response**: Near-instant message generation
- **Seamless integration**: Native Claude Code slash command
- **Personalized**: Uses your name from .env
- **Thematic variety**: 8 different mindfulness themes
- **Audio support**: Optional TTS playback
- **Contextual**: Appropriate for coding/work sessions
- **Calming**: Reduces stress and improves focus

Perfect for:
- Starting work sessions with intention
- Taking mindful breaks between tasks
- Re-centering when feeling stuck
- Ending the day with gratitude
- Finding balance during intense coding sessions

Use `/motivation` whenever you need a moment of mindfulness encouragement!