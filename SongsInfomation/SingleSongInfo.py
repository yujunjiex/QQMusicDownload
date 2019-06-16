# coding: UTF-8
"""通过mid获取单首歌曲的详细信息"""
from MusicAPI.QQMusic import QQMusicAPI as qq
from RequestsHelper import RequestsHelper as reqhelper


class SingleSongInfo:
    def __init__(self, song_mid):
        self.single_song_url = qq.single_song_url.format(song_mid)

        self.album_pic_url = None   # album封面链接
        self._search_response = {}   # json格式的信息

        # Init
        self.__set_search_json()
        self.__set_album_pic_url()

    def __set_search_json(self):
        self._search_response = reqhelper.get_response_json(self.single_song_url)

    def __set_album_pic_url(self):
        album_id = self._search_response["songinfo"]["data"]["track_info"]["album"]["id"]
        self.album_pic_url = qq.album_pic_url.format(album_id % 100, album_id)

    def get_album_url(self):
        """返回歌曲的封面链接"""
        return self.album_pic_url

    def get_detail_info(self):
        """获取歌曲详细信息(例如唱片发行时间，专辑信息)"""
        pass

    @staticmethod
    def get_song_name(song_mid):
        """返回对应mid的歌曲名"""
        single_song_url = qq.single_song_url.format(song_mid)
        search_response = reqhelper.get_response_json(single_song_url)
        singers = ""  # 一首歌的歌手可能有多个
        for singer in search_response["songinfo"]["data"]["track_info"]["singer"]:
            singers += (singer["name"] + "/")
        singers = singers[:-1]  # 删去最后一个左斜杠
        return search_response["songinfo"]["data"]["track_info"]["title"] + " - " + singers

    @staticmethod
    def get_song_interval(song_mid):
        """返回对应mid的歌曲时长"""
        single_song_url = qq.single_song_url.format(song_mid)
        search_response = reqhelper.get_response_json(single_song_url)
        return search_response["songinfo"]["data"]["track_info"]["interval"]

    @staticmethod
    def get_song_content_size(song_mid, quality):
        single_song_url = qq.single_song_url.format(song_mid)
        search_response = reqhelper.get_response_json(single_song_url)
        if quality == 'mp3':
            return search_response["songinfo"]["data"]["track_info"]["file"]["size_128mp3"]
        elif quality == 'm4a':
            return search_response["songinfo"]["data"]["track_info"]["file"]["size_96aac"]


if __name__ == '__main__':
    print(SingleSongInfo.get_song_interval('000g3Mdb3KYGPM'))
    print(SingleSongInfo.get_song_name('000g3Mdb3KYGPM'))



