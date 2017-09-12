import requests
import http.cookiejar as cookielib
import xlwt
from PIL import Image
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    "Accept-Encoding": "gzip, deflate",
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded',
    "Host": "jwxt.swpu.edu.cn",
    "Referer": "http://jwxt.swpu.edu.cn/",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载！")


def get_captcha():
    captcha_url = "http://jwxt.swpu.edu.cn/validateCodeAction.do?random=0.8173650402446375"
    rp = session.get(captcha_url, headers=headers)
    with open("captcha.jpg", "wb") as f:
        f.write(rp.content)

    img = Image.open('captcha.jpg')
    img.show()
    img.close()
    captcha = input("please enter the captcha:")
    return captcha


def login(account, password):
    post_url = 'http://jwxt.swpu.edu.cn/loginAction.do'
    captcha = get_captcha()
    post_data = {
        "zjh1": "",
        "tips": "",
        "lx": "",
        "evalue": "",
        "eflag": "",
        "fs": "",
        "dzslh": "",
        "zjh": account,
        "mm": password,
        "v_yzm": captcha
    }
    response = session.post(post_url, data=post_data, headers=headers)
    session.cookies.save()


def crawl_cj():
    url = "http://jwxt.swpu.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017学年春(两学期)#qb_2016-2017学年春(两学期)"
    cj_data = session.get(url, headers=headers, allow_redirects=False)
    cj_data_text = cj_data.text
    html = etree.HTML(cj_data_text)
    xq_titles = html.xpath("//a/@name")
    bts = html.xpath('//th[@class="sortable"]/text()')[:7]
    kchs = html.xpath('//tr[@class="odd"]/td[1]/text()')
    kxhs = html.xpath('//tr[@class="odd"]/td[2]/text()')
    kcms = html.xpath('//tr[@class="odd"]/td[3]/text()')
    kcm_ens = html.xpath('//tr[@class="odd"]/td[4]/text()')
    xfs = html.xpath('//tr[@class="odd"]/td[5]/text()')
    kcsxs = html.xpath('//tr[@class="odd"]/td[6]/text()')
    cjs = html.xpath('//tr[@class="odd"]/td[7]/p/text()')
    data = [kchs, kxhs, kcms, kcm_ens, xfs, kcsxs, cjs]

    # 整理数据
    wb = xlwt.Workbook("swpu_zx.xls")

    nums1 = [0, 11, 23, 35]
    nums2 = [11, 23, 35, 48]
    x = 0

    for xq_title in xq_titles:
        col_num = 0
        m = 0

        sheet = wb.add_sheet(xq_title.strip(), cell_overwrite_ok=True)

        for bt in bts:
            sheet.write(0, col_num, bt.strip())
            row_num = 1
            for i in range(nums1[x], nums2[x]):
                sheet.write(row_num, col_num, data[m][i].strip())
                row_num += 1

            m += 1

            col_num += 1

        x += 1

    wb.save("swpu_zx.xls")
    print("写入EXCEL完毕!")


if __name__ == '__main__':
    login("your number", "your pwd")
    crawl_cj()
