import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd



class FigureTSNE(FigureCanvas):

    def __init__(self,dataframes,data, tsneType,nameExp, parent,lr=None,perp=None,width=5, height=4, dpi=100): #create figure
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.parent = parent
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.dfs = dataframes
        if dataframes == None: #is imported, not have dataframes
            self.isImport = True
        else:
            self.isImport = False
        self.data = data #experiments
        self.fig = fig
        self.type = tsneType #type
        self.array = []
        if lr ==None: #if normal execution, first lr and perp are 10 and 3.
            self.perp=3
            self.lr = 10
        else: #for add perp and lr
            self.perp=perp
            self.lr=lr
        self.nameExp = nameExp
        self.removeStrains=[] #strains hide by user
        self.dfPlot = ''
        self.compute_initial_figure() #plot figure
        self.name = ''
        self._flag = False
        self.normal = True # to difference between normal tsne execution and add lr and perp


    def getData(self): #get info from main thread
        if self.isImport:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: This is an imported experiment. Please recalculate the experiment as normal')
            error_dialog.exec()
        else:
            return self.dfs,self.data,self.nameExp

    def getType(self): #get type from main thread
        return self.type

    def newtSNE(self,dataframes,data, tsneType,nameExp,lr=None,perp=None): #update figure, similiar to init figure
        self.removeStrains = []
        if dataframes == None:
            self.isImport = True
        else:
            self.isImport = False
        if lr==None:
            self.perp = 3
            self.lr = 10
        else:
            self.perp=perp
            self.lr = lr
        self.normal = True
        self.data=data
        self.dfs= dataframes
        self.axes.cla() #clear plot
        self.perp=3
        self.lr = 10
        self.type = tsneType
        self.nameExp = nameExp
        self.compute_initial_figure() #plot figure

    def updateData(self,newData,perp,lr,expName): #add perp and lr selected by user
        if self.isImport:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: This is an imported experiment. Please recalculate the experiment as normal')
            error_dialog.exec()
        else:
            self.normal = False
            self.data = newData
            self.lr = lr
            self.perp = perp
            self.expName = expName
            self.updateParameters(perp,lr,True)

    def updateParameters(self,perp,lr,flag=False): #flag is to difference calling updateParameters from vev or from updateData
        #if is from vev, is when user move sliders to change lr and perp, if not, is where user add new perp and lr
        self.axes.cla() #clear plot
        self.perp = perp #set new perp
        self.lr = lr #set new lr
        if flag:
            self.normal = False
        else:
            self.normal = True
        self.compute_initial_figure() #plot figure


    def exportCSV(self,filename): #export info where user select(this save in filename)
        df = self.data
        df = df.drop(columns=['StrainNumber','Plot']) #not need this columns
        if self.type == 'Positions': #to add column positions or passage
            df["Position"] = df.apply(lambda row: row.Info.split(",")[2], axis=1)
            columnsTitles = ['Position', 'Strain', 'Repetition', 'tsne_1', 'tsne_2', 'LR', 'Perp', 'Info']
        else:
            df["Passage"] = df.apply(lambda row: row.Info.split(",")[2], axis=1)
            columnsTitles = ['Passage', 'Strain', 'Repetition', 'tsne_1', 'tsne_2', 'LR', 'Perp', 'Info']
        df["Repetition"] = df.apply(lambda row: row.Info.split(",")[1], axis=1)

        df = df.reindex(columns=columnsTitles)

        exps = ''
        i = 0
        j = 0

        while i < len(self.nameExp):
            j +=1
            if j==len(self.nameExp):
                exps += self.nameExp[i].split('.')[0]
            else:
                exps += self.nameExp[i].split('.')[0]+'-'
            i+=1
        if not self.normal:
            df = df[df.Perp.eq(self.perp) & df.LR.eq(self.lr)]

        df.to_csv(filename) #save csv
        return self.nameExp, self.normal,self.lr,self.perp,self.type #return info to main thread




    def compute_initial_figure(self): #plot figure

        self.array=[]

        self.dfPlot = self.data[self.data.Perp.eq(self.perp) & self.data.LR.eq(self.lr)] #get info for this perp and lr


        self.annot = self.axes.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->")) #create annotations

        self.annot.set_visible(False)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover) #hande on mouse event

        strains = self.dfPlot.Strain.unique() #get strains

        indexColor = 0
        for s in strains:
            if s not in self.removeStrains: #if not hide by user
                #plot
                d = self.dfPlot.loc[self.dfPlot['Strain'] == s]
                x = d.tsne_1
                y = d.tsne_2
                aux =self.axes.scatter(x, y, label=s, color='C'+str(indexColor), alpha=0.3)
                self.array.append(aux)
            indexColor = indexColor + 1

        self.axes.legend()
        self.draw()


    def onOffStrains(self,strains):
        self.removeStrains=strains
        self.axes.cla()
        self.compute_initial_figure()


    def update_annot(self,ind,i): #update info annot
        pos = self.array[i].get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        dinfo =self.dfPlot.loc[self.dfPlot.tsne_1.eq(pos[0]) & self.dfPlot.tsne_2.eq(pos[1])] #get info point from point
        if len(dinfo['Info'].values) > 0:
            info = dinfo['Info'].values[0]
            auxInfo= info.split(',')
            if self.type == 'Passages':
                pointInfo='Repetition: ' + auxInfo[1] + '\nPassage: ' + auxInfo[2] #tsne passage
            else:
                pointInfo = 'Repetition: ' + auxInfo[1] + '\nPositions: ' + auxInfo[2] #tsne positions

            self.annot.set_text(pointInfo) #set text
            self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self,event):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes: #if in axes
            cont = False
            i = 0
            while not cont and i < len(self.array):
                cont, ind = self.array[i].contains(event) #over a point
                i = i +1
            if cont: #if is over a point
                self.update_annot(ind,(i-1)) #update annot
                self.annot.set_visible(True) #show info
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()


