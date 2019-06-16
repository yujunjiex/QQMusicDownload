# coding: UTF-8
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import *
import sys
import sip
import time


class IndexBar(QWidget):
    sig_currentPageChanged = pyqtSignal(int)

    def __init__(self, total_num=None, bottom_page=10, parent=None):
        super(IndexBar, self).__init__(parent)

        # Init control member
        self.total_num = total_num  # 总页数
        self.bottom_page = bottom_page  # 底部固定页数
        self.current_page = 1

        # Init ui member
        self.total_label = QLabel()
        self.last_btn = QPushButton("< 上一页")
        self.next_btn = QPushButton("下一页 >")
        self.btn_widget = QWidget()

        self.first_btn = QPushButton()  # 第一个button手动管理，用于判断上下步情况

        # Init
        self.init_ui()
        self.init_connect()

    def init_ui(self):
        self.total_label.setFixedSize(130, 32)
        self.last_btn.setFixedSize(100, 36)
        self.next_btn.setFixedSize(100, 36)
        # temp = self.total_num // self.bottom_page
        # self.pages = temp + (1 if self.total_num % self.bottom_page > 0 else 0)
        if self.total_num < self.bottom_page:
            self.btn_widget = self.init_bottom_btn(self.total_num)
            self.bottom_page = self.total_num   # 当总页数小于默认的底部页数时，将底部页数设为总页数
        else:
            self.btn_widget = self.init_bottom_btn(self.bottom_page)

        hlyaout_above = QHBoxLayout()
        self.hlyaout_under = QHBoxLayout()
        vlyaout_total = QVBoxLayout()
        spacer_item = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        hlyaout_above.addItem(spacer_item)
        hlyaout_above.addWidget(self.total_label)
        hlyaout_above.addItem(spacer_item)

        self.hlyaout_under.addWidget(self.last_btn)
        self.hlyaout_under.addWidget(self.btn_widget)
        self.hlyaout_under.addWidget(self.next_btn)

        vlyaout_total.addLayout(hlyaout_above)
        vlyaout_total.addLayout(self.hlyaout_under)
        self.setLayout(vlyaout_total)
        self.update_label()

    def init_bottom_btn(self, bottom_num):
        layout = QHBoxLayout()
        widget = QWidget()

        # 第一个btn要控制它的生命周期
        self.first_btn.setText("1")
        self.first_btn.setFixedSize(36, 36)
        self.first_btn.clicked.connect(self.slot_send_page_index)

        layout.addWidget(self.first_btn)
        for i in range(2, bottom_num+1):
            btn = QPushButton(str(i))
            btn.setFixedSize(36, 36)
            btn.clicked.connect(self.slot_send_page_index)
            layout.addWidget(btn)
        widget.setLayout(layout)
        return widget

    def init_connect(self):
        self.last_btn.clicked.connect(self.slot_lastbtn_clicked)
        self.next_btn.clicked.connect(self.slot_nextbtn_clicked)
        self.sig_currentPageChanged.connect(self.update_label)

    @pyqtSlot()
    def slot_lastbtn_clicked(self):
        if self.current_page == 1:
            return

        if self.current_page == int(self.first_btn.text()) > 1:  # 满足上一步更新底部button的情况
            for sub_btn in self.btn_widget.children():
                if type(sub_btn) is QPushButton:
                    sub_btn.setText(str(int(sub_btn.text())-1))

        self.current_page = self.current_page - 1
        self.sig_currentPageChanged.emit(self.current_page)  # 发送page改变的信号

    @pyqtSlot()
    def slot_nextbtn_clicked(self):
        if self.current_page == self.total_num:
            return
        if self.current_page == int(self.first_btn.text())+self.bottom_page-1 < self.total_num:  # 满足下一步更新底部button的情况
            for sub_btn in self.btn_widget.children():
                if type(sub_btn) is QPushButton:
                    sub_btn.setText(str(int(sub_btn.text())+1))
        self.current_page = self.current_page + 1
        self.sig_currentPageChanged.emit(self.current_page)     # 发送page改变的信号

    @pyqtSlot()
    def slot_send_page_index(self):
        self.current_page = int(self.sender().text())
        self.sig_currentPageChanged.emit(self.current_page)     # 发送page改变的信号

    def update_label(self):
        self.total_label.setText("共" + str(self.total_num) + "页" + ", 当前第 " + str(self.current_page) + " " + "页")

    def update_IndexBar(self, total_num, bottom_page=10):
        """用于更新IndexBar"""
        self.hlyaout_under.removeWidget(self.btn_widget)
        sip.delete(self.btn_widget)     # 这里必须要用sip再删一遍

        self.first_btn = QPushButton()  # 重新初始化first_btn和btn_widget
        # update control members
        self.total_num = total_num  # 总页数
        self.bottom_page = bottom_page  # 底部固定页数
        self.current_page = 1
        if self.total_num < self.bottom_page:
            self.btn_widget = self.init_bottom_btn(self.total_num)
            self.bottom_page = self.total_num   # 当总页数小于默认的底部页数时，将底部页数设为总页数
        else:
            self.btn_widget = self.init_bottom_btn(self.bottom_page)

        self.hlyaout_under.insertWidget(1, self.btn_widget)
        self.update_label()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = IndexBar(20)    # 20页
    demo.show()

    # timer = QTimer()
    # timer.setSingleShot(True)
    # timer.timeout.connect(lambda: demo.update_IndexBar(5))
    # timer.start(500)

    sys.exit(app.exec_())
