def sendEmail(receivers, subject, content):
    import smtplib
    from email.mime.text import MIMEText
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
            sender, receivers, message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)


if __name__ == '__main__':
    with open('test.html', 'r') as f:
        sendEmail(['2742331300@qq.com'], 'question url for you', f.read())
