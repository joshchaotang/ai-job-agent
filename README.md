# 🎯 AI Job Search Agent

**版本**：v3.9.0 Olympus Edition
**畢業論文專案** - AI 智能求職助手

---

## ⚡ 一鍵部署到 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FYOUR_USERNAME%2Fai-job-agent&env=DEEPSEEK_API_KEY,EMAIL_USER,EMAIL_PASS,EMAIL_TO&envDescription=Required%20API%20Keys%20and%20Email%20Settings&envLink=https%3A%2F%2Fgithub.com%2FYOUR_USERNAME%2Fai-job-agent%2Fblob%2Fmain%2FDEPLOY_GUIDE.md&project-name=ai-job-agent&repository-name=ai-job-agent)

**部署步驟**：
1. 點擊上方「Deploy with Vercel」按鈕
2. 登入 Vercel（可用 GitHub 登入）
3. 輸入環境變數（API Keys）
4. 點擊「Deploy」
5. 等待 1-2 分鐘，完成！

> ⚠️ **重要**：請將 `YOUR_USERNAME` 替換為您的 GitHub 用戶名

---

## 🚀 快速開始

### 使用自動化腳本（推薦）

```bash
cd ~/Downloads/ai-job-agent-cloud
bash auto-deploy.sh
```

腳本會自動完成：
- ✅ Git 初始化
- ✅ 推送到 GitHub
- ✅ 安裝 Vercel CLI
- ✅ 登入 Vercel
- ✅ 部署到生產環境

### 手動部署

詳細步驟請參考：[DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md)

---

## ✨ 主要功能

### Phase 1：基礎功能
- 🔍 職位搜尋與智能篩選
- ⭐ 收藏系統
- 📊 求職追蹤器（Pipeline 管理）
- 🎤 AI 面試題生成
- 📈 技能雷達圖

### Step 1：履歷智能匹配
- 📄 履歷上傳（PDF/DOCX）
- 🤖 AI 履歷分析（DeepSeek）
- 🎯 AI 職位匹配（0-100 分）
- ⚡ 並行處理（高效能）
- ✅ 匹配技能高亮
- ❌ 缺少技能標記

### Step 2：自動爬蟲與推送
- 🕷️ JobSpy 爬蟲（Indeed 無限流）
- 🔄 4 來源聚合（Indeed, Remotive, Arbeitnow, Adzuna）
- 🚫 智能去重
- ⏰ GitHub Actions 定時任務（3 時段）
- 📧 Gmail HTML 郵件推送
- 🎯 每日自動匹配 + 排序

### Phase 3：進階功能

#### 3.1 客製化履歷生成
- 📝 jsPDF 整合
- 🎨 兩種專業模板（專業 + 現代）
- 🧠 智能優化（根據匹配度調整）
- ⬇️ 一鍵下載 PDF

#### 3.2 UI/UX 大升級
- 🌓 深色/淺色雙主題
- 💾 localStorage 主題持久化
- 🪟 Glassmorphism 毛玻璃效果
- 📐 Bento Grid 佈局（Apple 風格）
- ⭐ Featured 卡片（高分職位 2x2 網格）

#### 3.3 Telegram Bot 推送
- 💬 即時通知到 Telegram
- 📱 Markdown 格式化
- 🔥 Emoji 匹配度標記

#### 3.4 Slack Webhook 推送
- 👥 團隊協作頻道通知
- 🎛️ Block Kit 互動式按鈕
- 📊 職位卡片視覺化

#### 3.5-3.9 架構完成
- 📊 Chart.js（數據儀表板）
- 🌐 社群眾包系統（規劃）
- 🔗 LinkedIn OAuth（規劃）
- 🤖 Playwright 自動投遞（規劃）
- 🧩 Chrome 擴充套件（規劃）

---

## 🔑 環境變數設定

### 必須設定（4 個）

| 變數 | 說明 | 取得方式 |
|------|------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API Key | [platform.deepseek.com](https://platform.deepseek.com/api_keys) |
| `EMAIL_USER` | Gmail 帳號 | 您的 Gmail |
| `EMAIL_PASS` | Gmail App Password | [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |
| `EMAIL_TO` | 收件者信箱 | 接收通知的信箱 |

### 可選設定（4 個）

| 變數 | 說明 | 取得方式 |
|------|------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 詳見 [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md) |
| `SLACK_WEBHOOK_URL` | Slack Webhook URL | [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks) |
| `ADZUNA_APP_ID` + `KEY` | Adzuna API | [Adzuna API](https://developer.adzuna.com/) |

---

## 📊 技術架構

### 前端
- 原生 JavaScript（無框架）
- Chart.js 4.4.0
- jsPDF 2.5.1
- CSS Variables 雙主題
- Glassmorphism

### 後端
- Vercel Serverless Functions
- Python 3.10
- DeepSeek API
- JobSpy 1.1.70
- Requests

### 自動化
- GitHub Actions
- Gmail SMTP
- Telegram Bot API
- Slack Webhooks

### 儲存
- localStorage（無需資料庫）

---

## 📁 專案結構

```
ai-job-agent-cloud/
├── index.html                    # 主應用（1950+ 行）
├── api/                          # Serverless Functions
│   ├── analyze.py                # AI 職位分析
│   ├── analyze_resume.py         # 履歷分析
│   ├── parse_resume.py           # PDF/DOCX 解析
│   ├── match_jobs.py             # AI 匹配引擎
│   ├── scrape_jobs.py            # JobSpy 爬蟲
│   ├── aggregate_jobs.py         # 4 來源聚合
│   ├── telegram_push.py          # Telegram 推送
│   ├── slack_push.py             # Slack 推送
│   └── ...
├── scripts/
│   └── daily_scrape.py           # 每日爬蟲（355 行）
├── .github/workflows/            # GitHub Actions
│   ├── scrape-morning.yml
│   ├── scrape-noon.yml
│   └── scrape-evening.yml
├── vercel.json                   # Vercel 配置
├── requirements.txt              # Python 依賴
├── auto-deploy.sh                # 一鍵部署腳本
└── README.md                     # 本檔案
```

---

## 📖 完整文件

| 文件 | 說明 |
|------|------|
| [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md) | 詳細部署教學（最重要）|
| [CHECKPOINT_v3.9.0.md](./CHECKPOINT_v3.9.0.md) | 完整架構說明 |
| [PHASE3_DELIVERY_REPORT.md](./PHASE3_DELIVERY_REPORT.md) | Phase 3 詳細報告 |
| [FINAL_SUMMARY.md](./FINAL_SUMMARY.md) | 專案總覽 |

---

## 🧪 測試

部署後測試清單：

- [ ] 訪問網站，確認登入頁面正常
- [ ] 測試職位搜尋功能
- [ ] 上傳履歷（PDF/DOCX）
- [ ] 測試 AI 分析與匹配
- [ ] 生成客製化履歷 PDF
- [ ] 切換深色/淺色主題
- [ ] 手動觸發 GitHub Action
- [ ] 確認收到郵件/Telegram/Slack 通知

---

## 📊 統計數據

| 項目 | 數量 |
|------|------|
| 總程式碼 | ~5190 行 |
| 檔案數量 | 39 個 |
| 功能數量 | 30+ 項 |
| API 端點 | 9 個 |
| 開發時間 | ~24 小時 |

---

## 🎓 論文應用

本專案可用於以下研究主題：
- AI 輔助求職效率研究
- 多渠道推送對求職行為的影響
- 履歷客製化對面試機會的影響
- UI/UX 設計對使用者黏著度的影響

詳見：[FINAL_SUMMARY.md](./FINAL_SUMMARY.md)

---

## 📝 授權

本專案為畢業論文專案，版權所有。

---

## 👤 作者

**CK（大周天工作室）**
協作開發：Claude Sonnet 4.5

---

## 🙏 致謝

- DeepSeek（AI 分析引擎）
- Vercel（免費部署平台）
- JobSpy（職位爬蟲）
- Chart.js、jsPDF（前端 Library）

---

**需要協助？** 請參考 [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md) 或提交 Issue。
