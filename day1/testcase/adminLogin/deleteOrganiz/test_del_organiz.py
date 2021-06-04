import pytest
from pylib.webapi.OrganizAPI import delete_organizations, add_organizations, list_organizations


# 新增一个部门，再删除新增的部门，再列出部门
def test_tc000091(before_admin, no_organiz):
    global cookies
    cookies = before_admin
    org = add_organizations('测试部', cookies)['value'][0]
    _id = org['_id']
    del_resp = delete_organizations(_id, cookies)
    assert del_resp == {}
    resp = list_organizations(cookies)['value'][1:]
    assert resp == []


# 新增分部，删除一个公司没有的分部，再列出分部，查看新增的分部是否还在
def test_tc000092():
    orgs = add_organizations('测试部', cookies)['value'][0]
    list_resp = list_organizations(cookies)
    response = delete_organizations('1', cookies)  # 删除没有的id也返回{}
    assert response == {}
    new_list_resp = list_organizations(cookies)
    assert list_resp == new_list_resp
    delete_organizations(orgs['_id'], cookies)


if __name__ == '__main__':
    pytest.main(['-s'])
