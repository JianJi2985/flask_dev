import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = "2419335621@qq.com"
token = "ipuplztjgrzodieh"
smtp_svr = "smtp.qq.com"
smtp_port = 465

# send_plain_mail 发送纯文本邮件
# @param target 目标邮箱地址：
# @param subject 主题，邮件标题
# @param text 要发送的内容，纯文本形式
def send_plain_mail(target: str, subject: str, text: str):
    message = MIMEText(text, "plain", "utf-8")
    message["From"] = Header(sender, "utf-8")
    message["To"] = Header(target, "utf-8")
    message["Subject"] = Header(subject, "utf-8")

    smtp = smtplib.SMTP_SSL(smtp_svr, smtp_port)
    smtp.login(sender, token)
    smtp.sendmail(sender, [target], message.as_string())


# send_plain_mail 发送纯文本邮件
# @param target 目标邮箱地址：
# @param subject 主题，邮件标题
# @param html 要发送的内容，html 形式
def send_html_mail(target: str, subject: str, html: str):
    message = MIMEText(html, "html", "utf-8")
    message["From"] = Header(sender, "utf-8")
    message["To"] = Header(target, "utf-8")
    message["Subject"] = Header(subject, "utf-8")

    smtp = smtplib.SMTP_SSL(smtp_svr, smtp_port)
    smtp.login(sender, token)
    smtp.sendmail(sender, [target], message.as_string())

