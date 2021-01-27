# -*- coding: utf-8 -*-
import requests


# Server酱推送
def server(title, content):
    sckey = ''  # Server酱sckey
    url = 'http://sc.ftqq.com/%s.send' % sckey
    body = {
        'text': title,
        'desp': content
    }
    requests.post(url, data=body)


# push plus
def pushplus(title, content):
    url = 'http://pushplus.hxtrip.com/send'
    body = {
        'token': '',
        'title': title,
        'content': content,
        'template': 'json'
    }
    requests.post(url=url, data=body)
