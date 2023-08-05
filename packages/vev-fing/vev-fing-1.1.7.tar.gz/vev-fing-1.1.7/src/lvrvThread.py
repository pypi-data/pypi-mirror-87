from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSlot
from src.Filtrados import decomposition_Poly_LV_RV,decomposition_PM_LV_RV

class lvrvSignals(QObject):

    finished = pyqtSignal(list)
    error = pyqtSignal()


class lvrv_poly(QRunnable): #create lvrv poly class
    def __init__(self,parameters,grade,nameExps):
        super(lvrv_poly, self).__init__()
        self.experiments = parameters
        self.grade = grade
        self.nameExps = nameExps
        self.signals = lvrvSignals()



    @pyqtSlot()
    def run(self):
        try:
            l_LV_RV = []

            for df in self.experiments: #for every experiment
                decomposition = decomposition_Poly_LV_RV(df,self.grade) #get descompoistions
                l_LV_RV.append(decomposition) #add to array

        except:
            self.signals.Error.emit()


        finally:
            self.signals.finished.emit([l_LV_RV,'Polynomial',self.nameExps,self.grade])  # Done, send to main thred


class lvrv_average(QRunnable): #create lvrv moving average class
    def __init__(self,parameters,window,nameExps):
        super(lvrv_average, self).__init__()
        self.experiments = parameters
        self.window = window
        self.nameExps = nameExps
        self.signals = lvrvSignals()


    @pyqtSlot()
    def run(self):
        #same as lvrv_poly but with moving average
        try:
            l_LV_RV = []
            for df in self.experiments:
                decomposition = decomposition_PM_LV_RV(df,self.window)
                l_LV_RV.append(decomposition)
        except Exception as e:
            print(e)
            self.signals.error.emit()
        finally:
            self.signals.finished.emit([l_LV_RV,'Moving Average',self.nameExps,self.window]) # Done, send to main thre