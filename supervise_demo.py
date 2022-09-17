SID = "3************7"
PWD = "W*********1"
EMAIL = "1**********@qq.com"

SERVERNAME = "SUPERvise_ROBOT 2022-09-beta"
MAIL_HOST = "smtp.qq.com"       # 设置服务器
MAIL_USER = "2********4"        # 用户名
MAIL_PASS = "lfjilqyhgdhbcffi"  # 口令
SENDER = "2********4@qq.com"    # 发送邮箱

SANDBOX = False
SLEEP_TIME = 4

import re
import time
import base64
import random
import smtplib
import numpy as np
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
    
if __name__ == "__main__":
    mail_text = ""
    try:
        chrome_options = Options()
        if not SANDBOX:
            chrome_options.add_argument('--no-sandbox')derivatives  # 解决DevToolsActivePort文件不存在的报错
            chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
            chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1200, 800)

        url = "https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu"
        driver.get(url)
        time.sleep(SLEEP_TIME)

        username = driver.find_element(By.ID, 'username')
        password = driver.find_element(By.ID, 'password')
        username.send_keys(SID)
        password.send_keys(PWD)
        password.send_keys(Keys.ENTER)
        print("enter the id and pwd")
        time.sleep(SLEEP_TIME)

        divs = driver.find_elements(By.TAG_NAME, "div")
        needed_div = None
        for div in divs:
            if div.text =="Daily Health Check 健康信息登记":
                needed_div = div
                break
        needed_div.click()
        print("click the Daily Health Check")
        time.sleep(SLEEP_TIME)

        # 页面切换到第二个页面
        driver.switch_to.window(driver.window_handles[1])
        div_tags = driver.find_elements(By.TAG_NAME, "div")
        banwei = None
        for div in div_tags:
            if div.get_attribute("title") == "班委":
                banwei = div
                break
        banwei.click()
        print("click the 班委")
        time.sleep(SLEEP_TIME)

        # 选择用于选择的节点
        cls = "el-pagination__sizes"
        chosen_bt = driver.find_elements(By.CLASS_NAME, cls)[0]
        chosen_bt.click()

        # 选择显示100条
        sp_name = "100条/页"
        sps = driver.find_elements(By.TAG_NAME, "span")
        sp_clk = None
        for sp in sps:
            if sp.text == sp_name:
                sp_clk = sp
                break
        sp.click()
        print("choose 100条/页")
        time.sleep(SLEEP_TIME*2)

        # 开始遍历所有人的情况
        divs = driver.find_elements(By.TAG_NAME, "div")
        no_stt = None # 编号开始的序号
        for i in range(len(divs)):
            if divs[i].text=="操作":
                no_stt = i
                break
        no_stt+=2
        no_in_mail = 1
        for i in range(66):
            if divs[no_stt+i*14+12].text != "是 Yes":
                mail_text = mail_text + str(no_in_mail) + " "+ divs[no_stt+i*14+1].text + " " + divs[no_stt+i*14+2].text + " " + divs[no_stt+i*14+12].text + "\n"
                no_in_mail += 1
                print(divs[no_stt+i*14].text, end = " ")
                print(divs[no_stt+i*14+1].text, end = " ")
                print(divs[no_stt+i*14+2].text, end = " ")
                print(divs[no_stt+i*14+12].text)
        if send_email(EMAIL, mail_text, "SUPERvise success!"):
            print("send_mail success")
    except Exception as e:
        if send_email("SUPERvise error!", "SUPERvise error!"):
            print("send_mail success")
