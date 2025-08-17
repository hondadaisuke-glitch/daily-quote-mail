# send_mail.py
import os, random, ssl, smtplib
from email.message import EmailMessage
from pathlib import Path

# ★GitHub Secrets から受け取る
YAHOO_USER = os.environ["YAHOO_USER"]
YAHOO_PASS = os.environ["YAHOO_PASS"]
MAIL_TO = os.environ["MAIL_TO"]  # カンマ区切りで複数可

# ★quotes.txt からランダムに1行
lines = Path("quotes.txt").read_text(encoding="utf-8").splitlines()
lines = [l.strip() for l in lines if l.strip()]
quote = random.choice(lines) if lines else "（quotes.txt が空です）"

# ★メール作成
msg = EmailMessage()
msg["Subject"] = "今日の一文"
msg["From"] = YAHOO_USER
msg["To"] = [addr.strip() for addr in MAIL_TO.split(",")]
msg.set_content(quote)

# ★Yahoo!メールのSMTPで送信（SSL, 465）
with smtplib.SMTP_SSL("smtp.mail.yahoo.co.jp", 465, context=ssl.create_default_context()) as server:
    server.login(YAHOO_USER, YAHOO_PASS)
    server.send_message(msg)
