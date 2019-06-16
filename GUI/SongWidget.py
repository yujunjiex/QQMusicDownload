# coding: UTF-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import *
import sys
from GUI.songs_tablewidget import SongTableWidget
from GUI.TopBar import TopBar
from GUI.IndexBar import IndexBar
from GUI.search_widget import SearchWidget
from GUI.download_widget import DownloadWidget
from SongsInfomation.SearchInfo import SearchInfo
from SongsInfomation.SongUrl import SongUrl
from Download.music_downloader import Downloader

from WorkThread import WorkThread


class SongWidget(QWidget):
    sig_search = pyqtSignal(dict)
    sig_get_download_info = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(SongWidget, self).__init__(parent)

        # Init member
        self.top_bar = TopBar()
        self.center_tablewidget = SongTableWidget()
        self.index_bar = IndexBar(1)
        self.search_widget = SearchWidget()
        self.download_widget = DownloadWidget()

        # Init thread
        self.net_thread = QThread()
        self.word_thread = WorkThread()

        self.downloader = Downloader()
        self.download_info = []     # 提供下载一首歌曲所需的信息
        self.download_state = False     # 判断当前是否有下载任务

        # Init
        self.init()

    def init(self):
        self.init_ui()
        self.init_connect()
        self.init_thread()

    def init_ui(self):
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        vlayout.addWidget(self.search_widget)
        vlayout.addWidget(self.top_bar)
        vlayout.addWidget(self.center_tablewidget)
        vlayout.addWidget(self.index_bar)
        vlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.addLayout(vlayout)
        hlayout.addWidget(self.download_widget)
        self.top_bar.setFixedHeight(46)
        self.center_tablewidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.index_bar.setFixedHeight(100)
        self.setLayout(hlayout)

    def init_connect(self):
        self.top_bar.select_all_checkBox.stateChanged.connect(lambda state:\
                                                              self.center_tablewidget.select_all_songs(True) if state > 0 else \
                                                              self.center_tablewidget.select_all_songs(False))
        self.top_bar.download_btn.clicked.connect(self.center_tablewidget.emit_download_checked_songs)
        self.center_tablewidget.sig_checkbox_selected.connect(self.top_bar.set_download_btn_state)
        self.index_bar.sig_currentPageChanged.connect(self.update_current_page)
        self.search_widget.sig_search_info.connect(self.search_and_update_current_page)
        # 关联下载信号
        self.center_tablewidget.sig_download_song.connect(self.download_music)

    def init_thread(self):
        self.word_thread.moveToThread(self.net_thread)

        # 关联子线程
        self.word_thread.sig_searchReady.connect(self.update_page)
        self.sig_search.connect(self.word_thread.search)

        self.sig_get_download_info.connect(self.word_thread.get_download_info)

        self.net_thread.finished.connect(self.net_thread.deleteLater)

        # 关联下载线程
        self.downloader.moveToThread(self.net_thread)
        self.downloader.sig_download_process.connect(self.download_widget.update_download_item_by_songmid)
        self.downloader.sig_download_finished.connect(self.download_widget.update_download_item_finished)
        self.downloader.sig_download_finished.connect(self.update_download_state)

        self.downloader.sig_something_error.connect(self.notify_choose_other_path)
        self.downloader.sig_something_error.connect(self.download_widget.update_download_item_error)
        self.downloader.sig_something_error.connect(self.update_download_state)

        self.download_widget.sig_download_cancel.connect(self.stop_current_download)

        # 启动工作线程
        self.net_thread.start()

    @pyqtSlot(str)
    def search_and_update_current_page(self, search_info):
        """重新搜索"""
        search_dict = {"word": search_info}
        self.sig_search.emit(search_dict)

    @pyqtSlot(int)
    def update_current_page(self, page_id):
        """在当前已搜索的界面上翻页"""
        search_dict = {"page": page_id}
        self.sig_search.emit(search_dict)

    @pyqtSlot(dict)
    def update_page(self, song_info):
        """通过子线程传过来的信息来更新界面"""
        self.center_tablewidget.update_data(song_info)
        self.center_tablewidget.init_data(WorkThread.search_info.get_current_page())
        # update index bar
        if WorkThread.search_info.get_current_page() == 1:  # 当前页为1时默认进行了重新搜索操作
            self.index_bar.update_IndexBar(WorkThread.search_info.get_total_pages())

    @pyqtSlot(str)
    def download_music(self, song_mid):
        """音乐下载"""
        # 交给工作线程处理
        self.sig_get_download_info.emit({"song_mid": song_mid, "quality": self.top_bar.get_quality()})
        # self.top_bar.get_quality(), song_mid
        loop = QEventLoop()
        self.word_thread.sig_downloadinfoReady.connect(loop.quit)
        loop.exec()

        self.download_widget.add_download_item([WorkThread.download_info["song_name"],
                                                WorkThread.download_info["content_size"],
                                                WorkThread.download_info["song_mid"]])     # 先在界面上添加一个下载

        if self.download_state is False:
            directory_path = self.download_widget.get_directory_path()
            self.downloader.download_music_by_url(WorkThread.download_info["song_url"],
                                                  directory_path,
                                                  WorkThread.download_info["song_name"] + '.' + self.top_bar.get_quality(),
                                                  song_mid=song_mid)
        else:
            loop = QEventLoop()
            self.downloader.sig_download_finished.connect(loop.quit)
            self.downloader.sig_something_error.connect(loop.quit)
            loop.exec()

    def update_download_state(self):
        """当下载完成后重置此标记"""
        self.download_state = False

    def stop_current_download(self):
        """中断当前下载"""
        self.downloader.set_stop()

    @staticmethod
    def notify_choose_other_path():
        QMessageBox.information(None, "提示", "当前路径下载失败, 请选择其他路径下载")

    def is_downloading(self):
        """
        判断当前是否有歌曲正在下载
        :return: True 正在下载
                False 没有下载
        """
        return self.download_widget.is_downloading()

    def exit_all_thread(self):
        """关闭网络线程"""
        self.net_thread.quit()
        self.net_thread.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SongWidget()
    demo.show()

    sys.exit(app.exec_())
