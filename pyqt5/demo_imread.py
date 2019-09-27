from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import cv2
import sys

class MyWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle(self.tr('显示图片'))
        self.resize(500,400)
        self.label = QLabel(self)
        self.label.setFrameShape(QFrame.Box)
        self.label.setAlignment(Qt.AlignCenter)
        img = cv2.imread('resource/girl.jpeg')
        #cv2.imshow('111',img)
        #cv2.waitKey(0)
        width = img.shape[1]
        height = img.shape[0]
        print('cv2, width: '+str(width)+' height: '+str(height))
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB,img)
        qt_img = QImage(img.data,width,height,QImage.Format_RGB888)
        #print(type(qt_img))

        #self.label.setPixmap(QPixmap.fromImage(qt_img))

        self.label.setGeometry(0, 0, 400, 300)
        n_width = qt_img.width()
        n_height = qt_img.height()
        print('Qt, width: '+str(n_width)+' height: '+str(n_height))
        if n_width / 400 >= n_height / 300:
            ratio = n_width / 400
        else:
            ratio = n_height / 300
        new_width = n_width / ratio
        new_height = n_height / ratio
        new_img = qt_img.scaled(new_width, new_height, Qt.KeepAspectRatio)
        self.label.setPixmap(QPixmap.fromImage(new_img))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    #print(widget.children())
    sys.exit(app.exec_())