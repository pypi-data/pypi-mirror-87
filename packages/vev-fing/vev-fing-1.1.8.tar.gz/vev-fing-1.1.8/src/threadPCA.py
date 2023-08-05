from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSlot
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

class pcaSignals(QObject):

    finished = pyqtSignal(list)
    error = pyqtSignal()


class pcaProcess(QRunnable): #create pcaProcess

    def __init__(self,parameters,nameExp):
        super(pcaProcess, self).__init__()
        self.dfs = parameters
        self.nameExp = nameExp
        self.signals = pcaSignals()

    @pyqtSlot()
    def run(self):

        try:
            #auxiliars
            arrayDF=[]
            infoDF =[]
            strainDF = []
            repDF = []
            dfPuntosPCA=pd.DataFrame(columns=["PCA_1", "PCA_2", "Strain", "Repetition"]) #create dataframe

            for df in self.dfs: #every experiment

                arrayDF.append(df['Entropy']) #add entropy to array
                infoDF.append(df['info']) #add info to array

                info_df=str(df['info'].iloc[0])
                strain_df=info_df.split(',')[0]
                repet=info_df.split(',')[1]
                strainDF.append(strain_df) #add strain to array
                repDF.append(repet) #add repetition to array



            X = np.squeeze(np.array([arrayDF])) #reduce dimension
            infoDF = np.squeeze(np.array([infoDF])) #reduce dimension
            pca = PCA(n_components=2) #create PCA
            auxReturn = pca.fit_transform(X) #apply transformation PCA to experiments. Return eigenvalues
            pcaVector = pca.components_ #return eigenvector

            # add info to DF
            dfPuntosPCA['PCA_1']=auxReturn[:,0]
            dfPuntosPCA['PCA_2']=auxReturn[:,1]
            dfPuntosPCA['Strain']=strainDF
            dfPuntosPCA['Repetition']=repDF



        except:
            self.signals.error.emit()

        finally:

            self.signals.finished.emit([dfPuntosPCA,pcaVector,infoDF, self.nameExp,self.dfs])  # Done, send info to main thread

