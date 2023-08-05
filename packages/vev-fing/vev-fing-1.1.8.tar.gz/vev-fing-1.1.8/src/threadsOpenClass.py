from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSlot

from src.ReadData import readData,keepValidPositions
from src.GetEntropy import getEntropyExperiment, getEntropyExperimentAminos
import pandas as pd
import os


class loadSignals(QObject):

    finished = pyqtSignal(list)
    error = pyqtSignal(object)


class LoadFolder(QRunnable):

    def __init__(self,filename,fvp,lvp):
        super(LoadFolder, self).__init__()
        self.filename = filename
        self.fvp = fvp
        self.lvp = lvp
        self.signals = loadSignals()


    @pyqtSlot()
    def run(self):

        try:
            pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
            path_pkl = pathPip + 'src/data_experiments/'
            fileName = self.filename + '/'  # folder selected by user
            parameters = [fileName, self.fvp, self.lvp]  # parameters for readData
            df, strain, repetition, self.lvp = readData(
                parameters)  # return parameters, strain in folder, repetition and lvp(change if user select 0 or higher than positions)
            experimentName = strain + '_' + repetition + '(' + str(self.fvp) + '-' + str(
                self.lvp) + ').parquet'  # name to save parquet
            entropyName = strain + '_' + repetition + '(' + str(self.fvp) + '-' + str(
                self.lvp) + ')_entropy.parquet'  # name to save parquet entropy
            df.to_parquet(path_pkl + experimentName)  # save experiments with codons freq
            dfAux = getEntropyExperiment(strain, repetition, self.fvp, self.lvp, df)  # calculate entropy
            dfAux.to_parquet(path_pkl + entropyName)  # save exeriment with entropy

        except Exception as e:
            self.signals.error.emit(e)

        finally:
            self.signals.finished.emit([strain, repetition, self.fvp, self.lvp, True])  # Done, send this to main thread

class LoadFile(QRunnable):

    def __init__(self,filename):
        super(LoadFile, self).__init__()
        self.filename = filename
        self.signals = loadSignals()
        self.fvp = 0
        self.lvp = 0
    @pyqtSlot()
    def run(self):

        try:
            pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
            path_pkl = pathPip + 'src/data_experiments/'
            fileName = self.filename
            auxSplit = fileName.split('/')  # get where file is
            cantidad = len(auxSplit)
            i = 0
            directorio = ''
            # split directory and file from filename
            while i < (cantidad - 1):
                if i == 0:
                    directorio = auxSplit[i]
                else:
                    directorio = str(directorio) + '/' + str(auxSplit[i])
                i = i + 1
            directorio = str(directorio) + '/'  # get directory
            archivo = auxSplit[cantidad - 1]  # get file only

            aux = str(os.getcwd()) + '/' + path_pkl
            # get info of experiment for name of file
            archivoAux = archivo.split('.')[0]
            strain_repetion = archivoAux.split('_')
            strain = strain_repetion[0]
            auxSplit = strain_repetion[1].split('(')
            repetition = auxSplit[0]
            aux_fvp_lvp = auxSplit[1].split('-')
            self.fvp = int(aux_fvp_lvp[0])
            self.lvp = int(aux_fvp_lvp[1].split(')')[0])

            if "entropy" not in archivo:  # file loaded is not entropy exeriment
                aux_name_entroy = archivoAux + '_entropy.parquet'
                if os.path.exists(directorio + aux_name_entroy):  # look for entropy experiment file
                    if aux != directorio:  # if not in where vev save files
                        # copy and save in vev directory
                        df = pd.read_parquet(directorio + archivo)
                        df.to_parquet(path_pkl + archivo)
                        df = pd.read_parquet(directorio + aux_name_entroy)
                        df.to_parquet(path_pkl + aux_name_entroy)
                else:  # not exist entropy file
                    if aux != directorio:  # if not in where vev save files
                        # read freq file from folder, save in vev directory and calculate entropy and save in vev directory
                        df = pd.read_parquet(directorio + archivo)
                        df.to_parquet(path_pkl + archivo)
                        df = getEntropyExperiment(strain, repetition, self.fvp, self.lvp, df)
                        df.to_parquet(path_pkl + aux_name_entroy)
                    else:
                        # vev directory. Only calculate entropy and save in vev directory
                        df = pd.read_parquet(directorio + archivo)
                        df = getEntropyExperiment(os.getcwd(), strain, repetition, self.fvp, self.lvp, df)
                        df.to_parquet(path_pkl + aux_name_entroy)
            else:  # is entropy file
                if aux != directorio:  # not in vev directory
                    auxExperiment = archivo.replace('_entropy.parquet', '.parquet')
                    if os.path.exists(directorio + auxExperiment):  # if exist freq file
                        # save in vev directory
                        df = pd.read_parquet(directorio + auxExperiment)
                        df.to_parquet(path_pkl + auxExperiment)
                    df = pd.read_parquet(directorio + archivo)
                    df.to_parquet(path_pkl + archivo)


        except:
            self.signals.error.emit()

        finally:
            self.signals.finished.emit([strain, repetition, self.fvp, self.lvp, False])  # Done, send to main thread