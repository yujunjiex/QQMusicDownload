# coding: UTF-8
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from GUI.MainWindow import MainWindow
import PyQt5.sip
import sys


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()


    currentScreenWid = QApplication.desktop().width()
    currentScreenHei = QApplication.desktop().height()
    x = currentScreenWid / 1920.0
    y = currentScreenHei / 1080.0

    mainwindow.setMinimumSize(1366*x, 768*y)
    mainwindow.setGeometry((QApplication.desktop().width() - mainwindow.width())/2,
                           (QApplication.desktop().height() - mainwindow.height())/2, 1366*x, 768*y)
    mainwindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

