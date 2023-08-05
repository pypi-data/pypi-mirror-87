from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSlot
from src.Clustering import getClustering, plotClustersCurves, plotClustersDimRed, plot_confusion_matrix,getClusteringSSA
from sklearn.metrics import confusion_matrix
import numpy as np
from pathlib import Path
import os
import warnings
class clusterSignals(QObject):

    finished = pyqtSignal(list)
    error = pyqtSignal()


class clusterProcess(QRunnable):

    def __init__(self,dataframe,strain,repetition,fvp,lvp,typeCluster): #create Class
        super(clusterProcess, self).__init__()
        self.df = dataframe
        self.strain = strain
        self.repetition = repetition
        self.fvp = fvp
        self.lvp = lvp
        self.type = typeCluster
        self.signals = clusterSignals()


    @pyqtSlot()
    def run(self):

        try:
            pathPip = str(os.path.dirname(np.__file__)).split('numpy')[0]
            metrica="dtw" #metric use in clustering
            if self.type == 'Normal': #get type
                data_array, d_T, list_pos, list_bary = getClustering([self.df], metrica, perp=3, lr=100) #call getClustering
            else:
                data_array, d_T, list_pos, list_bary = getClusteringSSA([self.df], metrica, perp=3, lr=100) #call clusteringSSA
            threshold = int(len(d_T.Position.unique()) * 0.01) #threshold for number of elements in clusters
            dfAux = d_T[['6','Position']] #get information of positions clusters labels with 6 clusters
            dfAux = dfAux.rename(columns={"6":"Label","Position":"Position"}) #change column for 6 cluster labels to labels
            labels = dfAux.Label.unique() #get labels
            outliers = []
            for l in labels: #for every label
                df = dfAux[dfAux.Label.eq(l)] #get df with label l
                listOut = df['Position'].values.tolist()
                if len(listOut) <= threshold: #if cluster has less or equal elements than threshold, save this positions
                    outliers.append(listOut)
            outliers = [item for sublist in outliers for item in sublist] #get only 1 list
            outliers = list(map(int, outliers)) #transform to int
            outliers.sort() #sort elements
            directory = pathPip+'src/plot_images/' + str(self.strain) + '_'+ str(self.repetition) + '(' +str(self.fvp) + '-' + str(self.lvp)+')'
            Path(directory).mkdir(parents=True, exist_ok=True) #if directory not exists, create
            clusters = [2,4,6]
            for i in range(3):

                plotClustersCurves(data_array, list_pos[i], list_bary[i],clusters[i],directory) #plot cluster curves for every cluster
                if i == 1:
                    target_clusters = ['0', '1', '2', '3']
                    c_2 = np.array(d_T[['2']])
                    c_4 = np.array(d_T[['4']])
                    cnf_matrix = confusion_matrix(c_4, c_2)
                    c_m = cnf_matrix[:, :-2]
                    plot_confusion_matrix(c_m,clusters[i],directory, classes=target_clusters, title='Confusion matrix 2 and 4 clusters') #plot confusion matrix

                elif i == 2:
                    target_clusters = ['0', '1', '2', '3', '4', '5']
                    c_6 = np.array(d_T[['6']])
                    cnf_matrix = confusion_matrix(c_6, c_4)
                    c_m = cnf_matrix[:, :-2]
                    plot_confusion_matrix(c_m,clusters[i],directory, classes=target_clusters, title='Confusion matrix 4 and 6 clusters')

            d_T = d_T.rename(columns={"6": "Label 6 Cluster", "4": "Label 4 Cluster","2": "Label 2 Cluster"})  # change column for 6 cluster labels to labels

        except:
            self.signals.error.emit()

        finally:
            self.signals.finished.emit([self.strain,self.repetition,self.fvp,self.lvp,directory,outliers,d_T])  # Done


