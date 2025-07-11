import smtplib
from email.mime.text import MIMEText

From = "rohitpawar92006@gmail.com"
To = "recipient@example.com"

msg = MIMEText("This is the body of the email.")
msg['Subject'] = "Test Email"
msg['From'] = From
msg['To'] = To

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(From, "utxwq")
    server.sendmail(From, [To], msg.as_string())
if not To or '@' not in To:
    raise ValueError("Invalid recipient email address.")
