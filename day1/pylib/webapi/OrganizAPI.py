import requests
from conf.config import host, parentid, spaceid

# 公司部分API
# 1.删除所有部门--先列出所有部门，再根据返回的id循环删除


def delALL_organizations(cookies):
    organs = list_organizations(cookies)['value'][1:]  # 去掉第一个，因为第一个是总公司
    for org in organs:
        delete_organizations(org['_id'], cookies)


def delete_organizations(organization_id, cookies):
    resp = requests.delete(f'{host}/api/v4/organizations/{organization_id}', cookies=cookies)
    return resp.json()


# 2.添加部门
def add_organizations(name, cookies):
    payload = {"name": name,
               "parent": parentid,  # 因为上级id是不变的，所以通过页面新增部门获取该值即可
               "sort_no": 100,
               "hidden": False,
               "space": spaceid}
    resp = requests.post(f'{host}/api/v4/organizations', json=payload, cookies=cookies)
    return resp.json()


# 3.列出部门
def list_organizations(cookies):
    resp = requests.get(f'{host}/api/v4/organizations', cookies=cookies)
    return resp.json()


# 4.修改部门
def update_organizations(organization_id, name, cookies):
    payload = {
                 "$set": {
                   "name": name,
                   "parent": parentid,
                   "sort_no": 100,
                   "hidden": False,
                   "space": spaceid
                 }
                }
    resp = requests.put(f'{host}/api/v4/organizations/{organization_id}', json=payload, cookies=cookies)
    return resp.json()
