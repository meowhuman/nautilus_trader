---
description: Quick session summary with TTS playback
allowed-tools:
  - Bash(*)
---

Execute the catchup Python script to summarize recent session activity and play via ElevenLabs TTS.

Run the following command:

```bash
cd /Users/terivercheung/Documents/AI/CLI_setup/CLAUDE
uv run .claude/scripts/catchup.py $ARGUMENTS
```

The script will:
1. Analyze recent tool calls from the current session
2. Generate a soft and gentle summary using OpenAI/Anthropic
3. Play the summary via ElevenLabs TTS with your configured voice
4. Display activity statistics

Arguments are passed directly to the script (e.g., `--recent 5`, `--no-tts`, `--verbose`).
