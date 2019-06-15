#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#get links from configFile
fd = open('selenium_link.txt')
links = fd.readlines()
fd.close()

def openBrowser():
    #profile_directory：在FireFox中查看。 @右上角设置>帮助>故障排除信息>配置文件夹
    profile_directory = r'C:\Users\14225\AppData\Roaming\Mozilla\Firefox\Profiles\u2vh00jx.default'
    profile = webdriver.FirefoxProfile(profile_directory)
    return webdriver.Firefox(profile)  #driver

def openAndManageLinks(driver ,lnks = []):
    driver.implicitly_wait(4)
    for i in range(len(lnks)):
        #print(lnks[i])
        runBrw_testBaidu(driver, lnks[i])
        #runBrw_testGithub(driver, lnks[i])

def runBrw_testGithub(driver, lnk):
    if lnk != 'https://github.com/':
        return

    driver.get(lnk)
    x = driver.find_element_by_css_selector(".octicon-plus")
    ActionChains(driver).click(x).perform()

    xp = driver.find_element_by_xpath("//a[contains(text(),'New repository')]")
    ActionChains(driver).click(xp).perform()

def runBrw_testBaidu(driver, lnk):
    if lnk != 'https://www.baidu.com/':
        return

    driver.get(lnk)
    WebDriverWait(driver, 10).until(EC.title_is(u"百度一下，你就知道"))  #判断title
    kwEle = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element(By.ID, 'kw'))) #判断元素
    suEle = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'su'))) #判断元素, 且元素可见
    # ......更多等待方式见：https://www.jianshu.com/p/1531e12f8852

    kwEle.send_keys("python")   #等同 -> driver.find_element_by_id("kw").send_keys("python")
    suEle.send_keys(Keys.ENTER) #等同 -> driver.find_element_by_id("su").send_keys(Keys.ENTER)
    driver.find_element_by_xpath("//a[contains(., 'Python 基础教程 | 菜鸟教程')]").click()

'''
使用Firefox操作网页
要求：
0、安装python3(废话)
1、安装selenium(同时需要urllib3)
2、下载geckodriver(Firefox)并解压到python的安装文件夹

常见问题：
1、xpath写不对：用工具、F12等查看，多试几次
2、找不到要素：设置Wait
3、打开网页时间特别长，以至于运行失败：不知道，重新运行，看人品
4、多层框架/层级定位还没试过，不知道怎么处理，当前也没这个需求
'''
openAndManageLinks(openBrowser(), links)

