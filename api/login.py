"""
AI Job Agent - 登入 API
驗證密碼，回傳存取權杖
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import hmac
import hashlib


def make_token(password: str) -> str:
    secret = os.environ.get("APP_SECRET", "ai-job-agent-2026-secret")
    return hmac.new(secret.encode(), password.encode(), hashlib.sha256).hexdigest()


def verify_token(token: str) -> bool:
    password = os.environ.get("APP_PASSWORD", "agent2026")
    expected = make_token(password)
    return hmac.compare_digest(token, expected)


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

            password = body.get("password", "")
            correct = os.environ.get("APP_PASSWORD", "agent2026")

            if password == correct:
                token = make_token(password)
                self._respond(200, {"success": True, "token": token})
            else:
                self._respond(401, {"success": False, "error": "密碼錯誤"})

        except Exception as e:
            self._respond(500, {"success": False, "error": str(e)})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        pass
