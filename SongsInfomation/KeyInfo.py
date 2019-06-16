# coding: UTF-8
"""主要用于获取歌曲的vkey"""
from MusicAPI.QQMusic import QQMusicAPI as qq
from RequestsHelper import RequestsHelper as reqhelper


class KeyInfo:
    fcg_url = qq.fcg_url   # 固定链接

    @classmethod
    def get_vkey(cls):
        return reqhelper.get_response_json(cls.fcg_url)["key"]


if __name__ == '__main__':
    print(KeyInfo.get_vkey())
