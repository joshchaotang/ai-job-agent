"""
AI Job Agent - 混合來源聚合 API v1.0
整合 JobSpy(Indeed) + Remotive + Arbeitnow + Adzuna，去重後回傳
"""
from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 讀取 POST body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            keywords = data.get('keywords', '')
            location = data.get('location', 'Remote')
            limit_per_source = data.get('limit_per_source', 25)

            if not keywords:
                self.send_error_response(400, 'Missing keywords parameter')
                return

            # 並行抓取多個來源
            all_jobs = self.fetch_all_sources(keywords, location, limit_per_source)

            # 去重
            unique_jobs = self.deduplicate_jobs(all_jobs)

            response = {
                'success': True,
                'jobs': unique_jobs,
                'total': len(unique_jobs),
                'sources': {
                    'indeed': len([j for j in unique_jobs if j.get('source') == 'Indeed']),
                    'remotive': len([j for j in unique_jobs if j.get('source') == 'Remotive']),
                    'arbeitnow': len([j for j in unique_jobs if j.get('source') == 'Arbeitnow']),
                    'adzuna': len([j for j in unique_jobs if j.get('source') == 'Adzuna'])
                },
                'message': f'Aggregated {len(unique_jobs)} unique jobs from 4 sources'
            }

            self.send_json_response(response)

        except Exception as e:
            self.send_error_response(500, f'Aggregation error: {str(e)}')

    def fetch_all_sources(self, keywords, location, limit):
        """並行抓取所有來源"""
        jobs = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.fetch_indeed, keywords, location, limit): 'Indeed',
                executor.submit(self.fetch_remotive, keywords, limit): 'Remotive',
                executor.submit(self.fetch_arbeitnow, keywords, limit): 'Arbeitnow',
                executor.submit(self.fetch_adzuna, keywords, location, limit): 'Adzuna'
            }

            for future in as_completed(futures):
                source = futures[future]
                try:
                    result = future.result()
                    jobs.extend(result)
                except Exception as e:
                    print(f"{source} fetch failed: {str(e)}")

        return jobs

    def fetch_indeed(self, keywords, location, limit):
        """JobSpy 爬 Indeed（無限流）"""
        try:
            from jobspy import scrape_jobs
            jobs_df = scrape_jobs(
                site_name=["indeed"],
                search_term=keywords,
                location=location,
                results_wanted=limit,
                hours_old=168
            )

            if jobs_df is None or len(jobs_df) == 0:
                return []

            jobs = []
            for _, row in jobs_df.iterrows():
                jobs.append({
                    'id': f"indeed_{row.get('id', '')}",
                    'title': row.get('title', 'Untitled'),
                    'company': row.get('company', 'Unknown'),
                    'location': row.get('location', 'Remote'),
                    'date': str(row.get('date_posted', '')),
                    'url': row.get('job_url', ''),
                    'source': 'Indeed'
                })

            return jobs[:limit]

        except Exception as e:
            print(f"Indeed fetch error: {str(e)}")
            return []

    def fetch_remotive(self, keywords, limit):
        """Remotive API（官方，無限流）"""
        try:
            url = f"https://remotive.com/api/remote-jobs?search={quote(keywords)}&limit={limit}"
            req = Request(url)
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))

            jobs = []
            for job in data.get('jobs', [])[:limit]:
                jobs.append({
                    'id': f"remotive_{job.get('id', '')}",
                    'title': job.get('title', 'Untitled'),
                    'company': job.get('company_name', 'Unknown'),
                    'location': 'Remote',
                    'date': job.get('publication_date', '')[:10],
                    'url': job.get('url', ''),
                    'source': 'Remotive'
                })

            return jobs

        except Exception as e:
            print(f"Remotive fetch error: {str(e)}")
            return []

    def fetch_arbeitnow(self, keywords, limit):
        """Arbeitnow API（官方，無限流）"""
        try:
            url = f"https://arbeitnow.com/api/job-board-api?search={quote(keywords)}"
            req = Request(url)
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))

            jobs = []
            for job in data.get('data', [])[:limit]:
                jobs.append({
                    'id': f"arbeitnow_{job.get('slug', '')}",
                    'title': job.get('title', 'Untitled'),
                    'company': job.get('company_name', 'Unknown'),
                    'location': job.get('location', 'Remote'),
                    'date': job.get('created_at', '')[:10],
                    'url': job.get('url', ''),
                    'source': 'Arbeitnow'
                })

            return jobs

        except Exception as e:
            print(f"Arbeitnow fetch error: {str(e)}")
            return []

    def fetch_adzuna(self, keywords, location, limit):
        """Adzuna API（官方，需 API Key）"""
        try:
            app_id = os.environ.get('ADZUNA_APP_ID', '')
            app_key = os.environ.get('ADZUNA_APP_KEY', '')

            if not app_id or not app_key:
                print("Adzuna API credentials not configured")
                return []

            url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={app_id}&app_key={app_key}&results_per_page={limit}&what={quote(keywords)}&where={quote(location)}"
            req = Request(url)
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))

            jobs = []
            for job in data.get('results', [])[:limit]:
                jobs.append({
                    'id': f"adzuna_{job.get('id', '')}",
                    'title': job.get('title', 'Untitled'),
                    'company': job.get('company', {}).get('display_name', 'Unknown'),
                    'location': job.get('location', {}).get('display_name', 'Remote'),
                    'date': job.get('created', '')[:10],
                    'url': job.get('redirect_url', ''),
                    'source': 'Adzuna'
                })

            return jobs

        except Exception as e:
            print(f"Adzuna fetch error: {str(e)}")
            return []

    def deduplicate_jobs(self, jobs):
        """去重：依 URL + 公司名 + 職位名"""
        seen = set()
        unique_jobs = []

        for job in jobs:
            # 建立唯一鍵
            key = (
                job.get('url', ''),
                job.get('company', '').lower(),
                job.get('title', '').lower()
            )

            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        return unique_jobs

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
