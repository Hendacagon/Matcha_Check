# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# === 配置区域 ===
URL = 'https://www.marukyu-koyamaen.net/category/select/cid/315'
KEYWORD = '未发现商品'
INTERVAL = 300  # 检测间隔（单位：秒）

# 邮件配置
SENDER = '313408053@qq.com'
RECEIVERS = ['313408053@qq.com', 'yang.yu6@cn.bosch.com', '836822730@qq.com']  # 支持多个收件人
SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 465
PASSWORD = 'romsccrsroogbjhh'  # QQ邮箱SMTP授权码（不是登录密码）

# === 功能区 ===

def check_keyword():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        if KEYWORD in soup.get_text():
            print(f"{time.ctime()}: 发现关键词“{KEYWORD}”，继续监控...")
            return True
        else:
            print(f"{time.ctime()}: 关键词“{KEYWORD}”未出现！")
            return False
    except Exception as e:
        print(f"{time.ctime()}: 出错了：{e}")
        return True

def alert_user():
    # 弹窗提醒
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("监控通知", "目标商品可能已上架！关键词“未发现商品”未出现。")
    root.destroy()

def send_email():
    try:
        message = MIMEText('目标商品可能已上架！关键词“未发现商品”未出现。', 'plain', 'utf-8')
        message['From'] = formataddr(("商品监控程序", SENDER))
        message['To'] = Header(", ".join(RECEIVERS), 'utf-8')
        message['Subject'] = Header("【商品提醒】可能已上架", 'utf-8')

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVERS, message.as_string())
        server.quit()
        print("邮件已发送。")
    except Exception as e:
        print(f"邮件发送失败：{e}")

def main():
    should_continue = check_keyword()
    if not should_continue:
        alert_user()
        send_email()

    print("按 Enter 键退出...")


if __name__ == "__main__":
    main()
