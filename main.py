# -*- coding: utf-8 -*-
from antlinker import antlinker
from server import pushplus


if __name__ == "__main__":
    test = antlinker()
    try:
        test.refresh_token()
    except:
        test.get_token()
    # 体温上报
    # temp = test.upload_temperature()
    # test.query_temperature()

    # 今日任务
    code, bid = test.get_task()
    # 信息填报
    feedback = test.upload_list(code, bid)
    title, content = test.query_uplist(code)
    pushplus(title + feedback, content)
