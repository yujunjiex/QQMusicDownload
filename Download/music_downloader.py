# coding: UTF-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import *
import requests
import os
import re
"""歌曲下载模块"""


class Downloader(QObject):
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) "
                             "Chrome/17.0.963.56 Safari/535.11",
               'Referer': 'http://y.qq.com'}

    sig_download_process = pyqtSignal(list)     # [songmid, download_size]
    sig_notify_downloaded = pyqtSignal()
    sig_download_finished = pyqtSignal(str)

    sig_something_error = pyqtSignal(str)       # songmid

    def __init__(self, parent=None):
        super(Downloader, self).__init__(parent)
        self.is_stop = False

    def set_stop(self):
        self.is_stop = True

    def download_music_by_url(self, song_url, directory_path, song_name, song_mid):
        with requests.get(song_url, stream=True, headers=self.headers) as r:
            chunk_size = 1024
            content_size = int(r.headers['content-length'])
            song_name = self.validateTitle(song_name)   # 去掉文件名中的非法字符
            file_path = directory_path + song_name      # 2个变量，文件路径，文件名

            download_size = 0
            if os.path.exists(file_path) and os.path.getsize(file_path) == content_size:
                # Todo: 提示用户歌曲已存在
                print("歌曲已存在")
                self.sig_download_finished.emit(song_mid)   # 直接提示已完成
                return
            # else:
            # print("文件大小:", content_size)
            print(file_path)
            try:
                with open(file_path, "wb") as file:
                    for data in r.iter_content(chunk_size=chunk_size):
                        if self.is_stop is True:
                            self.is_stop = False
                            print("中断成功！")
                            return
                        file.write(data)
                        download_size += len(data)
                        self.sig_download_process.emit([song_mid, download_size])
            except PermissionError:
                self.sig_something_error.emit(song_mid)
                return
            self.sig_download_finished.emit(song_mid)

    @staticmethod
    def validateTitle(title):
        """
        替换Windows文件名中的非法字符
        摘自：https://blog.csdn.net/e15273/article/details/80632940
        """
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title


if __name__ == '__main__':
    pass
