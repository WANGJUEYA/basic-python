import math
import sys

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QGradient, QPalette, QPen, QPainter, QLinearGradient, QRadialGradient, QConicalGradient
from PyQt5.QtWidgets import QWidget, QSplitter, QFrame, QGridLayout, QStackedWidget, QVBoxLayout, QPushButton, \
    QComboBox, QColorDialog, QApplication


# QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))


class StockDialog(QWidget):

    def __init__(self, parent=None):
        super(StockDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("渐变效果"))

        self.startColor = Qt.green
        self.endColor = Qt.blue
        self.style = QGradient.LinearGradient
        self.spread = QGradient.PadSpread

        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.setOpaqueResize(True)

        frame = QFrame(mainSplitter)
        mainLayout = QGridLayout(frame)
        # mainLayout.setContentsMargins()
        # mainLayout.setMargin(10)
        # mainLayout.setSpacing(6)

        stack1 = QStackedWidget()
        stack1.setFrameStyle(QFrame.Panel | QFrame.Raised)

        mainSplitter1 = QSplitter(Qt.Horizontal)
        mainSplitter1.setOpaqueResize(True)

        self.area = PaintArea(self)

        stack1.addWidget(self.area)
        frame1 = QFrame(mainSplitter1)
        mainLayout1 = QVBoxLayout(frame1)
        # mainLayout1.setMargin(10)
        # mainLayout1.setSpacing(6)
        mainLayout1.addWidget(stack1)

        self.startPushButton = QPushButton(self.tr("start"))
        self.startPushButton.setAutoFillBackground(True)
        self.startPushButton.setPalette(QPalette(Qt.green))

        self.endPushButton = QPushButton(self.tr("end"))
        self.endPushButton.setAutoFillBackground(True)
        self.endPushButton.setPalette(QPalette(Qt.blue))

        self.startPushButton.clicked.connect(self.slotStartColor)
        self.endPushButton.clicked.connect(self.slotEndColor)
        # self.connect(self.startPushButton, SIGNAL("clicked()"), self.slotStartColor)
        # self.connect(self.endPushButton, SIGNAL("clicked()"), self.slotEndColor)

        self.grdientComboBox = QComboBox()
        self.grdientComboBox.addItem(self.tr("Linear Gradient"), QGradient.LinearGradient)
        self.grdientComboBox.addItem(self.tr("Radial Gradient"), QGradient.RadialGradient)
        self.grdientComboBox.addItem(self.tr("Conical Gradient"), QGradient.ConicalGradient)
        self.grdientComboBox.activated.connect(self.slotSetStyle)
        # self.connect(self.grdientComboBox, SIGNAL("activated(int)"), self.slotSetStyle)

        self.spreadComboBox = QComboBox()
        self.spreadComboBox.addItem(self.tr("PadSpread"), QGradient.PadSpread)
        self.spreadComboBox.addItem(self.tr("RepeatSpread"), QGradient.RepeatSpread)
        self.spreadComboBox.addItem(self.tr("ReflctSpread"), QGradient.ReflectSpread)
        self.spreadComboBox.activated.connect(self.slotSetSpread)
        # self.connect(self.spreadComboBox, SIGNAL("activated(int)"), self.slotSetSpread)

        mainLayout.addWidget(self.startPushButton, 1, 0)
        mainLayout.addWidget(self.endPushButton, 1, 1)
        mainLayout.addWidget(self.grdientComboBox, 1, 2)
        mainLayout.addWidget(self.spreadComboBox, 1, 3)

        layout = QGridLayout(self)
        layout.addWidget(mainSplitter1, 0, 0)
        layout.addWidget(mainSplitter, 1, 0)
        self.setLayout(layout)

    def slotStartColor(self):
        self.startColor = QColorDialog.getColor(Qt.green)
        self.startPushButton.setPalette(QPalette(self.startColor))
        self.area.setPen(QPen(self.startColor))

    def slotEndColor(self):
        self.endColor = QColorDialog.getColor(Qt.blue)
        self.endPushButton.setPalette(QPalette(self.endColor))
        self.area.setPen(QPen(self.endColor))

    def slotSetStyle(self, value):
        self.style = self.grdientComboBox.itemData(value, Qt.UserRole)
        # self.style = self.grdientComboBox.itemData(value, Qt.UserRole).toInt()[0]

    def slotSetSpread(self, value):
        self.spread = self.spreadComboBox.itemData(value, Qt.UserRole)
        # self.spread = self.spreadComboBox.itemData(value, Qt.UserRole).toInt()[0]


class PaintArea(QWidget):

    def __init__(self, StockDialog):
        super(PaintArea, self).__init__()
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(400, 400)
        self.startPoint = QPointF(0, 0)
        self.endPoint = QPointF(400, 400)
        self.pen = QPen()
        self.sd = StockDialog

    def setPen(self, p):
        self.pen = p
        self.update()

    def mousePressEvent(self, e):
        self.startPoint = QPointF(e.pos())

    def mouseReleaseEvent(self, e):
        self.endPoint = QPointF(e.pos())
        self.update()

    def paintEvent(self, QPaintEvent):
        p = QPainter(self)
        r = self.rect()
        p.setPen(self.pen)
        if (self.sd.style == QGradient.LinearGradient):
            linearGradient = QLinearGradient(self.startPoint, self.endPoint)
            linearGradient.setColorAt(0.0, self.sd.startColor)
            linearGradient.setColorAt(1.0, self.sd.endColor)
            linearGradient.setSpread(self.sd.spread)
            p.setBrush(linearGradient)
        elif (self.sd.style == QGradient.RadialGradient):
            rr = math.sqrt(
                math.pow(self.endPoint.x() - self.startPoint.x(), 2) + math.pow(self.endPoint.y() - self.startPoint.y(),
                                                                                2))
            radialGradient = QRadialGradient(self.startPoint, rr, self.startPoint)
            radialGradient.setColorAt(0.0, self.sd.startColor)
            radialGradient.setColorAt(1.0, self.sd.endColor)
            radialGradient.setSpread(self.sd.spread)
            p.setBrush(radialGradient)
        elif (self.sd.style == QGradient.ConicalGradient):
            angle = math.atan2(self.endPoint.y() - self.startPoint.y(), self.endPoint.x() - self.startPoint.x())
            conicalGradient = QConicalGradient(self.startPoint, -(180 * angle) / math.pi)
            conicalGradient.setColorAt(0.0, self.sd.startColor)
            conicalGradient.setColorAt(1.0, self.sd.endColor)
            p.setBrush(conicalGradient)
            p.drawRect(r)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StockDialog()
    form.show()
    app.exec_()
