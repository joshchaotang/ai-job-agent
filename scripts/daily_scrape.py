#!/usr/bin/env python3
"""
AI Job Agent - 每日自動爬蟲 + AI 匹配 + 郵件推送
由 GitHub Actions 定時執行（早/中/晚）
"""
import argparse
import json
import os
import random
import time
from datetime import datetime
from jobspy import scrape_jobs
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


# 使用者設定（從環境變數讀取）
USER_RESUME = {
    "skills": ["Python", "JavaScript", "React", "Node.js", "Docker", "AWS"],
    "experience": [
        {"title": "Software Engineer", "company": "Tech Corp", "years": 3}
    ],
    "education": "Bachelor in Computer Science"
}

SEARCH_KEYWORDS = os.environ.get('SEARCH_KEYWORDS', 'software engineer python')
SEARCH_LOCATION = os.environ.get('SEARCH_LOCATION', 'Remote')


def scrape_all_sources(keywords, location, limit=25):
    """
    混合來源爬取（模擬 aggregate_jobs.py 的邏輯）
    """
    all_jobs = []

    # 1. JobSpy 爬 Indeed（無限流）
    print(f"[{datetime.now()}] Scraping Indeed...")
    try:
        jobs_df = scrape_jobs(
            site_name=["indeed"],
            search_term=keywords,
            location=location,
            results_wanted=limit,
            hours_old=168
        )

        if jobs_df is not None and len(jobs_df) > 0:
            for _, row in jobs_df.iterrows():
                all_jobs.append({
                    'id': f"indeed_{row.get('id', '')}",
                    'title': row.get('title', 'Untitled'),
                    'company': row.get('company', 'Unknown'),
                    'location': row.get('location', 'Remote'),
                    'url': row.get('job_url', ''),
                    'source': 'Indeed'
                })
        print(f"  → Indeed: {len(all_jobs)} jobs")
    except Exception as e:
        print(f"  → Indeed failed: {str(e)}")

    # 2. Remotive API
    print(f"[{datetime.now()}] Fetching Remotive...")
    try:
        url = f"https://remotive.com/api/remote-jobs?search={keywords}&limit={limit}"
        res = requests.get(url, timeout=15)
        data = res.json()

        for job in data.get('jobs', [])[:limit]:
            all_jobs.append({
                'id': f"remotive_{job.get('id', '')}",
                'title': job.get('title', 'Untitled'),
                'company': job.get('company_name', 'Unknown'),
                'location': 'Remote',
                'url': job.get('url', ''),
                'source': 'Remotive'
            })
        print(f"  → Remotive: +{len([j for j in all_jobs if j['source']=='Remotive'])} jobs")
    except Exception as e:
        print(f"  → Remotive failed: {str(e)}")

    # 3. Arbeitnow API
    print(f"[{datetime.now()}] Fetching Arbeitnow...")
    try:
        url = f"https://arbeitnow.com/api/job-board-api?search={keywords}"
        res = requests.get(url, timeout=15)
        data = res.json()

        for job in data.get('data', [])[:limit]:
            all_jobs.append({
                'id': f"arbeitnow_{job.get('slug', '')}",
                'title': job.get('title', 'Untitled'),
                'company': job.get('company_name', 'Unknown'),
                'location': job.get('location', 'Remote'),
                'url': job.get('url', ''),
                'source': 'Arbeitnow'
            })
        print(f"  → Arbeitnow: +{len([j for j in all_jobs if j['source']=='Arbeitnow'])} jobs")
    except Exception as e:
        print(f"  → Arbeitnow failed: {str(e)}")

    # 去重
    unique_jobs = deduplicate_jobs(all_jobs)
    print(f"[{datetime.now()}] Total unique jobs: {len(unique_jobs)}")

    return unique_jobs


def deduplicate_jobs(jobs):
    """去重：依 URL + 公司名 + 職位名"""
    seen = set()
    unique_jobs = []

    for job in jobs:
        key = (
            job.get('url', ''),
            job.get('company', '').lower(),
            job.get('title', '').lower()
        )
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs


def match_jobs_simple(jobs, resume):
    """
    簡化版匹配（不呼叫 DeepSeek API，用關鍵字匹配）
    節省 API 成本，適合每日自動執行
    """
    user_skills = set([s.lower() for s in resume.get('skills', [])])
    matched_jobs = []

    for job in jobs:
        title = job.get('title', '').lower()
        company = job.get('company', '').lower()

        # 簡單匹配：技能出現在職位名稱中
        matches = [skill for skill in user_skills if skill in title]
        score = min(100, len(matches) * 15 + 50)  # 每個匹配技能 +15 分，基礎分 50

        job['match_score'] = score
        job['matched_skills'] = matches
        matched_jobs.append(job)

    # 排序
    matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    return matched_jobs


def send_email(jobs, time_label):
    """發送郵件（HTML 格式）"""
    email_user = os.environ.get('EMAIL_USER', '')
    email_pass = os.environ.get('EMAIL_PASS', '')
    email_to = os.environ.get('EMAIL_TO', '')

    if not email_user or not email_pass or not email_to:
        print("Email credentials not configured, skipping email")
        return

    # 建立 HTML 郵件
    html = f"""
<html>
<head>
<style>
  body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
  .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; }}
  h1 {{ color: #F37021; }}
  .job-card {{ background: #f9f9f9; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #F37021; }}
  .job-title {{ font-size: 18px; font-weight: bold; color: #333; }}
  .job-company {{ color: #666; margin: 5px 0; }}
  .match-score {{ background: #3FB950; color: white; padding: 5px 12px; border-radius: 16px; font-weight: bold; display: inline-block; margin-top: 10px; }}
  .matched-skills {{ color: #F37021; font-size: 13px; margin-top: 8px; }}
  a {{ color: #F37021; text-decoration: none; }}
</style>
</head>
<body>
<div class="container">
  <h1>🎯 AI Job Agent - {time_label.capitalize()} Report</h1>
  <p>找到 <strong>{len(jobs)}</strong> 個推薦職位（依匹配度排序）</p>
  <hr>
"""

    for i, job in enumerate(jobs[:15], 1):  # Top 15
        html += f"""
  <div class="job-card">
    <div class="job-title">{i}. {job['title']}</div>
    <div class="job-company">🏢 {job['company']} · 📍 {job['location']} · 來源：{job['source']}</div>
    <span class="match-score">{job['match_score']}% 匹配</span>
    <div class="matched-skills">✨ 匹配技能：{', '.join(job.get('matched_skills', []))}</div>
    <div style="margin-top: 10px;"><a href="{job['url']}" target="_blank">→ 查看職位詳情</a></div>
  </div>
"""

    html += """
  <hr>
  <p style="color: #999; font-size: 12px; text-align: center;">
    Generated by AI Job Agent v3.1.0 Atlas Edition<br>
    Powered by DeepSeek + JobSpy
  </p>
</div>
</body>
</html>
"""

    # 發送郵件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🎯 AI Job Agent - {len(jobs)} 個推薦職位 ({time_label.capitalize()})'
    msg['From'] = email_user
    msg['To'] = email_to

    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
        print(f"[{datetime.now()}] Email sent to {email_to}")
    except Exception as e:
        print(f"[{datetime.now()}] Email failed: {str(e)}")


def send_telegram(jobs, time_label):
    """發送 Telegram 通知"""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')

    if not bot_token or not chat_id:
        print("Telegram credentials not configured, skipping telegram")
        return

    # 格式化訊息（Telegram Markdown）
    message = f"*🎯 AI Job Agent - {time_label.capitalize()} Report*\n\n"
    message += f"找到 *{len(jobs)}* 個推薦職位\n"
    message += "─" * 30 + "\n\n"

    for i, job in enumerate(jobs[:10], 1):  # Top 10
        match_score = job.get('match_score', 0)
        emoji = '🔥' if match_score >= 85 else '⭐' if match_score >= 70 else '📌'

        message += f"{emoji} *{i}. {job['title']}*\n"
        message += f"🏢 {job['company']} · 📍 {job['location']}\n"
        message += f"🎯 匹配度：*{match_score}%*\n"

        matched_skills = job.get('matched_skills', [])
        if matched_skills:
            message += f"✨ {', '.join(matched_skills[:3])}\n"

        if job.get('url'):
            message += f"[→ 查看職位]({job['url']})\n"

        message += "\n"

    message += "─" * 30 + "\n"
    message += "_Generated by AI Job Agent v3.3.0_"

    # 發送到 Telegram
    try:
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }

        response = requests.post(telegram_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[{datetime.now()}] Telegram sent to chat_id: {chat_id}")
    except Exception as e:
        print(f"[{datetime.now()}] Telegram failed: {str(e)}")


def send_slack(jobs, time_label):
    """發送 Slack Webhook 通知"""
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL', '')

    if not webhook_url:
        print("Slack Webhook URL not configured, skipping slack")
        return

    # 建立 Slack 訊息格式（Block Kit）
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🎯 AI Job Agent - {time_label.capitalize()} Report",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"找到 *{len(jobs)}* 個推薦職位"
            }
        },
        {"type": "divider"}
    ]

    # 職位卡片（Top 10）
    for i, job in enumerate(jobs[:10], 1):
        match_score = job.get('match_score', 0)
        emoji = '🔥' if match_score >= 85 else '⭐' if match_score >= 70 else '📌'

        matched_skills = job.get('matched_skills', [])
        skills_text = f"\n✨ {', '.join(matched_skills[:3])}" if matched_skills else ""

        job_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{emoji} *{i}. {job['title']}*\n"
                        f"🏢 {job['company']} · 📍 {job['location']}\n"
                        f"🎯 匹配度：*{match_score}%*{skills_text}"
            }
        }

        if job.get('url'):
            job_block["accessory"] = {
                "type": "button",
                "text": {"type": "plain_text", "text": "查看職位", "emoji": True},
                "url": job['url'],
                "style": "primary" if match_score >= 85 else "default"
            }

        blocks.append(job_block)

    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": "_Generated by AI Job Agent v3.4.0_"}]
    })

    # 發送到 Slack
    try:
        payload = {"blocks": blocks, "text": f"AI Job Agent - {time_label.capitalize()} Report"}
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[{datetime.now()}] Slack sent successfully")
    except Exception as e:
        print(f"[{datetime.now()}] Slack failed: {str(e)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--time', default='morning', choices=['morning', 'noon', 'evening'])
    args = parser.parse_args()

    print(f"{'='*60}")
    print(f"AI Job Agent - Daily Scrape ({args.time.upper()})")
    print(f"Time: {datetime.now()}")
    print(f"Keywords: {SEARCH_KEYWORDS}")
    print(f"Location: {SEARCH_LOCATION}")
    print(f"{'='*60}\n")

    # 隨機延遲（模擬真人，2-5 秒）
    delay = random.uniform(2, 5)
    print(f"Random delay: {delay:.2f}s")
    time.sleep(delay)

    # 爬取職位
    jobs = scrape_all_sources(SEARCH_KEYWORDS, SEARCH_LOCATION, limit=25)

    if len(jobs) == 0:
        print("No jobs found, exiting")
        return

    # 簡單匹配
    matched_jobs = match_jobs_simple(jobs, USER_RESUME)

    # 發送通知（郵件 + Telegram + Slack）
    send_email(matched_jobs, args.time)
    send_telegram(matched_jobs, args.time)
    send_slack(matched_jobs, args.time)

    print(f"\n{'='*60}")
    print(f"Daily scrape completed!")
    print(f"Total jobs: {len(matched_jobs)}")
    print(f"Top 5 matches:")
    for i, job in enumerate(matched_jobs[:5], 1):
        print(f"  {i}. [{job['match_score']}%] {job['title']} @ {job['company']}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
