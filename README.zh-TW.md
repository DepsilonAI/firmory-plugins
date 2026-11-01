<p align="center"><img src="plugins/ask-firmory/assets/logo-blue.png" alt="Firmory" width="88" height="88"></p>

# Firmory

**接續團隊的 AI 成果。**

在 Codex 或 Claude Code 裡，查詢團隊檔案、版本與來源關係。Firmory 預計透過已連接的工作空間回答，並讓你在網頁版 Ask Firmory 接著同一段對話。

[English](README.md) · 繁體中文

[官網](https://firmory.ai/) · [安裝指南（英文）](docs/installation.md) · [版本紀錄（英文）](CHANGELOG.md) · [回報問題](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose)

> **設計預覽版 — 0.2.0-alpha.1。** 目前可安裝並檢視插件套件；雲端 MCP、OAuth 登入及網頁對話接續尚未開放，安裝後還不能查詢工作空間。這是 Firmory 自行管理的 marketplace，尚未通過 OpenAI 或 Anthropic 官方目錄審核。

## 預計可以問什麼

以下為預期使用情境，尚非已連通雲端服務的示範結果：

- 我們團隊這週更新了哪些文件？
- 幫我查一份報告是根據哪一版需求寫的。
- 我準備更新一份規格。哪些文件是根據它目前這一版做的？

## 安裝預覽版

需要支援插件 marketplace 的 Codex 或 Claude Code。本套件不需要你啟動本機 MCP server，也不需要額外安裝 Node.js 或 Python。雲端功能開放後，需使用有團隊存取權限的 Firmory 帳號。

### Codex

在終端機執行：

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add ask-firmory@firmory-plugins
```

安裝後開啟新的對話。顯示名稱為 **Firmory**，安裝識別名稱維持 `ask-firmory`。

### Claude Code

在終端機執行：

```sh
claude plugin marketplace add DepsilonAI/firmory-plugins
claude plugin install ask-firmory@firmory-plugins
```

安裝後開啟新的 session。雲端功能發布後，在 Claude Code 輸入 `/ask-firmory:setup` 連接工作空間。

桌面安裝、驗證、更新、移除與錯誤處理請見[安裝指南](docs/installation.md)。

## 首次使用流程

預計流程為：安裝 Firmory → 執行設定並登入 → 確認團隊 → 提問並查看版本參考 → 開啟 Ask Firmory 網頁接續同一段私人對話。

目前只有套件安裝可用，後續連線與對話流程仍待完成。設定流程須成功查得已授權團隊後，才會回報連線成功。

## 資料如何使用

預計會將問題與相關檔案、時區或對話上下文傳送至 Firmory。Firmory Agent 讀取你有權存取的工作空間紀錄，並儲存私人對話。提問不會修改工作空間檔案，但會產生對話資料。

套件包含兩個 skills、品牌圖片與遠端 MCP 設定，沒有本機伺服器執行檔、安裝腳本或生命週期 hooks。登入憑證只應輸入於客戶端連線流程，不要貼到聊天或 GitHub issue。詳見[隱私政策](https://firmory.ai/privacy)與[服務條款](https://firmory.ai/terms)。

## 協助與維護

兩個平台的 catalog 指向同一份插件資料夾；後端程式與客戶資料不在此倉庫。套件與文件問題可透過 [GitHub issues](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose) 回報；安全問題請使用 [SECURITY.md](SECURITY.md) 的私人聯絡方式。

維護規則見 [CONTRIBUTING.md](CONTRIBUTING.md) 與[發布指南](docs/maintaining.md)。目前尚未選定散布授權；公開倉庫不等於開源授權，正式送審前需完成此項。
