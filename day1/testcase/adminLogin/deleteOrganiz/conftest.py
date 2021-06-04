from pylib.webapi.OrganizAPI import delALL_organizations
import pytest


# 当前公司没有分部
@pytest.fixture(scope='package')
def no_organiz(before_admin):
    cookies = before_admin
    delALL_organizations(cookies)
