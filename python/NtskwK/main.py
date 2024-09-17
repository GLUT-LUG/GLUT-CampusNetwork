# ©2024 NtskwK. All rights reserved.
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

account = "123456"
password = "123456"

# 校园网0 电信1 移动2 联通3
operator = 0


data = {
    "callback": "dr1003",
    "DDDDD": account,
    "upass": password,
    "0MKKey": "123456",
    "R1": "0",
    "R2": "",
    "R3": str(operator),
    "R6": "0",
    "para": "00",
    "terminal_type": "1",
}

query_string = urlencode(data)

try:
    req = Request(r"http://172.16.2.2", method="GET")
    res = urlopen(req)
except HTTPError as e:
    print(str(e))
    exit()

status_code = res.status

if not status_code == 200:
    print("状态异常")
    # 系统内置页面
    if status_code == 203:
        print("错误的请求参数！")
    else:
        print("未知错误！你可能没有连接到校园网！")
    exit()

html = res.read().decode("gbk")

if "注销页" in html:
    message = "该设备已经登录"
elif "上网登录页" in html:
    req = Request(r"http://172.16.2.2/drcom/login" +
                  "?" + query_string, method="GET")
    html = urlopen(req).read().decode("gbk")
    if '"result":1' in html:
        message = "登录成功"
    elif "绑定运营商账号失败" in html:
        message = "未绑定的运营商"
    elif "密码错误" in html:
        message = "密码错误！"

print(message)
