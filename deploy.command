#!/bin/bash
cd "$(dirname "$0")"
echo ""
echo "═══════════════════════════════════════"
echo "  AI Job Agent - 部署到 Vercel"
echo "═══════════════════════════════════════"
echo ""

# 檢查 Vercel CLI
if command -v vercel &> /dev/null; then
    echo "→ 使用 vercel CLI 部署..."
    vercel --yes --prod 2>&1
elif command -v npx &> /dev/null; then
    echo "→ 使用 npx vercel 部署..."
    npx vercel --yes --prod 2>&1
else
    echo "→ 找不到 vercel CLI，嘗試安裝..."
    npm install -g vercel 2>&1
    vercel --yes --prod 2>&1
fi

echo ""
echo "═══════════════════════════════════════"
echo "  部署完成！請訪問："
echo "  https://ai-job-agent-three.vercel.app"
echo "═══════════════════════════════════════"
echo ""
read -p "按 Enter 關閉..."
