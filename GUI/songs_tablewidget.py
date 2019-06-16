# coding: UTF-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import *
import sys


class SongTableWidget(QTableWidget):
    sig_download_song = pyqtSignal(str)
    sig_checkbox_selected = pyqtSignal(bool)

    def __init__(self, song_info=None, parent=None):
        super(SongTableWidget, self).__init__(parent)

        # TEST Data!
        self.song_info = song_info
        self.headers = ["", "歌曲", "歌手", "专辑", "时长", "下载"]

        # Init member
        self.selected_checkbox_num = 0  # 被选中的checkbox数量
        self.current_page = 1   # 当前显示的是第几页

        # Init
        self.init_ui()
        self.init_connect()
        # self.init_data(1)

    def init_ui(self):
        # Init property
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.setFixedSize(750, 500)
        # self.setMinimumWidth(500)
        # self.setMinimumHeight(300)
        self.setRowCount(30)    # 默认一页显示30行信息
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(self.headers)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def init_connect(self):
        pass

    def update_data(self, song_info):
        self.song_info = song_info

    def init_data(self, page):
        # 设置新的cellwidget时，会自动取代掉以前的cellwidget
        self.current_page = page    # 更新变量
        for row in range(30):
            self.add_one_row(row, self.song_info[row])

    def add_one_row(self, row, info):
        check_box = QCheckBox()
        check_box.setFixedSize(30, 30)
        label_songname = QLabel(info["song_name"])
        label_songname.setMinimumSize(100, 30)
        label_songname.setMaximumSize(180, 30)
        label_songname.setToolTip(info["song_name"])
        label_singer = QLabel(info["singer"])
        label_singer.setMinimumSize(50, 30)
        label_singer.setMaximumSize(100, 30)
        label_singer.setToolTip(info["singer"])
        label_album = QLabel(info["album_name"])
        label_album.setMinimumSize(100, 30)
        label_album.setMaximumSize(180, 30)
        label_album.setToolTip(info["album_name"])
        label_duration = QLabel(info["interval"])
        label_duration.setToolTip(info["interval"])
        label_duration.setFixedSize(80, 30)
        btn_download = QPushButton("下载")

        check_box.stateChanged.connect(self.datect_checkbox)
        btn_download.clicked.connect(self.emit_download_sig)

        self.setCellWidget(row, 0, check_box)
        self.setCellWidget(row, 1, label_songname)
        self.setCellWidget(row, 2, label_singer)
        self.setCellWidget(row, 3, label_album)
        self.setCellWidget(row, 4, label_duration)
        self.setCellWidget(row, 5, btn_download)

    @pyqtSlot(bool)
    def select_all_songs(self, flag=True):
        """flag参数为True时表示全选,False为取消全选"""
        for row in range(self.rowCount()):
            if flag is True:
                if self.cellWidget(row, 0).checkState() == 0:
                    self.cellWidget(row, 0).setCheckState(Qt.Checked)
            else:
                if self.cellWidget(row, 0).checkState() == 2:
                    self.cellWidget(row, 0).setCheckState(Qt.Unchecked)

    @pyqtSlot()
    def emit_download_checked_songs(self):
        # Todo:给外部的下载按钮调用
        for row in range(self.rowCount()):
            if self.cellWidget(row, 0).checkState() > 0:
                # Todo:发送下载信号(参数:mid)
                song_mid = self.song_info[row]["song_mid"]
                self.sig_download_song.emit(song_mid)

    @pyqtSlot()
    def emit_download_sig(self):
        sender_obj = self.sender()
        idx = self.indexAt(QPoint(sender_obj.frameGeometry().x(), sender_obj.frameGeometry().y()))
        song_mid = self.song_info[idx.row()]["song_mid"]
        # Todo:发送下载信号(参数:mid)
        self.sig_download_song.emit(song_mid)

    def datect_checkbox(self, isCheck):
        if isCheck > 0:
            self.selected_checkbox_num += 1
        elif isCheck == 0:
            self.selected_checkbox_num -= 1

        if self.selected_checkbox_num == 1:     # 当大于1时并不需要发送信号去更新
            self.sig_checkbox_selected.emit(True)
        elif self.selected_checkbox_num == 0:
            self.sig_checkbox_selected.emit(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SongTableWidget()
    demo.show()
    demo.select_all_songs()
    sys.exit(app.exec_())
