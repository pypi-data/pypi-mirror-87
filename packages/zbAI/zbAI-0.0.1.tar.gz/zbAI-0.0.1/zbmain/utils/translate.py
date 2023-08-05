#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/14 16:37
# @Blog    : https://blog.zbmain.com

import hashlib
import http.client
import json
import random
import urllib
from urllib.request import urlopen
__all__ = ['__getBaiduTranslateConfigFromJson','BaiduTranslate','YoudaoTranslate','GoogleTranslate']

def __getBaiduTranslateConfigFromJson(configUrl=''):
    '''
    json格式：
    {
        "translate":{
            "baidu":{
                "appid":"",
                "secretKey":""
            },
            "google":{
                "appid":"",
                "secretKey":""
            },"youdao":{
                "appid":"",
                "secretKey":""
            }
        }
    }
    :param configUrl:
    :return:
    '''
    configJSON = configUrl or 'https://zbmain.com/files/others/config.json'
    resultJSON = json.loads(urlopen(configJSON).read())
    return resultJSON['translate']['baidu']['appid'], resultJSON['translate']['baidu']['secretKey']


class BaiduTranslate():
    def __init__(self, appid, secretKey, fromLang='en', toLang='cn', apiUrl=''):
        '''
        appid、secretKey自行前往官方注册
        :param appid:
        :param secretKey:
        :param fromLang: 翻译器的源语种，默认英文
        :param toLang: 翻译器的目标语种，默默中文
        :param apiUrl: api地址，默认空，若官方更新接口可新设置
        '''
        self.apiUrl = apiUrl or '/api/trans/vip/translate'
        self.appid = appid
        self.secretKey = secretKey
        self.fromLang = fromLang
        self.toLang = toLang

    def __call__(self, text, fromLang='', toLang=''):
        '''
        :param text: 翻译输入
        :param fromLang: 临时源语种【可选】
        :param toLang: 临时目标语种【可选】
        :return: (是否成功,输出,输入)
        '''
        fromLang = fromLang or self.fromLang
        toLang = toLang or self.toLang
        salt = str(random.randint(32768, 65536))
        sign = self.appid + text + salt + self.secretKey
        sign = hashlib.md5(sign.encode(encoding='utf-8')).hexdigest()

        requestUrl = self.apiUrl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(
            text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + salt + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', requestUrl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            return True, result["trans_result"][0]["dst"], result["trans_result"][0]["src"]
        except Exception as e:
            return False, e
        finally:
            if httpClient:
                httpClient.close()


class YoudaoTranslate():
    def __init__(self):
        print('To be updated')


class GoogleTranslate():
    def __init__(self):
        print('To be updated')


if __name__ == "__main__":
    appid, secretKey = __getBaiduTranslateConfigFromJson()
    baiduTranslate = BaiduTranslate(appid, secretKey, 'auto', 'en')
    print(baiduTranslate('你好，世界！'))
