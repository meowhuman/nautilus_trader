#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

import sys
import subprocess
import random
import platform

def main():
    """
    macOS Say TTS Script

    Uses macOS native 'say' command for text-to-speech synthesis.
    Accepts optional text prompt as command-line argument.

    Usage:
    - ./macos_say_tts.py                    # Uses default text
    - ./macos_say_tts.py "Your custom text"  # Uses provided text

    Features:
    - Native macOS TTS (no dependencies required)
    - High-quality system voices
    - Voice customization options
    - Fast and responsive
    """

    # Check if running on macOS
    if platform.system() != "Darwin":
        print("❌ Error: This script is designed for macOS only")
        print("Use pyttsx3_tts.py for cross-platform compatibility")
        sys.exit(1)

    # Get text from command line argument or use default
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])  # Join all arguments as text
    else:
        # Default completion messages
        completion_messages = [
            "Work complete!",
            "All done!",
            "Task finished!",
            "Job complete!",
            "Ready for next task!"
        ]
        text = random.choice(completion_messages)

    try:
        print("🎙️  macOS Say TTS")
        print("=" * 20)
        print(f"🎯 Text: {text}")
        print("🔊 Speaking...")

        # Use macOS say command with optimized settings
        # -r: rate (default 200, lower = slower)
        # -v: voice (optional, uses system default)
        cmd = ["say", "-r", "180", text]

        # Execute the command
        subprocess.run(cmd, check=True, capture_output=True)

        print("✅ Playback complete!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing say command: {e}")
        print("Make sure 'say' command is available on your system")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()