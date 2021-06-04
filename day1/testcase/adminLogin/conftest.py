import pytest
from pylib.webapi.common import login
from conf.config import email, pwd
from pylib.webapi.OrganizAPI import delALL_organizations
'''@pytest.fixture(scope='session')
scope有4个作用范围：function、class、module、session

function：每个函数或方法都会调用

class：每个类只调用1次

module：每个模块只调用1次

session：多个模块调用1次，通常写在conftest中
'''


# 测试之前实现管理员登录
@pytest.fixture(scope='session')
def before_admin():
    cookies = login(email, pwd)
    delALL_organizations(cookies)  # 删除所有部门
    return cookies
