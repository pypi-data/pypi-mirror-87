import numpy as np
import pandas as pd
from PIL import Image
from sklearn.decomposition import PCA
import matplotlib
import os
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.PlotEntropyPosition import  plotEntropiesPosition




class FigurePCA(FigureCanvas):

    def __init__(self, dfPointsPCA, pcaVector, infoDF, nameExps,dfs, parent,allinfo=None, width=5, height=4, dpi=100): #create pca figure

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.parent = parent

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.dfPointsPCA = dfPointsPCA
        self.infoDF = infoDF
        self.pcaVector = pcaVector
        self.nameExps = nameExps
        self.dfsAux = dfs
        self.fig = fig
        self.aux = []
        if allinfo is not None: #if all information is in this df(because is imported)
            self.allInfoDF=allinfo
            self.reWritePCAInfoImported() #rewrite information to obtain the same information as if it were not imported
            self.isImported = True
        else:
            self.allInfoDF = self.joinDataFrames() #create dataframe with all info. This is for export function
            self.isImported = False

        self.compute_initial_figure() #plot figure
        self.name = ''
        self._flag = False

    def joinDataFrames(self):

        df2 = pd.DataFrame(self.pcaVector) #create dataframe from numpy pcaVector
        df3 = pd.DataFrame(self.infoDF) #create new dataframe from info arry
        df = pd.concat([self.dfPointsPCA,df2,df3]) #concat all info
        df = df.reset_index() #reset index

        return df

    def updatePCA(self,dfPointsPCA,pcaVector,infoDF,nameExps,dfs,allinfo=None): #update figure, new PCA
        self.dfPointsPCA = dfPointsPCA
        self.pcaVector = pcaVector
        self.infoDF = infoDF
        self.nameExps = nameExps
        self.dfsAux = dfs
        if allinfo is not None:
            self.allInfoDF=allinfo
            self.reWritePCAInfoImported()
            self.isImported = True
        else:
            self.isImported = False
            self.allInfoDF = self.joinDataFrames()

        self.axes.cla() #clear plot
        self.compute_initial_figure() #plot figure

    def reWritePCAInfoImported(self):
        count_row = self.allInfoDF.shape[0] #counts rows
        index = int((((count_row - 2) / 2)) * -1) #get index(there are two rows for pcaVector, and there are two rows for every experiment(info and pca points))
        indexT = index - 2
        df = self.allInfoDF.iloc[indexT:] #get last indexT rows(has info and pcaVector)
        df = df.drop(['index','PCA_1','PCA_2','Repetition','Strain'],axis=1)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        dfI = df.iloc[index:] #get last index rows(has info)
        dfvector = df.head(2) #get only pcaVector, there is in first 2 rows
        vectorPCA = dfvector.to_numpy()
        info = dfI.to_numpy()
        self.infoDF=info
        vectorPCA = vectorPCA.astype(np.float)
        self.pcaVector=vectorPCA
        df = self.allInfoDF[['PCA_1','PCA_2','Strain','Repetition']] #get all info again, and get only this columns
        df = df.dropna()  #drops na, drops every row with nulls
        self.dfPointsPCA=df


    def compute_initial_figure(self):

        strains = self.dfPointsPCA.Strain.unique()
        self.fig.canvas.mpl_connect('button_press_event', self.check_click) #connect with function to handle click evets
        self.aux = self.axes.scatter(self.pcaVector[0, :], self.pcaVector[1, :], marker='o', c="grey", alpha=0.2) #plot eigenvector
        #to scale points, gets max in eigenvector and eigenvalues
        pointx = np.max(self.pcaVector[0, :])
        pointy = np.max(self.pcaVector[1, :])
        auxPointX = np.max(self.dfPointsPCA["PCA_1"].values)
        auxPointY = np.max(self.dfPointsPCA["PCA_2"].values)
        scalex = auxPointX / pointx
        scaley = auxPointY / pointy
        for s in strains: #plot eigenvalues
            d = self.dfPointsPCA.loc[self.dfPointsPCA['Strain'] == s]
            x = d.PCA_1 / scalex
            y = d.PCA_2 / scaley
            self.axes.scatter(x, y, label=s)
        self.axes.set_xlabel('X1')
        self.axes.set_ylabel('X2')
        self.axes.legend()
        title = 'Distribution coefficients of principal components position '
        plt.suptitle(title, fontsize=16)
        self.axes.grid(True)
        self.draw()

    def find_nearest(self, points, value): #find nearest value in eigenvector for value data clicked. Returns index position
        arrayAux = np.asarray(points)
        idx = (np.abs(arrayAux - value)).argmin()
        return idx

    def check_click(self, event): #checks if clicks position have a plot point
        if event.inaxes == self.axes:
            cont, ind = self.aux.contains(event)
            if cont and not self.isImported:
                self.onclick(event)


    def onclick(self, event):
        pathPip = str(os.path.dirname(Image.__file__)).split('PIL')[0]
        ix, iy = event.xdata, event.ydata
        indx = self.find_nearest(self.pcaVector[0,], ix)
        exp = self.infoDF[0,]
        experiment = exp[indx]
        experimentAux = experiment.split(',')
        position = experimentAux[3]
        plotEntropiesPosition(int(position), self.dfsAux)
        self.name = pathPip+'src/plot_images/Entropy_' + position + '.png'
        img = Image.open(self.name)
        titleAux = pathPip+"plot_images/Entropy for position " + position
        img.show(title=titleAux)

    def exportPCA(self,filename): #export PCA result
        if self.isImported:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Unable to export an imported file')
            error_dialog.exec()
        else:
            self.allInfoDF.to_csv(filename)
            return self.nameExps

