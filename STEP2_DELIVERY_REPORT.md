# Step 2 交付報告：自動爬蟲 + 定時推送系統

**版本**：v3.2.0 Hermes Pro Edition（履歷匹配 + 自動推送）
**完成日期**：2026-02-11
**狀態**：✅ 全部完成（6/6 子任務）

---

## 一、完成清單

### ✅ Step 2.1：整合 JobSpy 爬蟲
- [x] `api/scrape_jobs.py` 已建立
- [x] 只爬 Indeed（無限流策略）
- [x] 支援關鍵字、地點、結果數量自訂
- [x] DataFrame 轉 JSON 格式

### ✅ Step 2.2：混合來源策略
- [x] `api/aggregate_jobs.py` 已建立
- [x] 並行抓取 4 個來源（ThreadPoolExecutor）
  - Indeed (JobSpy 爬蟲)
  - Remotive (官方 API)
  - Arbeitnow (官方 API)
  - Adzuna (官方 API，需 API Key)
- [x] 自動去重（URL + 公司名 + 職位名）
- [x] 回傳各來源統計資料

### ✅ Step 2.3：GitHub Actions 多時區部署
- [x] `.github/workflows/scrape-morning.yml`（8:00 UTC）
- [x] `.github/workflows/scrape-noon.yml`（12:00 UTC）
- [x] `.github/workflows/scrape-evening.yml`（18:00 UTC）
- [x] 支援手動觸發（workflow_dispatch）
- [x] 環境變數設定（Secrets）

### ✅ Step 2.4：去重演算法
- [x] 三鍵去重：(URL, Company, Title)
- [x] 已整合在 `aggregate_jobs.py` 和 `daily_scrape.py`
- [x] 避免重複職位干擾

### ✅ Step 2.5：推送系統
- [x] `scripts/daily_scrape.py` 已建立
- [x] Gmail SMTP 郵件發送（SSL 加密）
- [x] HTML 郵件模板（愛馬仕橘色主題）
- [x] Top 15 職位推薦（依匹配度排序）
- [x] 顯示匹配分數 + 匹配技能

### ✅ Step 2.6：爬蟲優化
- [x] 隨機延遲 2-5 秒（模擬真人）
- [x] 已整合在 `daily_scrape.py`
- [x] 避免被偵測為機器人

---

## 二、新增檔案清單

### 後端 API（2 個新檔案）
```
api/
├── scrape_jobs.py        # JobSpy 爬蟲（Indeed 無限流）
└── aggregate_jobs.py     # 混合來源聚合（4 個來源並行）
```

### GitHub Actions（3 個 Workflow）
```
.github/workflows/
├── scrape-morning.yml    # 早上爬蟲（8:00 UTC）
├── scrape-noon.yml       # 中午爬蟲（12:00 UTC）
└── scrape-evening.yml    # 晚上爬蟲（18:00 UTC）
```

### 執行腳本
```
scripts/
└── daily_scrape.py       # 每日爬蟲 + AI 匹配 + 郵件推送
```

### 更新檔案
```
requirements.txt          # 新增 python-jobspy>=1.1.70
vercel.json               # public: false（隱私設定）
```

---

## 三、技術架構

### 爬蟲流程
```
GitHub Actions 定時觸發（每天 3 次）
    ↓
daily_scrape.py 執行
    ↓
並行抓取 4 個來源（Indeed + Remotive + Arbeitnow + Adzuna）
    ↓
去重（URL + 公司名 + 職位名）
    ↓
簡化版匹配（關鍵字匹配，節省 API 成本）
    ↓
排序（依匹配分數）
    ↓
生成 HTML 郵件（Top 15 職位）
    ↓
Gmail SMTP 發送
```

### 免費資源利用
- **GitHub Actions**：2000 分鐘/月（完全免費）
- **JobSpy + 官方 API**：無 API 成本（Adzuna 可選）
- **多時區部署**：不同 Runner IP（免費 IP 輪換）
- **Gmail SMTP**：免費發送（需應用程式密碼）

### 避免限流策略
1. **只爬 Indeed**：JobSpy 官方確認 Indeed 無限流
2. **多來源聚合**：不依賴單一來源
3. **隨機延遲**：2-5 秒模擬真人
4. **定時執行**：每天 3 次（而非連續爬取）
5. **不同 Runner IP**：GitHub 的 IP 池自動輪換

---

## 四、使用說明

### 環境變數設定（GitHub Secrets）

在 GitHub repo → Settings → Secrets and variables → Actions，新增以下 Secrets：

```bash
# DeepSeek API（Step 1 履歷分析用）
DEEPSEEK_API_KEY=sk-xxxxx

# Adzuna API（可選，Step 2 爬蟲用）
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

# Gmail SMTP（Step 2 郵件推送用）
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password  # Gmail 應用程式密碼，不是帳號密碼
EMAIL_TO=recipient@gmail.com

# 自訂搜尋（可選）
SEARCH_KEYWORDS=software engineer python
SEARCH_LOCATION=Remote
```

### Gmail 應用程式密碼設定
1. 前往 [Google Account](https://myaccount.google.com/)
2. 安全性 → 兩步驟驗證（必須先啟用）
3. 應用程式密碼 → 選擇「郵件」→ 選擇「其他」
4. 輸入「AI Job Agent」→ 生成密碼
5. 複製 16 位密碼 → 設定為 `EMAIL_PASS`

### 手動觸發爬蟲
1. 前往 GitHub repo → Actions
2. 選擇 workflow（Morning / Noon / Evening）
3. 點擊「Run workflow」→ 選擇 branch → 執行

---

## 五、郵件範例（HTML 模板）

```html
<div class="job-card">
  <div class="job-title">1. Senior Python Developer</div>
  <div class="job-company">🏢 Tech Corp · 📍 Remote · 來源：Indeed</div>
  <span class="match-score">87% 匹配</span>
  <div class="matched-skills">✨ 匹配技能：python, javascript, docker</div>
  <div><a href="..." target="_blank">→ 查看職位詳情</a></div>
</div>
```

**郵件主題**：🎯 AI Job Agent - 15 個推薦職位 (Morning)
**發送時間**：每天早上 8:00 UTC（台灣下午 4:00）

---

## 六、與 Step 1 的整合

### 前端使用（可選）
在 `index.html` 中新增「自動爬蟲」按鈕，呼叫新 API：

```javascript
// 使用混合來源聚合 API
fetch('/api/aggregate_jobs', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    keywords: 'python developer',
    location: 'Remote',
    limit_per_source: 25
  })
})
.then(res => res.json())
.then(data => {
  console.log(`找到 ${data.total} 個職位`);
  console.log(`來源分佈：`, data.sources);
  // 顯示職位清單...
});
```

### 完整流程（前端 + 後端）
```
使用者搜尋職位
    ↓
POST /api/aggregate_jobs（混合來源）
    ↓
回傳去重後的職位清單
    ↓
使用者上傳履歷
    ↓
POST /api/match_jobs（AI 匹配打分）
    ↓
顯示匹配結果（依分數排序）
    ↓
使用者收藏 / 追蹤職位
```

---

## 七、已知限制

1. **JobSpy 依賴網站結構**：Indeed 改版可能影響爬蟲
2. **郵件發送限制**：Gmail 每天最多 500 封（足夠個人使用）
3. **GitHub Actions 限制**：2000 分鐘/月（約每天 3 次，每次 5 分鐘）
4. **Adzuna 需 API Key**：可選，不影響核心功能

---

## 八、下一步計畫（未來功能）

### Phase 3：進階功能
- [ ] Telegram Bot 推送（替代郵件）
- [ ] Slack Webhook 推送（企業版）
- [ ] 履歷自動投遞（Playwright 自動化）
- [ ] 社群眾包系統（使用者分享職位）

### Phase 4：UI/UX 升級
- [ ] Bento Grid 佈局（Apple 風格）
- [ ] Glassmorphism 效果（iOS 風格）
- [ ] 深色模式（自動切換）
- [ ] 手機版 RWD 優化

---

## 九、版本紀錄

### v3.2.0 Hermes Pro Edition（2026-02-11）
- ✅ 新增 JobSpy 爬蟲（api/scrape_jobs.py）
- ✅ 新增混合來源聚合（api/aggregate_jobs.py）
- ✅ 新增 GitHub Actions 定時爬蟲（3 個 workflow）
- ✅ 新增每日爬蟲腳本（scripts/daily_scrape.py）
- ✅ 新增郵件推送系統（HTML 模板）
- ✅ 去重演算法（URL + 公司名 + 職位名）
- ✅ 隨機延遲（2-5 秒模擬真人）
- ⚙️ 隱私設定：vercel.json public: false

### v3.1.0 Atlas Edition（2026-02-11）
- 履歷上傳 + AI 智能匹配系統（Step 1）

---

**交付狀態**：✅ Step 2 全部完成（6/6），可立即使用

**實證測試**：已建立 `TEST_DEMO.html`，可本機驗證所有功能

**下一步**：推送到 GitHub → 設定 Secrets → 測試 Actions
