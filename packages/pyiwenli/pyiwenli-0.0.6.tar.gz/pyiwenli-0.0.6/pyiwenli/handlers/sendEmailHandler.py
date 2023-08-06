#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-12-06 20:49:36
LastEditors: iwenli
LastEditTime: 2020-12-07 13:15:56
Description: 发送邮件
'''
__author__ = 'iwenli'

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr


class SendEmailHandler(object):
    """
    发送邮件
    """
    def __init__(self, **kwargs):
        """[实例化]
        参数：
            kwargs = {
                "host": "smtp.exmail.qq.com",
                "port": 465,
                "user": "open@iwenli.org",
                "password": os.getenv("emall_pwd"),
                "sender": "open@iwenli.org",
                "display":"ebook-spider"
                "ssl":False
            }
        """
        self.user = kwargs.get("user", "open@iwenli.org")
        self.password = kwargs.get("password", "")
        self.host = kwargs.get("host", "smtp.exmail.qq.com")
        self.port = kwargs.get("port", 465)
        self.display = kwargs.get("display", "iwenli.org")
        self.sender = kwargs.get("sender", "open@iwenli.org")
        self.ssl = kwargs.get("ssl", True)

        if self.ssl:
            self.smtp = smtplib.SMTP_SSL(self.host, self.port)
        else:
            self.smtp = smtplib.SMTP(self.host, self.port)

    def send_text(self, to, subject, text, **kwargs):
        """[发送 TEXT 邮件]

        Args:
            to ([list]]): [收件人列表]
            subject ([string]): [邮件标题]
            text ([string]): [邮件内容]
        """
        content = MIMEText(text, 'plain', 'utf-8')
        return self.__send(to, subject, content, **kwargs)

    def send_html(self, to, subject, html, **kwargs):
        """[发送 HTML 邮件]

        Args:
            to ([list]]): [收件人列表]
            subject ([string]): [邮件标题]
            html ([string]): [邮件内容]
        """
        content = MIMEText(html, 'html', 'utf-8')
        return self.__send(to, subject, content, **kwargs)

    def __check_receiver(self, addrs):
        """[检测是否是标准的收件地址集合]

        Args:
            addrs ([string | list]): [收件地址：收件人，抄送，密送]

        Returns:
            [list]: [标准的收件地址集合]
        """
        if not isinstance(addrs, list):
            addrs = [addrs]
        return addrs

    def __gen_header(self, addrs):
        """[将收件地址转换为标准的 Header]

        Args:
            addrs ([list]): [description]

        Returns:
            [type]: [description]
        """

        return ",".join([
            formataddr((Header(addr, 'utf-8').encode(), addr))
            for addr in addrs
        ])

    def __send(self, to, subject, content, **kwargs):
        """[发送邮件的具体实现]

        Args:
            to ([list]]): [收件人列表]
            subject ([string]): [邮件标题]
            content ([MIMEText]): [邮件内容]
        """
        msg, files = None, None
        # 构建正文和附件
        if "files" in kwargs:
            files = kwargs["files"]

        if files is None:
            msg = content
        else:
            # 创建一个带附件的实例
            msg = MIMEMultipart()
            # 附加正文
            msg.attach(content)
            for file in files:
                # 添加附加
                file_name = os.path.split(file)[1]
                part = MIMEApplication(open(file, 'rb').read())
                part.add_header('Content-Disposition',
                                'attachment',
                                filename='%s' % file_name)
                msg.attach(part)

        # 构建标题
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = formataddr((Header(self.display,
                                         'utf-8').encode(), self.sender))

        # 构建收件人
        to = self.__check_receiver(to)
        cc, bcc = None, None
        receivers = []
        # 抄送
        if "cc" in kwargs:
            cc = self.__check_receiver(kwargs["cc"])
        # 密送
        if "bcc" in kwargs:
            bcc = self.__check_receiver(kwargs["bcc"])

        if to is not None and len(to) > 0:
            receivers.extend(to)
            msg['To'] = self.__gen_header(to)

        if cc is not None and len(cc) > 0:
            receivers.extend(cc)
            msg['Cc'] = self.__gen_header(cc)

        if bcc is not None and len(bcc) > 0:
            receivers.extend(bcc)
            msg['Bcc'] = self.__gen_header(bcc)

        try:
            self.smtp.login(self.user, self.password)
            self.smtp.sendmail(self.sender, receivers, msg.as_string())
            return True
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.smtp.quit()


if __name__ == '__main__':
    dic = {
        "host": "smtp.exmail.qq.com",
        "user": "open@iwenli.org",
        "password": os.getenv("email_pwd"),
        "port": 465,
        "display": "ebook-spider",
        "sender": "open@iwenli.org",
        "ssl": True
    }

    handler = SendEmailHandler(**dic)
    # res = handler.send_text(
    #     "admin@iwenli.org",
    #     "邮件标题",
    #     "邮件内容",
    #     # cc="499243647@qq.com",
    #     # bcc="zhangyulong0203@gmail.com",
    #     files=["D:\\0.data\\1.self\\4.python\\pyiwenli\\readme.md"])

    html = """<h1>标题</h1>
  <h2>小标题</h1>
    <table>
      <tr>
        <td>1</td>
        <td>2</td>
        <td>3</td>
      </tr>
      <tr>
        <td>11</td>
        <td>22</td>
        <td>33</td>
      </tr>
      <tr>
        <td>111</td>
        <td>222</td>
        <td>333</td>
      </tr>
    </table>"""
    res = handler.send_html("admin@iwenli.org", "HTML邮件测试", html)
    print(res)
