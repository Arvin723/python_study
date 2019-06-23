#coding=utf-8
import json
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

with open("cfg.json") as ff:
    data = json.load(ff)

username = data["username"]
password = data["password"]
profile_directory = data["profile_directory"]

songlnks = data['songlinks']
isUserAble = data["isUserAble"]

headers = {
        "Host": "www.xiami.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }
ss = requests.session()
songMenuLinks = []
fd = open('songs.txt', 'w')
'''
Browser ctrol
openBrowser：打开浏览器，返回 driver
openAndManageLinks:主运行函数
'''
def openBrowser():
    #profile_directory：在FireFox中查看。 @右上角设置>帮助>故障排除信息>配置文件夹
    profile = webdriver.FirefoxProfile(profile_directory)
    return webdriver.Firefox(profile)  #driver

driver = openBrowser()
#===============================================================================================
def openAndManageLinks(slnks = []):
    driver.implicitly_wait(4)
    driver.maximize_window()
    cookies = xiamiLogin('https://www.xiami.com/', isUserAble)
    for i in range(len(slnks)):
        runBrwXiami(slnks[i], cookies)
        time.sleep(3)

#----------------------------------------------------------------------------------------------
'''
cookieTrans
'''
def cookieTrans(seleniumCookies):
    reqCookies = dict()
    for i in range(len(seleniumCookies)):
        reqCookies[seleniumCookies[i]['name']] = seleniumCookies[i]['value']
    return reqCookies
#----------------------------------------------------------------------------------------------
'''
openSongLink:获取目标页面
getSongMenu：从目标页面获取歌单
xiamiLogin：用于登录(目前使用Firefox缓存，不用缓存时有不明原因导致验证时滑块不能到位)
'''
def openSongLink(songlnk, cookies):
    rs = ss.get(songlnk, headers=headers, cookies=cookies, verify=False)
    #ss.cookies = rs.cookies
    rs.encoding = 'utf-8'
    #print(rs.text)
    return rs

def getSongMenu(response):
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        #todo:此处正则写的不好，没匹配到
        #title = soup.find('div', {'class': 'collect-info'}).find('div', {'style': 'font-size: 24px; font-weight: 500;'}).text
        title = soup.find('div', {'class': 'collect-info'}).find('div', {'style': re.compile('font-size*24*font-weight*500*')}).text
        fd.writelines(title + "\n\n")
    except:
        pass
    songs = soup.find_all('div', {'class': 'song-name em'})
    for s in songs:
        try:
            buf = s.find('a').text
            print(buf)
            fd.writelines(buf + "\n")
        except:
            pass
    print("===================================================")
    fd.writelines("===================================================\n")


def listUserLink():
    xpath = "//a[text()='我的音乐']"
    href = driver.find_element(By.XPATH, xpath)
    hrefStr = href.get_attribute("href")
    userlink = hrefStr
    print(userlink)

    href.click()
    listOflkEle = driver.find_elements_by_xpath("//div[@class='name']/a")

    for i in range(len(listOflkEle)):
        smlink = listOflkEle[i].get_attribute("href")
        songMenuLinks.append(smlink)
        print(smlink)
    return songMenuLinks

def xiamiLogin(lnk, uerAble):
    driver.get(lnk)

    #这里登录操作没问题，但是滑块到达位置时，页面报错，手动尝试也不行，是否网站做了其他的保护？
    xpath = "//div[@class='user']/div[@class='login-text' and contains(., '登录/注册')]"
    if len(driver.find_elements(By.XPATH, xpath)) > 0:
        WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element(By.XPATH, xpath))).click()

        xpath = "//span[@title='账户登录']"  #登录方式
        WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element(By.XPATH, xpath))).click()

        #账号密码
        WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_id("account"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_id("password"))).send_keys(password)

        #拖动
        xpath = "//span[@class='nc_iconfont btn_slide']"
        element = driver.find_element_by_xpath(xpath)
        print(str(element.location["y"]) + "  " + str(element.location["x"]))
        ActionChains(driver).click_and_hold(element).move_by_offset(240, 0).perform()
        time.sleep(3)
        ActionChains(driver).release().perform()

        #点击登录
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element_by_id('account - login - submit'))).click()

    listUserLink()
    if uerAble == 1:
        for s in songMenuLinks:
            songlnks.append(s)
    cookies = driver.get_cookies()
    return cookieTrans(cookies)
#----------------------------------------------------------------------------------------------
def runBrwXiami(songlnk, cookies):
    fd.writelines(songlnk + "\n")
    getSongMenu(openSongLink(songlnk, cookies))

#===============================================================================================
'''
从 xiami 爬取歌单
要求：
0、bs4，requests，selenium，urllib3
1、下载geckodriver(Firefox)并解压到python的安装文件夹

大概没收到一次response，都应该重新设置一下ss.cookies

主要问题：
1，requests受限
2，selenium被挡
3,目前无法翻页，只能拿到一页
4,拿不到私有歌单是因为仅自己可见，需要post
'''
openAndManageLinks(songlnks)
fd.close()




