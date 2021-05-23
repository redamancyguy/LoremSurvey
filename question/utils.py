def sendEmail(receiver, subject,content):
    import smtplib
    from email.mime.text import MIMEText
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.qq.com'
    # 163用户名
    mail_user = '1506607292@qq.com'
    # 密码(部分邮箱为授权码)
    mail_pass = 'reuymrffxxxriidd'
    # 邮件发送方邮箱地址
    sender = '1506607292@qq.com'
    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = subject
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receiver

    message['url'] = None

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        receivers = []
        receivers.append(receiver)
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误


if __name__ == '__main__':
    sendEmail('2742331300@qq.com','question url for you','please answer your question there ,url: http://www.1506607292.top')