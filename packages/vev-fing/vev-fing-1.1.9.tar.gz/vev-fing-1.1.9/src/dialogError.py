from PyQt5 import QtWidgets,uic, QtCore
from PyQt5.QtGui import QPixmap
import os

class dError(QtWidgets.QDialog):
    def __init__(self, errorMessage,parent=None):
        super(dError, self).__init__()
        pathPip = str(os.path.dirname(uic.__file__)).split('PyQt5')[0]
        uic.loadUi(pathPip+'src/ui_files/dialogError.ui', self)
        self._flag = False
        self.pushButton.clicked.connect(self.closeWindow)
        self.pushButton.setToolTip("Click to close window")
        self.errorText.setText(errorMessage)



    def closeWindow(self):
        self.close()
