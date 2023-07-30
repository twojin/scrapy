import json

import scrapy
from functools import reduce
from hashlib import md5
import urllib.parse
import time
from ..items import BilibiliUserItem
class BilibiliScrapy(scrapy.Spider):
    img_key = None
    sub_key = None
    url = "https://api.bilibili.com/x/space/wbi/acc/info"
    url2 = "https://api.bilibili.com/x/relation/stat"
    referer_url = "https://space.bilibili.com/%s?spm_id_from=333.1007.tianma.1-2-2.click"

    mixinKeyEncTab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]

    # 爬虫名 必须唯一
    name = "bilibili"
    # 允许爬取的域名，如果不在这些域名内的链接将被过滤掉。start_urls里的域名不会被过滤。
    # allowed_domains = [""]
    start_urls = [
        "https://api.bilibili.com/x/web-interface/nav"
    ]

    def parse(self, response):
        if response.status != 200:
           return
        else:
            self.getWbiKeys(response)

        for mid in range(35368644, 35369645):
            add_params = {
                "mid": str(mid)
            }
            yield scrapy.FormRequest(url=self.url, formdata=self.getParams(mid), method="get", headers=self.getHeaders(mid), callback=self.my_parse, dont_filter = True, cb_kwargs=add_params)

    def my_parse(self, response, mid):

        if ( response.status == 200 ):
            request = response.request
            userInfo = response.json()
            data = userInfo['data']
            if userInfo['code'] == -404:
                print(str(mid) + "无效")
                print("-----------------------------------")
            elif userInfo['code'] == -403:
                print("访问权限不足！！！")
                print(request)
                print("-----------------------------------")
            elif userInfo['code'] == -400:
                print("请求错误！！！")
                print(request)
                print("-----------------------------------")
            else:
                item = BilibiliUserItem()
                item[item.name2] = data['name']
                item[item.mid2] = data['mid']
                item[item.sex2] = data['sex']
                item[item.sign2] = data['sign']
                item[item.rank2] = data['rank']
                item[item.level2] = data['level']
                item[item.silence2] = data['silence']
                item[item.official_role2] = data['official']['role']
                item[item.official_type2] = data['official']['type']
                item[item.vip_type2] = data['vip']['type']
                item[item.vip_status2] = data['vip']['status']
                item[item.vip_due_date2] = data['vip']['due_date']
                item[item.vip_label_text2] = data['vip']['label']['text']
                item[item.vip_label_label_theme2] = data['vip']['label']['label_theme']
                item[item.vip_role2] = data['vip']['role']
                item[item.vip_tv_vip_status2] = data['vip']['tv_vip_status']
                item[item.birthday2] = data['birthday']
                if data['school'] != None:
                    item[item.school_name2] = data['school']['name']
                else:
                    data['school'] = ''
                item[item.is_senior_member2] = data['is_senior_member']
                item[item.elec_show_info_show2] = data['elec']['show_info']['show']
                item[item.elec_show_info_state2] = data['elec']['show_info']['state']

                add_params = {
                    "item": item
                }
                yield scrapy.FormRequest(url=self.url2, formdata=self.getParams2(mid), method="get",
                                         headers=self.getHeaders2(), callback=self.my_parse2, dont_filter=True,
                                         cb_kwargs=add_params)
        else:
            print("状态码异常！！请求接口失败")
            print(response.request)
            print("-----------------------------------")


    def my_parse2(self, response, item:BilibiliUserItem):
        request = response.request
        if ( response.status == 200 ):
            userInfo = response.json()
            data = userInfo['data']
            if userInfo['code'] != 0:
                print("请求错误！！！")
                print(request)
                print("-----------------------------------")
            else:
                item[item.follower2] = data['follower']
                item[item.following2] = data['following']
                yield item
        else:
            print("状态码异常！！请求接口失败")
            print(request)
            print("-----------------------------------")


    def getWbiKeys(self, response):
        json_content = response.json()
        img_url: str = json_content['data']['wbi_img']['img_url']
        sub_url: str = json_content['data']['wbi_img']['sub_url']
        img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        print("img_key:" + img_key)
        print("sub_key:" + sub_key)
        self.img_key = img_key
        self.sub_key = sub_key

    def getParams(self, mid):
        w_rid, wts = self.getWridWts(mid)
        params = {
            "mid": str(mid),
            "platform": "web",
            "web_location": str(1550101),
            "w_rid": w_rid,
            "wts": wts
        }

        return params

    def getParams2(self, mid):
        params = {
            "vmid": str(mid)
        }
        return params
    def getHeaders(self, mid):
        headers = {
            "Accept":"application/json, text/plain, */*",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Origin":"https://space.bilibili.com",
            "Referer":self.referer_url %(str(mid)),
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"Windows",
            "Sec-Fetch-Dest":"empty",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-site",
            "Connection":"keep-alive"
        }
        return headers

    def getHeaders2(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        return headers

    def getWridWts(self, mid):
        params = {
            'foo': '',
            'bar': '',
            'baz': mid
        }
        orig = self.img_key + self.sub_key
        mixin_key = reduce(lambda s, i: s + orig[i], self.mixinKeyEncTab, '')[:32]
        curr_time = round(time.time())
        wts = curr_time
        params = dict(sorted(params.items()))
        params = {
            k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
            for k, v
            in params.items()
        }
        query = urllib.parse.urlencode(params)  # 序列化参数
        wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
        w_rid = wbi_sign
        return w_rid, str(wts)





