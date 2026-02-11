"""
AI Job Agent - JobSpy 爬蟲 API v1.0
只爬 Indeed（無限流），配合官方 API 做混合來源
"""
from http.server import BaseHTTPRequestHandler
import json
import os


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 讀取 POST body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            keywords = data.get('keywords', '')
            location = data.get('location', 'Remote')
            results_wanted = data.get('results_wanted', 50)

            if not keywords:
                self.send_error_response(400, 'Missing keywords parameter')
                return

            # 只爬 Indeed（無限流）
            jobs = self.scrape_indeed(keywords, location, results_wanted)

            response = {
                'success': True,
                'jobs': jobs,
                'total': len(jobs),
                'source': 'Indeed (JobSpy)',
                'message': f'Scraped {len(jobs)} jobs from Indeed'
            }

            self.send_json_response(response)

        except Exception as e:
            self.send_error_response(500, f'Scraping error: {str(e)}')

    def scrape_indeed(self, keywords, location, results_wanted):
        """使用 JobSpy 爬取 Indeed 職位"""
        try:
            from jobspy import scrape_jobs

            # JobSpy 參數
            jobs_df = scrape_jobs(
                site_name=["indeed"],  # 只爬 Indeed（無限流）
                search_term=keywords,
                location=location,
                results_wanted=results_wanted,
                hours_old=168,  # 一週內的職位
                country_indeed='USA'  # 可改為其他國家
            )

            # 轉換 DataFrame 到 JSON
            if jobs_df is None or len(jobs_df) == 0:
                return []

            jobs = []
            for _, row in jobs_df.iterrows():
                job = {
                    'id': f"indeed_{row.get('id', '')}",
                    'title': row.get('title', 'Untitled'),
                    'company': row.get('company', 'Unknown'),
                    'location': row.get('location', 'Remote'),
                    'date': row.get('date_posted', ''),
                    'url': row.get('job_url', ''),
                    'description': row.get('description', '')[:500],  # 限制長度
                    'salary': row.get('min_amount', ''),
                    'source': 'Indeed'
                }
                jobs.append(job)

            return jobs

        except ImportError:
            raise Exception('JobSpy not installed. Please run: pip install python-jobspy')
        except Exception as e:
            raise Exception(f'JobSpy scraping failed: {str(e)}')

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
