import feedparser
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

RSS_URL = "https://community.sap.com/t5/technology-blogs-by-members/bg-p/technology-blog-membersblog-board/label-name/basis/rss"

GMAIL_USER = "yerraradhakrishnasap@gmail.com"
GMAIL_APP_PASSWORD = "Capacitor@5629"
TO_EMAIL = "yerraradhakrishnasap@gmail.com"

KEYWORDS = [
    "kernel", "hana", "netweaver", "dispatcher" "BTP" "ALM",
    "enqueue", "icm", "spool", "st22", "sm21",
    "update", "patch", "security"
]

feed = feedparser.parse(RSS_URL)

items = []
for entry in feed.entries[:20]:
    text = f"{entry.title} {entry.summary}".lower()
    if any(k in text for k in KEYWORDS):
        items.append(f"- {entry.title}\n  {entry.link}\n")

if not items:
    print("No matching SAP Basis issues found.")
    raise SystemExit(0)

body = f"""
SAP Basis Digest - {datetime.now():%Y-%m-%d %H:%M}

Latest matching community posts:

{chr(10).join(items)}
"""

msg = MIMEText(body)
msg["Subject"] = "SAP Basis Community Digest"
msg["From"] = GMAIL_USER
msg["To"] = TO_EMAIL

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.send_message(msg)

print("Email sent successfully.")
