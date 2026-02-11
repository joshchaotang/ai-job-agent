"""
AI Job Agent - 職缺搜尋 API v2.2
使用免費 API 搜尋遠端科技職缺
v2.2: 修復 Unix 時間戳顯示、Remotive 可靠性、來源計數
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import hmac
import hashlib
import ssl
from urllib.request import urlopen, Request
from urllib.parse import urlencode, parse_qs, urlparse, quote
from html import unescape
from datetime import datetime, timezone
import re


def verify_token(token: str) -> bool:
    secret = os.environ.get("APP_SECRET", "ai-job-agent-2026-secret")
    password = os.environ.get("APP_PASSWORD", "agent2026")
    expected = hmac.new(secret.encode(), password.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(token or "", expected)


def strip_html(text: str) -> str:
    """移除 HTML 標籤"""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = unescape(clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean[:600]


def make_ssl_context():
    """建立寬鬆的 SSL context，避免 Vercel 環境的憑證問題"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def search_remotive(query: str, limit: int = 30) -> list:
    """搜尋 Remotive API（免費，無需 API Key）"""
    url = f"https://remotive.com/api/remote-jobs?search={quote(query)}&limit={limit}"
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
    })
    ctx = make_ssl_context()
    resp = urlopen(req, timeout=12, context=ctx)
    data = json.loads(resp.read())

    jobs = []
    for j in data.get("jobs", []):
        salary_text = j.get("salary", "") or ""
        salary_min, salary_max = parse_salary(salary_text)

        jobs.append({
            "title": j.get("title", ""),
            "company": j.get("company_name", ""),
            "location": j.get("candidate_required_location", "Remote"),
            "url": j.get("url", ""),
            "date": (j.get("publication_date", "") or "")[:10],
            "description": strip_html(j.get("description", "")),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_text": salary_text,
            "tags": j.get("tags", []),
            "job_type": j.get("job_type", ""),
            "source": "Remotive",
            "score": None,
            "analysis": None,
        })
    return jobs


def format_timestamp(raw_date) -> str:
    """將各種日期格式統一轉成 YYYY-MM-DD"""
    if not raw_date:
        return ""
    # 整數或浮點數 → Unix 時間戳
    if isinstance(raw_date, (int, float)):
        try:
            return datetime.fromtimestamp(raw_date, tz=timezone.utc).strftime("%Y-%m-%d")
        except (ValueError, OSError, OverflowError):
            return ""
    # 字串：可能是 ISO 格式或純數字
    s = str(raw_date).strip()
    # 純數字字串 → 當作 Unix 時間戳
    if s.isdigit() and len(s) >= 9:
        try:
            return datetime.fromtimestamp(int(s), tz=timezone.utc).strftime("%Y-%m-%d")
        except (ValueError, OSError, OverflowError):
            return s[:10]
    # 已經是日期格式 → 取前 10 字元（YYYY-MM-DD）
    return s[:10]


def search_arbeitnow(query: str, limit: int = 20) -> list:
    """搜尋 Arbeitnow API（免費，無需 API Key）"""
    url = f"https://www.arbeitnow.com/api/job-board-api?search={quote(query)}&page=1"
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    })
    ctx = make_ssl_context()
    resp = urlopen(req, timeout=12, context=ctx)
    data = json.loads(resp.read())

    jobs = []
    for j in data.get("data", [])[:limit]:
        # created_at 可能是整數（Unix 時間戳）或字串，統一轉 YYYY-MM-DD
        date_str = format_timestamp(j.get("created_at", ""))

        # tags 可能是字串列表或其他格式，確保是字串列表
        raw_tags = j.get("tags", [])
        if isinstance(raw_tags, list):
            tags = [str(t) for t in raw_tags if t]
        else:
            tags = []

        jobs.append({
            "title": str(j.get("title", "")),
            "company": str(j.get("company_name", "")),
            "location": str(j.get("location", "Remote")),
            "url": str(j.get("url", "")),
            "date": date_str,
            "description": strip_html(str(j.get("description", "") or "")),
            "salary_min": 0,
            "salary_max": 0,
            "salary_text": "",
            "tags": tags,
            "job_type": "full_time" if j.get("remote", False) else "full_time",
            "source": "Arbeitnow",
            "score": None,
            "analysis": None,
        })
    return jobs


def parse_salary(text: str) -> tuple:
    """從薪資文字中提取數字"""
    if not text:
        return 0, 0
    numbers = re.findall(r"[\d,]+", text.replace(",", ""))
    nums = [int(n) for n in numbers if n.isdigit() and int(n) > 1000]
    if len(nums) >= 2:
        return min(nums), max(nums)
    elif len(nums) == 1:
        return nums[0], nums[0]
    return 0, 0


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            token = query.get("token", [""])[0]

            if not verify_token(token):
                self._respond(401, {"error": "未授權，請先登入"})
                return

            search_term = query.get("q", ["software engineer"])[0]

            # 搜尋多個來源
            all_jobs = []
            errors = []
            source_counts = {"Remotive": 0, "Arbeitnow": 0}

            # 來源一：Remotive
            try:
                remotive_jobs = search_remotive(search_term, limit=30)
                source_counts["Remotive"] = len(remotive_jobs)
                all_jobs.extend(remotive_jobs)
            except Exception as e:
                errors.append(f"Remotive: {str(e)}")

            # 來源二：Arbeitnow
            try:
                arbeitnow_jobs = search_arbeitnow(search_term, limit=20)
                source_counts["Arbeitnow"] = len(arbeitnow_jobs)
                all_jobs.extend(arbeitnow_jobs)
            except Exception as e:
                errors.append(f"Arbeitnow: {str(e)}")

            # 去重（依公司+職稱）
            seen = set()
            unique_jobs = []
            for job in all_jobs:
                key = f"{job['company']}|{job['title']}"
                if key not in seen:
                    seen.add(key)
                    unique_jobs.append(job)

            self._respond(200, {
                "jobs": unique_jobs,
                "total": len(unique_jobs),
                "sources": ["Remotive", "Arbeitnow"],
                "source_counts": source_counts,
                "errors": errors,
            })

        except Exception as e:
            self._respond(500, {"error": str(e)})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        pass
