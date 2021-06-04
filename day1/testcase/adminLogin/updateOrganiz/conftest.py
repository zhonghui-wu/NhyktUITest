import pytest
from pylib.webapi.OrganizAPI import add_organizations, list_organizations, delALL_organizations


@pytest.fixture(scope='package')
def have_organiz(before_admin):
    cookies = before_admin
    delALL_organizations(cookies)
    org = add_organizations('测试部', cookies)['value'][0]
    resp = list_organizations(cookies)['value']
    assert org in resp
    return org
