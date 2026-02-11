#!/bin/bash

# AI Job Agent - 一鍵自動部署腳本
# 使用方式：在 Mac 終端執行 `bash auto-deploy.sh`

set -e  # 遇到錯誤立即停止

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   AI Job Agent v3.9.0 - 一鍵自動部署腳本                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ========================================
# 步驟 1：Git 初始化
# ========================================
echo "📦 步驟 1/5：初始化 Git..."

# 解壓縮 git 資料夾
if [ -f "git-v3.9.0.tar.gz" ]; then
    echo "   → 解壓縮 git-v3.9.0.tar.gz..."
    tar -xzf git-v3.9.0.tar.gz
    echo "   ✅ Git 解壓縮完成"
else
    echo "   ⚠️  找不到 git-v3.9.0.tar.gz，重新初始化 Git..."
    git init
    git config user.name "CK (大周天工作室)"
    git config user.email "a122233456@gmail.com"
    git add .
    git commit -m "v3.9.0 Olympus Edition - Initial Commit"
fi

echo ""

# ========================================
# 步驟 2：GitHub 推送（需要使用者提供資訊）
# ========================================
echo "🔗 步驟 2/5：推送到 GitHub..."

# 檢查是否已有 remote
if git remote | grep -q "origin"; then
    echo "   ✅ Git remote 已設定"
else
    echo ""
    echo "   請輸入您的 GitHub Repository URL："
    echo "   格式：https://github.com/YOUR_USERNAME/ai-job-agent.git"
    read -p "   URL: " GITHUB_URL

    git remote add origin "$GITHUB_URL"
    echo "   ✅ Git remote 已設定"
fi

echo "   → 推送到 GitHub..."
git branch -M main
git push -u origin main || {
    echo ""
    echo "   ⚠️  推送失敗，可能需要認證。"
    echo "   請手動執行：git push -u origin main"
    echo ""
    read -p "   按 Enter 繼續部署到 Vercel..."
}

echo ""

# ========================================
# 步驟 3：安裝 Vercel CLI（如果未安裝）
# ========================================
echo "📦 步驟 3/5：檢查 Vercel CLI..."

if ! command -v vercel &> /dev/null; then
    echo "   → Vercel CLI 未安裝，正在安裝..."
    npm install -g vercel
    echo "   ✅ Vercel CLI 安裝完成"
else
    echo "   ✅ Vercel CLI 已安裝"
fi

echo ""

# ========================================
# 步驟 4：Vercel 登入（如果未登入）
# ========================================
echo "🔐 步驟 4/5：Vercel 登入檢查..."

if [ ! -f "$HOME/.vercel/auth.json" ]; then
    echo "   → 尚未登入 Vercel，開始登入流程..."
    vercel login
else
    echo "   ✅ Vercel 已登入"
fi

echo ""

# ========================================
# 步驟 5：部署到 Vercel
# ========================================
echo "🚀 步驟 5/5：部署到 Vercel..."

echo "   → 部署到生產環境..."
vercel --prod --yes

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   ✅ 部署完成！                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "下一步："
echo "1. 前往 Vercel Dashboard 設定環境變數"
echo "2. 前往 GitHub Settings 設定 Secrets"
echo "3. 測試網站功能"
echo ""
echo "詳細說明請參考：DEPLOY_GUIDE.md"
echo ""
