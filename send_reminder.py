
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os

# 이메일 정보 (환경변수 또는 GitHub Secrets로 설정)
EMAIL_ADDR = os.environ["EMAIL_ADDR"]
EMAIL_PASS = os.environ["EMAIL_PASS"]

# 엑셀 파일 불러오기
df = pd.read_excel("rental_contracts.xlsx")
df["만기일"] = pd.to_datetime(df["만기일"])

# 오늘 기준 30~70일 이내 만기 필터링
today = datetime.today()
target_start = today + timedelta(days=30)
target_end = today + timedelta(days=70)
df_notify = df[(df["만기일"] >= target_start) & (df["만기일"] <= target_end)]

# 이메일 발송
if not df_notify.empty:
    with smtpllib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDR, EMAIL_PASS)
        for _, row in df_notify.iterrows():
            html_content = f"""<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
      <h2 style="color: #2E86C1;">🏠 임대 계약 만기 알림</h2>
      <p><strong>📍 주소:</strong> {row['주소']}</p>
      <p><strong>👤 임차인:</strong> {row['임차인']}</p>
      <p><strong>💰 보증금:</strong> {row['보증금']:,} 원</p>
      <p><strong>🏢 부동산:</strong> {row['부동산']}</p>
      <p><strong>🗓 만기일:</strong> {row['만기일'].date()}</p>
      <hr style="margin: 20px 0;">
      <p style="font-size: 0.9em; color: #888;">본 메일은 임대 관리 자동화 시스템에서 발송되었습니다.</p>
    </div>
  </body>
</html>
"""
            msg = MIMEText(html_content, "html")
            msg["Subject"] = f"[알림] 임대 만기 예정 - {row['주소']} ({row['만기일'].date()})"
            msg["From"] = EMAIL_ADDR
            msg["To"] = EMAIL_ADDR  # 또는 row['임차인 이메일']

            smtp.send_message(msg)
else:
    print("알림 대상 계약 없음.")
