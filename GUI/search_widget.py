# coding: UTF-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from SongsInfomation.SearchInfo import SearchInfo
from WorkThread import WorkThread
from PyQt5.Qt import *
import sys


class SearchWidget(QWidget):
    sig_search_info = pyqtSignal(str)
    sig_search_smart_box = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SearchWidget, self).__init__(parent)

        # Init member
        self.search_lineEdit = QLineEdit()
        self.btn_search = QPushButton("搜索")
        self.completer = QCompleter()  # 用于实现lineEdit自动补全
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.list_model = QStringListModel()
        self.completer.setModel(self.list_model)

        # Init thread
        self.net_thread = QThread()
        self.word_thread = WorkThread()

        self.init_ui()
        self.init_connect()
        self.init_thread()

    def init_ui(self):
        search_layout = QHBoxLayout()
        hlayout = QHBoxLayout()

        # self.search_lineEdit.setFixedSize(700, 40)
        self.search_lineEdit.setMinimumWidth(400)
        self.search_lineEdit.setFixedHeight(40)
        self.search_lineEdit.setCompleter(self.completer)
        self.search_lineEdit.setStyleSheet("QLineEdit{border-radius:10px;background:rgb(255,255,255,150);}")
        self.search_lineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.btn_search.setCursor(Qt.PointingHandCursor)
        self.btn_search.setFixedSize(60, 36)

        self.search_lineEdit.setPlaceholderText("搜索歌曲")
        margins = self.search_lineEdit.textMargins()
        self.search_lineEdit.setTextMargins(margins.left() + 15, margins.top(), self.btn_search.width() + 15, margins.bottom())

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        search_layout.addStretch()
        search_layout.addWidget(self.btn_search)
        search_layout.setSpacing(0)
        search_layout.setContentsMargins(0, 0, 15, 0)
        self.search_lineEdit.setLayout(search_layout)

        hlayout.addWidget(self.search_lineEdit)
        self.setLayout(hlayout)

    def init_connect(self):
        self.search_lineEdit.returnPressed.connect(self.btn_search.click)
        self.search_lineEdit.textChanged.connect(self.send_smart_box_signal)
        self.btn_search.clicked.connect(lambda: self.sig_search_info.emit(self.search_lineEdit.text()))

    def init_thread(self):
        self.word_thread.moveToThread(self.net_thread)

        # 关联子线程
        self.word_thread.sig_smartBoxReady.connect(self.update_completer)
        self.net_thread.finished.connect(self.net_thread.deleteLater)
        self.sig_search_smart_box.connect(self.word_thread.search_smart_box)

        # 启动工作线程
        self.net_thread.start()

    @pyqtSlot(str)
    def send_smart_box_signal(self, info):
        if info != "":
            self.sig_search_smart_box.emit(self.search_lineEdit.text())

        loop = QEventLoop()
        self.word_thread.sig_smartBoxReady.connect(loop.quit)  # 开启事件循环，在这次结果没有获取之前不会再发信号
        loop.exec()

    @pyqtSlot(list)
    def update_completer(self, search_result):
        print(search_result)
        self.list_model.setStringList(search_result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SearchWidget()
    demo.show()

    sys.exit(app.exec_())
