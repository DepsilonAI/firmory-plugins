# Firmory for Claude Code

[Illustrated installation guide](https://firmory.ai/plugins#claude-code) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Claude Code with plugin support and sign in to your account.
2. Extract this ZIP. Keep the entire firmory-claude-code folder, including its hidden catalog files.
3. Open a terminal in the extracted firmory-claude-code folder. Run these commands one at a time.

```sh
claude plugin marketplace add .
claude plugin install firmory@firmory-plugins
```

4. Connect Firmory in your client's MCP settings. If needed, run this in the terminal.

```sh
claude mcp login plugin:firmory:firmory_cloud
```

5. In the browser, sign in to Firmory, select your team and allow access. Start a new chat and run Firmory setup to confirm the team. In Claude Code, run /firmory:setup.
6. Ask a first question.

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

## Install from GitHub instead

```sh
claude plugin marketplace add DepsilonAI/firmory-plugins
claude plugin install firmory@firmory-plugins
```

The plugin connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).

## 简体中文

下载并解压 ZIP，保留整个 firmory-claude-code 文件夹（包括隐藏文件）。在该文件夹中打开终端，依次执行上面的安装命令。在客户端的 MCP 设置中连接 Firmory，在浏览器登录、选择团队并授权。开启新对话，运行 Firmory 设置以确认团队，然后即可用中文提问。

## 繁體中文

下載並解壓縮 ZIP，保留整個 firmory-claude-code 資料夾（包括隱藏檔案）。在該資料夾中開啟終端機，依序執行上方的安裝指令。在客戶端的 MCP 設定中連接 Firmory，於瀏覽器登入、選擇團隊並授權。開啟新對話，執行 Firmory 設定以確認團隊，再開始提問。
