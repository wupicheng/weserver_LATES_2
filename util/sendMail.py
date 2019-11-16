#coding=utf-8

# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header

import smtplib
from email.mime.text import MIMEText
from email.header import Header

class SendMail:

    @staticmethod
    def  sendMail(to_addrs,checkcode):
        print()
        from_addr = 'wupicheng@qq.com'  # 邮件发送账号
        # to_addrs = 'accept@qq.com'  # 接收邮件账号
        qqCode = 'cqomtawwhwkvcaee'  # 授权码（这个要填自己获取到的）
        smtp_server = 'smtp.qq.com'  # 固定写死
        smtp_port = 465  # 固定端口

        # 配置服务器
        stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        stmp.login(from_addr, qqCode)

        # 组装发送内容
        message = MIMEText('白杨在线网课正在重置密码，请输入以下验证码：'+checkcode+'  有效期30分钟', 'plain', 'utf-8')  # 发送的内容
        message['From'] = Header("wupicheng@qq.com", 'utf-8')  # 发件人
        message['To'] = Header(to_addrs, 'utf-8')  # 收件人
        subject = '白杨在线网课重置密码验证码邮件'
        message['Subject'] = Header(subject, 'utf-8')  # 邮件标题

        try:
            stmp.sendmail(from_addr, to_addrs, message.as_string())
        except Exception as e:
            print('邮件发送失败--' + str(e))
        print('邮件发送成功')


# SendMail.sendMail("tuobu_a@sohu.com","5678")
