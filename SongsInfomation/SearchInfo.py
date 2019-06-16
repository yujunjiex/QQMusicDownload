# coding: UTF-8
"""获取音乐搜索信息"""
from MusicAPI.QQMusic import QQMusicAPI as qq
from RequestsHelper import RequestsHelper as reqhelper
from SongsInfomation.SingleSongInfo import SingleSongInfo
import json


class SearchInfo:
    default_page = 1
    default_nums = 30

    def __init__(self, word=None, page=1, nums=30):
        self.params = {
            '?aggr': 1,
            '&cr': 1,
            '&flag_qc': 0,
            '&p': None,
            '&n': None,
            '&w': None
        }
        self.word = None    # 当前正在搜索的word
        self.nums = None  # 每页显示的数量

        self.current_page = None    # 最近一次搜索的页数
        self.pages = None   # 总页数

        self._search_json = {}      # json格式的信息
        self._search_result = {}     # 更加友好的格式信息
        self.search_url = reqhelper.splice_url(qq.search_url, self.params)

        # Init
        self.search(word, page, nums)

    def search(self, word=None, page=1, nums=30):
        """重新搜索"""
        self.params["&p"] = page
        self.params["&n"] = nums
        if word is None:
            self.params["&w"] = self.word
        else:
            self.params["&w"] = self.word = word

        self.current_page = page
        self.nums = nums

        self.search_url = reqhelper.splice_url(qq.search_url, self.params)
        self.__set_search_json()
        self.__set_total_pages()

        return self._get_search_result()

    def _get_search_result(self):
        """返回更人性化格式的信息"""
        for order, info in enumerate(self._search_json["data"]["song"]["list"]):    # 这里本应该不用order(用界面来控制)

            album_name = info["albumname"]
            singers = ""    # 一首歌的歌手可能有多个
            for singer in info["singer"]:
                singers += (singer["name"] + "/")
            singers = singers[:-1]     # 删去最后一个左斜杠
            song_name = info["songname"]
            song_mid = info["songmid"]
            # Todo:当interval为0时要用SingleSongInfo进行查找
            if info["interval"] == 0:
                _interval = SingleSongInfo.get_song_interval(song_mid)
            else:
                _interval = info["interval"]
            interval = self.convert_interval_format(_interval)

            self._search_result[order] = {"song_name": song_name, "singer": singers, "album_name": album_name, "interval": interval, "song_mid": song_mid}
        return self._search_result

    def __set_search_json(self):
        response = reqhelper.get_response_text(self.search_url)[9:-1]  # 除去开头和结尾非json格式的字符
        self._search_json = json.loads(response)

    def __set_total_pages(self):
        temp = self.get_total_songs() // self.nums
        self.pages = temp + (1 if self.get_total_songs() % self.nums > 0 else 0)

    def get_current_page(self):
        """获取最近一次搜索的页数"""
        return self.current_page

    def get_total_pages(self):
        """获取歌曲总页数"""
        return self.pages

    def get_total_songs(self):
        """获取歌曲总数"""
        return self._search_json["data"]["song"]["totalnum"]

    @staticmethod
    def get_smart_box_info(word):
        response = reqhelper.get_response_json(qq.smart_box_url.format(word))
        singers = []
        for singer in response["data"]["singer"]["itemlist"]:
            singers.append(singer["singer"])
        songs = []
        for song in response["data"]["song"]["itemlist"]:
            songs.append(song["name"]+"-"+song["singer"])
        albums = []
        for album in response["data"]["album"]["itemlist"]:
            albums.append(album["name"]+"  "+album["singer"])
        smart_box_info = {"singers": singers, "songs": songs, "albums": albums}
        return smart_box_info

    @staticmethod
    def convert_interval_format(interval):
        """转换interval的格式为 s:m"""
        m = interval // 60
        s = interval % 60
        return "%02d" % m + ":" + "%02d" % s


if __name__ == '__main__':
    demo = SearchInfo("我曾")
    # import timeit
    # print(timeit.timeit(lambda :SearchInfo("我曾"), number=1))
    # print("总页数:", demo.get_total_pages())
    # print(demo.search(page=1))
    # print(demo.search("周杰伦", page=1))
    # print("总页数", demo.get_total_pages())



