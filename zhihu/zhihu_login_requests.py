import requests
import http.cookiejar as cookielib
import re

# 构造Request headers
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
headers = {
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")


def get_xrsf():
    # 获取表单数据中的_xsrf
    index_url = 'https://www.zhihu.com'
    response = session.get(index_url, headers=headers)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)


def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print("手机号码登录 \n")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xrsf(),
            "phone_num": account,
            "password": password
        }
    else:
        if "@" in account:
            post_url = 'http://www.zhihu.com/login/email'
            print("邮箱登录 \n")
            post_data = {
                "_xsrf": get_xrsf(),
                "email": account,
                "password": password
            }

    login_page = session.get(post_url, data=post_data, headers=headers)
    session.cookies.save()


def is_login():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    response = session.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    if is_login():
        print('您已经登录')
    else:
        zhihu_login("xxx", "xxx")