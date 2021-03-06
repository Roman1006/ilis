# -*- coding: utf-8 -*-
# @Time : 2020-12-08 16:40
# @Author : Roman
# @FileName : SendEmail.py
# @Email : 13883575239@163.com
# @Software: PyCharm
#该文件是构造发送邮件的方法，用到python标准库smtplib和email
#可以获取最新的测试报告，把最新的测试报告以文本和附件的形式发送
import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from iLIS import readconf
from iLIS.common.Log import MyLog
import base64
# 路径
path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
reportpath = path_dir + '/report'
testpath = path_dir + '/logs'

local_readConfig =  readconf.Read_conf()


class SendEmail:
    def __init__(self):
        global host, user, password, sender, title
        host = local_readConfig.get_email('mail_host')  # 邮箱服务器
        user = local_readConfig.get_email('mail_user')  # 发件人用户名
        password = local_readConfig.get_email('mail_pass')  # 发件人邮箱授权码，非登录密码
        sender = local_readConfig.get_email('sender')  # 发件人邮箱
        title = local_readConfig.get_email('subject')  # 邮件标题
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.receive_user = local_readConfig.get_email('receiver')  # 收件人邮箱
        self.receive_user_list = []
    def send_email(self):
        """把最新的测试报告以邮件的方式发送"""
        # 构造邮件
        self.logger.info("----------------构造邮件----------------")
        file_new = self.get_new_report()
        f = open(file_new, 'rb')
        content = f.read()
        message = MIMEMultipart()
        message['From'] = "{}".format(sender)  # 发件人
        self.logger.info("----------------发件人%s----------------",sender)
        for i in str(self.receive_user).split('/'):
            self.receive_user_list.append(i)
        message['To'] = ",".join(self.receive_user_list)  # 收件人
        self.logger.info("----------------收件人%s----------------", self.receive_user_list)

        message['Subject'] = Header(title, 'utf-8')  # 标题
        self.logger.info("----------------邮件标题%s----------------", title)
        message.attach(MIMEText(content, 'html', 'utf-8'))

        # 添加附件
        self.logger.info("----------------构造邮件附件----------------")
        testfile = os.path.join(readconf.proDir,"logs")
        reportfile = os.path.join(readconf.proDir,"report")
        testlist = os.listdir(os.path.join(testfile+"\\"))
        reportlist = os.listdir(reportfile)
        testlist.sort(key=lambda fn:os.path.getmtime(testfile + "\\" + fn))
        reportlist.sort(key=lambda fn:os.path.getmtime(reportfile + "\\" + fn))
        test_new = os.path.join(testfile,testlist[-1])
        # print(test_new)
        test_report = os.path.join(reportfile,reportlist[-1])
        self.logger.info("----------------选取最新的log和report文件----------------")
        sendfile = open(test_new,'rb').read()
        time.sleep(1)
        sendreport = open(test_report,'rb').read()
        test_att = MIMEText(sendfile,'base64', 'utf-8')
        test_att1 = MIMEText(sendreport,'base64', 'utf-8')
        test_att ["Content-Type"] = 'application/octet-stream'
        test_att["Content-Disposition"] = 'attachment; filename="testlog.txt"'
        test_att1["Content-Type"] = 'application/octet-stream'
        test_att1["Content-Disposition"] = 'attachment; filename="testreport.html"'
        message.attach(test_att)
        message.attach(test_att1)

        # filename = file_new[-31:]
        # att = MIMEText(content, 'base64', 'utf-8')
        # att["Content-Type"] = 'application/octet-stream'
        # att["Content-Disposition"] = 'attachment; filename=%s' % filename
        # message.attach(att)

        # 发送邮件
        try:
            server = smtplib.SMTP()
            self.logger.info("----------------connect邮件服务----------------")
            server.connect(host)
            self.logger.info("----------------邮箱登录验证----------------")
            server.login(user, password)  # 登录验证
            self.logger.info("----------------邮箱登录验证成功----------------")
            server.sendmail(sender, self.receive_user_list, message.as_string())  # 发送
            self.logger.info("----------------邮件发送----------------")
            server.quit()  # 关闭
            self.logger.info("----------------邮件发送成功！----------------")
            self.logger.info("----------------close邮件服务----------------")
        except smtplib.SMTPException as e:
            self.logger.error("----------------邮件发送失败！请检查邮件配置:%s,%s----------------" , e.smtp_code, e.smtp_error)
        except smtplib.SMTPConnectError as e:
            self.logger.error('----------------邮件发送失败，连接失败:%s,%s----------------', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            self.logger.error('----------------邮件发送失败，认证错误:%s,%s----------------', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            self.logger.error('----------------邮件发送失败，发件人被拒绝:%s,%s----------------', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            self.logger.error('----------------邮件发送失败，收件人被拒绝:%s,%s----------------', e.args, e.recipients)
        except smtplib.SMTPDataError as e:
            self.logger.error('----------------邮件发送失败，数据接收拒绝:%s,%s----------------', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            self.logger.error('----------------邮件发送失败:%s---------------- ', str(e))
        except Exception as e:
            self.logger.error('----------------邮件发送失败:%s---------------- ', str(e))
    def get_new_report(self):
        """获取最新的测试报告"""
        lists = os.listdir(reportpath)
        if lists:
            lists.sort(key=lambda fn: os.path.getmtime(reportpath + '\\' + fn))
            file_new = os.path.join(reportpath, lists[-1])
            return file_new