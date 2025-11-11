# Claude Code Hooks 設定指南

## 概要
Claude Code hooks 係自動執行 Python scripts 嘅機制，響應各種事件（如 tool 使用前後、session 開始等）。

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

### 4. 環境依賴
運行前確保：
```bash
uv sync  # 同步虛擬環境
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

### 檢查 hooks 狀態
```bash
# 檢查所有 hooks 檔案 shebang
head -1 .claude/hooks/*.py

# 檢查檔案權限
ls -la .claude/hooks/*.py
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