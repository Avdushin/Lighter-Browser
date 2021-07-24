from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import os
import sys

class History(QDialog):
    def __init__(self, *args, **kwargs,):
        super(History, self).__init__(*args, **kwargs)
        self.setFixedSize(580, 520)

        QBtn = QDialogButtonBox.Ok
        self.buttonbox = QDialogButtonBox(QBtn)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        size = QtCore.QSize(1280, 720)

        layout = QVBoxLayout()

        title = QLabel("History")
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)

        layout.addWidget(title)

        # logo = QLabel()
        # logo.setPixmap(QPixmap(os.path.join('images', 'icon.ico')))
        # layout.addWidget(logo)

        layout.addWidget(QLabel("Здесь находится ваша история "))


        layout.addWidget(QLabel(" "))
        layout.addWidget(QLabel(" "))


        layout.addWidget(QLabel("Version 0.2"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)
        
        layout.addWidget(self.buttonbox)

        self.setLayout(layout)
