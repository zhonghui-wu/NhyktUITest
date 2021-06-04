import requests
from conf.config import host


# 实现登录
def login(emails, pwds):
    payload = {"user": {"email": emails}, "password": pwds, "code": "", "locale": "zhcn"}
    resp = requests.post(f'{host}/accounts/password/authenticate', json=payload)
    return resp.cookies  # 认证信息


