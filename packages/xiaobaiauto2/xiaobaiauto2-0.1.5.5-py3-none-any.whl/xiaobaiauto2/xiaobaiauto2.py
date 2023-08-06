#! /usr/bin/PUBLIC_VARS python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2.py'
__create_time__ = '2020/7/2 18:20'

from xiaobaiauto2.utils.xiaobaiauto2db import DB
# from xiaobaiauto2.utils.xiaobaiCaptcha import find_text
from xiaobaiauto2.data.GLO_VARS import PUBLIC_VARS
from requests import request
from jmespath import search
from re import findall
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver  # , WebElement, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait  # , TimeoutException

def cmd2action(b=None, r=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    wait = WebDriverWait(b, PUBLIC_VARS['WebDriverWait'], PUBLIC_VARS['poll_frequency'])
    if r[0][0] == 1:
        if loc not in ('', None):
            if isinstance(b, WebDriver):
                e = wait.until(lambda b: b.find_element_by_xpath(loc))
                # e = b.find_element_by_xpath(loc)
                if '%s' in r[0][2] or '%d' in r[0][2]:
                    eval(r[0][2] % data)
                    if contains_assert:
                        assert contains_assert in eval(r[0][2] % data)
                    elif equal_assert:
                        assert equal_assert == eval(r[0][2] % data)
                else:
                    eval(r[0][2])
                    if contains_assert:
                        assert contains_assert in eval(r[0][2])
                    elif equal_assert:
                        assert equal_assert == eval(r[0][2])
    elif r[0][1] == 1:
        if isinstance(b, WebDriver):
            if '%s' in r[0][2] or '%d' in r[0][2]:
                eval(r[0][2] % data)
                if contains_assert:
                    assert contains_assert in eval(r[0][2] % data)
                elif equal_assert:
                    assert equal_assert == eval(r[0][2] % data)
            else:
                eval(r[0][2])
                if contains_assert:
                    assert contains_assert in eval(r[0][2])
                elif equal_assert:
                    assert equal_assert == eval(r[0][2])
    else:
        if '%s' in r[0][2] or '%d' in r[0][2]:
            eval(r[0][2] % data)
            if contains_assert:
                assert contains_assert in eval(r[0][2] % data)
            elif equal_assert:
                assert equal_assert == eval(r[0][2] % data)
        else:
            eval(r[0][2])
            if contains_assert:
                assert contains_assert in eval(r[0][2])
            elif equal_assert:
                assert equal_assert == eval(r[0][2])

def action(app_type=1, b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    '''
    操作方法
    :param app_type: 操作对象类型1为web，2为app
    :param b: 操作对象
    :param cmd: 操作命令
    :param loc: 操作路径
    :param data: 操作数据
    :param contains_assert: 包含校验
    :param equal_assert: 相等校验
    :return:
    '''
    if b is not None:
        db = DB()
        r = db.select(f"select is_element,is_driver,code\
                      from keyword\
                      where testtype like '%{app_type}%' and command like '%{cmd}%' or key='{cmd}' limit 1;")
        cmd2action(b, r, loc, data, contains_assert, equal_assert)

def web_action(b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    action(app_type=1, b=b, cmd=cmd, loc=loc, data=data, contains_assert=contains_assert, equal_assert=equal_assert)

def app_aciton(b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    action(app_type=2, b=b, cmd=cmd, loc=loc, data=data, contains_assert=contains_assert, equal_assert=equal_assert)

class cmd(object):
    ''' UI动作 '''
    url = '打开网页'
    click = '点击'
    sendkey = '输入'
    refresh = '刷新'
    back = '后退'
    close = '关闭'
    quit = '退出'
    tag = '标签'
    attr = '属性'
    curl = 'URL'
    title = '标题'
    frame = '内嵌页'
    window = '标签页[序号(1开始)]'
    alter0 = 'JS_确定'
    alter1 = 'JS_取消'
    alter2 = 'JS_输入框'
    alter3 = 'JS_文本'
    wait = '停止'
    script = '脚本'
    addcookie = '添加cookie'
    swipe = '滑屏'
    dscreenshot = '截屏'
    escreenshot = '元素截图'
    findtext = '识别验证码'
    location = '坐标'
    打开网页 = 'URL'
    点击 = 'CLICK'
    输入 = 'SENDKEY'
    刷新 = 'REFRESH'
    后退 = 'BACK'
    关闭 = 'CLOSE'
    退出 = 'QUIT'
    标签 = 'TAG'
    属性 = 'ATTR'
    URL = 'CURL'
    标题 = 'ITLE'
    内嵌页 = 'FRAME'
    标签页 = 'WINDOW'
    JS_确定 = 'ALERT0'
    JS_取消 = 'ALERT1'
    JS_输入框 = 'ALERT2'
    JS_文本 = 'ALERT3'
    停止 = 'WAIT'
    脚本 = 'SCRIPT'
    添加cookie = 'ADDCOOKIE'
    滑屏 = 'SWIPE'
    截屏 = 'DSCREENSHOT'
    元素截图 = 'ESCREENSHOT'
    识别验证码 = 'FINDTEXT'
    坐标 = 'LOCATION'

class assert_mode(object):
    ''' 断言格式 '''
    json = 'json'
    contains = 'contains'

class extract_at(object):
    ''' 提取位置 '''
    status = 'status'
    headers = 'headers'
    body = 'body'
    all = 'all'

class extract_mode(object):
    ''' 提取方式 '''
    json = 'json'
    re = 're'

def apiTestCase(func):
    '''
    接口装饰器
    :param func:
    :return:
    '''
    def xiaobai(**kwargs):
        d = func.__name__.split('_')
        try:
            data_list = d[:d.index('')]
        except ValueError as e:
            data_list = d
        doc = func.__doc__
        if PUBLIC_VARS.get('base') in ['', None]:
            PUBLIC_VARS['base'] = 'https://test.xiaobaiit.com/'
        kw = kwargs.copy()
        keyword = ['assert_mode','assert_path','assert_value','extract_at','extract_mode','extract_path','extract_name']
        for k in keyword:
            if k in kw.keys():
                kw.pop(k)
        res = request(method=data_list[0], url=PUBLIC_VARS.get('base') + '/'.join(data_list[1:]), **kw)
        if 'json' == kwargs.get('assert_mode') and \
                'assert_mode' in kwargs.keys() and 'application/json' in res.headers.get('Content-Type'):
            assert kwargs.get('assert_value') == search(kwargs.get('assert_path'), res.json())
        elif 'contains' == kwargs.get('assert_mode') and 'assert_mode' in kwargs.keys():
            assert kwargs.get('assert_value') in res.text
        if 'status' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
            PUBLIC_VARS[kwargs.get('extract_name')] = res.status_code
        elif 'headers' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
            if 'json' == kwargs.get('extract_mode') and 'extract_mode' in kwargs.keys():
                value = search(kwargs.get('extract_path'), res.headers)
                PUBLIC_VARS[kwargs.get('extract_name')] = value if value is not None else ''
            elif 're' == kwargs.get('extract_mode') and 'extract_mode' in kwargs.keys():
                value = findall(kwargs.get('extract_path'), res.headers.__str__())
                PUBLIC_VARS[kwargs.get('extract_name')] = value if value != [] else ['']
        elif 'body' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
            if 'json' == kwargs.get('extract_mode') and\
                    'extract_mode' in kwargs.keys() and 'application/json' in res.headers.get('Content-Type'):
                value = search(kwargs.get('extract_path'), res.json())
                PUBLIC_VARS[kwargs.get('extract_name')] = value if value is not None else ''
            elif 're' == kwargs.get('extract_mode') and 'extract_mode' in kwargs.keys():
                value = findall(kwargs.get('extract_path'), res.text)
                PUBLIC_VARS[kwargs.get('extract_name')] = value if value != [] else ['']
        elif 'all' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
            ''' search in headers and body '''
            PUBLIC_VARS[kwargs.get('extract_name')] = []
            value = search(kwargs.get('extract_path'), res.headers)
            v = value if value is not None else ''
            PUBLIC_VARS[kwargs.get('extract_name')].append(v)
            if 'application/json' in res.headers.get('Content-Type'):
                value = search(kwargs.get('extract_path'), res.json())
                v = value if value is not None else ''
                PUBLIC_VARS[kwargs.get('extract_name')].append(v)
            else:
                value = search(kwargs.get('extract_path'), res.json())
                v = value if value != [] else ['']
                PUBLIC_VARS[kwargs.get('extract_name')].append(v)
    return xiaobai

def api_action(method='POST', url='', **kwargs):
    '''
    接口操作方法
    :param method: 接口请求方式
    :param url: 接口地址
    :param assert_mode: 校验模式[json, contains]
    :param assert_path:  校验预期结果路径
    :param assert_value: 校验预期结果
    :param extract_at:  提取数据所在位置 [status, headers, body, all]
    :param extract_mode: 提取方式 [json, re]
    :param extract_path: 提取路径表达式
    :param extract_name: 提取数据变量名
    :param kwargs: 其他参数参考requests的api
    :return:
    例如：api_action(
            method='POST',
            url='https://api.xiaobai.com/login',
            data='{"username": "xiaobai", "password": "abcdef"}',
            headers={},
            assert_mode='json', # 例如：assert_mode=assert_mode.json()
            assert_path='code',
            assert_value=200,
            extract_at='body', # 例如：extract_at=extract_at.body()
            extract_mode='json', # 例如：extract_at=extract_at.json()
            extract_path='data.accessToken',
            extract_name='accessToken'
        )
    '''
    res = request(method=method.upper(), url=url, kwargs=kwargs)
    if 'json' == kwargs.get('assert_mode') and \
            'assert_mode' in kwargs.keys() and 'application/json' in res.headers.get('Content-Type'):
        assert kwargs.get('assert_value') == search(kwargs.get('assert_path'), res.json())
    elif 'contains' == kwargs.get('assert_mode') and 'assert_mode' in kwargs.keys():
        assert kwargs.get('assert_value') in res.text
    if 'status' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
        PUBLIC_VARS[kwargs.get('extract_name')] = res.status_code
    elif 'headers' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
        if 'json' == kwargs.get('extract_mode') and 'extract_mode' in kwargs.keys():
            value = search(kwargs.get('extract_path'), res.headers)
            PUBLIC_VARS[kwargs.get('extract_name')] = value if value is not None else ''
        elif 're' == kwargs.get('extract_mode') and 'extract_mode' in kwargs.keys():
            value = findall(kwargs.get('extract_path'), res.headers.__str__())
            PUBLIC_VARS[kwargs.get('extract_name')] = value if value != [] else ['']
    elif 'body' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
        if 'json' == kwargs.get('extract_mode') and \
                'extract_mode' in kwargs.keys() and 'application/json' in res.headers.get('Content-Type'):
            value = search(kwargs.get('extract_path'), res.json())
            PUBLIC_VARS[kwargs.get('extract_name')] = value if value is not None else ''
        elif 're' == kwargs.get('extract_mode') and 'extract_mode' in kwargs.keys():
            value = findall(kwargs.get('extract_path'), res.text)
            PUBLIC_VARS[kwargs.get('extract_name')] = value if value != [] else ['']
    elif 'all' == kwargs.get('extract_at') and 'extract_at' in kwargs.keys():
        ''' search in headers and body '''
        PUBLIC_VARS[kwargs.get('extract_name')] = []
        value = search(kwargs.get('extract_path'), res.headers)
        v = value if value is not None else ''
        PUBLIC_VARS[kwargs.get('extract_name')].append(v)
        if 'application/json' in res.headers.get('Content-Type'):
            value = search(kwargs.get('extract_path'), res.json())
            v = value if value is not None else ''
            PUBLIC_VARS[kwargs.get('extract_name')].append(v)
        else:
            value = search(kwargs.get('extract_path'), res.json())
            v = value if value != [] else ['']
            PUBLIC_VARS[kwargs.get('extract_name')].append(v)
    return res