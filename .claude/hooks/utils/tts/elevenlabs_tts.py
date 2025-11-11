#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "python-dotenv",
# ]
# ///

import os
import sys
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
    ElevenLabs Turbo v2.5 TTS Script

    Uses ElevenLabs' Turbo v2.5 model for fast, high-quality text-to-speech.
    Accepts optional text prompt as command-line argument.

    Usage:
    - ./eleven_turbo_tts.py                    # Uses default text
    - ./eleven_turbo_tts.py "Your custom text" # Uses provided text

    Features:
    - Fast generation (optimized for real-time use)
    - High-quality voice synthesis
    - Stable production model
    - Cost-effective for high-volume usage
    """

    # Load environment variables from .env file
    load_env_from_file()

    # Get API key from environment
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY not found in environment variables")
        print("Please add your ElevenLabs API key to .env file:")
        print("ELEVENLABS_API_KEY=your_api_key_here")
        sys.exit(1)
    
    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import play
        
        # Initialize client
        elevenlabs = ElevenLabs(api_key=api_key)
        
        print("🎙️  ElevenLabs Turbo v2.5 TTS")
        print("=" * 40)
        
        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # Join all arguments as text
        else:
            text = "The first move is what sets everything in motion."
        
        print(f"🎯 Text: {text}")
        print("🔊 Generating and playing...")
        
        try:
            from elevenlabs import VoiceSettings

            # Get voice ID from environment or use Mina as default
            voice_id = os.getenv('ELEVENLABS_VOICE_ID', 'BpjGufoPiobT79j2vtj4')

            # Soft and gentle voice settings - calm, soothing, natural
            voice_settings = VoiceSettings(
                stability=0.4,         # Medium stability for natural, gentle tone
                similarity_boost=0.3,  # Maintain voice character but soft
                style=0.2,            # Low style for calm, understated delivery
                use_speaker_boost=False # Keep it natural and gentle
            )

            # Generate and play audio directly
            audio = elevenlabs.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                voice_settings=voice_settings,  # Apply relaxed settings
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128",
            )

            # Handle generator response properly
            audio_bytes = b''.join(audio)

            # Save and play
            with open('/tmp/elevenlabs_test.mp3', 'wb') as f:
                f.write(audio_bytes)

            import subprocess
            subprocess.run(['afplay', '/tmp/elevenlabs_test.mp3'])
            print("✅ Playback complete!")

        except Exception as e:
            print(f"❌ Playback error: {e}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        
    except ImportError:
        print("❌ Error: elevenlabs package not installed")
        print("This script uses UV to auto-install dependencies.")
        print("Make sure UV is installed: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()