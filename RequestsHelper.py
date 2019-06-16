# coding: UTF-8
import requests
"""通用的工具类"""


class RequestsHelper:
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/72.0.3626.121 Safari/537.36",
               'Referer': 'http://y.qq.com'}

    @classmethod
    def set_domain(cls):
        """为之后更新不同音乐平台的api留接口"""
        pass

    @classmethod
    def url_is_error(cls, url):
        res = requests.get(url, headers=cls.headers)
        return res.raise_for_status()

    @staticmethod
    def splice_url(url, params: dict):
        """拼接url"""
        for k, v in params.items():
            url += (k + "=" + str(v))

        return url

    @classmethod
    def get_response_json(cls, url):
        response = requests.get(url, headers=cls.headers)
        return response.json()

    @classmethod
    def get_response_text(cls, url):
        response = requests.get(url, headers=cls.headers)
        return response.text

