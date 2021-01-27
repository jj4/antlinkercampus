# -*- coding: utf-8 -*-
import requests, json, base64, hashlib


class antlinker(object):
    def __init__(self):
        self.usr = ''  # 手机号
        self.pwd = ''  # 密码
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'User-Agent: Dalvik/2.1.0 (Linux; U; Android 10; MI 9 MIUI/21.1.13)',
            'Authorization': 'BASIC '
                             'NTgyYWFhZTU5N2Q1YjE2ZTU4NjhlZjVmOmRiMzU3YmRiNmYzYTBjNzJkYzJkOWM5MjkzMmFkMDYyZWRkZWE5ZjY=',
        }
        self.user_info = {}

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
        access_token = token["access_token"]
        refresh_token = token["refresh_token"]
        # 更新headers
        self.headers['AccessToken'] = 'ACKEY_' + access_token
        # 保存refresh token
        with open("./refresh.token", "w") as f:
            f.write(refresh_token)
        return refresh_token

    # 检查access token是否有效
    def verify_token(self, token):
        url = f'https://auth.xiaoyuanjijiehao.com/oauth2/verify?access_token={token}'
        verify = self.s.get(url)
        user_info = json.loads(verify.text)
        if "user_id" in user_info:
            # 更新headers
            self.headers['AccessToken'] = 'ACKEY_' + token
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
            refresh = self.s.post(url, headers=self.headers, data=payload)
            response = json.loads(refresh.text)
            access_token = response["access_token"]
            # 更新headers
            self.headers['AccessToken'] = 'ACKEY_' + access_token
            # 保存access token
            with open("./access.token", "w") as f:
                f.write(access_token)
        return access_token

    # 查询用户信息
    def get_user_info(self):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        data = {
            "Router": "/api/system/myhead",
            "Method": "POST",
            "Body": "{}"
        }
        user_info = self.s.post(url, headers=self.headers, data=json.dumps(data))
        response = json.loads(user_info.text)
        self.user_info["academy"] = response["Data"]["StudentAcademy"]
        self.user_info["usercode"] = response["Data"]["UserCode"]
        self.user_info["name"] = response["Data"]["Name"]
        self.user_info["in_usercode"] = response["Data"]["IntelUserCode"]
        return True

    # 报平安
    def safe_report(self):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface?="
        data = {
            "Router": "/api/studentsafetyreport/report",
            "Method": "POST",
            "Body": "{\"ReportArea\":\"xx市\",\"ReportCode\":\"984b5551-4a33-11ea-98a9-005056bc6061\",\"UID\":\"\",\"Temperature\":\"1\",\"ReportAreaLat\":\"{\\\"lng\\\":119.xxxxxxxxxxx,\\\"lat\\\":35.xxxxxxxxxxx,\\\"of\\\":\\\"inner\\\"}\",\"ReportAreaChoiceCode\":\"\",\"ReportAreaChoiceName\":\"xx省xx市xx市\"}"
        }
        report = self.s.post(url, headers=self.headers, data=json.dumps(data).encode('utf-8'))
        response = json.loads(report.text)
        try:
            feedback = response["FeedbackText"]
        except Exception as reason:
            feedback = str(reason)
        return feedback

    # 体温上报
    def upload_temperature(self):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        # 校内
        data = {
            "Router": "/api/studentncpback/puttemperature",
            "Method": "POST",
            "Body": "{\"user\":\"%s\",\"temperature\":\"1\",\"reportArea\":\"校内\",\"memo\":\"\"}" % self.user_info["in_usercode"]
        }
        upload = self.s.post(url, headers=self.headers, data=json.dumps(data).encode('utf-8'))
        response = json.loads(upload.text)
        try:
            feedback = response["FeedbackText"]
        except Exception as reason:
            feedback = str(reason)
        return feedback

    # 获取 task code
    def get_task(self):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        data = {
            "Router": "/api/newcommtask/getstudenttasklist",
            "Method": "POST",
            "Body": "{\"UID\":\"\"}"
        }
        query = self.s.post(url, headers=self.headers, data=json.dumps(data))
        response = json.loads(query.text)
        task_code = response["Data"]["list"][0]["TaskCode"]
        business_id = response["Data"]["list"][0]["BusinessId"]
        return task_code, business_id

    # 信息采集
    def upload_list(self, task_code, template_id):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        data = {
            "Router": "/api/newcustomerform/submit",
            "Method": "POST",
            "Body": "{\"Field\":[{\"FieldCode\":\"disabled\",\"Content\":\"学院\"},{\"FieldCode\":\"disabled\",\"Content\":\"学号\"},{\"FieldCode\":\"disabled\",\"Content\":\"姓名\"},{\"FieldCode\":\"\",\"Content\":\"< 37.3℃\"},{\"FieldCode\":\"\",\"Content\":\"< 37.3℃\"},{\"FieldCode\":\"\",\"Content\":\"< 37.3℃\"},{\"FieldCode\":\"\",\"Content\":\"校外\"},{\"FieldCode\":\"\",\"Content\":\"xxxxxx\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"},{\"FieldCode\":\"\",\"Content\":\"否\"}],\"TaskCode\":\"%s\",\"TemplateId\":\"%s\"}" % (task_code, template_id)
        }
        upload = self.s.post(url, headers=self.headers, data=json.dumps(data).encode('utf-8'))
        response = json.loads(upload.text)
        try:
            feedback = response["FeedbackText"]
        except Exception as reason:
            feedback = str(reason)
        return feedback

    # 查询填报情况
    def query_uplist(self, code):
        url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        data = {
            "Router": "/api/newcommtask/getclasstaskstudentuplist",
            "Method": "POST",
            "Body": "{\"TaskCode\":\"%s\",\"Page\":0,\"memo\":\"\"}" % code
        }
        query = self.s.post(url, headers=self.headers, data=json.dumps(data))
        response = json.loads(query.text)
        title = response["Data"]["detail"]["Title"]
        content = response["Data"]["list"]
        content = str(content).replace('UpdateDatetime', 'UpdateTime')
        return title, content
