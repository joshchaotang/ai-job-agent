# 🚀 Vercel 部署完整指南
**AI Job Agent v4.0.0 Aurora Edition**

> 📌 **目標**：5 分鐘完成部署，零 Terminal 操作
> 💰 **成本**：完全免費（Vercel 免費額度 + DeepSeek 約 NT$5-20/月）

───────────────────────────────────────────────────────

## 🎯 部署流程總覽（3 大步驟）

```
步驟 1          步驟 2              步驟 3
GitHub    →   Vercel         →    環境變數
(1 分鐘)      (2 分鐘)            (2 分鐘)
```

完成後 → 🎉 打開網址，立即使用！

───────────────────────────────────────────────────────

## 📋 準備清單

在開始之前，請確認您有：

- [ ] GitHub 帳號（[免費註冊](https://github.com/signup)）
- [ ] Vercel 帳號（[免費註冊](https://vercel.com/signup)）
- [ ] DeepSeek API Key（[免費申請](https://platform.deepseek.com/api_keys)）
- [ ] Email 帳號（Gmail 或其他 SMTP）

**選填**（推送通知用）：
- [ ] Telegram Bot Token（[建立教學](#telegram-bot-設定)）
- [ ] Slack Webhook URL（[建立教學](#slack-webhook-設定)）

───────────────────────────────────────────────────────

## 步驟 1：上傳到 GitHub（1 分鐘）

### 方式 A：使用 GitHub Desktop（推薦新手）

1. **下載 GitHub Desktop**
   前往 [desktop.github.com](https://desktop.github.com/) 下載並安裝

2. **建立新 Repository**
   - 開啟 GitHub Desktop
   - 點擊：`File` → `New Repository...`
   - Repository Name：`ai-job-agent`
   - Local Path：選擇專案資料夾
   - 點擊 `Create Repository`

3. **Commit 並 Push**
   - 在 GitHub Desktop 中，勾選所有檔案
   - Commit Message：`Initial commit - v4.0.0`
   - 點擊 `Commit to main`
   - 點擊 `Publish repository`
   - 取消勾選 `Keep this code private`（如果要公開）
   - 點擊 `Publish Repository`

✅ **完成！** GitHub 上已有您的專案

### 方式 B：使用 Web 介面（最簡單）

1. **前往 GitHub**
   登入 [github.com](https://github.com)

2. **建立新 Repository**
   - 點擊右上角 `+` → `New repository`
   - Repository name：`ai-job-agent`
   - Description：`AI Job Search Agent - 智能求職助手`
   - 選擇 `Public` 或 `Private`
   - 點擊 `Create repository`

3. **上傳檔案**
   - 點擊 `uploading an existing file`
   - 將專案資料夾中的所有檔案拖曳進去
   - Commit message：`Initial commit - v4.0.0`
   - 點擊 `Commit changes`

✅ **完成！** 複製您的 Repository URL（例：`https://github.com/your-username/ai-job-agent`）

───────────────────────────────────────────────────────

## 步驟 2：部署到 Vercel（2 分鐘）

### 1. **登入 Vercel**

前往 [vercel.com](https://vercel.com)，點擊 `Sign Up`

建議選擇：**Continue with GitHub**（最方便）

### 2. **匯入專案**

登入後，點擊：`Add New...` → `Project`

您會看到您的 GitHub Repositories 列表

找到 `ai-job-agent`，點擊 `Import`

### 3. **設定專案**

**Configure Project** 頁面：

```
Project Name: ai-job-agent
Framework Preset: Other（保持預設）
Root Directory: ./（保持預設）
Build Command: （留空）
Output Directory: （留空）
```

**重要**：點擊 `Environment Variables` 下拉展開（先不填，等第 3 步）

點擊 `Deploy`

### 4. **等待部署**

部署進度：`Building...` → `Deploying...` → `Ready!`

約 1-2 分鐘完成

### 5. **取得網址**

部署完成後，您會看到：

```
🎉 Congratulations!
Your project is deployed!

https://ai-job-agent-abc123.vercel.app
```

✅ **完成！** 複製這個網址

**⚠️ 重要**：此時網站還無法使用，需要設定環境變數（步驟 3）

───────────────────────────────────────────────────────

## 步驟 3：設定環境變數（2 分鐘）

### 進入專案設定

1. 在 Vercel Dashboard，點擊您的專案 `ai-job-agent`
2. 點擊頂部 `Settings` 標籤
3. 左側選單點擊 `Environment Variables`

### 必填變數（4 個）

#### 1. `DEEPSEEK_API_KEY`（AI 分析）

**取得方式**：
1. 前往 [platform.deepseek.com](https://platform.deepseek.com/api_keys)
2. 註冊/登入帳號
3. 點擊 `Create API Key`
4. 複製產生的 Key（格式：`sk-...`）

**填入 Vercel**：
```
Name: DEEPSEEK_API_KEY
Value: sk-1234567890abcdef...（貼上您的 Key）
Environment: Production, Preview, Development（全選）
```

點擊 `Save`

#### 2. `EMAIL_USER`（Email 推送）

**使用 Gmail 為例**：

```
Name: EMAIL_USER
Value: your-email@gmail.com
Environment: Production, Preview, Development（全選）
```

點擊 `Save`

#### 3. `EMAIL_PASS`（Email 密碼）

**⚠️ 重要**：不是您的 Gmail 密碼，是「應用程式密碼」

**取得 Gmail 應用程式密碼**：
1. 前往 [Google 帳戶安全性](https://myaccount.google.com/security)
2. 啟用「兩步驟驗證」（如未啟用）
3. 搜尋「應用程式密碼」
4. 選擇應用程式：`Mail`
5. 選擇裝置：`Other (Custom name)` → 輸入 `AI Job Agent`
6. 點擊 `Generate`
7. 複製 16 位數密碼（格式：`abcd efgh ijkl mnop`）

**填入 Vercel**：
```
Name: EMAIL_PASS
Value: abcdefghijklmnop（移除空格）
Environment: Production, Preview, Development（全選）
```

點擊 `Save`

#### 4. `EMAIL_TO`（接收職缺的 Email）

```
Name: EMAIL_TO
Value: your-email@gmail.com（您要接收通知的 Email）
Environment: Production, Preview, Development（全選）
```

點擊 `Save`

### 選填變數（推送通知）

#### 5. `TELEGRAM_BOT_TOKEN`（Telegram 推送）

**取得方式**：[見下方 Telegram 設定教學](#telegram-bot-設定)

```
Name: TELEGRAM_BOT_TOKEN
Value: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
Environment: Production, Preview, Development（全選）
```

#### 6. `TELEGRAM_CHAT_ID`（您的 Telegram ID）

**取得方式**：[見下方 Telegram 設定教學](#telegram-bot-設定)

```
Name: TELEGRAM_CHAT_ID
Value: 123456789
Environment: Production, Preview, Development（全選）
```

#### 7. `SLACK_WEBHOOK_URL`（Slack 推送）

**取得方式**：[見下方 Slack 設定教學](#slack-webhook-設定)

```
Name: SLACK_WEBHOOK_URL
Value: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
Environment: Production, Preview, Development（全選）
```

### 重新部署

**重要**：設定完環境變數後，需要重新部署

1. 點擊頂部 `Deployments` 標籤
2. 找到最新的部署
3. 點擊右側 `...` → `Redeploy`
4. 勾選 `Use existing Build Cache`
5. 點擊 `Redeploy`

等待約 30 秒，部署完成！

✅ **完成！** 現在打開您的網址，開始使用

───────────────────────────────────────────────────────

## 🔔 推送通知設定（選填）

### Telegram Bot 設定

#### 步驟 1：建立 Bot

1. 在 Telegram 搜尋 `@BotFather`
2. 開啟對話，輸入 `/newbot`
3. 輸入 Bot 名稱：`AI Job Agent`
4. 輸入 Bot Username：`your_name_job_bot`（必須以 `_bot` 或 `Bot` 結尾）
5. 複製 Bot Token（格式：`1234567890:ABCdefGHI...`）

#### 步驟 2：取得 Chat ID

1. 在 Telegram 搜尋您剛建立的 Bot（`@your_name_job_bot`）
2. 點擊 `Start` 開始對話
3. 隨便傳一則訊息（例如：`/start`）
4. 開啟瀏覽器，前往：
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   （將 `<YOUR_BOT_TOKEN>` 替換為您的 Bot Token）
5. 找到 `"chat":{"id":123456789}` 中的數字
6. 複製這個數字（您的 Chat ID）

#### 填入 Vercel

將 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 填入環境變數（見上方步驟 3）

### Slack Webhook 設定

#### 步驟 1：建立 Webhook

1. 前往 [api.slack.com/apps](https://api.slack.com/apps)
2. 點擊 `Create New App` → `From scratch`
3. App Name：`AI Job Agent`
4. 選擇您的 Workspace
5. 點擊 `Create App`

#### 步驟 2：啟用 Incoming Webhooks

1. 左側選單點擊 `Incoming Webhooks`
2. 切換 `Activate Incoming Webhooks` 為 **On**
3. 點擊底部 `Add New Webhook to Workspace`
4. 選擇要接收訊息的頻道
5. 點擊 `Allow`

#### 步驟 3：複製 Webhook URL

您會看到 Webhook URL：
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
```

複製這個 URL

#### 填入 Vercel

將 `SLACK_WEBHOOK_URL` 填入環境變數（見上方步驟 3）

───────────────────────────────────────────────────────

## ✅ 驗證部署成功

### 1. 開啟網站

前往您的 Vercel 網址：`https://ai-job-agent-abc123.vercel.app`

### 2. 檢查歡迎畫面

**預期結果**：
- 🎉 看到「歡迎使用 AI Job Agent」歡迎畫面
- 有「開始 5 分鐘導覽」按鈕
- 右下角有 💡 幫助按鈕

### 3. 測試功能

**步驟 1**：上傳履歷
→ 選擇一個 PDF 或 Word 檔案
→ 應該成功上傳並解析

**步驟 2**：搜尋職缺
→ 輸入關鍵字（例：`python developer`）
→ 應該返回職缺列表

**步驟 3**：AI 分析
→ 點擊「分析全部」
→ 應該開始分析並顯示評分

如果以上都正常 → ✅ **部署成功！**

### 4. 測試推送通知（如有設定）

**Email 測試**：
- 分析完成後，檢查您的 Email
- 應該收到職缺推送郵件

**Telegram 測試**：
- 檢查您的 Telegram Bot 對話
- 應該收到職缺訊息

───────────────────────────────────────────────────────

## ❓ 常見問題

### Q1：部署後網站顯示 500 錯誤

**原因**：環境變數設定錯誤

**解決**：
1. 檢查 Vercel → Settings → Environment Variables
2. 確認 `DEEPSEEK_API_KEY` 格式正確（以 `sk-` 開頭）
3. 確認 `EMAIL_PASS` 是應用程式密碼，不是登入密碼
4. 重新部署：Deployments → Redeploy

### Q2：AI 分析沒反應

**原因**：DeepSeek API Key 無效或餘額不足

**解決**：
1. 前往 [platform.deepseek.com](https://platform.deepseek.com/usage)
2. 檢查餘額
3. 如需充值，最低充值 $5 美金（約 NT$150）
4. 重新生成 API Key 並更新到 Vercel

### Q3：沒收到 Email 推送

**原因**：Gmail 應用程式密碼設定錯誤

**解決**：
1. 確認已啟用「兩步驟驗證」
2. 重新產生應用程式密碼
3. 更新 `EMAIL_PASS` 環境變數（移除空格）
4. 重新部署

### Q4：想要自訂網域

**設定自訂網域**：
1. Vercel Project → Settings → Domains
2. 輸入您的網域（例：`jobs.yourdomain.com`）
3. 依照指示設定 DNS（CNAME 記錄）
4. 等待 DNS 生效（約 5-60 分鐘）

### Q5：如何更新程式碼？

**方式 A：GitHub Desktop**
1. 修改本地檔案
2. GitHub Desktop → Commit → Push
3. Vercel 自動部署

**方式 B：GitHub Web**
1. GitHub.com → 您的 Repository
2. 點擊檔案 → 編輯
3. Commit changes
4. Vercel 自動部署

───────────────────────────────────────────────────────

## 📊 成本估算（真實數據）

### Vercel（免費）

```
免費額度：100 GB-Hours/月
實際使用：~5 GB-Hours/月（個人使用）
結論：完全在免費額度內
```

### DeepSeek API

```
定價：$0.14/1M tokens
使用情境：每天分析 50 個職缺 × 30 天 = 1500 職缺/月
每個職缺：~2000 tokens
總消耗：3M tokens/月
費用：$0.42/月 ≈ NT$13/月
```

### Email / Telegram / Slack

```
Gmail：免費
Telegram：免費
Slack：免費（Incoming Webhooks）
```

### 總成本

```
最低：NT$0/月（只用免費 DeepSeek 額度）
一般：NT$5-20/月（輕度使用）
重度：NT$50/月（每天分析 200+ 職缺）
```

**對比競品**：
- LazyApply：NT$3,000/月
- LinkedIn Premium：NT$3,600/月
- **本專案：NT$5-20/月**（省 99%）

───────────────────────────────────────────────────────

## 🎓 下一步學習

**進階功能**：
- ⏰ [設定自動爬蟲](./DEPLOY_GUIDE.md#github-actions-設定)（GitHub Actions）
- 📊 [匯出分析報告](./README.md#匯出功能)（Excel / PDF）
- 🎨 [自訂主題](./README.md#主題設定)（深色 / 淺色）

**社群支援**：
- 💬 [GitHub Discussions](https://github.com/your-username/ai-job-agent/discussions)
- 🐛 [回報問題](https://github.com/your-username/ai-job-agent/issues)
- ⭐ [Star 本專案](https://github.com/your-username/ai-job-agent)

───────────────────────────────────────────────────────

**製作團隊**：大周天工作室 ☯
**版本**：v4.0.0 Aurora Edition
**最後更新**：2026-02-11

祝您求職順利！🎉
