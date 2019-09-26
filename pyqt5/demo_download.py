#! /usr/bin/python
# -*- coding: utf-8 -*-
# datetime:2019/8/24 21:37
# software: PyCharm
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QProgressBar, QDesktopWidget, \
    QTextEdit,QMessageBox
import time, requests, os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
class WorkThread(QThread):
    trigger = pyqtSignal(int)
    trigger2 = pyqtSignal(str)
    url = ""
    def __init__(self):
        super(WorkThread, self).__init__()
    def run(self):
        print("thread run..")
        url = self.url
        print("down file:" + url)
        path = os.path.basename(url)
        start = time.time()
        size = 0
        response = requests.get(url, stream=True)  # stream 必须带上
        chunk_size = 1024  # 每次下载大小
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            print("[文件大小]:%.2f MB" % (content_size / chunk_size / 1024))
            with open(path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)  # 已下载大小
                    num = int(size / content_size * 100)
                    self.trigger.emit(num)
                    # \r 指定第一个字符开始，搭配end属性完成覆盖进度条
                    print("\r" + "[下载进度]：%s%.2f%%" % (
                        ">" * int(size * 50 / content_size), float(size / content_size * 100)), end="")
            end = time.time()  # 结束时间
            self.trigger2.emit("下载完成！用时%.2f秒" % (end - start))
            print("\n" + "全部下载完成！用时%.2f秒" % (end - start))
class DownLoad(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #self.setWindowIcon(QIcon("web.png"))
        lbl = QLabel("请输入链接:", self)
        lbl.move(30, 30)
        self.text = QLineEdit("", self)
        self.text.resize(350, 20)
        self.text.move(100, 28)
        self.text.textChanged.connect(self.changeText)
        self.textedit = QTextEdit("", self)
        self.textedit.resize(510, 200)
        self.textedit.move(100, 140)
        btn = QPushButton("下载", self)
        btn.move(460, 28)
        btn.clicked.connect(self.down)
        self.cancelbtn = QPushButton("重置", self)
        self.cancelbtn.move(540, 28)
        self.cancelbtn.clicked.connect(self.cancel)
        self.cancelbtn.setDisabled(True)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(100, 80, 300, 25)
        self.lbl2 = QLabel("", self)
        self.lbl2.move(100, 110)
        self.setGeometry(300, 300, 650, 400)
        self.center()
        self.setWindowTitle("下载文件")
        # 创建线程
        self.workthread = WorkThread()
        self.workthread.trigger.connect(self.progressbar)
        self.workthread.trigger2.connect(self.downresult)
    def cancel(self):
        self.text.setText("")
        self.lbl2.setText("")
        self.pbar.setValue(0)
    def down(self):
        self.cancelbtn.setDisabled(True)
        self.workthread.url = self.text.text()
        if self.workthread.url == "":
            QMessageBox.information(self,"错误信息","URL不能为空")
            return
        self.workthread.start()
    def downresult(self,info):
        self.lbl2.setText(info)
        self.lbl2.adjustSize()
    def progressbar(self, num):
        self.pbar.setValue(num)
        if num == 100:
            info = time.strftime("%y/%M/%d %H:%M:%S", time.localtime()) + ":" + self.text.text() + "\n" + self.textedit.toPlainText()
            self.textedit.setText(info)
            self.cancelbtn.setDisabled(False)
    def changeText(self, text):
        if text == "":
            self.lbl2.setText("")
            self.pbar.setValue(0)
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    down = DownLoad()
    down.show()
    sys.exit(app.exec_())