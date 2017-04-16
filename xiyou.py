import urllib.request
import http.cookiejar
import urllib.parse
from scrapy import Selector


def getcookie_str(cj):
    cookie = ''
    for item in cj:
        cookie += item.name
        cookie += '='
        cookie += item.value
        cookie += ';'
    return cookie

def get_http(url,data,headers,cookie,charset,yzm):
    # proxy = "http://202.106.16.36:3128"
    # proxy_support = urllib.request.ProxyHandler({'http': proxy})
    # opener = urllib.request.build_opener(proxy_support)
    # urllib.request.install_opener(opener)

    res = {}
    if charset is None:
        charset = 'utf-8'
    if data is None:
        req = urllib.request.Request(url)
    else:
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data)
    for (k, v) in headers.items():
        req.add_header(k,v)
    if cookie is None:
        response = urllib.request.urlopen(req)
        if yzm is None:
            html = response.read().decode(charset)
        else:
            html = response.read()
        res['html'] = html
    else:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        response = opener.open(req)
        if yzm is None:
            html = response.read().decode(charset)
        else:
            html = response.read()
        res['html'] = html
        res['cookie'] = getcookie_str(cj)
    return res


#获取验证码
url = "http://222.24.62.120/CheckCode.aspx"
header  = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
result = get_http(url,None,header,1,'gb2312',1)
cookie = result['cookie']

#下载验证码
fp = open('验证码.jpg','wb')
fp.write(result['html'])
fp.close()



name = input("please input name :")
passwd = input("please input passwd :")
code = input("please input 验证码：")

url = 'http://222.24.62.120/default2.aspx'
data = {
'__VIEWSTATE' : 'dDwtNTE2MjI4MTQ7Oz5O9kSeYykjfN0r53Yqhqckbvd83A==',
'Textbox1': '',
'txtUserName' : name,
'TextBox2': passwd,
'txtSecretCode': code,
'RadioButtonList1':'(unable to decode value)',
'Button1':'',
'lbLanguage':'',
'hidPdrs':'',
'hidsc':''
}
header = {
'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
'Cookie' : cookie
}
result = get_http(url,data,header,None,'gb2312',None)




url = 'http://222.24.62.120/xscjcx.aspx?xh='+ name +'&xm=%CD%F5%E6%AF&gnmkdm=N121605'
header = {
'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
'Referer':'http://222.24.62.120/xs_main.aspx?xh='+ name,
'Cookie' : cookie
}
result = get_http(url,None,header,None,'gb2312',None)
rs = Selector(text=result['html']).xpath('//input[@name="__VIEWSTATE"]/@value').extract()
VIEWSTATE = rs[0]




XN = input("请输入所查询的学年（比如 2013-2014） : ")
XQ = input("请输入所查询的学期（比如 1） : ")

url = 'http://222.24.62.120/xscjcx.aspx?xh='+ name +'&xm=%CD%F5%E6%AF&gnmkdm=N121605'
header = {
'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
'Referer':'http://222.24.62.120/xscjcx.aspx?xh='+ name +'&xm=%CD%F5%E6%AF&gnmkdm=N121605',
'Cookie' : cookie
}
data = {
'__EVENTTARGET':'',
'__EVENTARGUMENT':'',
'__VIEWSTATE':VIEWSTATE,
'hidLanguage':'',
'ddlXN':XN,
'ddlXQ':XQ,
'ddl_kcxz':'',
'btn_xn':'(unable to decode value)'
}
result = get_http(url,data,header,None,'gb2312',None)
rs = Selector(text=result['html']).xpath('//tr/td/text()').extract()


res1 = []
res2 = ['学年','学期','课程名称', '成绩']
i = 0
j = -1
for val in rs:
    if i > 11:
        flag = (i-12)%13
        if flag == 0:
            j += 1
            res1.append(res2)
            res2 = []
        if flag == 0 or flag == 1 or flag == 3 or flag == 8 :
            res2.append(val)
    i += 1

for val in res1:
    print(val)


