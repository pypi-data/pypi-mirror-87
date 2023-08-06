from PySide2.QtWidgets import QDialog, QLabel, QProgressBar
from PySide2 import QtWidgets
from PySide2.QtCore import QSize, Qt


class LoadingHitDialog(QDialog):
    _instance = None
    _object = None

    @classmethod
    def getInstance(cls):
        if not cls._object:
            cls._object = LoadingHitDialog()
        return cls._object

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoadingHitDialog, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("温馨提示")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initView()
        size = QSize()
        size.setHeight(200)
        size.setWidth(300)
        self.setFixedSize(size)
        self.openCount = 0

    def initView(self):
        mainLayout = QtWidgets.QGridLayout()

        self.label = QLabel()
        self.label.setText("处理中,请稍后.....")
        self.label.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar = QProgressBar()
        mainLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.setLayout(mainLayout)

    def updateProgressvalue(self, value):
        self.progressBar.setValue(value)

    def updateHitMessage(self, value):
        self.label.setText(value)

    def show(self, text: str = None):
        if text:
            self.label.setText(text)
        self.openCount = self.openCount + 1
        if self.openCount > 1:
            return
        QDialog.exec_(self)

    def hide(self):
        self.openCount = self.openCount - 1
        if self.openCount < 0:
            self.openCount = 0
        if self.openCount == 0:
            self.close()
