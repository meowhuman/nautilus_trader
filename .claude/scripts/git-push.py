#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic",
#     "openai",
#     "python-dotenv",
# ]
# ///

"""
Git add, commit, and push with AI-generated summary.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment
env_path = Path.cwd() / ".env"
load_dotenv(env_path, override=True)


def get_git_status():
    """Get current git status."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Failed to get git status: {e}")
        return ""


def get_git_diff():
    """Get git diff for staged and unstaged changes."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--stat'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def generate_commit_message():
    """Generate AI commit message based on changes."""
    try:
        # Try OpenAI first
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)

                status = get_git_status()
                diff = get_git_diff()

                prompt = f"""Generate a detailed git commit message for these changes in Traditional Chinese and English:

Files changed:
{status}

Summary:
{diff}

Requirements:
- Format: type(scope): 繁體中文 (English)
- Types: feat, fix, docs, style, refactor, test, chore
- Include specific improvements (hooks, TTS, commands, etc.)
- Keep under 100 characters total
- One line only, no period
- Return ONLY the commit message

Example: feat(hooks): 優化 TTS 同 summarizer (Improve TTS and summarizer)

Generate:"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    temperature=0.7,
                )

                return response.choices[0].message.content.strip()
            except Exception:
                pass

        # Fallback to Anthropic
        from anthropic import Anthropic
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return None

        client = Anthropic(api_key=api_key)
        status = get_git_status()
        diff = get_git_diff()

        prompt = f"""Generate a detailed git commit message for these changes in Traditional Chinese and English:

Files changed:
{status}

Summary:
{diff}

Requirements:
- Format: type(scope): 繁體中文 (English)
- Types: feat, fix, docs, style, refactor, test, chore
- Include specific improvements (hooks, TTS, commands, etc.)
- Keep under 100 characters total
- One line only, no period
- Return ONLY the commit message

Example: feat(hooks): 優化 TTS 同 summarizer (Improve TTS and summarizer)

Generate:"""

        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text.strip()

    except Exception as e:
        print(f"⚠️  Failed to generate message: {e}")
        return None


def main():
    print("🔄 Git workflow: add → commit → push\n")

    # Check for changes
    status = get_git_status()
    if not status:
        print("✅ No changes to commit")
        return 0

    print(f"📝 Changes detected:\n{status}\n")

    # Stage all changes
    print("📦 Staging changes...")
    result = subprocess.run(['git', 'add', '.'], capture_output=True)
    if result.returncode != 0:
        print(f"❌ Failed to stage changes")
        return 1

    # Generate commit message
    print("🤖 Generating commit message...")
    commit_msg = generate_commit_message()

    if not commit_msg:
        print("⚠️  Using default message")
        commit_msg = f"chore: update files ({datetime.now().strftime('%Y-%m-%d %H:%M')})"

    print(f"💬 Message: {commit_msg}\n")

    # Commit
    print("💾 Committing...")
    result = subprocess.run(
        ['git', 'commit', '-m', commit_msg],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Commit failed: {result.stderr}")
        return 1

    print(result.stdout)

    # Push
    print("🚀 Pushing to remote...")
    result = subprocess.run(
        ['git', 'push'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Push failed: {result.stderr}")
        return 1

    print(result.stdout)
    print("✅ All done!")

    # Show summary with date/time
    print(f"\n📊 Summary:")
    print(f"   Message: {commit_msg}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
