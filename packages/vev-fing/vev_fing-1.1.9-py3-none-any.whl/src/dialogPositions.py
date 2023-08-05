from PyQt5 import QtWidgets,uic
from src.dialogError import dError
import os

class valuesPositions(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(valuesPositions, self).__init__()
        pathPip = str(os.path.dirname(uic.__file__)).split('PyQt5')[0]
        path_buttons = pathPip + 'src/buttons_and_background/'
        uic.loadUi(pathPip+'src/ui_files/dialogPositions.ui', self)
        self.pushButton.clicked.connect(self.setParameters)
        self.fvpValue = 774
        self.lvpValue = 7332
        self.setIt = False

    def setParameters(self):

        fvp = self.FVP.toPlainText()
        lvp = self.LVP.toPlainText()
        try:
            if fvp == '':
                fvp = 0
            if lvp == '':
                lvp = 0

            self.fvpValue = int(fvp)
            self.lvpValue = int(lvp)
            if self.fvpValue > self.lvpValue:
                error_dialog = dError('LVP must be Higher tan FVP')
                error_dialog.exec()
            else:
                self.setIt = True
                self.close()
        except:
            error_dialog = dError('Please enter only integer values')
            error_dialog.exec()()
            self.close()

    def getIfSet(self):
        return self.setIt
    def getFVP(self):
        return self.fvpValue
    def getLVP(self):
        return self.lvpValue