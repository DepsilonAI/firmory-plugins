<p align="center"><img src="plugins/firmory/assets/logo-blue.png" alt="Firmory" width="88" height="88"></p>

# Firmory

**在共享的數位資產上延續創作**

在 Codex 或 Claude Code 連接 Firmory 工作空間，尋找專案、選取文件，並追溯它使用的來源版本。

[English](README.md) · 繁體中文

[官網](https://firmory.ai/) · [安裝指南（英文）](docs/installation.md) · [版本紀錄（英文）](CHANGELOG.md) · [回報問題](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose)

**版本 1.0.1** · [MCP 端點](https://firmory.ai/mcp)。套件由 Firmory 自有的 marketplace 提供。

## Codex

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
codex -c 'mcp_servers.firmory_cloud.url="https://firmory.ai/mcp"' mcp login firmory_cloud --scopes user:org:read --oauth-client-registration cimd
```

在瀏覽器完成登入與授權，再開新對話執行 Firmory 設定，確認連接的團隊。桌面版安裝方式見[安裝指南](docs/installation.md)。

## Claude Code

```sh
claude plugin marketplace add DepsilonAI/firmory-plugins
claude plugin install firmory@firmory-plugins
```

開新對話，在 `/mcp` 選擇 Firmory 雲端連線並完成授權，再執行 `/firmory:setup`。需要有團隊存取權限的 Firmory 帳號，不需要安裝本機 Firmory CLI。

## 開始提問

- 顯示我的工作空間中可用的專案和檔案。
- 找出專案簡報，整理目標和關鍵決策。
- 開啟「Welcome.pdf」，整理重點。

Firmory 會傳回團隊有權查看的紀錄。若想追問某份文件或某個版本，可在同一個 Codex 或 Claude Code 對話繼續。

## 資料如何使用

客戶端會將本次工具呼叫需要的查詢文字、檔案或版本識別碼等參數傳送至 Firmory。可用工具與資料由服務端依帳號權限決定；查詢流程不會為了回答問題而修改檔案。不要把帳號憑證貼到聊天或 GitHub issue。詳見[隱私政策](https://firmory.ai/privacy)與[服務條款](https://firmory.ai/terms)。

## 協助與維護

兩個平台的 catalog 指向同一份插件資料夾；後端程式與客戶資料不在此倉庫。套件與文件問題可透過 [GitHub issues](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose) 回報；安全問題請使用 [SECURITY.md](SECURITY.md) 的私人聯絡方式。

維護規則見 [CONTRIBUTING.md](CONTRIBUTING.md) 與[發布指南](docs/maintaining.md)。目前尚未選定散布授權；公開倉庫不等於開源授權，正式送審前需完成此項。
