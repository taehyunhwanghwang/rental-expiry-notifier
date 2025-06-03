# HTML 문자열 내부 들여쓰기 문제를 해결하여 코드 재생성

modified_code = """
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

# 이메일 발송 (종합 요약 메일 방식)
if not df_notify.empty:
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDR, EMAIL_PASS)

        rows_html = ""
        for _, row in df_notify.iterrows():
            rows_html += f\"\"\"
<tr>
  <td>{row['주소']}</td>
  <td>{row['임차인']}</td>
  <td>{row['보증금']:,} 원</td>
  <td>{row['부동산']}</td>
  <td>{row['만기일'].date()}</td>
</tr>
\"\"\"

        html_content = f\"\"\"\
<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 800px; margin: auto; border: 1px solid #ccc; padding: 20px; border-radius: 10px;">
      <h2 style="color: #2E86C1;">🏠 임대 계약 만기 알림 ({len(df_notify)}건)</h2>
      <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <tr style="background-color: #f2f2f2;">
          <th>주소</th><th>임차인</th><th>보증금</th><th>부동산</th><th>만기일</th>
        </tr>
        {rows_html}
      </table>
      <p style="font-size: 0.9em; color: #888; margin-top: 20px;">본 메일은 임대 관리 자동화 시스템에서 발송되었습니다.</p>
    </div>
  </body>
</html>
\"\"\"

        msg = MIMEText(html_content, "html")
        msg["Subject"] = f"[알림] 임대 만기 예정 계약 {len(df_notify)}건"
        msg["From"] = EMAIL_ADDR
        msg["To"] = EMAIL_ADDR

        smtp.send_message(msg)
else:
    print("알림 대상 계약 없음.")
"""

# 저장
file_path = "/mnt/data/send_reminder_summary.py"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(modified_code)

file_path
