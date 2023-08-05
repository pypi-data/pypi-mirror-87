from PyQt5 import QtWidgets,uic
import os

class dOK(QtWidgets.QDialog):
    def __init__(self, errorMessage,parent=None):
        super(dOK, self).__init__()
        pathPip = str(os.path.dirname(uic.__file__)).split('PyQt5')[0]
        path_buttons = pathPip + 'src/buttons_and_background/'
        uic.loadUi(pathPip+'src/ui_files/dialogOK.ui', self)
        self._flag = False
        self.pushButton.clicked.connect(self.closeWindow)
        self.pushButton.setStyleSheet("QPushButton{border-image:url("+path_buttons+"Ok.png);}")
        self.pushButton.setToolTip("Click to close window")
        self.text.setText(errorMessage)
    def closeWindow(self):
        self.close()
