# -*- coding: utf-8 -*-
import requests, json, base64, hashlib


class report:
    def __init__(self):
        self.usr = ' '  # 手机号
        self.pwd = ' '  # 密码
        self.sckey = ' '  # Server酱sckey
        # 定义一个session()的对象实体s来储存cookie
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Version/4.0 Chrome/81.0.4044.62 Mobile Safari/537.36Ant-Android-WebView ',
            'Authorization': 'BASIC '
                             'NTgyYWFhZTU5N2Q1YjE2ZTU4NjhlZjVmOmRiMzU3YmRiNmYzYTBjNzJkYzJkOWM5MjkzMmFkMDYyZWRkZWE5ZjY='
        }

    # Server酱通知
    def server(self, text):
        requests.get('https://sc.ftqq.com/' + self.sckey + '.send?text=' + text)

    # 模拟登录
    def login(self):
        usr1 = "{\"LoginModel\":1,\"Service\":\"ANT\",\"UserName\":\"%s\"}" % self.usr
        log_url = "https://auth.xiaoyuanjijiehao.com/oauth2/token"
        data = {
            'password': hashlib.md5(self.pwd.encode()).hexdigest(),
            'grant_type': 'password',
            'username': str(base64.b64encode(usr1.encode('utf-8')), 'utf-8'),
        }
        log_page = self.s.post(log_url, headers=self.headers, data=data).text
        # 获取access_token
        token = json.loads(log_page.strip())["access_token"]
        # 更新header
        self.s.headers.update({'AccessToken': 'ACKEY_' + token})

    # 报平安
    def save(self):
        re_url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface?="
        # 选择口号、体温、位置
        # data 本身即是json格式
        data = "{\"Router\":\"/api/studentsafetyreport/report\",\"Method\":\"POST\",\"Body\":\"{" \
               "\\\"ReportArea\\\":\\\"xx市\\\",\\\"ReportCode\\\":\\\"984b5551-4a33-11ea-98a9-005056bc6061\\\"," \
               "\\\"UID\\\":\\\"\\\",\\\"Temperature\\\":\\\"1\\\",\\\"ReportAreaLat\\\":\\\"{" \
               "\\\\\\\"lng\\\\\\\":119.xxxxxxxxxxx,\\\\\\\"lat\\\\\\\":35.xxxxxxxxxxx," \
               "\\\\\\\"of\\\\\\\":\\\\\\\"inner\\\\\\\"}\\\",\\\"ReportAreaChoiceCode\\\":\\\"\\\"," \
               "\\\"ReportAreaChoiceName\\\":\\\"xx省xx市xx市\\\"}\"} "
        # 报平安请求
        re_page = self.s.post(re_url, headers=self.headers, data=data.encode('utf-8'))
        # 解析json 获取反馈
        decoded = json.loads(re_page.text.strip())
        if "FeedbackText" in decoded:
            feedback = '报平安成功&desp=' + decoded["FeedbackText"]
        else:
            feedback = '报平安失败&desp=未知错误，请及时排查'
        # Server酱通知
        self.server(feedback)

    # 温度上报
    def temp(self):
        temp_url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        data = "{\"Router\":\"/api/studentncpback/puttemperature\",\"Method\":\"POST\",\"Body\":\"{" \
               "\\\"user\\\":\\\"24a04c8e-xxxx-xxxx-xxxx-00163e08212a\\\",\\\"temperature\\\":\\\"1\\\"," \
               "\\\"reportArea\\\":\\\"xx省xx市xx市\\\",\\\"memo\\\":\\\"\\\"}\"} "
        # 报平安请求
        temp_page = self.s.post(temp_url, headers=self.headers, data=data.encode('utf-8'))
        # 解析json 获取反馈
        decoded = json.loads(temp_page.text.strip())
        if "FeedbackText" in decoded:
            feedback = '体温上报成功&desp=' + decoded["FeedbackText"]
        else:
            feedback = '体温上报失败&desp=未知错误，请及时排查'
        print(feedback)
        self.server(feedback)


def main():
    re = report()
    re.login()  # 登录
    # re.save() # 报平安
    re.temp()  # 体温上报


if __name__ == '__main__':
    main()
