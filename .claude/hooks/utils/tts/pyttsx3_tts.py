#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyttsx3",
# ]
# ///

import sys
import random

def main():
    """
    pyttsx3 TTS Script

    Uses pyttsx3 for offline text-to-speech synthesis.
    Accepts optional text prompt as command-line argument.

    Usage:
    - ./pyttsx3_tts.py                    # Uses default text
    - ./pyttsx3_tts.py "Your custom text" # Uses provided text

    Features:
    - Offline TTS (no API key required)
    - Cross-platform compatibility
    - Enhanced voice quality settings
    - Voice selection and customization
    - Immediate audio playback
    """

    try:
        import pyttsx3

        # Initialize TTS engine
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')

        # Enhanced engine settings for better voice quality
        engine.setProperty('rate', 150)     # Slower rate for clarity (was 180)
        engine.setProperty('volume', 0.9)    # Slightly louder (was 0.8)

        # Try to find and set the best available voice
        best_voice = None

        if voices:
            print(f"🔍 Found {len(voices)} voices:")

            # Voice selection logic
            for i, voice in enumerate(voices):
                voice_info = f"Voice {i}: {voice.name}"
                if hasattr(voice, 'languages') and voice.languages:
                    voice_info += f" (Languages: {voice.languages})"
                if hasattr(voice, 'gender'):
                    voice_info += f" (Gender: {voice.gender})"
                print(f"   {voice_info}")

                # Prefer English voices, especially female ones
                voice_name_lower = voice.name.lower()
                voice_id = voice.id.lower()

                # Priority: English female voices
                if ('english' in voice_id or 'en_' in voice_id or 'english' in voice_name_lower) and \
                   (hasattr(voice, 'gender') and voice.gender == 'female') or \
                   ('female' in voice_name_lower or 'samantha' in voice_name_lower or 'victoria' in voice_name_lower):
                    best_voice = i

                # Alternative: Any English voice
                elif best_voice is None and ('english' in voice_id or 'en_' in voice_id or 'english' in voice_name_lower):
                    best_voice = i

            # Set the best voice found
            if best_voice is not None:
                engine.setProperty('voice', voices[best_voice].id)
                print(f"✅ Selected voice: {voices[best_voice].name}")
            else:
                # Fallback to first voice if no English voice found
                engine.setProperty('voice', voices[0].id)
                print(f"🔧 Using default voice: {voices[0].name}")

        print("🎙️  pyttsx3 TTS (Enhanced)")
        print("=" * 25)
        
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
        
        print(f"🎯 Text: {text}")
        print("🔊 Speaking...")
        
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
        print("✅ Playback complete!")
        
    except ImportError:
        print("❌ Error: pyttsx3 package not installed")
        print("This script uses UV to auto-install dependencies.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()