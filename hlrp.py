SANDBOX = False
SERVERNAME = "health_report_ROBOT 2022-08-beta"
MAIL_HOST = "smtp.qq.com"       # 设置服务器
MAIL_USER = "2111111114"        # 用户名
MAIL_PASS = "lfjilqhyipqbcffi"  # 口令
SENDER = "2111111114@qq.com"    # 发送邮箱
USERS = [
    {
        "id": "3111111114",
        "password": "H11111118",
        "email": "1111111115@qq.com"
    }
]

import re
import time
import base64
import random
import smtplib
import numpy as np
from PIL import Image
from io import BytesIO
from datetime import datetime
from selenium import webdriver
from email.header import Header
from email.mime.text import MIMEText
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



def send_email(address, msg, title=""):
    """
    to send mail to the user
    :param address:
    :param msg: the main message of the mail
    :param title: the title of the mail
    :return:
    """
    mail_host = MAIL_HOST  # 设置服务器
    mail_user = MAIL_USER  # 用户名
    mail_pass = MAIL_PASS  # 口令
    sender = SENDER

    receivers = [address]

    message = MIMEText((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n' + msg), 'plain',
                       'utf-8')
    message['From'] = Header(title + " " + SERVERNAME)
    message['To'] = Header(address)

    subject = title + time.strftime('%Y-%m-%d', time.localtime(time.time()))
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        # print("email send success!")
        return True
    except smtplib.SMTPException:
        print(smtplib.SMTPException)
        return False


def health_report(sid, pwd, eml, sandbox):
    """
    the main func of the health report
    :param sid: student's id
    :param pwd: student's password
    :param eml: email address to report the result of the health report
    :param sandbox: if run in the linux or other env, let the sandbox = False
    :return: True or False means for the success or not
    """
    eml_text = ""
    try:
        chrome_options = Options()
        if not sandbox:
            chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
            chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
            chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1200, 800)

        url = 'https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu'
        driver.get(url)
        time.sleep(1)

        username = driver.find_element(By.ID, 'username')
        password = driver.find_element(By.ID, 'password')
        username.send_keys(sid)
        password.send_keys(pwd)
        password.send_keys(Keys.ENTER)
        time.sleep(1)
        divs = driver.find_elements(By.TAG_NAME, "div")
        needed_div = None
        for div in divs:
            if div.text == "Daily Health Check 健康信息登记":
                needed_div = div
                break
        needed_div.click()

        # choose my form
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        div_tags = driver.find_elements(By.TAG_NAME, "div")
        my_form = None
        for div in div_tags:
            if div.get_attribute("title") == "我的表单":
                my_form = div
                break
        my_form.click()

        time.sleep(1)
        choose = []
        last_time = None
        spans = driver.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if span.get_attribute("title") == "请选择":
                choose.append(span)
            if re.match("....-..-.. ..:..:..", span.get_attribute("title")) != None:
                last_time = span.get_attribute("title")
        last_time = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
        now_time = datetime.now()
        if last_time.year == now_time.year and last_time.month == now_time.month and last_time.day == now_time.day:
            if send_email(eml, "you have already done the health report today!", "already done"):
                print("send_mail success")
            print("you have already done the health report today!")
        # 如果今天还没有打卡过 那么就再对于今天进行打卡
        else:
            choose[-3].click()
            # choose yes
            time.sleep(1)
            labels = driver.find_elements(By.TAG_NAME, "label")
            yes_tag = None
            for label in labels:
                # print(label.get_attribute("title"))
                if label.get_attribute("title") == "是 Yes":
                    yes_tag = label
            yes_tag.click()

            # save
            save = None
            for span in driver.find_elements(By.TAG_NAME, "span"):
                if span.get_attribute("class") == "form-save position-absolute":
                    save = span
                    break
            save.click()
            print("report saved")

            # accept the alert
            driver.switch_to.alert.accept()
            print("alert accepted")
            if send_email(eml, "health report success!", "report success"):
                print("send_mail success")
        driver.close()
        print("driver closed")
        return True
    except Exception as e:
        if send_email(eml, e.__str__(), "report error"):
            print("send_mail success")
        print(e)
        return False


if __name__ == "__main__":
    for user in USERS:
        print("start " + user["id"])
        health_report(user["id"], user["password"], user["email"], sandbox=SANDBOX)
