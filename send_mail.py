# send_mail.py (Yahoo復旧用: 465→587自動フォールバック)
import os, random, ssl, smtplib, sys, traceback
from email.message import EmailMessage
from pathlib import Path

YAHOO_USER = os.environ["YAHOO_USER"]
YAHOO_PASS = os.environ["YAHOO_PASS"]
MAIL_TO    = os.environ["MAIL_TO"]

lines = [l.strip() for l in Path("quotes.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
quote = random.choice(lines) if lines else "（quotes.txt が空です）"

msg = EmailMessage()
msg["Subject"] = "今日の一文"
msg["From"] = YAHOO_USER
msg["To"] = [a.strip() for a in MAIL_TO.split(",")]
msg.set_content(quote)

ctx = ssl.create_default_context()

def send_via_ssl_465():
    with smtplib.SMTP_SSL("smtp.mail.yahoo.co.jp", 465, context=ctx) as s:
        s.set_debuglevel(1)  # ログ出力
        s.login(YAHOO_USER, YAHOO_PASS)
        s.send_message(msg)

def send_via_starttls_587():
    with smtplib.SMTP("smtp.mail.yahoo.co.jp", 587) as s:
        s.set_debuglevel(1)
        s.ehlo()
        s.starttls(context=ctx)  # ← STARTTLS
        s.ehlo()
        s.login(YAHOO_USER, YAHOO_PASS)
        s.send_message(msg)

try:
    send_via_ssl_465()
    print("OK via 465/SSL")
except Exception as e1:
    print("SSL(465) 失敗:", e1)
    try:
        send_via_starttls_587()
        print("OK via 587/STARTTLS")
    except Exception as e2:
        print("STARTTLS(587) も失敗:", e2)
        traceback.print_exc()
        sys.exit(1)

