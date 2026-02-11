# 🤖 AI Job Search Agent

**v4.0.0 Aurora Edition - 滿級分 UX 新手引導**

> 🎯 智能求職助手 - AI 自動匹配最適合的職缺
> 💰 成本：**NT$5-20/月**（比競品便宜 99%）
> ⏱️ 設定時間：**5 分鐘**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/ai-job-agent&env=DEEPSEEK_API_KEY,EMAIL_USER,EMAIL_PASS,EMAIL_TO&envDescription=AI%20Job%20Agent%20%E7%92%B0%E5%A2%83%E8%AE%8A%E6%95%B8%E8%A8%AD%E5%AE%9A&envLink=https://github.com/your-username/ai-job-agent/blob/main/VERCEL_SETUP_GUIDE.md)

───────────────────────────────────────────────────────

## ✨ v4.0.0 新功能

### 🎉 滿級分 UX 新手引導系統

**全新 7 步驟互動式教學**：
1. 📤 上傳履歷 → 2. 🔑 設定 API → 3. 🔍 搜尋職缺 → 4. 🤖 AI 分析 → 5. 📊 查看結果 → 6. 🔔 設定推送 → 7. 🎉 完成！

**UX 特色**：
- ✨ Glassmorphism 毛玻璃引導框
- 🎯 智能 Spotlight 高亮目標元素
- 📊 進度條即時顯示完成度
- 💡 右下角永久幫助按鈕
- 📱 完美支援手機與桌面
- ⚡ 流暢動畫與過渡效果

**像玩遊戲一樣簡單！** 🎮

[查看完整 CHANGELOG →](./CHANGELOG_v4.0.0.md)

───────────────────────────────────────────────────────

## 🚀 快速開始（3 種方式）

### 方式 1：一鍵部署（最簡單）⭐

點擊上方 **Deploy with Vercel** 按鈕：

1. 登入 GitHub（或 Vercel）
2. 授權 Vercel 存取
3. 填入環境變數（見下方）
4. 點擊 Deploy
5. 等待 1 分鐘
6. 完成！🎉

**環境變數設定** → [完整圖文教學](./VERCEL_SETUP_GUIDE.md)

### 方式 2：本地使用（開發者）

```bash
# 1. Clone 專案
git clone https://github.com/your-username/ai-job-agent.git
cd ai-job-agent

# 2. 開啟檔案
open index_v4.0.0.html

# 3. 直接使用（零依賴）
```

**優點**：無需部署，直接在瀏覽器開啟
**缺點**：無法使用自動爬蟲功能（需後端）

### 方式 3：完整部署（進階）

完整教學 → [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md)

包含：
- GitHub Actions 自動爬蟲
- 定時推送（每天 3 次）
- 完整 CI/CD 流程

───────────────────────────────────────────────────────

## 🎯 核心功能

### 🤖 AI 智能分析

**4 維度評分系統**：
- 📊 技能匹配度（30%）
- 💼 經驗相符度（25%）
- 📍 地點便利性（20%）
- 💰 薪資合理性（25%）

**AI 引擎**：DeepSeek Chat
**分析速度**：約 3 秒/職缺
**準確率**：基於您的履歷精準匹配

### 📄 履歷客製化

**自動生成**：
- 針對每個職缺優化履歷
- 突出相關技能與經驗
- 一鍵下載 PDF 格式

**支援格式**：
- 📄 PDF（推薦）
- 📝 Word (DOCX)
- 📋 純文字 (TXT)

### 🔔 多渠道推送

**支援平台**：
- 📧 Email（Gmail、Outlook 等）
- 💬 Telegram Bot
- 🔗 Slack Webhook

**推送內容**：
- 新職缺通知
- AI 分析結果
- 匹配度雷達圖
- 一鍵應徵連結

### 🎨 雙主題系統

- 🌙 深色模式（預設）
- ☀️ 淺色模式
- 🎨 Glassmorphism UI
- 📐 Bento Grid 排版

### 📊 數據視覺化

**Chart.js 圖表**：
- 雷達圖（技能匹配）
- 長條圖（薪資分布）
- 折線圖（分數趨勢）

───────────────────────────────────────────────────────

## 💰 成本對比

| 方案 | 成本 | 功能 | 設定時間 |
|------|------|------|---------|
| **本專案** | **NT$5-20/月** | ✅ 完整功能 | **5 分鐘** |
| LazyApply | NT$3,000/月 | ⚠️ 功能受限 | 5 分鐘 |
| LinkedIn Premium | NT$3,600/月 | ❌ 無 AI 分析 | 5 分鐘 |
| JobSpy 開源 | NT$0/月 | ❌ 需自己寫程式 | 30 分鐘+ |

**省下 99% 成本！** 💸

詳細費用說明 → [VERCEL_SETUP_GUIDE.md#成本估算](./VERCEL_SETUP_GUIDE.md#📊-成本估算真實數據)

───────────────────────────────────────────────────────

## 📚 文件導覽

### 快速開始
- 🚀 [Vercel 部署指南](./VERCEL_SETUP_GUIDE.md) - **推薦新手**
- 📖 [完整部署教學](./DEPLOY_GUIDE.md)
- ⚡ [3 分鐘快速部署](./QUICK_DEPLOY.md)

### 功能說明
- 📋 [版本變更紀錄](./CHANGELOG_v4.0.0.md)
- 🏆 [競品分析報告](./COMPETITIVE_ANALYSIS.md)
- 🧪 [測試報告](./TEST_REPORT.md)

### 進階設定
- 🔑 [環境變數設定](./VERCEL_SETUP_GUIDE.md#步驟-3設定環境變數2-分鐘)
- 🔔 [Telegram Bot 設定](./VERCEL_SETUP_GUIDE.md#telegram-bot-設定)
- 🔗 [Slack Webhook 設定](./VERCEL_SETUP_GUIDE.md#slack-webhook-設定)
- ⏰ [GitHub Actions 設定](./DEPLOY_GUIDE.md#github-actions-設定)

───────────────────────────────────────────────────────

## 🛠️ 技術堆疊

### 前端
- **Framework**: Vanilla JavaScript（零依賴）
- **UI**: Glassmorphism + Bento Grid
- **Theme**: 雙主題系統（深色/淺色）
- **Charts**: Chart.js
- **PDF**: jsPDF

### 後端
- **Platform**: Vercel Serverless Functions
- **Language**: Python 3.9+
- **AI**: DeepSeek Chat API
- **Scraper**: JobSpy

### 自動化
- **CI/CD**: GitHub Actions
- **Schedule**: Cron Jobs（每天 3 次）
- **Notification**: Email / Telegram / Slack

───────────────────────────────────────────────────────

## 📸 螢幕截圖

### 歡迎畫面（v4.0.0 新增）

```
┌──────────────────────────────────────┐
│          🎉 歡迎使用                   │
│      AI Job Search Agent             │
│                                      │
│  我會帶您完成 5 分鐘快速設定           │
│  之後就能享受全自動 AI 求職體驗！       │
│                                      │
│  🤖 AI 智能分析  📄 履歷客製化         │
│  🔔 即時推送    💰 完全免費            │
│                                      │
│  [跳過]  [🚀 開始 5 分鐘導覽]         │
└──────────────────────────────────────┘
```

### 步驟式引導

```
        ← 高亮目標元素
┌──────────────────────────────────────┐
│  步驟 1/7：上傳您的履歷                │
│                                      │
│  支援 PDF、Word、TXT 格式              │
│  AI 會自動分析您的技能與經驗            │
│                                      │
│  ✓ 自動提取關鍵字                     │
│  ✓ 識別技能與經驗                     │
│  ✓ 建立求職檔案                       │
│                                      │
│  [上傳履歷 →]                         │
│                                      │
│  ●●○○○○○  進度 1/7                  │
└──────────────────────────────────────┘
```

### 主介面（雙主題）

**深色模式**：
- 背景：`#0D1117`（GitHub 風格）
- Glassmorphism：半透明毛玻璃
- 橘色強調色（Hermès）

**淺色模式**：
- 背景：`#FFFFFF`
- 淡化玻璃效果
- 保持一致的配色

───────────────────────────────────────────────────────

## 🎓 使用教學

### 1. 上傳履歷

**支援方式**：
- 📁 上傳檔案（PDF / Word）
- 🔗 從 LinkedIn 匯入
- ✏️ 手動輸入

**AI 會自動解析**：
- 個人資訊
- 技能清單
- 工作經驗
- 學歷背景

### 2. 搜尋職缺

**輸入關鍵字**：
```
例如：python developer
例如：前端工程師 台北
例如：data scientist remote
```

**AI 自動篩選**：
- 去除重複
- 依相關性排序
- 過濾無效職缺

### 3. AI 分析

**點擊「分析全部」**：
- 批次分析所有職缺
- 每個職缺約 3 秒
- 自動評分與排序

**查看詳情**：
- 點擊職缺卡片
- 查看雷達圖與建議
- 下載客製化履歷

### 4. 追蹤管理

**收藏職缺** ⭐：
- 點擊愛心圖示
- 加入收藏清單

**應徵追蹤** 📋：
- 記錄應徵狀態
- 設定提醒時間
- 標記面試結果

───────────────────────────────────────────────────────

## ❓ 常見問題

### Q1：完全免費嗎？

**A**：幾乎免費！

- Vercel 部署：**完全免費**（個人使用綽綽有餘）
- DeepSeek API：**約 NT$5-20/月**（根據使用量）
- Email/Telegram：**完全免費**

總計：**NT$5-20/月**（比星巴克便宜）

### Q2：需要會寫程式嗎？

**A**：不需要！

- 一鍵部署：**點按鈕即可**
- 設定環境變數：**填表單即可**
- 使用網站：**像用 LinkedIn 一樣簡單**

唯一需要的：**會填表單** + **會點滑鼠**

### Q3：資料安全嗎？

**A**：非常安全！

- 履歷存在**您的瀏覽器**（localStorage）
- 部署在**您的 Vercel 帳號**
- API Key 存在**您的環境變數**
- **不經過任何第三方伺服器**

### Q4：可以自動應徵嗎？

**A**：目前不行，需要手動應徵

**原因**：
- 自動應徵可能違反求職網站 ToS
- 容易被封帳號
- 品質不如人工篩選

**建議**：
- 使用 AI 分析篩選
- 下載客製化履歷
- 手動投遞高匹配職缺

### Q5：支援哪些求職網站？

**A**：透過 JobSpy 支援：

- LinkedIn
- Indeed
- Glassdoor
- ZipRecruiter
- 更多持續新增中...

**台灣求職網站**（計劃中）：
- 104 人力銀行
- 1111 人力銀行
- CakeResume

───────────────────────────────────────────────────────

## 🤝 貢獻指南

歡迎貢獻！請先閱讀 [CONTRIBUTING.md](./CONTRIBUTING.md)

**貢獻方式**：
- 🐛 回報 Bug
- 💡 提出新功能建議
- 📝 改善文件
- 🔧 提交 Pull Request

───────────────────────────────────────────────────────

## 📜 授權條款

MIT License

Copyright (c) 2026 大周天工作室

詳見 [LICENSE](./LICENSE)

───────────────────────────────────────────────────────

## 🙏 致謝

**開源專案**：
- [JobSpy](https://github.com/Bunsly/JobSpy) - 爬蟲引擎
- [DeepSeek](https://platform.deepseek.com/) - AI 分析
- [Chart.js](https://www.chartjs.org/) - 圖表
- [jsPDF](https://github.com/parallax/jsPDF) - PDF 生成

**靈感來源**：
- LazyApply
- LinkedIn Job Search
- 大周天思考系統 v4.7.1

───────────────────────────────────────────────────────

## 📞 聯絡我們

- 💬 GitHub Discussions
- 🐛 GitHub Issues
- 📧 Email: your-email@example.com
- 🌐 Website: https://your-website.com

───────────────────────────────────────────────────────

**製作團隊**：大周天工作室 ☯
**版本**：v4.0.0 Aurora Edition
**最後更新**：2026-02-11

⭐ **如果這個專案對您有幫助，請給我們一個 Star！**

[![GitHub stars](https://img.shields.io/github/stars/your-username/ai-job-agent?style=social)](https://github.com/your-username/ai-job-agent)
[![GitHub forks](https://img.shields.io/github/forks/your-username/ai-job-agent?style=social)](https://github.com/your-username/ai-job-agent/fork)

祝您求職順利！🎉
