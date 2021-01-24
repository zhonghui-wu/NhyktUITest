from pylib.webapi.OrganizAPI import add_organizations, delete_organizations
import pytest


# 创建销售部
@pytest.fixture(scope='package', autouse=True)
def init_organiz(before_admin):
    cookies = before_admin
    org = add_organizations('销售部', cookies)['value'][0]
    yield
    del_organiz(org['_id'], cookies)


def del_organiz(_id, cookies):
    print('删除销售部')
    delete_organizations(_id, cookies)
