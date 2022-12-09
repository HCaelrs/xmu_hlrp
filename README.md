# xmu_hlrp

青春才几年 疫情占三年

健康打卡完成了它的使命 感谢之前用我脚本打卡的同学还有朋友

希望疫情能够尽快过去 希望大家尽快能够过上疫情前的生活

这也是本项目最后一次更新 peace and love

![57e1302012a88b483551e747c7b1a4af](https://user-images.githubusercontent.com/53749904/206694860-f42d8592-2b37-49c5-911e-ed016f3bff9a.jpg)




~~use for xmu health report automation~~



~~本脚本用于自动完成Xlender Moriarty University的健康上报。~~

~~同时附带能够破解Xlender Moriarty University新生登录系统图像滑动验证的模块（9张二次元图） 成功率低 但是能用~~

**目前网页经过更新之后替换掉了原来的二次元图 使用了风景的图片 该功能暂时无法使用 如需使用需要再图片路径中自行更改图片 以及每一个test中分割线的位置**

~~仅供学习参考学习webdriver的基础使用，切不可作它用。~~


## centos 安装

chrome driver安装

```bash
# 安装浏览器
curl https://intoli.com/install-google-chrome.sh | bash
ldd /opt/google/chrome/chrome | grep "not found"
google-chrome-stable --no-sandbox --headless --disable-gpu --screenshot https://www.baidu.com

# 安装chromedriver
yum install chromedriver.x86_64
```

[(42条消息) centos 安装 chromedriver_PeasantWorker的博客-CSDN博客_centos chromedriver](https://blog.csdn.net/qq_44193969/article/details/123901407)

```python
# 在python中进行测试
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
driver = webdriver.Chrome(chrome_options=chrome_options) #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
driver.get("https://www.baidu.com”)
print(driver.page_source)
```





## windows安装

1. 安装chromedriver

   [Chromedriver的安装教程 - 谜语+ - 博客园 (cnblogs.com)](https://www.cnblogs.com/022414ls/p/15171863.html)

   添加完环境变量之后重启，进入cmd进行测试chromedriver。

2. 安装selenium

3. 在selenium中测试webdriver

   ```python
   from selenium import webdriver
   webdriver.Chrome()
   ```

   看到有浏览器打开就能算成功	



## 运行

在代码开头对于一些项目进行配置

```python
SANDBOX = True	# 如果在linux上需要将sandbox设置为False
SERVERNAME = "health_report_ROBOT 2022-08-beta"
MAIL_HOST = "smtp.qq.com"       # 设置服务器
MAIL_USER = "2100000000"        # 用户名
MAIL_PASS = "lfjilqhyipqbcffi"  # 口令
SENDER = "2100000000@qq.com"    # 发送邮箱
USERS = [
    {
        "id": "***2022******",
        "password": "aaaaaaaa",
        "email": "1111111111@qq.com"
    },
    {
        "id": "***2021******",
        "password": "vbbbbbbbb",
        "email": "22222222@qq.com"
    },
    # 可以在后面继续添加
]
```

如果是需要滑动验证码进行验证（freshmen_pic_auth），请运行pics文件夹中的all_use（由于numpy版本不同会导致不兼容的问题）。之后记得在文件中修改输入的用户名和密码。



## supervise_demo

通过这个脚本可以以班委身份对于班级学生的打卡情况进行监测。检测到没有打卡的同学，通过邮件发送学生信息给指定的邮箱。

在代码开头对于其中登录的班委的信息以及接收未打卡学生信息的邮箱进行配置。

其中发送邮件的邮箱信息同健康打卡的信息。

```python
SID = "3************7"
PWD = "W*********1"
EMAIL = "1**********@qq.com"

SERVERNAME = "SUPERvise_ROBOT 2022-09-beta"
MAIL_HOST = "smtp.qq.com"       # 设置服务器
MAIL_USER = "2********4"        # 用户名
MAIL_PASS = "lfjilqyhgdhbcffi"  # 口令
SENDER = "2********4@qq.com"    # 发送邮箱
```

