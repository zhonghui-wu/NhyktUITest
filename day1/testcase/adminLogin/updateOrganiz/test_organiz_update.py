import pytest

from pylib.webapi.OrganizAPI import list_organizations, update_organizations


def test_tc000051(before_admin, have_organiz):
    global cookies
    global org
    cookies = before_admin
    org = have_organiz
    _id = org['_id']
    update_organizations(_id, '开发部', cookies)
    resp = list_organizations(cookies)['value'][1]
    assert '开发部' in resp['name']
    return resp


def test_tc000052():
    resp = update_organizations('iOiJIUzI1Ni', '开发部', cookies)['error']['message']
    assert "Cannot read property 'owner' of undefined" in resp


if __name__ == '__main__':
    pytest.main(['-s'])