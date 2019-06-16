# coding: UTF-8
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from GUI.SongWidget import SongWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("QQ音乐爬取下载——仅用作参考学习")

        self.song_widget = SongWidget()

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.song_widget)

    def closeEvent(self, event):
        """
        判断当前有没有任务正在下载来提示用户
        :param event: close()触发的事件
        :return: None
        """
        # Todo: 判断当前是否有任务正在下载
        if self.song_widget.is_downloading() is True:
            reply = QMessageBox.question(self,
                                         '音乐下载器',
                                         "当前还有歌曲正在下载，是否退出？(没有做暂停功能哦~)")
        else:
            reply = QMessageBox.question(self,
                                         '音乐下载器',
                                         "是否退出程序？",
                                         QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Todo:关闭网络线程
            self.song_widget.exit_all_thread()
            event.accept()
        else:
            event.ignore()
