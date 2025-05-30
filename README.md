# NIKKE CJJC Automator

NIKKE CJJC Automator 是一款現代化、可維護、可擴充的 NIKKE 自動化腳本工具，支援多模式自動化、互動式 CLI、Windows 提權偵測、圖片暫存與合併、熱鍵安全終止等功能。

## 特色功能
- 現代化 Python package 架構，分層（MVC）設計，型別提示
- 設定集中於 `settings.default.toml`，自動管理與版本檢查，支援延遲參數
- 互動式 CLI（Typer + Questionary），無參數自動進入選單
- 多模式自動化（策略模式），主流程高度模組化
- 圖片暫存與自動合併，支援自訂 output 目錄
- 支援 PyInstaller 打包為單一 EXE，Windows 提權偵測與自動重啟
- 熱鍵（含 Ctrl+C）與安全終止，所有提示統一 logging
- 友善錯誤防呆，所有重要操作皆有提示

## 安裝與執行

### 1. 下載可執行檔
- 前往 [Releases](https://github.com/t106362512/releases) 下載最新的 `nikke-cjjc-automator.exe`
- 直接雙擊執行，或於命令列執行

### 2. 原始碼安裝
```bash
# 安裝依賴
pdm install
# 執行 CLI
pdm run nikke-cjjc-automator
```

### 3. 打包 EXE
```bash
pdm run nikke-cjjc-automator-build
```

## 使用說明
- 執行程式時，若未以系統管理員身份啟動，會自動開啟 `img/manual.jpg` 並彈窗提示
- 進入互動式選單，選擇自動化模式
- 可於 `settings.default.toml` 調整延遲、熱鍵、輸出目錄等參數
- 執行過程可用 Ctrl+C 或自訂熱鍵安全終止

## 設定檔說明
- `settings.default.toml`：集中管理所有參數，首次執行會自動複製到用戶目錄
- 重要參數：
  - `START_DELAY`、`INITIAL_PLAYER_DELAY`、`ACTION_DELAY`：各階段延遲
  - `OUTPUT_DIR`：圖片合併輸出目錄
  - `STOP_HOTKEY`：自訂停止熱鍵（支援 ctrl+c）

## 開發/架構
- 主程式：`nikke_cjjc_automator/main.py`
- CLI 入口：`nikke_cjjc_automator/cli.py`
- 設定管理：`nikke_cjjc_automator/config.py`
- 控制器/模型/視圖分層，易於擴充與維護
- 圖片合併、熱鍵、模式策略皆為獨立模組

## CI/CD
- 已整合 GitHub Actions，自動打包 EXE 並上傳至 Release
- 推送 tag（如 v1.0.0）自動觸發

## 注意事項
- 僅支援 Windows 系統
- 執行時請確保有管理員權限
- 若遇到防毒軟體誤報，請加入白名單

---

如有問題或建議，歡迎於 GitHub Issue 回報。

