# ⚡ 極速部署（3 分鐘）

**複製下方指令，在 Mac 終端貼上執行即可！**

---

## 🚀 一鍵執行（全自動）

打開 Mac 終端（Terminal），複製貼上下方**完整指令**：

```bash
cd ~/Downloads/ai-job-agent-cloud && \
tar -xzf git-v3.9.0.tar.gz 2>/dev/null || echo "Git already extracted" && \
chmod +x auto-deploy.sh && \
bash auto-deploy.sh
```

執行後會自動：
1. ✅ 解壓縮 Git
2. ✅ 詢問您的 GitHub Repository URL
3. ✅ 推送到 GitHub
4. ✅ 安裝 Vercel CLI（如需要）
5. ✅ 登入 Vercel（如需要）
6. ✅ 部署到生產環境

---

## 📝 準備工作（3 步驟）

### 1. 建立 GitHub Repository

訪問：https://github.com/new

- Repository name：`ai-job-agent`
- Privacy：**Private**（推薦）
- **不要勾選任何初始化選項**

複製 Repository URL（例如）：
```
https://github.com/YOUR_USERNAME/ai-job-agent.git
```

### 2. 取得 DeepSeek API Key

訪問：https://platform.deepseek.com/api_keys

- 註冊/登入
- 點擊「Create API Key」
- 複製 API Key（sk-開頭）

### 3. 設定 Gmail App Password

訪問：https://myaccount.google.com/apppasswords

- 選擇「郵件」和「其他（自訂名稱）」
- 輸入：`AI Job Agent`
- 複製 16 位數密碼（移除空格）

---

## 🎯 執行部署（貼上指令）

```bash
cd ~/Downloads/ai-job-agent-cloud && bash auto-deploy.sh
```

**過程中會詢問**：
1. GitHub Repository URL → 貼上您的 URL
2. Vercel 登入 → 瀏覽器會自動開啟，登入即可

**完成後會顯示**：
```
✅ 部署完成！
Your deployment is ready at:
https://ai-job-agent-abc123.vercel.app
```

---

## ⚙️ 設定環境變數（2 分鐘）

### A. Vercel Dashboard

1. 訪問：https://vercel.com/dashboard
2. 選擇您的專案
3. Settings → Environment Variables
4. 逐一新增（4 個必須）：

| Name | Value |
|------|-------|
| `DEEPSEEK_API_KEY` | sk-xxxxx（您的 DeepSeek Key）|
| `EMAIL_USER` | your@gmail.com |
| `EMAIL_PASS` | abcdefghijklmnop（Gmail App Password）|
| `EMAIL_TO` | recipient@gmail.com |

5. 點擊「Redeploy」重新部署

### B. GitHub Secrets（用於定時任務）

1. 訪問：https://github.com/YOUR_USERNAME/ai-job-agent/settings/secrets/actions
2. 點擊「New repository secret」
3. 逐一新增（同上 4 個 + 可選的 Telegram/Slack）

---

## ✅ 驗證部署

訪問您的 Vercel URL，應該看到：
- ✅ 愛馬仕橘色主題
- ✅ 深色模式
- ✅ 登入頁面正常

測試功能：
1. 登入（任意 API Key）
2. 搜尋職位
3. 上傳履歷
4. 測試 AI 分析

---

## 🔄 測試自動推送

**手動觸發 GitHub Action**：

1. 訪問：https://github.com/YOUR_USERNAME/ai-job-agent/actions
2. 選擇「Scrape Morning」
3. 點擊「Run workflow」
4. 等待 1-2 分鐘

檢查是否收到：
- 📧 Gmail 郵件
- 💬 Telegram 訊息（如已設定）
- 💼 Slack 訊息（如已設定）

---

## 🆘 遇到問題？

### Q1：部署後網站顯示錯誤
**A**：前往 Vercel Dashboard → Deployments → Logs 查看錯誤

### Q2：推送到 GitHub 失敗
**A**：可能需要 GitHub Personal Access Token
```bash
# 建立 Token：https://github.com/settings/tokens
# 替換 URL 中的 github.com 為 YOUR_TOKEN@github.com
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/ai-job-agent.git
git push -u origin main
```

### Q3：AI 分析不工作
**A**：確認 Vercel 環境變數中的 `DEEPSEEK_API_KEY` 已設定，並點擊「Redeploy」

---

## 🎉 完成！

現在您的 AI Job Agent 已正式上線！

**下一步**：
- 📱 測試所有功能
- 📊 收集使用數據（論文用）
- 🎓 開始撰寫論文

**完整文件**：參考 `DEPLOY_GUIDE.md`

---

**部署時間**：3-5 分鐘
**難度等級**：⭐☆☆☆☆（極簡單）

祝您部署順利！🚀
