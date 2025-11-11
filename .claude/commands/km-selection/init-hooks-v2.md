# Claude Code Hooks 設定指南

## 概要
Claude Code hooks 係自動執行 Python scripts 嘅機制，響應各種事件（如 tool 使用前後、session 開始等）。

## 快速開始（初次設定）

### 前置檢查
```bash
# 1. 驗證必要檔案存在
test -f CLAUDE.md && echo "✅ CLAUDE.md found" || echo "❌ Missing CLAUDE.md"
test -f .env && echo "✅ .env found" || echo "⚠️ Missing .env (will use .env.sample)"
test -f .env.sample && echo "✅ .env.sample found" || echo "❌ Missing .env.sample"
```

### 一鍵初始化
```bash
# 1. 驗證 pyproject.toml 已正確配置
if [ ! -f .claude/pyproject.toml ]; then
    echo "❌ .claude/pyproject.toml not found!"
    exit 1
fi
echo "✅ pyproject.toml found, proceeding..."

# 2. 檢查環境變數設定 (TTS 必需)
if [ ! -f .env ]; then
    if [ -f .env.sample ]; then
        cp .env.sample .env
        echo "✅ .env created from .env.sample"
        echo "⚠️ Please edit .env and add your API keys"
    else
        echo "❌ No .env or .env.sample found"
        exit 1
    fi
else
    echo "✅ .env already exists"
fi

# 3. 在 .claude 目錄中同步環境（pyproject.toml 已就緒）
cd .claude
uv sync
cd ..

# 4. 設定所有 hook 檔案權限
chmod +x .claude/hooks/*.py
echo "✅ Hook files permissions set"
```

✅ 完成！所有 hooks 現已準備就緒。

## 正確設定方法

### 1. Shebang 設定
所有 hooks 檔案必須使用正確嘅 shebang：
```bash
#!/usr/bin/env uv run python
```

**避免使用：**
- `#!/usr/bin/env python3` - 可能搵唔到正確嘅 Python 環境
- `#!/Users/mac/.local/bin/uv run --script` - 路徑硬編碼，唔通用

### 2. 檔案權限設定
確保所有 hook 檔案有執行權限：
```bash
chmod +x .claude/hooks/*.py
```

### 3. Settings.json 配置
hooks 透過 `.claude/settings.json` 配置，使用 `uv run` command 格式：
```json
"hooks": {
  "Stop": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "uv run .claude/hooks/stop.py --chat"
        }
      ]
    }
  ]
}
```

### 4. pyproject.toml 配置
`.claude/pyproject.toml` 定義項目資訊和所有依賴：

```toml
[project]
name = "claude"  # 必須符合根目錄名稱（此專案為 CLAUDE）
version = "0.1.0"
description = "Claude Code configuration with hooks, agents, and skills"
requires-python = ">=3.11"
```

**配置要點：**
- `name` 應與根目錄名稱一致（轉小寫、用連字符）
  - `CLAUDE` → `claude`
  - `Information-collection` → `information-collection`
- `requires-python` 指定最低 Python 版本
- 所有依賴定義在 `[project] dependencies` 中

### 5. 環境依賴管理
運行前確保環境已同步：
```bash
# 進入 .claude 目錄
cd .claude

# 同步虛擬環境和依賴
uv sync

# 返回根目錄
cd ..
```

**pyproject.toml 包含的依賴：**
- `python-dotenv` - 環境變數管理
- `openai` - OpenAI API (用於 TTS)
- `elevenlabs` - ElevenLabs TTS (優先順序最高)
- `pyttsx3` - 本地 TTS (無需 API)
- `requests` - HTTP 請求

### 6. 環境變數設定 (.env 配置)
TTS 功能需要環境變數配置：

```bash
# 1. 驗證和設定 .env 檔案
if [ ! -f .env ]; then
    if [ -f .env.sample ]; then
        cp .env.sample .env
        echo "✅ .env 已從 .env.sample 建立"
    else
        echo "❌ 找不到 .env 和 .env.sample"
        exit 1
    fi
fi

# 2. 檢查 CLAUDE.md 是否存在
if [ ! -f CLAUDE.md ]; then
    echo "⚠️ CLAUDE.md 不存在，請確保文檔存在"
fi

# 3. 編輯 .env 並設定 API keys
# 編輯器打開 .env，根據以下優先順序設定：
```

**API 優先順序（從高到低）：**
1. **ElevenLabs** (最推薦)
   ```env
   ELEVENLABS_API_KEY=your-elevenlabs-key-here
   ```
   - 高質量語音合成
   - 獲取：https://elevenlabs.io

2. **OpenAI**
   ```env
   OPENAI_API_KEY=your-openai-key-here
   ```
   - 需要 OpenAI 帳戶
   - 獲取：https://platform.openai.com

3. **pyttsx3** (默認)
   - 無需 API key
   - 本地文字轉語音
   - 質量較低但無成本

**其他可選設定：**
```env
ENGINEER_NAME=Your Name      # 用於個性化通知 (30% 機率使用)
```

## 可用 Hook 類型

1. **PreToolUse** - Tool 使用前執行
2. **PostToolUse** - Tool 使用後執行  
3. **Notification** - 通知事件
4. **Stop** - Session 結束時
5. **SubagentStop** - Subagent 停止時
6. **UserPromptSubmit** - 用戶提交 prompt 時
7. **PreCompact** - Context 壓縮前
8. **SessionStart** - Session 開始時

## 故障排除

### 常見錯誤
- `No such file or directory` → 檢查 shebang 和檔案權限
- `ModuleNotFoundError` → 運行 `uv sync` 確保依賴安裝
- **TTS 無聲音** → 檢查 `.env` 是否配置了 API keys
- **找不到 .env** → 執行 `cp .env.sample .env` 建立檔案
- **找不到 CLAUDE.md** → 確保根目錄存在 CLAUDE.md 文檔

### 初始化檢查
```bash
# 驗證所有必要檔案
echo "=== Checking required files ==="
[ -f CLAUDE.md ] && echo "✅ CLAUDE.md" || echo "❌ CLAUDE.md missing"
[ -f .env ] && echo "✅ .env" || echo "⚠️ .env missing"
[ -f .env.sample ] && echo "✅ .env.sample" || echo "❌ .env.sample missing"
[ -d .claude/hooks ] && echo "✅ .claude/hooks" || echo "❌ .claude/hooks missing"
```

### TTS 調試
```bash
# 檢查 API keys 是否設定
grep -E "ELEVENLABS_API_KEY|OPENAI_API_KEY" .env

# 測試 TTS 直接執行
uv run .claude/hooks/utils/tts/elevenlabs_tts.py "Test message"

# 如果都沒有 API key，應使用 pyttsx3（本地合成）
```

### 檢查 hooks 狀態
```bash
# 檢查所有 hooks 檔案 shebang
head -1 .claude/hooks/*.py

# 檢查檔案權限
ls -la .claude/hooks/*.py

# 檢查 pyproject.toml 有效性
cd .claude && uv sync --dry-run
```

## 最佳實踐

1. **統一 shebang**：所有 hooks 使用 `#!/usr/bin/env uv run python`
2. **錯誤處理**：hooks 內應該包含適當嘅 try-catch
3. **日誌記錄**：重要 hooks 應該記錄到 `logs/` 目錄
4. **性能考慮**：hooks 執行要快，避免阻塞主程序

## 修復腳本
批量修復所有 hooks shebang：
```bash
# 修復 shebang
for file in .claude/hooks/*.py; do
  sed -i '1s|.*|#!/usr/bin/env uv run python|' "$file"
done

# 設定執行權限
chmod +x .claude/hooks/*.py
```