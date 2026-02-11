# AI Job Agent - 部署與測試指南

**版本**：v3.9.0 Olympus Edition
**建立日期**：2026-02-11

---

## 🚀 快速開始（5 分鐘部署）

### 前置需求
- ✅ GitHub 帳號
- ✅ Vercel 帳號（免費）
- ✅ DeepSeek API Key（免費額度）
- ⚠️ Mac 終端（需要您操作）

---

## 一、Git 初始化（在 Mac 終端執行）

### 選項 A：使用打包好的 Git（推薦）

```bash
cd ~/Downloads/ai-job-agent-cloud

# 解壓縮 git 資料夾（v3.9.0）
tar -xzf git-v3.9.0.tar.gz

# 驗證 git 歷史
git log --oneline -3

# 應該看到：
# f8c51cf v3.9.0 Olympus: Phase 3 全部完成
# 6cb6245 v3.2.0 Hermes Pro: 履歷匹配 + 自動爬蟲推送
```

### 選項 B：重新初始化 Git

```bash
cd ~/Downloads/ai-job-agent-cloud

# 刪除現有 .git（如果有問題）
rm -rf .git

# 重新初始化
git init
git config user.name "CK (大周天工作室)"
git config user.email "a122233456@gmail.com"

# 添加所有檔案
git add .

# 提交
git commit -m "v3.9.0 Olympus Edition - Initial Commit"
```

---

## 二、GitHub 推送

### 1. 在 GitHub 建立新 Repository

前往：https://github.com/new

- **Repository name**：`ai-job-agent`
- **Privacy**：Private（推薦）
- **不要**勾選任何初始化選項（README, .gitignore, License）

### 2. 推送到 GitHub

```bash
cd ~/Downloads/ai-job-agent-cloud

# 連接遠端 repository（替換成您的 GitHub username）
git remote add origin https://github.com/YOUR_USERNAME/ai-job-agent.git

# 推送
git branch -M main
git push -u origin main
```

### 3. 設定 GitHub Secrets

前往：https://github.com/YOUR_USERNAME/ai-job-agent/settings/secrets/actions

點擊「New repository secret」，逐一新增：

| Name | Value | 說明 |
|------|-------|------|
| `DEEPSEEK_API_KEY` | sk-xxxxx | DeepSeek API Key |
| `EMAIL_USER` | your@gmail.com | Gmail 帳號 |
| `EMAIL_PASS` | xxxxxxxxxxxx | Gmail App Password |
| `EMAIL_TO` | recipient@gmail.com | 收件者 |
| `TELEGRAM_BOT_TOKEN` | 123456:ABC... | Telegram Bot Token（可選）|
| `TELEGRAM_CHAT_ID` | 123456789 | Telegram Chat ID（可選）|
| `SLACK_WEBHOOK_URL` | https://hooks... | Slack Webhook URL（可選）|

---

## 三、Vercel 部署

### 1. 安裝 Vercel CLI

```bash
npm install -g vercel
```

### 2. 登入 Vercel

```bash
vercel login
```

### 3. 部署專案

```bash
cd ~/Downloads/ai-job-agent-cloud

# 部署到生產環境
vercel --prod
```

執行過程中會詢問：
- **Set up and deploy?** → Y
- **Which scope?** → 選擇您的帳號
- **Link to existing project?** → N
- **Project name?** → ai-job-agent（或自訂）
- **Directory?** → .（當前目錄）
- **Override settings?** → N

部署完成後會顯示 URL，例如：
```
https://ai-job-agent-abc123.vercel.app
```

### 4. 設定 Vercel 環境變數

**方法 A：透過 Vercel Dashboard（推薦）**

1. 前往：https://vercel.com/dashboard
2. 選擇您的專案
3. Settings → Environment Variables
4. 逐一新增所有環境變數（同 GitHub Secrets）

**方法 B：透過 CLI**

```bash
vercel env add DEEPSEEK_API_KEY production
# 輸入值：sk-xxxxx

vercel env add EMAIL_USER production
# 輸入值：your@gmail.com

# ... 重複所有變數
```

### 5. 重新部署（套用環境變數）

```bash
vercel --prod
```

---

## 四、驗證部署

### 1. 檢查網站

訪問您的 Vercel URL，應該看到：
- ✅ 登入頁面正常顯示
- ✅ 愛馬仕橘色主題
- ✅ 深色模式

### 2. 測試功能

**A. 基本搜尋**
1. 輸入任意 API Key 登入（或設定正確的）
2. 搜尋職位（例：software engineer）
3. 確認職位卡片正常顯示

**B. 履歷上傳（Step 1）**
1. 切換到「履歷」Tab
2. 上傳 PDF 或 DOCX
3. 確認 AI 分析結果顯示
4. 點擊「生成客製化履歷」
5. 確認 PDF 下載成功

**C. 主題切換（Phase 3.2）**
1. 點擊右上角 🌙 按鈕
2. 確認切換到淺色模式
3. 重新整理頁面，確認主題持久化

### 3. 測試 GitHub Actions（自動爬蟲）

**A. 手動觸發**
1. 前往：https://github.com/YOUR_USERNAME/ai-job-agent/actions
2. 選擇「Scrape Morning」
3. 點擊「Run workflow」
4. 等待執行完成（約 1-2 分鐘）

**B. 檢查通知**
- Gmail：收到 HTML 格式的職位報告
- Telegram（如已設定）：收到 Markdown 訊息
- Slack（如已設定）：收到 Block Kit 卡片

---

## 五、Telegram Bot 設定（可選）

### 1. 建立 Bot

1. 在 Telegram 搜尋 `@BotFather`
2. 發送 `/newbot`
3. 按指示設定 Bot 名稱和 username
4. 複製 Bot Token（例：`123456789:ABCdefGHI...`）
5. 設定為 GitHub Secret：`TELEGRAM_BOT_TOKEN`

### 2. 取得 Chat ID

1. 在 Telegram 搜尋您剛建立的 Bot
2. 發送任意訊息給它（例：`/start`）
3. 在瀏覽器訪問：
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```
   替換 `<BOT_TOKEN>` 為您的 Bot Token

4. 在返回的 JSON 中找到：
   ```json
   "chat": {
     "id": 123456789,
     ...
   }
   ```

5. 複製 ID（例：`123456789`）
6. 設定為 GitHub Secret：`TELEGRAM_CHAT_ID`

### 3. 測試推送

觸發 GitHub Action（見上方「測試 GitHub Actions」），確認收到 Telegram 訊息。

---

## 六、Slack Webhook 設定（可選）

### 1. 建立 Incoming Webhook

1. 前往：https://api.slack.com/messaging/webhooks
2. 點擊「Create your Slack app」
3. 選擇「From scratch」
4. 輸入 App Name 和 Workspace
5. 在左側選單選擇「Incoming Webhooks」
6. 開啟「Activate Incoming Webhooks」
7. 點擊「Add New Webhook to Workspace」
8. 選擇要發布的頻道
9. 複製 Webhook URL（例：`https://hooks.slack.com/services/...`）
10. 設定為 GitHub Secret：`SLACK_WEBHOOK_URL`

### 2. 測試推送

觸發 GitHub Action，確認 Slack 頻道收到職位卡片。

---

## 七、Gmail App Password 設定

### 1. 開啟兩步驟驗證

1. 前往：https://myaccount.google.com/security
2. 「登入 Google」→「兩步驟驗證」
3. 按指示開啟

### 2. 產生 App Password

1. 前往：https://myaccount.google.com/apppasswords
2. 選擇「郵件」和「其他（自訂名稱）」
3. 輸入名稱：`AI Job Agent`
4. 點擊「產生」
5. 複製 16 位數密碼（例：`abcd efgh ijkl mnop`，移除空格）
6. 設定為 GitHub Secret：`EMAIL_PASS`

---

## 八、DeepSeek API Key 取得

### 1. 註冊 DeepSeek

1. 前往：https://platform.deepseek.com/
2. 註冊帳號（可用 Google 登入）
3. 新用戶有免費額度

### 2. 產生 API Key

1. 前往：https://platform.deepseek.com/api_keys
2. 點擊「Create API Key」
3. 輸入名稱：`AI Job Agent`
4. 複製 API Key（以 `sk-` 開頭）
5. 設定為 GitHub Secret 和 Vercel 環境變數：`DEEPSEEK_API_KEY`

---

## 九、常見問題排除

### Q1：部署後網站空白或報錯
**A**：檢查 Vercel Dashboard → Deployments → 最新部署 → Logs
查看錯誤訊息，通常是環境變數未設定

### Q2：AI 分析功能報錯
**A**：
1. 確認 `DEEPSEEK_API_KEY` 已正確設定
2. 檢查 API 額度是否用盡
3. 前往 DeepSeek Dashboard 查看使用量

### Q3：GitHub Actions 執行失敗
**A**：
1. 檢查 Secrets 是否都已設定
2. 查看 Actions 的執行日誌
3. 確認 `scripts/daily_scrape.py` 中的 `SEARCH_KEYWORDS` 符合需求

### Q4：收不到郵件通知
**A**：
1. 確認 Gmail App Password 正確
2. 檢查垃圾郵件匣
3. 查看 GitHub Actions 日誌中的錯誤訊息

### Q5：Telegram/Slack 收不到訊息
**A**：
1. 確認 Token/Webhook URL 正確
2. Telegram：確認已發送訊息給 Bot
3. Slack：確認 Webhook 已連接正確頻道

---

## 十、進階自訂

### 修改搜尋關鍵字

編輯 `scripts/daily_scrape.py`（line 18-19）：

```python
SEARCH_KEYWORDS = "software engineer python"  # 改成您的關鍵字
SEARCH_LOCATION = "Remote"  # 改成您的地點
```

提交變更並推送到 GitHub：

```bash
git add scripts/daily_scrape.py
git commit -m "Update search keywords"
git push
```

### 修改爬蟲時間

編輯 `.github/workflows/scrape-morning.yml`（line 6）：

```yaml
- cron: '0 8 * * *'  # 改成您要的時間（UTC）
```

**時區對照**：
- `0 8 * * *` = 每天 8:00 UTC（台灣下午 4:00）
- `0 16 * * *` = 每天 16:00 UTC（台灣凌晨 0:00）
- `0 0 * * *` = 每天 0:00 UTC（台灣早上 8:00）

---

## 十一、備份與還原

### 備份

```bash
cd ~/Downloads
tar -czf ai-job-agent-backup-$(date +%Y%m%d).tar.gz ai-job-agent-cloud
```

### 還原

```bash
cd ~/Downloads
tar -xzf ai-job-agent-backup-YYYYMMDD.tar.gz
cd ai-job-agent-cloud
```

---

## 十二、下一步

### 立即可用功能
- [x] 職位搜尋與收藏
- [x] 履歷上傳與 AI 匹配
- [x] 客製化履歷 PDF 生成
- [x] 深色/淺色主題切換
- [x] 自動爬蟲 + 多渠道推送

### Phase 4 開發建議
- [ ] 完整實作 Chart.js 圖表
- [ ] 社群眾包系統（Supabase）
- [ ] LinkedIn OAuth 整合
- [ ] Playwright 自動投遞
- [ ] Chrome 擴充套件

---

**部署狀態檢查清單**：

- [ ] Git 推送到 GitHub
- [ ] GitHub Secrets 全部設定
- [ ] Vercel 部署成功
- [ ] Vercel 環境變數全部設定
- [ ] 網站可正常訪問
- [ ] 履歷上傳功能測試通過
- [ ] AI 分析功能測試通過
- [ ] 主題切換功能測試通過
- [ ] GitHub Actions 手動觸發成功
- [ ] 郵件/Telegram/Slack 通知收到

**完成上述清單後，您的 AI Job Agent 就完全上線了！** 🎉

---

需要協助？參考：
- `CHECKPOINT_v3.9.0.md`：完整架構說明
- `PHASE3_DELIVERY_REPORT.md`：Phase 3 詳細報告
- GitHub Issues：在 repository 提交問題

---

大周天工作室 ☯ CK 謹製
Claude Sonnet 4.5 協作開發
