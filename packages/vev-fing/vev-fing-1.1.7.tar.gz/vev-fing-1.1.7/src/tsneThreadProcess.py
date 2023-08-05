from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSlot
from src.TSNE_exp import tsnePassages,tsnePositions

class tsneSignals(QObject):

    finished = pyqtSignal(list)
    error = pyqtSignal()


class tsneProcess(QRunnable): #process normal tsne execution

    def __init__(self,parameters,tsneType,nameExp):
        super(tsneProcess, self).__init__()
        self.data = parameters
        self.type = tsneType
        self.signals = tsneSignals()
        self.nameExp = nameExp


    @pyqtSlot()
    def run(self):

        try:
            if self.type == 'Passages':
                df = tsnePassages(self.data) #get dataframe info from tsne Passages
            else:
                df = tsnePositions(self.data) #get dataframe info from tsne positions


        except:
            self.signals.error.emit()

        finally:
            self.signals.finished.emit([self.data,df,self.type,self.nameExp])  # Done, send to main thread


class tsneProcessUpdate(QRunnable): #process add lr and perp

    def __init__(self,parameters,perp,lr,oldData,tsneType,nameExp):
        super(tsneProcessUpdate, self).__init__()
        self.data = parameters
        self.type = type
        self.signals = tsneSignals()
        self.lr = lr
        self.perp = perp
        self.oldData = oldData #data from tsne normal execution
        self.type = tsneType
        self.nameExp = nameExp


    @pyqtSlot()
    def run(self):
        try:
            if self.type == 'Passages':
                df = tsnePassages(self.data,[self.perp],[self.lr],self.oldData) #get new data from tsne passages, send old data and new perp and lr
            else:
                df = tsnePositions(self.data, [self.perp], [self.lr], self.oldData) #get new data from tsne positions, send old data and new perp and lr


        except:
            self.signals.error.emit()

        finally:
            self.signals.finished.emit([df,self.perp,self.lr,self.type,self.nameExp])  # Done, send to main thread