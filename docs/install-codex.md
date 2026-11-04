# Firmory for Codex

[Illustrated installation guide](https://firmory.ai/plugins#codex) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Codex with plugin support and sign in to your account.
2. Extract this ZIP. Keep the entire firmory-codex folder, including its hidden catalog files.
3. Open a terminal in the extracted firmory-codex folder. Run these commands one at a time.

```sh
codex plugin marketplace add .
codex plugin add firmory@firmory-plugins
```

4. Connect Firmory in your client's MCP settings. If needed, run this in the terminal.

```sh
codex mcp login firmory_cloud --scopes user:org:read
```

5. In the browser, sign in to Firmory, select your team and allow access. Start a new chat and run Firmory setup to confirm the team. In Claude Code, run /firmory:setup.
6. Ask a first question.

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

The PDF question needs a Welcome.pdf file in your connected workspace. No example workspace files are included in the plugin.

## Install from GitHub instead

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
```

The plugin connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).

## 简体中文

下载并解压 ZIP，保留整个 firmory-codex 文件夹（包括隐藏文件）。在该文件夹中打开终端，依次执行上面的安装命令。在客户端的 MCP 设置中连接 Firmory，在浏览器登录、选择团队并授权。开启新对话，运行 Firmory 设置以确认团队，然后即可用中文提问。

Welcome.pdf 需事先放入连接的工作空间，插件不附带该文件。

## 繁體中文

下載並解壓縮 ZIP，保留整個 firmory-codex 資料夾（包括隱藏檔案）。在該資料夾中開啟終端機，依序執行上方的安裝指令。在客戶端的 MCP 設定中連接 Firmory，於瀏覽器登入、選擇團隊並授權。開啟新對話，執行 Firmory 設定以確認團隊，再開始提問。
