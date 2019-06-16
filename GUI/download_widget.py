# coding: UTF-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import *
import sys
import re
import os
current_path = (os.path.dirname(os.path.realpath(sys.argv[0]))+'/').replace('\\', '/')


class DownloadWidget(QWidget):
    sig_download_cancel = pyqtSignal()

    def __init__(self, parent=None):
        super(DownloadWidget, self).__init__(parent)

        # Init member
        self.path_lineEdit = QLineEdit()
        self.select_path_btn = QPushButton("选择路径")
        self.download_table = QTableWidget()

        self.__default_path = current_path
        self.headers = ["歌曲", "下载进度", "大小", ""]

        self.song_mids = []  # 维护一个mid列表,来找到位置row

        # Init
        self.init_ui()
        self.init_connect()
    #     # Test
    #     self.init_data()
    #
    # def init_data(self):
    #     # 设置新的cellwidget时，会自动取代掉以前的cellwidget
    #     for row in range(30):
    #         self.add_download_item(["一路向北-周杰伦", 3000000, "songmid"+str(row)], row)

    def init_ui(self):
        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()

        self.path_lineEdit.setFixedSize(400, 36)
        self.select_path_btn.setFixedSize(90, 36)

        self.path_lineEdit.setFocusPolicy(Qt.NoFocus)
        self.path_lineEdit.setText(self.__default_path)

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Init download table
        self.download_table.setMinimumWidth(530)
        self.download_table.setColumnCount(4)
        self.download_table.setHorizontalHeaderLabels(self.headers)
        self.download_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.download_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.download_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.download_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.download_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        hlayout.addWidget(self.path_lineEdit)
        hlayout.addWidget(self.select_path_btn)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.download_table)

        self.setLayout(vlayout)

    def init_connect(self):
        self.select_path_btn.clicked.connect(self.select_path)

    def select_path(self):
        file_path = QFileDialog.getExistingDirectory(self, "选择下载路径", "/")
        if file_path == '':
            return
        else:
            self.path_lineEdit.setText(file_path+'/')

    def _set_directory_path(self, file_path):
        """设置当前路径"""
        self.path_lineEdit.setText(file_path + '/')

    def get_directory_path(self):
        """返回当前选择的路径"""
        return self.path_lineEdit.text()

    def add_download_item(self, info, row=None):
        if row is None:
            row = self.download_table.rowCount()

        label_song = QLabel(info[0])
        label_song.setToolTip(info[0])
        label_song.setFixedSize(180, 30)

        processbar = QProgressBar()
        processbar.setRange(0, 100)
        processbar.setMinimumWidth(200)
        processbar.setValue(0)
        processbar.setStyleSheet(
                "QProgressBar {border: 2px solid grey;   border-radius: 5px;"
                "background-color: #FFFFFF;"
                "text-align: center;}"
                "QProgressBar::chunk {background-color: rgb(0,250,0) ;}"
                )

        label_downloading = QLabel("0.0M/" + str(self.convert_B_to_MB(info[1])) + "M")

        remove_btn = QPushButton("X")
        remove_btn.setFixedSize(30, 30)
        remove_btn.clicked.connect(self.remove_download_item)

        self.download_table.insertRow(row)
        self.download_table.setCellWidget(row, 0, label_song)
        self.download_table.setCellWidget(row, 1, processbar)
        self.download_table.setCellWidget(row, 2, label_downloading)
        self.download_table.setCellWidget(row, 3, remove_btn)

        self.song_mids.append(info[2])      # 更新song_mids

    def update_download_item(self, current_size, row):
        """更新下载进度"""
        total_size = float(re.findall(r'/([^M]+)', self.download_table.cellWidget(row, 2).text())[0])   # 利用re获取歌曲大小
        download_percent = (current_size / (total_size*1024*1024)) * 100

        download_str = str(self.convert_B_to_MB(current_size)) + 'M/' + str(total_size) + 'M'

        self.download_table.cellWidget(row, 2).setText(download_str)
        self.download_table.cellWidget(row, 1).setValue(download_percent)
        QApplication.processEvents()    # 让程序处理那些还没有处理的事件,防止UI阻塞(此处因为频繁的调用update，除了setText和setValue操作以外的界面来不及更新)

    def update_download_item_finished(self, song_mid):
        """下载完成"""
        for order, value in enumerate(self.song_mids):
            if value == song_mid:
                self.download_table.cellWidget(order, 2).setText("下载完成")
                self.download_table.cellWidget(order, 1).setValue(100)

    def update_download_item_error(self, song_mid):
        """下载失败"""
        for order, value in enumerate(self.song_mids):
            if value == song_mid:
                self.download_table.cellWidget(order, 2).setText("下载失败")
                # self.download_table.cellWidget(order, 1).setValue(0)

    def update_download_item_by_songmid(self, song_info):
        song_mid = song_info[0]
        for order, value in enumerate(self.song_mids):
            if value == song_mid:
                if self.download_table.cellWidget(order, 2).text() == '下载失败':
                    continue
                else:
                    self.update_download_item(song_info[1], order)

    @pyqtSlot()
    def remove_download_item(self):
        sender_obj = self.sender()
        idx = self.download_table.indexAt(QPoint(sender_obj.frameGeometry().x(), sender_obj.frameGeometry().y()))

        # Todo:当未下载完成时提示用户，并发送中断信号
        if self.download_table.cellWidget(idx.row(), 2).text() == '下载失败':
            self.download_table.removeRow(idx.row())
            self.song_mids.pop(idx.row())

        elif self.download_table.cellWidget(idx.row(), 1).value() != 100:
            tip_msg_box = QMessageBox()
            tip_msg_box.setWindowTitle("Tips")
            ok_btn = tip_msg_box.addButton(QMessageBox.Ok)
            cancel_btn = tip_msg_box.addButton(QMessageBox.Cancel)
            tip_msg_box.setText("当前歌曲还未下载完成，确定取消吗?")
            tip_msg_box.exec()
            if tip_msg_box.clickedButton() is ok_btn:
                self.sig_download_cancel.emit()
                self.download_table.removeRow(idx.row())
                self.song_mids.pop(idx.row())
        else:
            self.download_table.removeRow(idx.row())
            self.song_mids.pop(idx.row())

    def is_downloading(self):
        """
        判断当前是否还有歌曲正在下载
        :return: True 正在下载
                 False 没有下载
        """
        for row in range(self.download_table.rowCount()):
            if self.download_table.cellWidget(row, 1).value() != 100:
                return True
        return False

    @staticmethod
    def convert_B_to_MB(content_size):
        """把格式B转换为MB"""
        return round(content_size / 1024 / 1024, 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DownloadWidget()
    demo.show()
    demo.add_download_item(["song_name", 3000000, "song_mid"])
    # print(demo.song_mids)
    # slipe = 3000000/50
    # import time
    # for x in range(50):
    #     time.sleep(0.5)
    #     demo.update_download_item_by_songmid(['song_mid', slipe*x])
    # # print(DownloadWidget.convert_B_to_MB(3755924))
    sys.exit(app.exec_())



