#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'test_template_0.py'
__create_time__ = '2020/7/17 2:15'

'''
    v1版，脚本与数据不分离，适合业务变更不频繁的场景
'''

import pytest, logging

log = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def login(caplog):
    log.debug('验证token是否有效，无效则重新执行登陆接口获取token')

def setup_module(caplog):
    log.debug("整个文档执行前执行一次")
    # global_vars = {'变量名': '变量值', '变量2': '值2'}

def teardown_module():
    log.debug("整个文件执行后执行一次")

def setup_function():
    log.debug("执行每个方法前执行一次，不适合单接口")

def teardown_function():
    log.debug("执行每个方法后执行一次，不适合单接口")


def test_xiaobai_api():
    log.debug("执行接口测试")
    assert '实际返回值' != '预期值'

class TestClass(object):

    def setup_class(self):
        log.debug("setup_class(self)：每个类之前执行一次")

    def teardown_class(self):
        log.debug("teardown_class(self)：每个类之后执行一次")

    def test_xiaobai_api2(self):
        log.debug("执行接口测试")
        assert '实际返回值' != '预期值'

if __name__=="__main__":
    pytest.main(["-s", "test_xiaobai_api_v1.py"])
    # pytest --html=report.html --self-contained-html