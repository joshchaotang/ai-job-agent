"""
AI Job Agent - 履歷解析 API v1.0
解析 PDF/DOCX 履歷檔案，提取文字內容
接收 base64 編碼的檔案（適用於 Vercel Serverless Functions）
"""
from http.server import BaseHTTPRequestHandler
import json
import io
import base64

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 讀取 POST body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            if 'file_base64' not in data or 'filename' not in data:
                self.send_error_response(400, 'Missing file_base64 or filename')
                return

            filename = data['filename']
            file_base64 = data['file_base64']

            # 解碼 base64
            try:
                file_data = base64.b64decode(file_base64)
            except Exception as e:
                self.send_error_response(400, f'Invalid base64 data: {str(e)}')
                return

            # 判斷檔案類型並解析
            if filename.lower().endswith('.pdf'):
                text = self.parse_pdf(file_data)
            elif filename.lower().endswith('.docx'):
                text = self.parse_docx(file_data)
            else:
                self.send_error_response(400, 'Unsupported file format. Only PDF and DOCX are supported.')
                return

            if not text or len(text.strip()) < 50:
                self.send_error_response(400, 'Failed to extract meaningful content from the file')
                return

            # 回傳原始文字（Step 1.3 會用 DeepSeek 分析）
            response = {
                'success': True,
                'filename': filename,
                'text': text,
                'length': len(text),
                'message': 'Resume parsed successfully. Text will be analyzed in Step 1.3.'
            }

            self.send_json_response(response)

        except Exception as e:
            self.send_error_response(500, f'Parse error: {str(e)}')

    def parse_pdf(self, file_data):
        """解析 PDF 檔案"""
        try:
            import pypdf
            pdf_file = io.BytesIO(file_data)
            reader = pypdf.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text.strip()
        except ImportError:
            # 備用方案：PyPDF2
            try:
                import PyPDF2
                pdf_file = io.BytesIO(file_data)
                reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
                return text.strip()
            except ImportError:
                raise Exception('PDF parsing library not installed. Please install pypdf or PyPDF2.')

    def parse_docx(self, file_data):
        """解析 DOCX 檔案"""
        try:
            from docx import Document
            docx_file = io.BytesIO(file_data)
            doc = Document(docx_file)
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text.strip()
        except ImportError:
            raise Exception('DOCX parsing library not installed. Please install python-docx.')

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
