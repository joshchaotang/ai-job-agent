"""
AI Job Agent - DeepSeek 履歷分析 API v1.0
使用 DeepSeek API 分析履歷文字，提取技能、經驗、教育
"""
from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.request import Request, urlopen


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 讀取 POST body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            if 'text' not in data:
                self.send_error_response(400, 'Missing text field')
                return

            resume_text = data['text']
            filename = data.get('filename', 'resume')

            if len(resume_text.strip()) < 50:
                self.send_error_response(400, 'Resume text too short (minimum 50 characters)')
                return

            # 呼叫 DeepSeek API 分析履歷
            resume_data = self.analyze_with_deepseek(resume_text)

            if not resume_data:
                self.send_error_response(500, 'DeepSeek API analysis failed')
                return

            response = {
                'success': True,
                'resume': resume_data,
                'filename': filename,
                'message': 'Resume analyzed successfully'
            }

            self.send_json_response(response)

        except Exception as e:
            self.send_error_response(500, f'Analysis error: {str(e)}')

    def analyze_with_deepseek(self, resume_text):
        """使用 DeepSeek API 分析履歷"""
        api_key = os.environ.get('DEEPSEEK_API_KEY', '')

        if not api_key:
            raise Exception('DEEPSEEK_API_KEY not configured')

        prompt = f"""
你是履歷分析專家。請分析以下履歷，提取關鍵資訊。

履歷內容：
{resume_text}

請以 JSON 格式回應，格式如下：
{{
  "skills": ["技能1", "技能2", ...],
  "experience": [
    {{"title": "職位名稱", "company": "公司名稱", "years": 2}},
    ...
  ],
  "education": "學歷摘要（一句話）",
  "summary": "整體摘要（50字內）"
}}

注意：
- skills: 列出所有技術技能、工具、程式語言
- experience: 提取工作經歷，years 是年資（整數）
- education: 簡短說明學歷背景
- summary: 一句話總結候選人的背景

只回應 JSON，不要任何其他文字。
"""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是履歷分析專家，專門從履歷中提取結構化資料。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }

        req = Request(
            'https://api.deepseek.com/v1/chat/completions',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
        )

        try:
            with urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))

            if 'choices' not in result or len(result['choices']) == 0:
                raise Exception('No response from DeepSeek API')

            content = result['choices'][0]['message']['content'].strip()

            # 解析 JSON（移除可能的 markdown 包裝）
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]

            resume_data = json.loads(content.strip())

            # 驗證必要欄位
            if 'skills' not in resume_data:
                resume_data['skills'] = []
            if 'experience' not in resume_data:
                resume_data['experience'] = []
            if 'education' not in resume_data:
                resume_data['education'] = 'Not specified'
            if 'summary' not in resume_data:
                resume_data['summary'] = 'No summary available'

            return resume_data

        except json.JSONDecodeError as e:
            raise Exception(f'Failed to parse DeepSeek response as JSON: {str(e)}')
        except Exception as e:
            raise Exception(f'DeepSeek API error: {str(e)}')

    def send_json_response(self, data, status_code=200):
        """發送 JSON 回應"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def send_error_response(self, status_code, message):
        """發送錯誤回應"""
        response = {
            'success': False,
            'error': message
        }
        self.send_json_response(response, status_code)

    def do_OPTIONS(self):
        """處理 CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
