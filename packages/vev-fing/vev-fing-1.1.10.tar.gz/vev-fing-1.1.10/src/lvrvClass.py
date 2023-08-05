import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from itertools import combinations
import pandas as pd



class FigureLVRV(FigureCanvas):

    def __init__(self,experiments, parent,nameExps,typelvrv=None,parameter=None,width=5, height=4, dpi=100): #create figure LVRV
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.parent = parent
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.experiments = experiments
        self.fig = fig
        self.array = []
        self.isImported = False #handle import lvrv
        if parameter == None:
            self.isImported =True

        self.name = ''
        self._flag = False
        self.points_marks = []
        self.type = typelvrv
        self.parameter = parameter
        self.nameExp = nameExps
        self.compute_initial_figure()


    def updatelvrv(self,dfs,nameExps=None,typeLVRV=None,param=None): #update figure
        self.array=[]
        self.experiments=dfs
        self.nameExp = nameExps
        self.type = typeLVRV
        self.parameter = param
        if param == None:
            self.isImported =True
        self.axes.cla() #clear figure
        self.compute_initial_figure() #plot new figure


    def compute_initial_figure(self):
        if self.isImported: #if is imported
            strains = self.experiments.Strain.unique()
            for s in strains:
                dfPlotAux = self.experiments[self.experiments.Strain.eq(s)]
                repetitions = dfPlotAux.Repetition.unique()
                for r in repetitions:
                    dfPlot = dfPlotAux[dfPlotAux.Repetition.eq(r)]
                    x = dfPlot.Entropy_Low
                    y = dfPlot.Entropy_High
                    aux = self.axes.scatter(x, y, alpha=0.5, label="Strain {s}, Repetition{r}".format(s=s,r=r))
                    self.array.append(aux)

        else:
            for df in self.experiments: #for every experiment
                info = (df.loc[0].Info).split(",")
                x = df.Entropy_Low
                y = df.Entropy_High
                aux =self.axes.scatter(x, y, alpha=0.5, label="Strain {s}, Repetition {r}".format(s=info[0], r=info[1]))
                self.array.append(aux)
        matplotlib.pyplot.grid()
        matplotlib.pyplot.legend(bbox_to_anchor=(1.1, 1.05))


        self.annot = self.axes.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->")) #create annotations

        self.annot.set_visible(False) #set visible false
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover) #handle mouse on events
        self.axes.legend()
        self.draw()


    def markRelatives(self,info):
        auxVal = []

        if self.isImported: #where gets info
            auxPos = self.experiments[self.experiments.Position.eq(int(info[2]))]
            auxStrains = auxPos[auxPos.Strain.eq(info[0])]
            positions = auxStrains.values.tolist()
            if len(positions) > 0:
                for p in positions: #get positions relatives
                    auxVal.append([p[6],p[7]])
        else:
            for dfPlot in self.experiments: #get positions relatives
                positions = dfPlot.loc[dfPlot.Position.eq(info[2]) & dfPlot.Strain.eq(info[0])].values.tolist()
                if len(positions) > 0:
                    auxVal.append([positions[0][5],positions[0][6]])
        comb = combinations(auxVal, 2) #gets combinations to get points
        for points in list(comb):
            point1 = points[0]
            point2 = points[1]
            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]
            self.axes.plot(x_values, y_values , color='red') #plot relatives lines


    def update_annot(self,ind,i):
        pos = self.array[i].get_offsets()[ind["ind"][0]]
        if self.isImported: #where gets info
            dfPlot = self.experiments
        else:
            dfPlot = self.experiments[i]
        dinfo =dfPlot.loc[dfPlot.Entropy_Low.eq(pos[0]) & dfPlot.Entropy_High.eq(pos[1])] #get info
        info = dinfo['Info'].values[0]
        auxInfo = info.split(',')
        self.markRelatives(auxInfo) #get relatives points(same positions and strain)
        self.annot.xy = pos
        pointInfo='Repetition: ' + auxInfo[1] + '\nPosition: ' + auxInfo[2]
        self.annot.set_text(pointInfo) #set text
        self.annot.get_bbox_patch().set_alpha(0.4)


    def removeOldPoints(self):
        i = 0
        for _ in self.axes.lines:
            self.axes.lines[i].remove()
            i = i+1

    def hover(self,event):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes: #if is in axes
            cont = False
            i = 0
            while not cont and i < len(self.array):
                cont, ind = self.array[i].contains(event)
                i = i +1
            if cont: #if is over a point
                self.removeOldPoints() #remove old relatives points
                self.update_annot(ind,(i-1)) #get info and mark relatives

                self.annot.set_visible(True) #show info
                self.fig.canvas.draw_idle() #draw

            else:
                if vis:
                    self.annot.set_visible(False) #set visible false
                    self.fig.canvas.draw_idle()


    def exportCSV(self,filename):
        if self.isImported:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Unable to export an imported file')
            error_dialog.exec()
        else:
            i = 0
            for df in self.experiments:
                if i == 0:
                    dfR = df
                    i = 1
                else:
                    dfR = pd.concat([dfR,df])
            exps = ''
            i = 0
            j = 0
            dfR["type"] = df.apply(lambda row: self.type, axis=1)


            dfR.to_csv(filename)
            return self.nameExp,self.type,self.parameter

