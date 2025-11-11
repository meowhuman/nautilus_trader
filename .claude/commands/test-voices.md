# ElevenLabs Voice Testing

## Setup Your API Key

First, add your ElevenLabs API key to `.env`:
```bash
# Edit .env file and add:
ELEVENLABS_API_KEY=your_api_key_here
```

## Available Voices

ElevenLabs offers many voices. Popular **female, young, fun** options:

### Recommended Voices:
- **Rachel** - Young, energetic American female
- **Drew** - Friendly, warm American female
- **Clyde** - Playful, youthful female
- **Paula** - Cheerful, upbeat female
- **Lily** - Sweet, young female voice
- **Jessie** - Fun, casual American female
- **Ava** - Modern, trendy female
- **Bella** - Bright, friendly female

## Test Commands

### Test a specific voice:
```bash
# Test Rachel (recommended young, fun female)
./.claude/hooks/utils/tts/elevenlabs_tts.py --voice Rachel "Hello! I'm Rachel, your fun assistant!"

# Test other voices
./.claude/hooks/utils/tts/elevenlabs_tts.py --voice Drew "Hi there! I'm Drew, let's have some fun!"

# Test with custom voice ID
./.claude/hooks/utils/tts/elevenlabs_tts.py --voice YOUR_VOICE_ID "Custom voice test!"
```

### Browse all voices:
Visit https://elevenlabs.io/voice-library to hear samples and find voice IDs.

## Voice Selection Tips

**For young, fun female voices:**
- Start with **Rachel** - most popular choice
- Try **Drew** for friendly warmth
- Try **Clyde** for playful energy
- Try **Lily** for sweet charm

**Voice characteristics:**
- **Rachel**: Energetic, clear, very popular
- **Drew**: Warm, approachable, friendly
- **Clyde**: Youthful, fun, expressive
- **Lily**: Sweet, gentle, young

## Set as Default

Once you find your favorite voice, set it in `.env`:
```bash
# Add to .env:
ELEVENLABS_VOICE_ID=Rachel  # or your chosen voice
```

The system will automatically use this voice for all notifications!