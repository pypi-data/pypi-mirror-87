#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'chinese_chromedriver_installer.py'
__create_time__ = '2020/7/17 1:04'

from urllib.request import urlretrieve, urlopen
from winreg import HKEY_CURRENT_USER, OpenKey, EnumValue
from re import findall, IGNORECASE
from zipfile import ZipFile
from os import remove, popen

def back(a,b,c):
    '''''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per = 100.0*a*b/c
    if per > 100:
        per = 100
    print(end='\r')
    print('当前已下载%.2f%%' % per, end='')

def chromedriver_download():
    TAOBAO_MIRROR_DOWNLOAD_URL = 'https://npm.taobao.org/mirrors/chromedriver/'
    try:
        chrome_current_version = EnumValue(OpenKey(HKEY_CURRENT_USER, 'Software\Google\Chrome\BLBeacon'), 0)[1]
        version_list = chrome_current_version.split('.')
        res = urlopen(TAOBAO_MIRROR_DOWNLOAD_URL).read().decode('utf-8')
        LAST_VERSION = findall(f'/mirrors/chromedriver/{version_list[0]}([0-9\.]+)/">', res, IGNORECASE)[0]
        DOWNLOAD_URL = f'https://npm.taobao.org/mirrors/chromedriver/{version_list[0]}{LAST_VERSION}/chromedriver_win32.zip'
        urlretrieve(DOWNLOAD_URL, 'chromedriver_win32.zip', back)
        ZipFile('chromedriver_win32.zip').extract('chromedriver.exe')
        remove('chromedriver_win32.zip')
    except Exception as e:
        raise ('是不是没安装Chrome浏览器呢？' + str(e))

def tesseract_download():
    TESSERACT_DOWNLOAD_URL = 'https://api.256file.com/download/56476_tesseract.exe'
    urlretrieve(TESSERACT_DOWNLOAD_URL, 'tesseract.exe', back)

def update_keyword_db():
    KEYWORD_DB_DOWNLOAD_URL = ''
    urlretrieve(KEYWORD_DB_DOWNLOAD_URL, 'xiaobaiauto2.db', back)
    # popen('xiaobaiauto2.db', )