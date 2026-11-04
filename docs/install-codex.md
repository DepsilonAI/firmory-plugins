# Firmory for Codex

[Illustrated installation guide](https://firmory.ai/download#codex) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Codex with plugin support and sign in to your account.
2. Open **Customize → Plugins** in Codex. Drag `firmory-1.0.1-codex.zip` into that page and follow the installation prompts. Keep the ZIP compressed; no extraction is needed.
3. Connect Firmory in your client's MCP settings. If needed, run this in the terminal.

```sh
codex mcp login firmory_cloud --scopes user:org:read
```

4. In the browser, sign in to Firmory, select your team and allow access. Start a new chat and run Firmory setup to confirm the team.
5. Ask a first question.

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

## Install from GitHub instead

For Codex CLI installation, run these commands in any folder. The CLI installs from GitHub rather than from this ZIP.

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
```

The plugin connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).

## 简体中文

在 Codex 中打开 Customize → Plugins，将 firmory-1.0.1-codex.zip 拖入页面，按照提示完成安装，无需解压。使用 Codex CLI 时，在任意文件夹执行上面的 GitHub 安装命令。在客户端的 MCP 设置中连接 Firmory，在浏览器登录、选择团队并授权。开启新对话，运行 Firmory 设置以确认团队，然后即可用中文提问。

## 繁體中文

在 Codex 中開啟 Customize → Plugins，將 firmory-1.0.1-codex.zip 拖入頁面，依照提示完成安裝，無需解壓縮。使用 Codex CLI 時，在任意資料夾執行上方的 GitHub 安裝指令。在客戶端的 MCP 設定中連接 Firmory，於瀏覽器登入、選擇團隊並授權。開啟新對話，執行 Firmory 設定以確認團隊，再開始提問。
