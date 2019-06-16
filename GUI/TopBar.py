# coding: UTF-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import *
import sys


class TopBar(QWidget):
    sound_quality = ["mp3", "m4a"]  # "mp3-high"

    def __init__(self, parent=None):
        super(TopBar, self).__init__(parent)

        # Init member
        self.select_all_checkBox = QCheckBox("全选")
        self.download_btn = QPushButton("全部下载")
        self.label = QLabel("音质: ")
        self.quality_comboBox = QComboBox()

        # Init
        self.init_ui()

    def init_ui(self):
        self.quality_comboBox.addItems(self.sound_quality)

        self.select_all_checkBox.setFixedSize(80, 36)
        self.download_btn.setFixedSize(120, 36)
        self.label.setFixedSize(50, 36)
        self.quality_comboBox.setFixedSize(100, 34)

        hlayout_left = QHBoxLayout()
        hlayout_right = QHBoxLayout()
        hlayout_total = QHBoxLayout()
        hlayout_left.addWidget(self.select_all_checkBox)
        hlayout_left.addWidget(self.download_btn)

        hlayout_right.addWidget(self.label)
        hlayout_right.addWidget(self.quality_comboBox)

        spacer_item = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        hlayout_total.addLayout(hlayout_left)
        hlayout_total.addItem(spacer_item)
        hlayout_total.addLayout(hlayout_right)
        self.setLayout(hlayout_total)

        # 下载按钮初始状态为disabled
        self.set_download_btn_state(False)

    @pyqtSlot(bool)
    def set_download_btn_state(self, is_disable):
        self.download_btn.setEnabled(is_disable)

    def get_quality(self):
        return self.quality_comboBox.currentText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TopBar()
    demo.show()

    sys.exit(app.exec_())
