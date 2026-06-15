# GitHub 部署指令

## 目标
把 C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\ 目录推送到 GitHub，
开启 GitHub Pages，使前端可以通过 raw.githubusercontent.com 读取 JSON 数据。

## 前置条件
- 确认你的 GitHub 账号信息（用户名、邮箱、PAT 或 gh 登录状态）
- 确认 git 已安装（已可用）

## 步骤

### 1. 初始化本地仓库

`powershell
cd C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs
git init
git add .gitignore index.html manifest.json sw.js
git add data/analysis.json data/config.json data/news.json
git add app背景图.png icon-192.png icon-512.png 店主微信.jpg
git commit -m "init: V3.3.3 World Cup 2026 app"
`

### 2. 在 GitHub 上创建仓库

用 gh CLI 或手动浏览器打开 github.com 创建：
- 仓库名：worldcup2026（或你想要的名称）
- 设为 **public**（raw 链接需要公开仓库才能访问）
- 不要勾选 README/.gitignore/LICENSE

### 3. 关联远程仓库并推送

`powershell
git remote add origin https://github.com/你的用户名/worldcup2026.git
git branch -M main
git push -u origin main
`

### 4. 开启 GitHub Pages

`powershell
gh api repos/你的用户名/worldcup2026/pages -X POST -f source.branch=main -f source.path=/
`

或者手动：浏览器打开 GitHub 仓库 → Settings → Pages → 选 main 分支，根目录 / → Save

### 5. 验证

浏览器打开这个网址，确认能看到 JSON 内容：
`
https://raw.githubusercontent.com/你的用户名/worldcup2026/main/data/analysis.json
`

### 6. 数据更新流程

以后每次更新了 data/ 下的 JSON 文件后，执行：

`powershell
cd C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs
git add data/analysis.json data/config.json data/news.json
git commit -m "update: match data YYYY-MM-DD HH:mm"
git push
`

GitHub 1-2 分钟后同步，前端读取的就是最新数据。
