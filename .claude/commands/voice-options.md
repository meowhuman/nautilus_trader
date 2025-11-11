# TTS Voice Options

## Available TTS Providers

### 1. macOS Say (Recommended for Mac)
**Native macOS voice synthesis**
```bash
# Test macOS say command directly
say -r 180 "Hello Teri, task complete!"

# List available voices
say -v ?
```

**Features:**
- 🎤 High-quality system voices
- 🚀 Fast and responsive
- 🎯 No API key required
- 📱 Native macOS integration

### 2. pyttsx3 (Cross-platform)
**Offline TTS with voice selection**
```bash
# Test with enhanced settings
./.claude/hooks/utils/tts/pyttsx3_tts.py "Hello Teri!"
```

**Features:**
- 🌍 Cross-platform (Windows, macOS, Linux)
- 🔍 Smart voice selection
- 🎛️ Configurable settings
- 📡 Works offline

### 3. OpenAI TTS (Cloud-based)
**Premium cloud voices** (requires API key)
```bash
# Add to .env:
# OPENAI_API_KEY=your_key_here
# TTS_PROVIDER=openai
```

**Features:**
- 🌟 Highest quality voices
- 🎭 Multiple voice options
- 🌐 Natural sounding
- 💸 Requires API key

### 4. ElevenLabs (Premium)
**Studio-quality voices** (requires API key)
```bash
# Add to .env:
# ELEVENLABS_API_KEY=your_key_here
# TTS_PROVIDER=elevenlabs
```

## Quick Setup

### Option 1: Use macOS Say (Recommended)
```bash
# Edit .env file and add:
TTS_PROVIDER=macos_say
```

### Option 2: Use Enhanced pyttsx3
```bash
# Edit .env file and add:
TTS_PROVIDER=pyttsx3
```

### Option 3: Test All Options
```bash
# Test macOS say
say -r 180 "Testing macOS voice"

# Test pyttsx3
./.claude/hooks/utils/tts/pyttsx3_tts.py "Testing pyttsx3 voice"
```

## Voice Customization

### macOS Voice Selection
```bash
# List available voices
say -v ?

# Use specific voice
say -v Samantha "Hello Teri"

# Adjust settings
say -r 180 -v 100 "Hello Teri"  # Slower rate
```

### pyttsx3 Settings
```bash
# The enhanced version automatically:
# - Slower rate (150 vs 180)
# - Higher volume (0.9 vs 0.8)
# - Best voice selection
# - Shows available options
```

## Configuration

Edit `.env` file to set your preference:
```bash
# Voice provider (auto, micos_say, pyttsx3, openai, elevenlabs)
TTS_PROVIDER=macos_say

# Voice speed adjustment
TTS_VOICE_SPEED=1.0

# Voice pitch adjustment
TTS_VOICE_PITCH=1.0
```

**Note:** Set to `auto` for automatic selection based on available API keys and platform.