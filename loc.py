from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import os


class ListOfChanges(QDialog):
    def __init__(self, *args, **kwargs,):
        super(ListOfChanges, self).__init__(*args, **kwargs)
        self.setFixedSize(240, 280)

        QBtn = QDialogButtonBox.Ok
        self.buttonbox = QDialogButtonBox(QBtn)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        size = QtCore.QSize(1300, 1400)

        layout = QVBoxLayout()

        title = QLabel("List Of Changes")
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)

        layout.addWidget(title)

        # logo = QLabel()
        # logo.setPixmap(QPixmap(os.path.join('images', 'icon.ico')))
        # layout.addWidget(logo)

        layout.addWidget(QLabel(" "))

        layout.addWidget(QLabel("Долбавлены шоткаты навигации"))
        layout.addWidget(QLabel("Долбавлены новые фунуции (copy/paste)"))
        layout.addWidget(QLabel("Обновлены иконки"))
        layout.addWidget(QLabel("Исправлены мелкие ошибки"))

        layout.addWidget(QLabel(" "))
        layout.addWidget(QLabel(" "))


        layout.addWidget(QLabel("Version 0.2"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)
        
        layout.addWidget(self.buttonbox)

        self.setLayout(layout)