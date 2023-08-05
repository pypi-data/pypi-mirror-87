from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSlot
import pandas as pd
from src.GetEntropySurface import getEntropySurface
from src.PlotEntropyPosition import plotEntropyPosition
from src.calculateGumbel import gumbelPlot
from src.PlotPopularDecay import plotPopularDecay
import os


class plotSignals(QObject):

    finished = pyqtSignal(list)
    error = pyqtSignal(object)

class plotSurface(QRunnable): #process in other thread plot surface

    def __init__(self,strain,repetition,fvp,lvp):
        super(plotSurface, self).__init__()
        self.strain = strain
        self.repetition = repetition
        self.fvp = fvp
        self.lvp = lvp
        self.signals = plotSignals()
    @pyqtSlot()
    def run(self):
        try:
            pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
            path_pkl = pathPip + 'src/data_experiments/'
            experimentName = self.strain + '_' + self.repetition + '(' + self.fvp + '-' + self.lvp + ')_entropy.parquet'  # get experiment
            df = pd.read_parquet(path_pkl + experimentName)  # read experiment
            getEntropySurface(df, self.strain, self.repetition)  # calculate entropy surface
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit(
                [self.strain, self.repetition, self.fvp, self.lvp])  # done, send info to main thread

class plotPositionEntropy(QRunnable): #process in other thread plot entropy * position

    def __init__(self,strain,repetition,position,fvp,lvp):
        super(plotPositionEntropy, self).__init__()
        self.strain = strain
        self.repetition = repetition
        self.fvp = fvp
        self.lvp = lvp
        self.position = position
        self.signals = plotSignals()

    @pyqtSlot()
    def run(self):
        try:
            pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
            path_pkl = pathPip + 'src/data_experiments/'
            intposition = int(self.position)
            experimentName = self.strain + '_' + self.repetition + '(' + self.fvp + '-' + self.lvp + ')_entropy.parquet'  # get experiment
            df = pd.read_parquet(path_pkl + experimentName)  # read dataframe
            plotEntropyPosition(intposition, df, self.strain, self.repetition, 'red')  # plot entropy position
        except:
            self.signals.error.emit()
        finally:
            self.signals.finished.emit([self.strain, self.repetition, self.position, self.fvp, self.lvp])  # done, send to main thread

class plotGumbel(QRunnable): #process in other thread, calculate gumbel
    def __init__(self,strain,repetition,fvp,lvp):
        super(plotGumbel, self).__init__()
        self.strain = strain
        self.repetition = repetition
        self.fvp = fvp
        self.lvp = lvp
        self.signals = plotSignals()

    @pyqtSlot()
    def run(self):
        try:
            pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
            path_pkl = pathPip + 'src/data_experiments/'
            experimentName = self.strain + '_' + self.repetition + '(' + self.fvp + '-' + self.lvp + ')_entropy.parquet'
            df = pd.read_parquet(path_pkl + experimentName)  # get dataframe
            outliers = gumbelPlot(df, self.strain, self.repetition)  # plot gumbel and get outliers
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit(
                [self.strain, self.repetition, self.fvp, self.lvp, outliers])  # done, send to main thread


class codonDecay(QRunnable): #process in other thread. Plot codon decay
    def __init__(self,strain,repetition,th,fvp,lvp):
        super(codonDecay, self).__init__()
        self.strain = strain
        self.repetition = repetition
        self.th = th
        self.fvp = fvp
        self.lvp = lvp
        self.signals = plotSignals()

    @pyqtSlot()
    def run(self):
        try:
            pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
            path_pkl = pathPip + 'src/data_experiments/'
            experimentName = self.strain + '_' + self.repetition + '(' + self.fvp + '-' + self.lvp + ').parquet'
            df = pd.read_parquet(path_pkl + experimentName)  # get dataframe experiment
            dfReturn = plotPopularDecay(df, )  # calculate codondecay info, get dataframe with this info
        except:
            self.signals.error.emit("ERROR")
        finally:
            self.signals.finished.emit(
                [dfReturn, df, self.th, self.strain, self.repetition, self.fvp, self.lvp])  # done, send to main thread