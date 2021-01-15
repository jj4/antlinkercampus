# -*- coding: utf-8 -*-
import requests


# Server酱推送
def server(msg):
    sckey = 'SCU98925T261aa3ebe1c0465264ccc59ef614f9dc5ec8a774a49d1'  # Server酱sckey
    url = 'http://sc.ftqq.com/%s.send' % sckey
    requests.post(url, data=msg)
