#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "python-dotenv",
# ]
# ///

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv


def load_env_from_file():
    """Load environment variables from .env file explicitly."""
    # Try multiple common locations
    env_paths = [
        Path.cwd() / ".env",
        Path.home() / ".env",
        Path(__file__).parent.parent.parent.parent.parent / ".env",  # Go up 5 levels to project root
    ]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path, override=True)
            return True

    return False


def main():
    """
    OpenAI TTS Script (Synchronous)

    Uses OpenAI's gpt-4o-mini-tts model for cheap, high-quality text-to-speech.
    Accepts optional text prompt as command-line argument.

    Usage:
    - ./openai_tts.py                    # Uses default text
    - ./openai_tts.py "Your custom text" # Uses provided text

    Features:
    - OpenAI gpt-4o-mini-tts model (cheapest)
    - Shimmer voice (intimate and engaging)
    - Direct file playback via afplay
    - Seductive tone configuration
    """

    # Load environment variables from .env file
    load_env_from_file()

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to .env file:")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        from openai import OpenAI

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        print("🎙️  OpenAI TTS (gpt-4o-mini-tts)")
        print("=" * 40)

        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # Join all arguments as text
        else:
            text = "Today is a wonderful day to build something people love!"

        print(f"🎯 Text: {text}")
        print("🔊 Generating audio...")

        try:
            # Generate audio using OpenAI TTS with soft and gentle tone
            response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="shimmer",  # Soft and gentle voice
                input=text,
                response_format="mp3",
            )

            # Save to temporary file
            audio_file = Path("/tmp/openai_tts.mp3")
            audio_file.write_bytes(response.content)

            print(f"✅ Audio generated ({audio_file.stat().st_size} bytes)")
            print("🔊 Playing...")

            # Play using afplay (macOS)
            subprocess.run(["afplay", str(audio_file)], check=True)

            print("✅ Playback complete!")

        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

    except ImportError as e:
        print("❌ Error: Required package not installed")
        print("This script uses UV to auto-install dependencies.")
        print("Make sure UV is installed: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
