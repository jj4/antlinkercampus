# -*- coding: utf-8 -*-
from antlinker import antlinker
from server import server


if __name__ == '__main__':
    test = antlinker()
    try:
        test.refresh_token()
    except:
        test.get_token()    

    temp = test.upload_temperature()
    server(temp)
