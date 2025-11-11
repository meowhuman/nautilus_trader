#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic",
#     "openai",
#     "elevenlabs",
#     "python-dotenv",
# ]
# ///

"""
/catchup - Session Summary with TTS
Summarizes recent workflow activity and plays it via TTS.
"""

import json
import sys
import os
import argparse
import subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime

try:
    from dotenv import load_dotenv
    # Force load from .env in current directory
    env_path = Path.cwd() / ".env"
    load_dotenv(env_path, override=True)
except ImportError:
    pass


def get_latest_session():
    """Get the most recent session directory."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return None

    sessions = sorted(logs_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
    return sessions[0].name if sessions else None


def read_tool_calls(session_id, limit=None):
    """Read tool calls from pre_tool_use.json."""
    log_file = Path("logs") / session_id / "pre_tool_use.json"

    if not log_file.exists():
        return []

    try:
        with open(log_file) as f:
            calls = json.load(f)
            return calls[:limit] if limit else calls
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def generate_summary(session_id, tool_calls):
    """Generate AI summary of the session."""
    if not tool_calls:
        return "No tool calls recorded in this session"

    # Count tool types
    tool_types = [call.get('tool_name', 'Unknown') for call in tool_calls]
    tool_counts = Counter(tool_types)

    # Build summary prompt
    tools_summary = ", ".join([f"{name} ({count})" for name, count in tool_counts.most_common()])

    # Get commands executed
    bash_calls = [call for call in tool_calls if call.get('tool_name') == 'Bash']
    commands = []
    for call in bash_calls[:3]:  # Last 3 commands
        cmd = call.get('tool_input', {}).get('command', '')
        if cmd:
            # Truncate long commands
            if len(cmd) > 50:
                cmd = cmd[:47] + "..."
            commands.append(cmd)

    commands_text = "\n".join([f"  - {cmd}" for cmd in commands]) if commands else "  (no bash commands)"

    prompt = f"""Summarize this development session activity in ONE gentle and encouraging sentence.

Session Activity:
- Total tool calls: {len(tool_calls)}
- Tools used: {tools_summary}
- Recent commands:{commands_text}

Requirements:
- ONE sentence only (no period)
- Soft, gentle, and kind tone
- Keep under 15 words
- Specific to what was done
- Use present tense
- Return ONLY the summary

Generate the summary:"""

    # Try OpenAI first (cheaper), fallback to Anthropic
    try:
        # Try OpenAI 4o-mini first (cheapest option)
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50,
                )
                summary = response.choices[0].message.content.strip().strip('"').strip("'").strip(".")
                return summary
            except Exception:
                pass  # Fall through to Anthropic

        # Fallback to Anthropic if OpenAI not available
        from anthropic import Anthropic
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return None

        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = message.content[0].text.strip().strip('"').strip("'").strip(".")
        return summary
    except Exception as e:
        print(f"⚠️  Summary generation failed: {e}", file=sys.stderr)
        return None


def get_tts_script_path():
    """Get the best available TTS script (ElevenLabs > OpenAI > pyttsx3)."""
    script_dir = Path(__file__).parent.parent / "hooks" / "utils" / "tts"

    # Check for ElevenLabs (highest priority)
    elev_key = os.getenv('ELEVENLABS_API_KEY')
    if elev_key:
        elevenlabs_script = script_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script), "ElevenLabs"

    # Check for OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        openai_script = script_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script), "OpenAI"

    # Fall back to pyttsx3
    pyttsx3_script = script_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script), "pyttsx3"

    return None, None


def play_tts(text):
    """Play summary via ElevenLabs TTS."""
    try:
        elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        if not elevenlabs_key:
            print("⚠️  No ElevenLabs API key found", file=sys.stderr)
            return False

        print(f"🎙️  Playing via ElevenLabs...")

        from elevenlabs.client import ElevenLabs
        from elevenlabs import VoiceSettings
        import time

        client = ElevenLabs(api_key=elevenlabs_key)
        voice_id = os.getenv('ELEVENLABS_VOICE_ID', 'BpjGufoPiobT79j2vtj4')

        # Soft and gentle voice settings
        voice_settings = VoiceSettings(
            stability=0.4,
            similarity_boost=0.3,
            style=0.2,
            use_speaker_boost=False
        )

        # Generate audio
        print(f"📝 Generating audio...")
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            voice_settings=voice_settings,
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128",
        )

        # Collect audio bytes
        audio_bytes = b''.join(audio_generator)
        print(f"✅ Audio generated ({len(audio_bytes)} bytes)")

        # Save to file
        audio_file = Path("/tmp/catchup_elevenlabs.mp3")
        with open(audio_file, 'wb') as f:
            f.write(audio_bytes)

        print(f"💾 Saved to {audio_file}")

        # Play audio in background using nohup
        print(f"🔊 Playing audio...")

        # Use nohup to detach from parent process
        subprocess.Popen(
            ['nohup', 'afplay', str(audio_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        print(f"✅ Audio playback started in background!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Summarize session activity with TTS',
        prog='/catchup'
    )
    parser.add_argument('--session', help='Session ID to summarize')
    parser.add_argument('--recent', type=int, default=None, help='Show last N tool calls')
    parser.add_argument('--no-tts', action='store_true', help='Skip TTS playback')
    parser.add_argument('--verbose', action='store_true', help='Show detailed tool calls')

    args = parser.parse_args()

    # Get session
    session_id = args.session or get_latest_session()

    if not session_id:
        print("❌ No sessions found")
        sys.exit(1)

    print(f"📊 Session: {session_id}\n")

    # Read tool calls
    tool_calls = read_tool_calls(session_id, limit=args.recent)

    if not tool_calls:
        print("❌ No tool calls recorded")
        sys.exit(0)

    # Show tool call summary
    tool_types = [call.get('tool_name', 'Unknown') for call in tool_calls]
    tool_counts = Counter(tool_types)

    print(f"🔍 Recent activity ({len(tool_calls)} tools):")
    for tool_name, count in tool_counts.most_common():
        print(f"   • {tool_name}: {count}")

    # Verbose mode: show details
    if args.verbose:
        print("\n📝 Detailed calls:")
        for i, call in enumerate(tool_calls[-5:], 1):  # Last 5
            tool_name = call.get('tool_name', 'Unknown')
            print(f"   {i}. {tool_name}")

            if tool_name == 'Bash':
                cmd = call.get('tool_input', {}).get('command', '')[:60]
                print(f"      → {cmd}...")
            elif tool_name == 'Read':
                path = call.get('tool_input', {}).get('file_path', '')
                print(f"      → {path}")
            elif tool_name == 'Edit':
                path = call.get('tool_input', {}).get('file_path', '')
                print(f"      → {path}")

    # Generate summary
    print("\n✨ Generating summary...")
    summary = generate_summary(session_id, tool_calls)

    if summary:
        print(f"💬 {summary}\n")

        # Play TTS
        if not args.no_tts:
            play_tts(summary)
    else:
        print("⚠️  Could not generate summary\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
