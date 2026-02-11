"""
AI Job Agent - AI 分析 API v3.0
使用 DeepSeek/OpenAI API 對職缺進行 AI 評分 + 面試問題生成
支援前端傳入 API Key（每位使用者用自己的 Key）
v3.0: 新增 mode=interview 面試問題生成模式
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import hmac
import hashlib
from urllib.request import urlopen, Request


DEFAULT_RESUME = """
Software Engineer with Master's degree in Computer Science.
Skills: Python, JavaScript, React, Node.js, TypeScript, PostgreSQL, MongoDB,
Docker, AWS, Git, REST API, GraphQL, Machine Learning, TensorFlow, PyTorch.
Experience: Full-stack web development, AI/ML projects, cloud deployment.
Built an AI-powered job search agent with automated analysis and scoring.
Strong problem-solving skills, team collaboration, agile methodology.
"""


def verify_token(token: str) -> bool:
    secret = os.environ.get("APP_SECRET", "ai-job-agent-2026-secret")
    password = os.environ.get("APP_PASSWORD", "agent2026")
    expected = hmac.new(secret.encode(), password.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(token or "", expected)


def call_llm(prompt: str, api_key: str, model: str, base_url: str) -> dict:
    """呼叫 LLM API（支援 DeepSeek / OpenAI）"""
    payload = json.dumps({
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a job match analyzer. Evaluate how well a job matches "
                    "a candidate's resume. Always respond in valid JSON format only, "
                    "no markdown, no extra text."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 500,
    }).encode("utf-8")

    req = Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    resp = urlopen(req, timeout=9)
    result = json.loads(resp.read())
    content = result["choices"][0]["message"]["content"]

    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1].rsplit("```", 1)[0]

    return json.loads(content)


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {}

            token = body.get("token", "")
            if not verify_token(token):
                self._respond(401, {"error": "未授權，請先登入"})
                return

            # API Key 優先順序：前端傳入 > 環境變數
            api_key = body.get("api_key", "").strip()
            if not api_key:
                api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                self._respond(400, {"error": "請在設定中輸入你的 API Key"})
                return

            # Model & Base URL
            model = body.get("model", "").strip() or os.environ.get("LLM_MODEL", "deepseek-chat")
            if "deepseek" in model:
                base_url = "https://api.deepseek.com"
            elif "gpt" in model:
                base_url = "https://api.openai.com/v1"
            else:
                base_url = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com")

            job = body.get("job", {})
            mode = body.get("mode", "analyze")
            resume = body.get("resume", "").strip() or DEFAULT_RESUME

            # === 面試問題生成模式 ===
            if mode == "interview":
                interview_prompt = f"""Based on this job posting, generate 6-8 likely interview questions.

JOB:
Title: {job.get('title', 'N/A')}
Company: {job.get('company', 'N/A')}
Location: {job.get('location', 'N/A')}
Description: {job.get('description', 'N/A')[:800]}
Tags: {', '.join(job.get('tags', [])[:10])}

Generate questions in these categories:
- 2 technical questions specific to this role
- 2 behavioral questions (STAR method)
- 2 situational/problem-solving questions
- 1-2 role/company specific questions

Return ONLY this JSON format:
{{
  "questions": [
    {{"type": "技術問題", "question": "...", "tip": "preparation tip in Chinese"}},
    {{"type": "行為問題", "question": "...", "tip": "..."}},
    {{"type": "情境問題", "question": "...", "tip": "..."}},
    {{"type": "職位相關", "question": "...", "tip": "..."}}
  ],
  "preparation_advice": "overall preparation advice in Chinese (2-3 sentences)"
}}"""
                result = call_llm(interview_prompt, api_key, model, base_url)
                self._respond(200, {
                    "questions": result.get("questions", []),
                    "preparation_advice": result.get("preparation_advice", ""),
                })
                return

            # === 原有的匹配分析模式 ===
            prompt = f"""Analyze this job match and return JSON:

RESUME:
{resume[:1500]}

JOB:
Title: {job.get('title', 'N/A')}
Company: {job.get('company', 'N/A')}
Location: {job.get('location', 'N/A')}
Description: {job.get('description', 'N/A')[:800]}
Tags: {', '.join(job.get('tags', [])[:10])}

Return ONLY this JSON format:
{{
  "score": <0-100 integer>,
  "tech_match": <0-100>,
  "exp_match": <0-100>,
  "edu_match": <0-100>,
  "highlights": ["strength1", "strength2", "strength3"],
  "gaps": ["gap1"],
  "recommendation": "one sentence in Chinese"
}}"""

            result = call_llm(prompt, api_key, model, base_url)

            score = int(result.get("score", 50))
            score = max(0, min(100, score))

            self._respond(200, {
                "score": score,
                "tech_match": int(result.get("tech_match", 50)),
                "exp_match": int(result.get("exp_match", 50)),
                "edu_match": int(result.get("edu_match", 50)),
                "highlights": result.get("highlights", []),
                "gaps": result.get("gaps", []),
                "recommendation": result.get("recommendation", ""),
            })

        except json.JSONDecodeError:
            self._respond(200, {
                "score": 60,
                "tech_match": 60,
                "exp_match": 50,
                "edu_match": 50,
                "highlights": ["Unable to parse detailed analysis"],
                "gaps": [],
                "recommendation": "AI 分析暫時無法解析，請稍後再試",
            })
        except Exception as e:
            self._respond(500, {"error": f"AI 分析失敗: {str(e)}"})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        pass
