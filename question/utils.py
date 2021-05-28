from email.header import Header
from email.mime.text import MIMEText
import smtplib


def sendEmail(receivers, subject, content):
    mail_host = 'smtp.qq.com'
    mail_user = '1506607292@qq.com'
    mail_pass = 'reuymrffxxxriidd'
    sender = '1506607292@qq.com'
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = subject
    message['From'] = sender
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(
            sender, [receivers], message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)


# 邮件发送
def SendEmail(recipients, subject, content):
    sender = '1506607292@qq.com'  # 发件人邮箱
    password = 'reuymrffxxxriidd'  # 发件人邮箱密码
    # 收件人邮箱
    host = 'smtp.qq.com' # 发件人邮箱主机
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = recipients
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP_SSL(host, 465)
    server.login(sender, password)
    server.sendmail(sender, [recipients], msg.as_string())
    server.quit()


if __name__ == '__main__':
    with open('test.html', 'r') as f:
        SendEmail('2742331300@qq.com', 'question url for you', f.read())
