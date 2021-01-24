from pylib.webapi.OrganizAPI import add_organizations, list_organizations, delete_organizations
import pytest


# 创建用例2
def test_tc000002(before_admin):  # 这里调用before_admin是因为需要他的返回值
    global cookies  # 声明全局变量
    global _id
    cookies = before_admin  # 使用before_admin的返回值cookies
    resp1 = add_organizations('采购部', cookies)
    org1 = resp1['value'][0]
    _id = org1['_id']
    resp2 = list_organizations(cookies)['value']
    assert org1 in resp2  # 判断列出的结果包含新增的内容


def teardown():
    global cookies
    delete_organizations(_id, cookies)


if __name__ == '__main__':
    pytest.main(['-s'])
