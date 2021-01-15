# -*- coding: utf-8 -*-
import requests, json, base64, hashlib


class antlinker(object):
    def __init__(self):
        self.usr = ' '  # 手机号
        self.pwd = ' '  # 密码
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'User-Agent: Dalvik/2.1.0 (Linux; U; Android 11; MI 10 MIUI/21.1.13)',
            'Authorization': 'BASIC '
                             'NTgyYWFhZTU5N2Q1YjE2ZTU4NjhlZjVmOmRiMzU3YmRiNmYzYTBjNzJkYzJkOWM5MjkzMmFkMDYyZWRkZWE5ZjY='
        }
 
    # 登录 获取token
    def get_token(self):
        usr = "{\"LoginModel\":1,\"Service\":\"ANT\",\"UserName\":\"%s\"}" % self.usr
        auth_url = "https://auth.xiaoyuanjijiehao.com/oauth2/token"
        data = {
            'password': hashlib.md5(self.pwd.encode()).hexdigest(),
            'grant_type': 'password',
            'username': str(base64.b64encode(usr.encode('utf-8')), 'utf-8'),
        }
        login = self.s.post(auth_url, headers=self.headers, data=data)
        token = json.loads(login.text)
        # 获取access token, refresh token
        # access token 有效期7200s
        access_token = token["access_token"]
        # refresh token 有效期30days
        refresh_token = token["refresh_token"]
        # 更新headers
        self.s.headers.update({'AccessToken': 'ACKEY_' + access_token})
        # 保存refresh token
        with open("./refresh.token", "w") as f:
            f.write(refresh_token)
        return refresh_token

    # 检查access token是否有效
    def verify_token(self, token):
        url = f'https://auth.xiaoyuanjijiehao.com/oauth2/verify?access_token={token}'
        verify = self.s.get(url)
        if "user_id" in json.loads(verify.text):
            return True
        else:
            return False

    # 刷新access token
    def refresh_token(self):
        with open("./access.token", "r") as f:
            access_token = f.read()
        # access token失效时
        if not self.verify_token(access_token):
            with open("./refresh.token", "r") as f:
                refresh_token = f.read()
            url = "https://auth.xiaoyuanjijiehao.com/oauth2/token"
            payload = {
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
            # 刷新access token
            response = self.s.post(url, headers=self.headers, data=payload)
            access_token = json.loads(response.text)["access_token"]
            # 更新headers
            self.s.headers.update({'AccessToken': 'ACKEY_' + access_token})
            with open("./access.token", "w") as f:
                f.write(access_token)
        return access_token

    # 报平安
    def save_report(self):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface?="
        # 选择口号、体温、位置
        data = "{\"Router\":\"/api/studentsafetyreport/report\",\"Method\":\"POST\",\"Body\":\"{" \
               "\\\"ReportArea\\\":\\\"xx市\\\",\\\"ReportCode\\\":\\\"984b5551-xxxx-xxxx-xxxx-005056bc6061\\\"," \
               "\\\"UID\\\":\\\"\\\",\\\"Temperature\\\":\\\"1\\\",\\\"ReportAreaLat\\\":\\\"{" \
               "\\\\\\\"lng\\\\\\\":119.xxxxxxxxxxx,\\\\\\\"lat\\\\\\\":35.xxxxxxxxxxx," \
               "\\\\\\\"of\\\\\\\":\\\\\\\"inner\\\\\\\"}\\\",\\\"ReportAreaChoiceCode\\\":\\\"\\\"," \
               "\\\"ReportAreaChoiceName\\\":\\\"xx省xx市xx市\\\"}\"} "
        # 报平安请求
        report = self.s.post(url, headers=self.headers, data=data.encode('utf-8'))
        # 解析json 获取反馈
        response = json.loads(report.text)
        try:
            decoded = response["FeedbackText"]
        except Exception as reason:
            decoded = str(reason) + '错误'
        feedback = {
            'text': '校园集结号： ' + decoded
            # 'desp':
            }
        return feedback

    # 温度上报
    def upload_temperature(self):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        # 校内上报
        data = "{\"Router\":\"/api/studentncpback/puttemperature\",\"Method\":\"POST\",\"Body\":\"{\\\"user\\\":\\\"24a04c8e-xxxx-xxxx-xxxx-00163e08212a\\\",\\\"temperature\\\":\\\"1\\\",\\\"reportArea\\\":\\\"校内\\\",\\\"memo\\\":\\\"\\\"}\"}"
        # 校外上报
        # data = "{\"Router\":\"/api/studentncpback/puttemperature\",\"Method\":\"POST\",\"Body\":\"{\\\"user\\\":\\\"24a04c8e-xxxx-xxxx-xxxx-00163e08212a\\\",\\\"temperature\\\":\\\"1\\\",\\\"reportArea\\\":\\\"xx省xx市xx市\\\",\\\"memo\\\":\\\"\\\"}\"}"
        upload = self.s.post(url, headers=self.headers, data=data.encode('utf-8'))
        response = json.loads(upload.text)
        try:
            decoded = response["FeedbackText"]
        except Exception as reason:
            decoded = str(reason) + '错误'
        feedback = {
            'text': '校园集结号： ' + decoded
            # 'desp':
            }
        return feedback
