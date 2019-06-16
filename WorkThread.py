# coding: UTF-8
from PyQt5.QtCore import *
from SongsInfomation.SearchInfo import SearchInfo
"""把网络操作放到工作线程中执行"""


class WorkThread(QObject):
    sig_searchReady = pyqtSignal(dict)
    search_info = SearchInfo()

    download_info = {}      # [song_mid, song_name, content_size, song_url]
    sig_downloadinfoReady = pyqtSignal()

    sig_smartBoxReady = pyqtSignal(list)

    def search(self, search_dict: dict):
        keywords = ["word", "page", "nums"]
        search_info = []
        for k in keywords:
            if k in search_dict:
                search_info.append(search_dict.get(k))
            else:
                search_info.append(None)

        if search_info[1] is None:
            search_info[1] = SearchInfo.default_page
        if search_info[2] is None:
            search_info[2] = SearchInfo.default_nums

        song_info = self.search_info.search(word=search_info[0], page=search_info[1], nums=search_info[2])
        self.sig_searchReady.emit(song_info)

    def search_smart_box(self, info):
        result = SearchInfo.get_smart_box_info(info)["singers"] + \
                 SearchInfo.get_smart_box_info(info)["songs"] + \
                 SearchInfo.get_smart_box_info(info)["albums"]
        self.sig_smartBoxReady.emit(result)

    def get_download_info(self, info: dict):
        song_mid = info["song_mid"]
        quality = info["quality"]
        from SongsInfomation.SingleSongInfo import SingleSongInfo
        from SongsInfomation.SongUrl import SongUrl
        song_url = SongUrl.get_url_by_mid(song_mid, quality=quality)
        content_size = SingleSongInfo.get_song_content_size(song_mid, quality=quality)
        song_name = SingleSongInfo.get_song_name(song_mid)
        self.download_info["song_url"] = song_url
        self.download_info["content_size"] = content_size
        self.download_info["song_name"] = song_name
        self.download_info["song_mid"] = song_mid
        self.sig_downloadinfoReady.emit()



