"""
AI Job Agent - AI 職位匹配打分 API v1.0
使用 DeepSeek API 分析履歷與職位的匹配度
"""
from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 讀取 POST body
            content_length = int(self.headers.get('Content-Type', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            if 'resume' not in data or 'jobs' not in data:
                self.send_error_response(400, 'Missing resume or jobs field')
                return

            resume = data['resume']
            jobs = data['jobs']

            if not jobs or len(jobs) == 0:
                self.send_error_response(400, 'Jobs list is empty')
                return

            # 並行處理職位匹配（最多 5 個並行）
            matched_jobs = self.match_jobs_parallel(resume, jobs, max_workers=5)

            response = {
                'success': True,
                'matched_jobs': matched_jobs,
                'total': len(matched_jobs),
                'message': f'Analyzed {len(matched_jobs)} jobs'
            }

            self.send_json_response(response)

        except Exception as e:
            self.send_error_response(500, f'Matching error: {str(e)}')

    def match_jobs_parallel(self, resume, jobs, max_workers=5):
        """並行處理職位匹配"""
        matched_jobs = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任務
            future_to_job = {
                executor.submit(self.match_single_job, resume, job): job
                for job in jobs
            }

            # 收集結果
            for future in as_completed(future_to_job):
                try:
                    result = future.result()
                    if result:
                        matched_jobs.append(result)
                except Exception as e:
                    # 單個職位失敗不影響整體
                    job = future_to_job[future]
                    print(f"Failed to match job {job.get('title', 'Unknown')}: {str(e)}")

        return matched_jobs

    def match_single_job(self, resume, job):
        """匹配單一職位"""
        api_key = os.environ.get('DEEPSEEK_API_KEY', '')

        if not api_key:
            raise Exception('DEEPSEEK_API_KEY not configured')

        # 建構簡化的履歷摘要
        resume_summary = f"""
技能：{', '.join(resume.get('skills', []))}
經驗：{len(resume.get('experience', []))} 個職位，總計約 {sum([exp.get('years', 0) for exp in resume.get('experience', [])])} 年
教育：{resume.get('education', 'Not specified')}
"""

        # 建構職位描述
        job_desc = f"""
職位：{job.get('title', 'Unknown')}
公司：{job.get('company', 'Unknown')}
地點：{job.get('location', 'Remote')}
"""

        prompt = f"""
你是求職匹配專家。請分析候選人履歷與職位的匹配度。

候選人履歷：
{resume_summary}

職位描述：
{job_desc}

請以 JSON 格式回應，格式如下：
{{
  "match_score": 85,
  "match_reason": "技能匹配度高，有相關經驗",
  "missing_skills": ["Docker", "Kubernetes"],
  "strengths": ["Python", "JavaScript", "React"]
}}

評分標準：
- 90-100: 完美匹配，強烈推薦
- 75-89: 高度匹配，推薦申請
- 60-74: 中等匹配，可以試試
- 40-59: 低度匹配，不太適合
- 0-39: 不匹配

注意：
- match_score: 0-100 分的整數
- match_reason: 50字內的匹配理由
- missing_skills: 候選人缺少的關鍵技能（最多5個）
- strengths: 候選人的優勢技能（最多5個）

只回應 JSON，不要任何其他文字。
"""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是求職匹配專家，專門評估候選人與職位的匹配度。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
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
            with urlopen(req, timeout=20) as response:
                result = json.loads(response.read().decode('utf-8'))

            if 'choices' not in result or len(result['choices']) == 0:
                raise Exception('No response from DeepSeek API')

            content = result['choices'][0]['message']['content'].strip()

            # 解析 JSON
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]

            match_data = json.loads(content.strip())

            # 合併原始職位資料與匹配結果
            matched_job = {
                'id': job.get('id', ''),
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'location': job.get('location', ''),
                'date': job.get('date', ''),
                'url': job.get('url', ''),
                'match_score': match_data.get('match_score', 50),
                'match_reason': match_data.get('match_reason', '待分析'),
                'missing_skills': match_data.get('missing_skills', []),
                'strengths': match_data.get('strengths', [])
            }

            return matched_job

        except Exception as e:
            # 失敗時回傳預設分數
            return {
                'id': job.get('id', ''),
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'location': job.get('location', ''),
                'date': job.get('date', ''),
                'url': job.get('url', ''),
                'match_score': 50,
                'match_reason': f'分析失敗：{str(e)}',
                'missing_skills': [],
                'strengths': []
            }

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
