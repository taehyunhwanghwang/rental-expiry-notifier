import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os

# 이메일 정보 (GitHub Secrets 등에서 설정)
EMAIL_ADDR = os.environ["EMAIL_ADDR"]
EMAIL_PASS = os.environ["EMAIL_PASS"]

# 엑셀 파일 로드
df = pd.read_excel("rental_contracts.xlsx")
df["만기일"] = pd.to_datetime(df["만기일"])

# 날짜 필터링: 오늘부터 30~70일 이내
today = datetime.today()
target_start = today + timedelta(days=30)
target_end = today + timedelta(days=70)

df_notify = df[(df["만기일"] >= target_start) & (df["만기일"] <= target_end)]

# 이메일 발송
if not df_notify.empty:
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDR, EMAIL_PASS)
        for _, row in df_notify.iterrows():
            msg = MIMEText(f"""
[임대 계약 만기 알림]
ID: {row['ID']}
주소: {row['주소']}
부동산: {row['부동산']}
임차인: {row['임차인']}
만기일: {row['만기일'].date()}
""")
            msg["Subject"] = f"[알림] 임대 만기 예정 - {row['주소']} ({row['만기일'].date()})"
            msg["From"] = EMAIL_ADDR
            msg["To"] = EMAIL_ADDR  # 본인 확인용 또는 관리용 이메일

            smtp.send_message(msg)
else:
    print("알림 대상 계약 없음.")
