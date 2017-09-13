import requests
import http.cookiejar as cookielib
import re
import time
import os.path

try:
    from PIL import Image
except:
    pass

# 构造Request headers
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
headers = {
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': agent
}

requests.adapters.DEFAULT_RETRIES = 5

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")


def get_xsrf():
    # 获取表单数据中的_xsrf
    index_url = 'https://www.zhihu.com'
    response = session.get(index_url, headers=headers)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""

def get_captcha():
    captcha_url = 'https://www.zhihu.cdom/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time() * 1000))
    response = session.get(captcha_url, headers=headers)
    with open('captcha.gif', 'wb') as f:
        f.write(response.content)
        f.close()

    # 自动打开刚获取的验证码
    from PIL import Image
    try:
        img = Image.open('captcha.gif')
        img.show()
        img.close()
    except:
        pass


def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print("手机号码登录 \n")
        post_url = "https://www.zhihu.com/login/phone_num"
        xsrf = get_xsrf()
        post_data = {
            '_xsrf': xsrf,
            'password': password,
            "captcha_type": "en",
            'phone_num': account,
            'captcha': get_captcha(),
        }
    else:
        if "@" in account:
            post_url = 'http://www.zhihu.com/login/email'
            print("邮箱登录 \n")
            xsrf = get_xsrf()
            post_data = {
                "_xsrf": xsrf,
                "password": password,
                "captcha_type": "cn",
                "email": account,
                'captcha': get_captcha(),
            }

    login_page = session.post(post_url, data=post_data, headers=headers)
    session.cookies.save()


def is_login():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    response = session.get(url, headers=headers, allow_redirects=False)
    if int(response.status_code) == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    zhihu_login("17780625910", "batman123")
    if is_login():
        print('您已经登录！')
    else:
        print("没有登录")

