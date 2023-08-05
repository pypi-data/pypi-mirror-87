from PyQt5 import QtWidgets,uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from src.dialogError import dError
from src.Interpolation import interpolationPassage,interpolationPassageFreq
import pandas as pd
import os

class dInterpolation(QtWidgets.QDialog):
    def __init__(self, experiments,parent=None):
        super(dInterpolation, self).__init__()
        self.pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
        self.path_pkl = self.pathPip + 'src/data_experiments/'
        self.path_buttons = self.pathPip + 'src/buttons_and_background/'
        uic.loadUi(self.pathPip+'src/ui_files/interpolateDialog.ui', self)
        self._flag = False
        self.pushButton.clicked.connect(self.interpolation)
        self.model2 = QStandardItemModel()
        self.model2.setHorizontalHeaderLabels(['Experiment '])
        self.tableView.setModel(self.model2)
        self.tableView.horizontalHeader().setSectionResizeMode(1)
        self.experiments = experiments
        self.pushButton.setStyleSheet("QPushButton{border-image:url("+self.path_buttons+"Ok.png);}")
        self.pushButton.setToolTip("Click this button to interpolate experiment")
        for df in experiments:
            experimentName = "Strain: " + str(df[0]) + " " + "Repetition: " + str(df[1])
            row = (QStandardItem(experimentName))
            self.model2.appendRow(row)
        self.executed = False
        self.typeInterpolation = ''
        self.lvp = ''
        self.fvp = ''
        self.strain = ''
        self.repetition = ''
        self.passage = 0

    def interpolation(self):
        indices = self.tableView.selectionModel().selectedRows()
        if len(indices) < 1:

            de = dError('Error: Please select one experiment')
            de.exec()
        elif len(indices) > 1:

            de = dError('Error: Please select only one experiment')
            de.exec()
        elif (self.EntropyB.isChecked()==False and self.FrequencyB.isChecked()==False):

            de = dError('Error: Please select type of interpolation')
            de.exec()
        else:
            try:

                self.passage = int(self.textEdit.toPlainText())

                for index in sorted(indices):
                    experimentIndex = (index.row())

                df = self.experiments[experimentIndex]
                self.strain = str(df[0])
                self.repetition = str(df[1])
                self.fvp = str(df[2])
                self.lvp = str(df[3])
                if self.EntropyB.isChecked() == True:
                    experimentName = self.strain + '_' + self.repetition + '(' + self.fvp + '-' + self.lvp + ')_entropy.parquet'
                    df = pd.read_parquet(self.path_pkl + experimentName)
                    passages = df.Passage.unique()
                    if str(self.passage) not in passages:
                        de = dError('Error: Please select a valid passage')
                        de.exec()
                        control = False
                    else:
                        control = True
                        dfAux = interpolationPassage(str(self.passage), df)
                        self.typeInterpolation = 'Entropy'
                else:
                    experimentName = self.strain + '_' + self.repetition + '(' + self.fvp + '-' + self.lvp + ').parquet'
                    df = pd.read_parquet(self.path_pkl + experimentName)
                    passages = df.Passage.unique()
                    if str(self.passage) not in passages:
                        control = False
                        de = dError('Error: Please select a valid passage')
                        de.exec()
                    else:
                        control = True
                        dfAux = interpolationPassageFreq(str(self.passage), df)
                        self.typeInterpolation = 'Frequency'
                if control:
                    dfAux.to_parquet(self.path_pkl + experimentName)
                    self.executed = True
                    self.close()
            except:

                de = dError('Error: Please enter a integer passage')
                de.exec()

    def getInfo(self):
        return self.executed,self.typeInterpolation,self.strain,self.repetition,self.fvp,self.lvp,str(self.passage)

