# Environment Setup Command

## Quick Setup

Copy the environment template:
```bash
cp .env.sample .env
```

## What This Does

- Creates a working `.env` file from the template
- Preserves all your API key configurations
- Sets up Teri as the default engineer name
- Ready for API key additions when needed

## Next Steps

Edit `.env` to add your API keys (optional):
- `OPENAI_API_KEY` - for OpenAI models and TTS
- `ANTHROPIC_API_KEY` - for Claude models
- `ELEVENLABS_API_KEY` - for premium TTS

## Usage

The hooks system will automatically use `.env` for:
- Personalized notifications ("Hey Teri, task complete!")
- API-based features when keys are available
- Offline fallbacks when no keys configured