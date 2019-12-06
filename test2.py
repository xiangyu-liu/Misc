# -*- coding: UTF-8 -*-
# https://www.censys.io/api/v1/search/ipv4
# post:{"query": "keyword", "page": 1, "fields": ["ip", "protocols", "location.country"]}
# query指的是相应的搜索语句;page代表返回的页码;fields指的是你希望返回值中包含哪些字段
#API_URL = "https://www.censys.io/api/v1"
#UID = "caa7db22-a928-4faa-9cf9-09c631bcdc8a"
#SECRET = "sjedIsIDvJMfj9vq0PQfcGuKUcgZNYiG"

import sys
import json
import requests
import time

API_URL = "https://www.censys.io/api/v1"
UID = "caa7db22-a928-4faa-9cf9-09c631bcdc8a"    #这两行记得要换成自己的账号
SECRET = "sjedIsIDvJMfj9vq0PQfcGuKUcgZNYiG"     #这两行记得要换成自己的账号
page = 1        #起始页
PAGES = 20      #终止页

'''
data = {
    "query": "80.http.get.headers.server: apache",
    "page": 1,
    "fields": ["ip", "location.country"]
}
'''
'''
    data = {
        "query": "apache",
        "page": page,
        "fields": ["ip", "protocols", "location.country"]
    }
'''

def getIp(page):
    iplist = []

    data = {
        "query": "80.http.get.headers.server: apache",
        "page": page,
        "fields": ["ip","protocols", "location.country"]
    }

    try:
        res = requests.post(API_URL + "/search/ipv4", data=json.dumps(data), auth=(UID, SECRET))    #/search/ipv4 这个是搜索条件
    except:
        pass
    try:
        results = res.json()
    except:
        pass
    if res.status_code != 200:
        print("error occurred: %s" % results["error"])
        sys.exit(1)
    iplist.append("Total_count:%s" % (results["metadata"]["count"]))
    for result in results["results"]:
        for i in result["protocols"]:
            iplist.append(result["ip"] + ':' + i)
    return iplist


if __name__ == '__main__':
    print("start...")
    with open('censys_apache_2.0.1.txt', 'a') as f:
        while page <= PAGES:
            iplist = (getIp(page))
            print('page is：' + str(page))
            page += 1
            time.sleep(1)
            for i in iplist:
                f.write(i + '\n')