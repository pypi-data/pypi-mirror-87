from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QSlider
import sys
from src.ReadData import readData,keepValidPositions
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPalette, QBrush, QImage, QIcon, QMovie
from src.pcaClass import FigurePCA
from src.dialogPositions import valuesPositions
import pandas as pd
from src.dialogInterpolation import dInterpolation
from src.threadsOpenClass import LoadFile, LoadFolder
from src.threadsPlotClass import plotSurface,plotPositionEntropy,plotGumbel, codonDecay
from src.tsneClass import FigureTSNE
from src.tsneThreadProcess import tsneProcess,tsneProcessUpdate
from src.lvrvClass import FigureLVRV
from src.lvrvThread import lvrv_poly,lvrv_average
from src.codonDecayClass import FigureCD
from src.threadPCA import pcaProcess
from datetime import datetime
import logging
import pymongo
import socket
import os
import json
from jsonschema import validate

def dbconnect(mode):
    if mode:
        client = pymongo.MongoClient("mongodb+srv://vevdb:MDp1atkxAv9R2KxZ@cluster0.lu8xi.gcp.mongodb.net/")
        db = client['VEV']
        return db
    else:
        return None

def logger(new,experiment,log):
    logging.info(log)

def getExperiments(ne,nameExps):
    #299_1(774-7332)
    otherexperiments = ''
    for exp in nameExps:
        if ne != exp:
            experiment = exp.split('.')[0]
            otherexperiments =otherexperiments + experiment + ' '
    return otherexperiments


def initLoggin():
    pathPip = str(os.path.dirname(pymongo.__file__)).split('pymongo')[0]
    date_time = datetime.now().strftime("%d-%m-%Y")
    logging.basicConfig(filename=pathPip+'src/logs/vev-'+date_time+'.log',format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('VEV Started')

class Interface(QtWidgets.QMainWindow):
    def __init__(self, mode=None):
        super(Interface, self).__init__()
        pathPip = str(os.path.dirname(pymongo.__file__)).split('pymongo')[0]
        uic.loadUi(pathPip+'src/ui_files/mainwindow.ui', self)
        self._flag = False
        if mode==None:
            self.Online= True
        else:
            self.Online = False
        #paths
        self.path_buttons = pathPip + 'src/buttons_and_background/'
        self.path_pkl = pathPip + 'src/data_experiments/'
        self.path_grafics = pathPip + 'src/plot_images'
        self.path_schemas = pathPip + 'src/'
        self.loaded_dfs = []
        #################
        self.threadpool = QtCore.QThreadPool()  # handle threads
        self.label_lvrv.hide()
        self.input_lvrv.hide()
        self.slidersTSNE = QtWidgets.QVBoxLayout(self.frame_sliders)
        self.arraySliders = []
        initLoggin()
        self.db = dbconnect(self.Online)
        self.namePC = socket.gethostname()
        self.addUser()
        # call functions

        self.buttonLoadExperiment.clicked.connect(self.loadExperiment)
        self.buttonLoadParquet.clicked.connect(self.loadExperimentParquet)
        self.plotPositionButton.clicked.connect(self.plotPostionFunction)
        self.plotSurfaceButton.clicked.connect(self.plotSurfaceFunction)
        self.codonButton.clicked.connect(self.codonDecayFunction)
        self.PCAButton.clicked.connect(self.pcaFunction)
        self.tsneButton.clicked.connect(self.tsneFunctions)
        self.buttonInterpolation.clicked.connect(self.interpolateFunction)
        self.gumbelButton.clicked.connect(self.gumbelWidget)
        self.addPerpLRButton.clicked.connect(self.tsneAddPerpAndLR)
        self.mvAverage.toggled.connect(lambda: self.changeLabel(self.mvAverage))
        self.poly.toggled.connect(lambda: self.changeLabel(self.poly))
        self.lvrv_button.clicked.connect(self.lvrvFunction)
        self.LRButton.clicked.connect(self.getLastResults)
        self.ClusterPlotButton.clicked.connect(self.clusteringFunction)
        self.exportCluster.clicked.connect(self.exportClusterDF)

        # exports functions
        self.exportCSVTSNE.clicked.connect(self.exportTSNE)
        self.importCSVTSNE.clicked.connect(self.importTSNE)
        self.exportCSVLVRV.clicked.connect(self.exportLVRV)
        self.ImportCSVLVRV.clicked.connect(self.importLVRV)
        self.ExportCSVPCA.clicked.connect(self.exportPCA)
        self.ImportCSVPCA.clicked.connect(self.importPCA)

        # Move stacked widgets

        self.stackedWidget.setCurrentIndex(0)  # main
        self.buttonplotposition.clicked.connect(self.entropyPosition)
        self.buttonEntropySurface.clicked.connect(self.entropySurface)
        self.buttonCodonDecay.clicked.connect(self.codonDecayWidget)
        self.buttonPCAFunction.clicked.connect(self.pcaWidget)
        self.buttonTsne.clicked.connect(self.tsne)
        self.plotGumbelButton.clicked.connect(self.gumbelFunction)
        self.buttonLVRV.clicked.connect(self.LVRV)
        self.buttonClustering.clicked.connect(self.Clustering)

        # style
        self.setMinimumSize(1000, 568)
        self.setWindowIcon(QIcon(self.path_buttons + 'ImageICON.jpg'))
        self.buttonLoadExperiment.setStyleSheet(
            "QPushButton{border-image:url(" + self.path_buttons + "Load Folder.png);}")
        self.buttonLoadExperiment.setToolTip("Click this button to open experiment folder")
        self.buttonLoadParquet.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "Load File.png);}")
        self.buttonLoadParquet.setToolTip("Click this button to open experiment file")
        self.buttonLVRV.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "LVRV.png);}")
        self.buttonLVRV.setToolTip("Plot Leading Variations and Random Variations")
        self.buttonplotposition.setStyleSheet(
            "QPushButton{border-image:url(" + self.path_buttons + "Plot Entropy x Position.png);}")
        self.buttonplotposition.setToolTip("Plot Entropy times position")
        self.buttonEntropySurface.setStyleSheet(
            "QPushButton{border-image:url(" + self.path_buttons + "Plot Entropy Surface.png);}")
        self.buttonEntropySurface.setToolTip("Plot Entropy Surface of an experiment")
        self.buttonCodonDecay.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "Codon Decay.png);}")
        self.buttonCodonDecay.setToolTip("Plot Codon Decay of an experiment")
        self.buttonPCAFunction.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "PCA.png);}")
        self.buttonPCAFunction.setToolTip("Plot PCA")
        self.gumbelButton.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "Gumbel.png);}")
        self.gumbelButton.setToolTip("Plot Gumbel distribution")
        self.buttonTsne.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "t-SNE.png);}")
        self.buttonTsne.setToolTip("Enter to t-SNE plot options")
        self.buttonInterpolation.setStyleSheet(
            "QPushButton{border-image:url(" + self.path_buttons + "Interpolation.png);}")
        self.buttonInterpolation.setToolTip("Interpolate experiment data")
        self.LRButton.setToolTip("Export info of results executed order by last modified")
        self.buttonClustering.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "Clustering.png);}")
        self.buttonClustering.setToolTip("Clustering Analysis ")

        # home buttons
        self.home1.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home1.setToolTip("Return to home")
        self.home2.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home2.setToolTip("Return to home")
        self.home3.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home3.setToolTip("Return to home")
        self.home4.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home4.setToolTip("Return to home")
        self.home5.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home5.setToolTip("Return to home")
        self.home6.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home6.setToolTip("Return to home")
        self.home7.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home7.setToolTip("Return to home")
        self.home8.setStyleSheet("QPushButton{border-image:url(" + self.path_buttons + "home.png);}")
        self.home8.setToolTip("Return to home")
        # connect home buttons
        self.home1.clicked.connect(self.returnHome)
        self.home2.clicked.connect(self.returnHome)
        self.home3.clicked.connect(self.returnHome)
        self.home4.clicked.connect(self.returnHome)
        self.home5.clicked.connect(self.returnHome)
        self.home6.clicked.connect(self.returnHome)
        self.home7.clicked.connect(self.returnHome)
        self.home8.clicked.connect(self.returnHome)

        # TABLE VIEW MODELS##
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Experiment '])
        self.tableView_PlotPostion.setModel(self.model)
        self.tableView_PlotPostion.horizontalHeader().setSectionResizeMode(1)
        self.tableTSNE.setModel(self.model)
        self.tableTSNE.horizontalHeader().setSectionResizeMode(1)
        self.tablePCA.setModel(self.model)
        self.tablePCA.horizontalHeader().setSectionResizeMode(1)
        self.tableViewCodon.setModel(self.model)
        self.tableViewCodon.horizontalHeader().setSectionResizeMode(1)
        self.tableViewEntropySurface.setModel(self.model)
        self.tableViewEntropySurface.horizontalHeader().setSectionResizeMode(1)
        self.tableViewGumbel.setModel(self.model)
        self.tableViewGumbel.horizontalHeader().setSectionResizeMode(1)
        self.tableLVRV.setModel(self.model)
        self.tableLVRV.horizontalHeader().setSectionResizeMode(1)
        self.tableCluster.setModel(self.model)
        self.tableCluster.horizontalHeader().setSectionResizeMode(1)
        # Sliders
        self.perplexitySlider.setMaximum(3)
        self.perplexitySlider.setMinimum(0)
        self.lrSlider.setMaximum(3)
        self.lrSlider.setMinimum(0)
        self.clusterSlider.setMaximum(2)
        self.clusterSlider.setMinimum(0)
        self.typeCluster.setMaximum(1)
        self.typeCluster.setMinimum(0)
        self.clusterSlider.valueChanged.connect(self.updateCluster)
        self.typeCluster.valueChanged.connect(self.updateTypeCluster)
        self.perplexitySlider.valueChanged.connect(self.updateTSNE)
        self.lrSlider.valueChanged.connect(self.updateTSNE)
        # FIGURES
        self.pca = None
        self.tsne = None
        self.lvrv = None
        self.condonDecay = None
        self.cluster = ''
        self.clusterDF = None
        # AUXILIAR
        self.perAux = [3, 6, 12, 15]
        self.lrAux = [10, 100, 300, 500]
        self.numberCluster = [2, 4, 6]
        self.movie = QMovie(self.path_buttons + 'Loading.gif')

    def scale_image(self, size):  # scale background image
        imageBack = QImage(self.path_buttons + 'background.png')
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(imageBack))
        self.setPalette(palette)

    def resizeEvent(self, e):  # function to handle resize main window
        if not self._flag:
            self._flag = True
            self.scale_image(e.size())
            QtCore.QTimer.singleShot(30, lambda: setattr(self, "_flag", False))
        super().resizeEvent(e)

        # CHANGE LABEL -- function to handle label in LV-RV function(Moving average or Polynomial)

    def changeLabel(self, b):  # b is the radio button
        self.label_lvrv.show()
        self.input_lvrv.show()
        if b.text() == "Moving Average":
            if b.isChecked() == True:
                self.label_lvrv.setText("Select Average Window:")
            else:
                self.label_lvrv.setText("Select Polynomial Grade:")

        else:
            if b.isChecked() == True:
                self.label_lvrv.setText("Select Polynomial Grade:")
            else:
                self.label_lvrv.setText("Select Average Window:")
        # Load FILES AND FOLDERS

    def loadExperiment(self):
        # opens dialog for user to select folder experiment
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        fileName = QFileDialog.getExistingDirectory(self, directory=os.getcwd(), caption='Select a directory',
                                                    options=options)
        if fileName != "":  # If user select folder
            vp = valuesPositions()
            vp.exec()
            fvp = vp.getFVP()
            lvp = vp.getLVP()
            setIt = vp.getIfSet()
            if setIt:  # if user set valid positions(fvp,lvp) then execute thread for load folder
                thread = LoadFolder(fileName, fvp, lvp)
                thread.signals.error.connect(self.openError)  # linked function to main thread if thread executes fails
                thread.signals.finished.connect(
                    self.openOK)  # linked function to main thread if thread executes correctly
                self.threadpool.start(thread)
            else:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Parameters was not correctly selected')
                error_dialog.exec()

    def loadExperimentParquet(self):
        # opens dialog for user to select  experiment parquet file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        (fileName, aux) = QFileDialog.getOpenFileName(self, directory=self.path_pkl, caption='Select a .parquet File',
                                                      filter='*.parquet', options=options)
        if fileName != "":  # If user select file then execute thread for load experiement file
            thread = LoadFile(fileName)
            thread.signals.error.connect(self.openError)  # linked function to main thread if thread throws an error
            thread.signals.finished.connect(self.openOK)  # linked function to main thread if thread executes correctly
            self.threadpool.start(thread)

        # Complete or Errors with open

    def openOK(self, parameters):  # parameters emitted by the executed thread
        strain = parameters[0]
        repetition = parameters[1]
        fvp = parameters[2]
        lvp = parameters[3]
        control = parameters[4]
        if (strain, repetition, fvp, lvp) in self.loaded_dfs:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('This experiment is already loaded')
            error_dialog.exec()
        else:
            self.loaded_dfs.append((strain, repetition, fvp, lvp))  # add to currents loaded experiments
            experimentName = "Strain: " + strain + " " + "Repetition: " + repetition
            row = (QStandardItem(experimentName))
            self.model.appendRow(row)  # add experiment to the table of experiments
            self.refreshFunction()  # refresh experiments tables
            if control:
                nameLog = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')'
                log = 'Experiment ' + nameLog + 'was loaded and entropy was calculated with First Value Position(FVP) = ' + str(
                    fvp) + ' and Last Value Position(LVP) = ' + str(lvp)
                logger(True, nameLog, log)  # logging function
                de = QtWidgets.QMessageBox()
                de.setText('Folder: ' + experimentName + ' loaded')
                de.exec()  # dialog to let the user know that the experiment was loaded succesufully
                self.addExperiment(strain, repetition, fvp, lvp)
            else:

                logging.info(' Experiment already calculated was load: ' + strain + '_' + repetition + '(' + str(
                    fvp) + '-' + str(lvp) + ')')

    def openError(self, error):  # if load throws error
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage(
            'An error has occurred when an experiment was loaded. Please verify if the folder contains only csv experiments files')
        error_dialog.exec()
        logging.info('An error has occurred when an experiment was loaded')

    def refreshFunction(self):  # refhresh tables
        self.tablePCA.update()
        self.tableViewEntropySurface.update()
        self.tableView_PlotPostion.update()
        self.tableViewCodon.update()
        self.tableTSNE.update()
        self.tableViewGumbel.update()
        self.tableLVRV.update()
        self.tableCluster.update()

    def interpolateFunction(self):  # function for interpolation
        di = dInterpolation(self.loaded_dfs)  # create interpolation class
        di.exec()  # execute interpolation
        executed, typeInterpolation, strain, repetition, fvp, lvp, passage = di.getInfo()  # get info from interpolation executed
        if executed:
            nameLog = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ').txt'
            log = typeInterpolation + ' interpolation was made for passage number ' + passage
            logger(False, nameLog, log)
            self.addEntrydb(strain, repetition, fvp, lvp, 'Interpolation ' + typeInterpolation, passage, '')
            self.addFunctions('Interpolation ' + typeInterpolation, passage)

        # PLOTS AND Interactive Functions

    def tsneAddPerpAndLR(self):  # Function to handle user add new Perplexity and LR.
        try:
            perp = int(self.newPerplexity.toPlainText())  # value of perp
            lr = int(self.newLR.toPlainText())  # value of LR
            if self.tsne is None:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Please plot t-SNE method first')
                error_dialog.exec()
            else:
                dfs, data, nameExps = self.tsne.getData()  # get tsne data ploted
                auxType = self.tsne.getType()  # get t-SNE type
                if auxType == 'Passages':
                    thread = tsneProcessUpdate(dfs, perp, lr, data, "Passages", nameExps)
                else:
                    thread = tsneProcessUpdate(dfs, perp, lr, data, "Positions", nameExps)
                thread.signals.error.connect(self.errorTSNEProcess)
                thread.signals.finished.connect(self.okProcessTSNEUpdate)

                self.loading.setMovie(self.movie)  # for loading bar
                self.movie.start()  # start gif
                self.threadpool.start(thread)  # start thread

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please enter integer values')
            error_dialog.exec()

    def okProcessTSNEUpdate(self, parameters):
        self.movie.stop()  # stop gif
        self.loading.clear()  # clear loading bar
        data = parameters[0]
        perp = parameters[1]
        lr = parameters[2]
        typeTSNE = parameters[3]
        nameExps = parameters[4]

        self.tsne.updateData(data, perp, lr, nameExps)  # update LR and Perp with user values
        for ne in nameExps:  # get names of experiments plotted in t-SNE
            otherexperiments = getExperiments(ne, nameExps)
            auxStrain = ne.split("_")
            strain = auxStrain[0]
            auxRep = auxStrain[1].split("(")
            repetition = auxRep[0]
            auxfvp = auxRep[1].split("-")
            fvp = auxfvp[0]
            lvp = auxfvp[1].split(")")[0]
            log = typeTSNE + ' t-SNE executed with perplexity = ' + str(perp) + ' and learning rate = ' + str(
                lr) + ' with this experiments: ' + otherexperiments
            # logger(False, ne, log)
            logging.info(log)
            self.addEntrydb(strain, repetition, fvp, lvp,
                            't-SNE ' + typeTSNE + ' with perp=' + str(perp) + ' and lr=' + str(lr), otherexperiments,
                            '')
            self.addFunctions('t-SNE ' + typeTSNE + ' with perp=' + str(perp) + ' and lr=' + str(lr), otherexperiments)

    def clearLayout(self, layout):  # clear ON/OFF sliders in t-SNE for new t-SNE execution
        self.arraySliders = []
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
                layout.removeItem(item)

    def addSlidersTSNE(self, strains):  # add ON/OFF slider for t-SNE
        self.clearLayout(self.slidersTSNE)

        for strain in strains:
            label = QLabel()
            label.setText(str(strain))
            self.slidersTSNE.addWidget(label)
            slid = QSlider(QtCore.Qt.Horizontal)
            slid.setMaximum(1)
            slid.setMinimum(0)
            self.slidersTSNE.addWidget(slid)
            slid.setValue(0)
            slid.valueChanged.connect(self.updateStrainsTSNE)
            self.arraySliders.append([slid, strain])

    def tsneFunctions(self):  # new t-SNE execution
        dfsAux = []
        dfs = []
        strains = []
        nameExperiments = []
        indices = self.tableTSNE.selectionModel().selectedRows()
        if len(indices) < 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select at least one Experiment')
            error_dialog.exec()


        elif (self.rb_passages.isChecked() == False and self.rb_positions.isChecked() == False):
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select method type')
            error_dialog.exec()

        else:  # valid parameters
            try:
                fvpMayor = 0
                lvpMenor = 0
                for index in sorted(indices):  # selected experiments in table
                    experimentIndex = (index.row())
                    df = self.loaded_dfs[experimentIndex]
                    strain = str(df[0])
                    if strain not in strains:  # unique strains for ON/OFF strains
                        strains.append(strain)
                    repetition = str(df[1])
                    fvp = df[2]
                    lvp = df[3]
                    if fvpMayor == 0 and lvpMenor == 0:
                        fvpMayor = fvp
                        lvpMenor = lvp
                    else:  # different experiments positions(fvp,lvp)
                        if fvp > fvpMayor:
                            fvpMayor = fvp
                        if lvp < lvpMenor:
                            lvpMenor = lvp
                    experimentNametxt = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ').txt'
                    experimentName = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')_entropy.parquet'
                    dfAux = pd.read_parquet(self.path_pkl + experimentName)
                    dfsAux.append(dfAux)
                    nameExperiments.append(experimentNametxt)  # array of experiments names
                for dataFrame in dfsAux:
                    df = keepValidPositions(dataFrame, fvpMayor, lvpMenor)
                    dfs.append(df)  # array of dataframes

                self.addSlidersTSNE(strains)  # add on off sliders
                if self.rb_passages.isChecked() == True:  # tpye of t-SNE
                    auxType = 'Passages'
                else:
                    auxType = 'Positions'
                thread = tsneProcess(dfs, auxType, nameExperiments)  # Class QRunnable tsneProcess
                thread.signals.error.connect(self.errorTSNEProcess)
                thread.signals.finished.connect(self.okProcessTSNE)
                self.loading.setMovie(self.movie)  # loading bar
                self.movie.start()
                self.threadpool.start(thread)  # execute thread
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error')
                error_dialog.exec()

    def errorTSNEProcess(self):
        self.movie.stop()
        self.loading.clear()
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('Error: An error has occurred when calculated t-SNE')
        error_dialog.exec()
        logging.info('An error has occurred when calculated t-SNE')

    def okProcessTSNE(self, parameters):  # parameters emitted for t-SNE
        self.newPerplexity.clear()
        self.newLR.clear()
        self.movie.stop()
        self.loading.clear()
        dfs = parameters[0]
        data = parameters[1]
        tsneType = parameters[2]
        nameExp = parameters[3]
        if self.tsne == None:  # first execution
            boxAux = QtWidgets.QVBoxLayout(self.tsneFrame)
            self.tsne = FigureTSNE(dfs, data, tsneType, nameExp, self.tsneFrame, width=6, height=5,
                                   dpi=100)  # create figure TSNE for plot and handle mouse events
            boxAux.addWidget(self.tsne)
        else:
            # handle sliders to set in first positions
            self.perplexitySlider.valueChanged.disconnect()
            self.lrSlider.valueChanged.disconnect()
            self.tsne.newtSNE(dfs, data, tsneType, nameExp)
            self.perplexitySlider.setValue(0)
            self.lrSlider.setValue(0)
            self.perplexity.setText(str(3))
            self.lr.setText(str(10))
            self.perplexitySlider.valueChanged.connect(self.updateTSNE)
            self.lrSlider.valueChanged.connect(self.updateTSNE)
        if tsneType == 'Passages':  # sliders has 4 positions
            self.perplexitySlider.setMaximum(3)
            self.lrSlider.setMaximum(3)
            self.perAux = [3, 6, 12, 15]
            self.lrAux = [10, 100, 300, 500]
        else:  # sliders has 2 positions
            self.perplexitySlider.setMaximum(1)
            self.lrSlider.setMaximum(1)
            self.perAux = [3, 12]
            self.lrAux = [10, 300]
        for ne in nameExp:
            auxStrain = ne.split("_")
            strain = auxStrain[0]
            auxRep = auxStrain[1].split("(")
            repetition = auxRep[0]
            auxfvp = auxRep[1].split("-")
            fvp = auxfvp[0]
            lvp = auxfvp[1].split(")")[0]
            otherexperiments = getExperiments(ne, nameExp)
            log = tsneType + ' t-SNE executed with this experiments: ' + otherexperiments
            logging.info(log)
            self.addEntrydb(strain, repetition, fvp, lvp, 't-SNE ' + tsneType, otherexperiments, '')
            self.addFunctions('t-SNE ' + tsneType, otherexperiments)

    def updateTSNE(self):  # handle sliders move
        perplexity = self.perAux[self.perplexitySlider.value()]
        lr = self.lrAux[self.lrSlider.value()]
        self.perplexity.setText(str(perplexity))
        self.lr.setText(str(lr))
        if self.tsne == None:  # not t-SNE executed
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please before change this, plot t-SNE method')
            error_dialog.exec()
            self.perplexitySlider.valueChanged.disconnect()
            self.lrSlider.valueChanged.disconnect()
            self.perplexitySlider.setValue(0)
            self.lrSlider.setValue(0)
            self.perplexity.setText(str(3))
            self.lr.setText(str(10))
            self.perplexitySlider.valueChanged.connect(self.updateTSNE)
            self.lrSlider.valueChanged.connect(self.updateTSNE)
        else:
            self.tsne.updateParameters(perplexity, lr)  # update figure

    def getChanges(self):  # changes in on off sliders
        changes = []
        for [slider, strain] in self.arraySliders:
            if slider.value() == 1:
                changes.append(strain)
        return changes

    def updateStrainsTSNE(self):  # for update strains in plotted figure
        if self.tsne == None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please before change this, plot t-SNE method')
            error_dialog.exec()
        else:
            changes = self.getChanges()
            self.tsne.onOffStrains(changes)

        ####Clustering#######

    def clusteringFunction(self):

        indices = self.tableCluster.selectionModel().selectedRows()
        if len(indices) < 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select  one Experiment')
            error_dialog.exec()
        elif len(indices) > 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select  only one Experiment')
            error_dialog.exec()
        elif (self.rbNormal.isChecked() == False and self.rbSSA.isChecked() == False):
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select method type')
            error_dialog.exec()
        else:  # valid parameters
            try:
                for index in sorted(indices):  # selected experiment
                    experimentIndex = (index.row())
                    df = self.loaded_dfs[experimentIndex]
                    strain = str(df[0])
                    repetition = str(df[1])
                    fvp = df[2]
                    lvp = df[3]
                    experimentName = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')_entropy.parquet'
                    dfAux = pd.read_parquet(self.path_pkl + experimentName)
                if self.rbNormal.isChecked() == True:  # clustering type
                    auxType = 'Normal'
                else:
                    auxType = 'SSA'
                thread = clusterProcess(dfAux, strain, repetition, fvp, lvp, auxType)  # new QRunnable clusterProcess
                thread.signals.error.connect(self.errorClustering)
                thread.signals.finished.connect(self.okClustering)
                self.loading_cluster.setMovie(self.movie)  # loading bar
                self.movie.start()
                self.threadpool.start(thread)  # start thread
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error with clustering')
                error_dialog.exec()

    def errorClustering(self):
        self.movie.stop()
        self.loading_cluster.clear()
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('Error: An error has occurred when calculated clustering')
        error_dialog.exec()
        logging.info('An error has occurred when calculated clustering')

    def okClustering(self, parameters):  # clustering execute successfully
        self.movie.stop()
        self.loading_cluster.clear()
        self.clusterSlider.valueChanged.disconnect()
        self.clusterSlider.setValue(0)
        self.number_cluster.setText(str(2))
        self.clusterSlider.valueChanged.connect(self.updateCluster)
        self.typeCluster.valueChanged.disconnect()
        self.typeCluster.setValue(0)
        self.typeCluster.valueChanged.connect(self.updateTypeCluster)
        strain = parameters[0]
        repetition = parameters[1]
        fvp = parameters[2]
        lvp = parameters[3]
        directory = parameters[4]
        outliers = parameters[5]
        self.clusterDF = parameters[6]  # dataframe for export function
        nameLog = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')'
        log = 'Clustering for experiment: ' + nameLog + ' was plotted'
        logging.info(log)

        self.addFunctions('Clustering', '')
        self.cluster = directory  # directory where plotted images are
        name = directory + '/Curves2.png'  # image to show
        pixmap = QPixmap(name)
        pixmap = pixmap.scaled(self.clustering1.size(), QtCore.Qt.KeepAspectRatio)
        self.clustering1.setPixmap(pixmap)  # show image
        pos = 'Positions of interest: '
        for p in outliers:
            pos = pos + str(p) + ', '
        pos = pos[:-2]
        self.addEntrydb(strain, repetition, fvp, lvp, 'Clustering', '', directory, pos)

        self.loading_cluster.setText(pos)  # set positions of interest
        self.loading_cluster.setStyleSheet('font: 75 11pt "Ubuntu Condensed";')  # style
        self.clusterSlider.valueChanged.disconnect()  # disconnect function to move slider.
        self.clusterSlider.setValue(0)
        self.number_cluster.setText(str(2))
        self.clusterSlider.valueChanged.connect(self.updateCluster)
        self.clusterSlider.setMaximum(2)

    def updateCluster(self):  # update nro cluster
        nroCluster = self.numberCluster[self.clusterSlider.value()]
        self.number_cluster.setText(str(nroCluster))

        if self.cluster == '':  # clustering not executed
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please before change this execute cluster method')
            error_dialog.exec()
            self.clusterSlider.valueChanged.disconnect()
            self.clusterSlider.setValue(0)
            self.number_cluster.setText(str(2))
            self.clusterSlider.valueChanged.connect(self.updateCluster)
            self.clusterSlider.setMaximum(2)
        else:
            directory = self.cluster
            type = self.typeCluster.value()  # type in slider (confusion matrix or curves)
            if type == 0:
                name = directory + '/Curves' + str(nroCluster) + '.png'
            else:
                if nroCluster == 2:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('Error: Not valid Nro Clusters for Confusion Matrix')
                    error_dialog.exec()
                    self.clusterSlider.valueChanged.disconnect()
                    self.clusterSlider.setValue(1)
                    self.number_cluster.setText(str(4))
                    self.clusterSlider.valueChanged.connect(self.updateCluster)
                    name = directory + '/confMatrix4' + '.png'
                else:
                    name = directory + '/confMatrix' + str(nroCluster) + '.png'
            pixmap = QPixmap(name)
            self.clustering1.setPixmap(pixmap)  # show image

    def updateTypeCluster(self):  # to handle type(curves or Conf matrix) slider
        if self.cluster == '':  # clustering not executed
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please before change this execute cluster method')
            error_dialog.exec()
            self.typeCluster.valueChanged.disconnect()
            self.typeCluster.setValue(0)
            self.typeCluster.valueChanged.connect(self.updateTypeCluster)
        else:
            directory = self.cluster
            nroCluster = self.numberCluster[self.clusterSlider.value()]
            if nroCluster == 2:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Confusion Matrix is Available for 4 or 6 clusters')
                error_dialog.exec()
                self.typeCluster.valueChanged.disconnect()
                self.typeCluster.setValue(0)
                self.typeCluster.valueChanged.connect(self.updateTypeCluster)
            type = self.typeCluster.value()
            if type == 0:
                name = directory + '/Curves' + str(nroCluster) + '.png'
            else:
                name = directory + '/confMatrix' + str(nroCluster) + '.png'
            pixmap = QPixmap(name)
            self.clustering1.setPixmap(pixmap)

    def exportClusterDF(self):
        if self.cluster == '':  # clustering not executed
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Plot cluster method before export result')
            error_dialog.exec()
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            options |= QFileDialog.DontUseCustomDirectoryIcons
            fileName, _ = QFileDialog.getSaveFileName(self, directory=os.getcwd(), caption='Save result',
                                                      filter='*.csv',
                                                      options=options)
            if fileName != '':  # if user selected filename
                if '.csv' not in fileName:
                    fileName = fileName.replace('.', '') + '.csv'
                self.clusterDF.to_csv(fileName)  # export clusterDF

        ##################### PCA #################

    def pcaFunction(self):
        dfsAux = []
        dfs = []
        nameExps = []
        indices = self.tablePCA.selectionModel().selectedRows()

        if len(indices) < 2:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select at least two Experiments')
            error_dialog.exec()

        else:  # valid positions
            try:
                # same as t-SNE get parameters
                fvpMayor = 0
                lvpMenor = 0
                for index in sorted(indices):
                    experimentIndex = (index.row())
                    df = self.loaded_dfs[experimentIndex]
                    strain = str(df[0])
                    repetition = str(df[1])
                    fvp = df[2]
                    lvp = df[3]
                    if fvpMayor == 0 and lvpMenor == 0:
                        fvpMayor = fvp
                        lvpMenor = lvp
                    else:
                        if fvp > fvpMayor:
                            fvpMayor = fvp
                        if lvp < lvpMenor:
                            lvpMenor = lvp
                    experimentNametxt = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ').txt'
                    experimentName = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')_entropy.parquet'
                    dfAux = pd.read_parquet(self.path_pkl + experimentName)
                    dfsAux.append(dfAux)
                    nameExps.append(experimentNametxt)
                for dataFrame in dfsAux:
                    df = keepValidPositions(dataFrame, fvpMayor, lvpMenor)
                    dfs.append(df)

                thread = pcaProcess(dfs, nameExps)  # create QRunnable pcaProcess
                thread.signals.error.connect(self.errorPCA)
                thread.signals.finished.connect(self.pcaOK)
                self.loadingPCA.setMovie(self.movie)
                self.movie.start()
                self.threadpool.start(thread)  # start thread
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: An error ocurred while PCA executed')
                error_dialog.exec()

    def pcaOK(self, parameters):
        self.movie.stop()
        self.loadingPCA.clear()
        dfPuntosPCA = parameters[0]
        pcaVector = parameters[1]
        infoDF = parameters[2]
        nameExps = parameters[3]
        dfs = parameters[4]
        if self.pca == None:  # first pca executed
            boxAux = QtWidgets.QVBoxLayout(self.widget_image)  # add to layout
            self.pca = FigurePCA(dfPuntosPCA, pcaVector, infoDF, nameExps, dfs, self.widget_image, width=6, height=5,
                                 dpi=100)  # create pcaFigure to handle events and plot
            boxAux.addWidget(self.pca)
        else:
            self.pca.updatePCA(dfPuntosPCA, pcaVector, infoDF, nameExps, dfs)  # update figure
        for ne in nameExps:
            auxStrain = ne.split("_")
            strain = auxStrain[0]
            auxRep = auxStrain[1].split("(")
            repetition = auxRep[0]
            auxfvp = auxRep[1].split("-")
            fvp = auxfvp[0]
            lvp = auxfvp[1].split(")")[0]
            otherexperiments = getExperiments(ne, nameExps)
            log = 'PCA executed with this experiments ' + otherexperiments
            logging.info(log)
            self.addEntrydb(strain, repetition, fvp, lvp, 'PCA', otherexperiments, '')
            self.addFunctions('PCA', otherexperiments)

    def errorPCA(self):
        self.movie.stop()
        self.loadingPCA.clear()
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('Error: An error has occurred when calculated PCA')
        error_dialog.exec()
        logging.info('An error has occurred when calculated PCA')

        ############ Codon Decay ##########################33

    def codonDecayFunction(self):
        indices = self.tableViewCodon.selectionModel().selectedRows()
        if len(indices) < 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select at least one Experiment')
            error_dialog.exec()
        elif len(indices) > 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select only one Experiment')
            error_dialog.exec()
        else:  # valid parameters
            try:
                th = self.threshold.toPlainText()
                fth = float(th)  # has to be float
                if fth < 0 or fth >= 1:  # valid threshold
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('Error: Please select threshold between 0 and 1')
                    error_dialog.exec()
                else:
                    for index in sorted(indices):
                        experimentIndex = (index.row())
                    df = self.loaded_dfs[experimentIndex]
                    strain = str(df[0])
                    repetition = str(df[1])
                    fvp = str(df[2])
                    lvp = str(df[3])
                    thread = codonDecay(strain, repetition, fth, fvp, lvp)  # create QRunnable codonDecay
                    thread.signals.error.connect(self.errorPlotCD)
                    thread.signals.finished.connect(self.codonDecayOK)
                    self.loadingCD.setMovie(self.movie)
                    self.movie.start()
                    self.threadpool.start(thread)
            except Exception as e:
                if e.__class__ == FileNotFoundError:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('Error: Please enter the experiment parquet with frequencies')
                    error_dialog.exec()
                else:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('Error: Please enter an float threshold')
                    error_dialog.exec()

    def errorPlotCD(self):
        self.movie.stop()
        self.loadingCD.clear()
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('Error: An error has occurred when calculated Codon Decay')
        error_dialog.exec()
        logging.info('An error has occurred when calculated Codon Decay')

    def codonDecayOK(self, parameters):
        self.movie.stop()
        self.loadingCD.clear()
        dfResult = parameters[0]
        df = parameters[1]
        th = parameters[2]
        strain = parameters[3]
        repetition = parameters[4]
        fvp = parameters[5]
        lvp = parameters[6]
        if self.condonDecay == None:  # first excution
            boxAux = QtWidgets.QVBoxLayout(self.codonDecayFrame)  # add to layout
            self.condonDecay = FigureCD(dfResult, df, th, self.codonDecayFrame, width=6, height=5,
                                        dpi=100)  # create figure for plotting and handle events
            boxAux.addWidget(self.condonDecay)
        else:
            self.condonDecay.updateCD(dfResult, df, th)  # update figure
        nameLog = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')'
        log = 'Codon Decay was plotted with threshold ' + str(th) + 'with experiment ' + nameLog
        logging.info(log)
        self.addEntrydb(strain, repetition, fvp, lvp, 'Codon Decay', str(th), '')
        self.addFunctions('Codon Decay', th)

        #### PLOT FUNCTIONS ##################

    def plotSurfaceFunction(self):  # function to plot entropy surface 3D
        indices = self.tableViewEntropySurface.selectionModel().selectedRows()
        if len(indices) < 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select at least one Experiment')
            error_dialog.exec()
        elif len(indices) > 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select only one Experiment')
            error_dialog.exec()
        else:  # valid parameters
            for index in sorted(indices):
                experimentIndex = (index.row())
            df = self.loaded_dfs[experimentIndex]
            strain = str(df[0])
            repetition = str(df[1])
            fvp = str(df[2])
            lvp = str(df[3])
            thread = plotSurface(strain, repetition, fvp, lvp)  # create QRunnable plotSurface class
            thread.signals.error.connect(self.errorPlot)
            thread.signals.finished.connect(self.plotSurfaceOK)
            self.loadingPS.setMovie(self.movie)
            self.movie.start()
            self.threadpool.start(thread)  # start thread

    def plotSurfaceOK(self, parameters):
        self.movie.stop()
        self.loadingPS.clear()
        strain = parameters[0]
        repetition = parameters[1]
        fvp = parameters[2]
        lvp = parameters[3]
        name = self.path_grafics + '/entropySurface_' + strain + '_' + repetition + '.png'
        pixmap = QPixmap(name)
        self.imageSurface.setPixmap(pixmap)  # show image
        nameLog = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')'
        log = 'Entropy surface is plotted and saved' + ' with experiment ' + nameLog
        logging.info(log)
        self.addEntrydb(strain, repetition, fvp, lvp, 'Plot Surface Entropy', '', name)
        self.addFunctions('Plot Surface Entropy', '')

    def plotPostionFunction(self):  # function to plot entropy position
        indices = self.tableView_PlotPostion.selectionModel().selectedRows()
        if len(indices) < 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select at least one Experiment')
            error_dialog.exec()
        elif len(indices) > 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select only one Experiment')
            error_dialog.exec()
        else:  # valid parameters
            try:
                position = self.textEditPosition.toPlainText()
                position = int(position)  # cast to int user position entry
                for index in sorted(indices):
                    experimentIndex = (index.row())
                df = self.loaded_dfs[experimentIndex]
                strain = str(df[0])
                repetition = str(df[1])
                fvp = str(df[2])
                lvp = str(df[3])
                thread = plotPositionEntropy(strain, repetition, position, fvp,
                                             lvp)  # QRunnable to process plotPositionEntropy
                thread.signals.error.connect(self.errorPlot)
                thread.signals.finished.connect(self.plotEntropyPositionOK)
                self.loadingPPP.setMovie(self.movie)
                self.movie.start()
                self.threadpool.start(thread)
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Please enter a valid position')
                error_dialog.exec()

    def plotEntropyPositionOK(self, parameters):  # succesfully process plot position
        self.movie.stop()
        self.loadingPPP.clear()
        strain = parameters[0]
        repetition = parameters[1]
        position = parameters[2]
        fvp = parameters[3]
        lvp = parameters[4]
        name = self.path_grafics + '/Entropy_' + str(position) + '_' + strain + '_' + repetition + '.png'
        pixmap = QPixmap(name)
        self.plotPositionImage.setPixmap(pixmap)  # show image
        nameLog = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')'
        log = 'Entropy is plotted and saved for position ' + str(position) + ' with experiment ' + nameLog
        logger(False, nameLog, log)
        self.addEntrydb(strain, repetition, fvp, lvp, 'Entropy times Position', position, name)
        self.addFunctions('Entropy times Position', position)

        ######## GUMBEL #################

    def gumbelFunction(self):
        indices = self.tableViewGumbel.selectionModel().selectedRows()
        if len(indices) < 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select at least one Experiment')
            error_dialog.exec()
        elif len(indices) > 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select only one Experiment')
            error_dialog.exec()
        else:  # valid parameters
            for index in sorted(indices):
                experimentIndex = (index.row())
            df = self.loaded_dfs[experimentIndex]
            strain = str(df[0])
            repetition = str(df[1])
            fvp = str(df[2])
            lvp = str(df[3])
            thread = plotGumbel(strain, repetition, fvp, lvp)  # QRunnable for gumbel process
            thread.signals.error.connect(self.errorPlot)
            thread.signals.finished.connect(self.plotGumbelOK)
            self.loadingGP.setMovie(self.movie)
            self.movie.start()
            self.threadpool.start(thread)  # start thread

    def plotGumbelOK(self, parameters):  # sucessfully gumbel process
        self.movie.stop()
        self.loadingGP.clear()
        strain = parameters[0]
        repetition = parameters[1]
        fvp = parameters[2]
        lvp = parameters[3]
        outliers = parameters[4]
        self.loadingGP.setText(outliers)  # set label por positions of interest
        self.loadingGP.setStyleSheet('font: 75 13pt "Ubuntu Condensed";')
        name = self.path_grafics + '/Gumbel' + '_' + strain + '_' + repetition + '.png'
        pixmap = QPixmap(name)  # show image
        self.imageGumbel.setPixmap(pixmap)
        nameLog = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')'
        log = 'Gumbel is plotted and saved' + ' with experiment ' + nameLog
        logging.info(log)
        self.addEntrydb(strain, repetition, fvp, lvp, 'Gumbel', '', name, outliers)
        self.addFunctions('Gumbel', '')

    def errorPlot(self, e):
        self.movie.stop()
        self.loadingGP.clear()
        self.loadingPPP.clear()
        self.loadingPS.clear()
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('An error has occurred when experiment was plotted')
        error_dialog.exec()
        logging.info('An error has occurred when experiment was plotted')

        ########### LV-RV Function ########################

    def lvrvFunction(self):
        dfsAux = []
        dfs = []
        nameExp = []
        indices = self.tableLVRV.selectionModel().selectedRows()
        if len(indices) < 1:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select at least one Experiment')
            error_dialog.exec()


        elif (self.mvAverage.isChecked() == False and self.poly.isChecked() == False):
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please select method type')
            error_dialog.exec()

        else:  # valid parameters
            try:
                input = self.input_lvrv.toPlainText()  # get user value for Window or Grade
                intInput = int(input)
                fvpMayor = 0
                lvpMenor = 0
                # same as t-SNE get parameters
                for index in sorted(indices):
                    experimentIndex = (index.row())
                    df = self.loaded_dfs[experimentIndex]
                    strain = str(df[0])
                    repetition = str(df[1])
                    fvp = df[2]
                    lvp = df[3]
                    if fvpMayor == 0 and lvpMenor == 0:
                        fvpMayor = fvp
                        lvpMenor = lvp
                    else:
                        if fvp > fvpMayor:
                            fvpMayor = fvp
                        if lvp < lvpMenor:
                            lvpMenor = lvp
                    experimentNametxt = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ').txt'
                    experimentName = strain + '_' + repetition + '(' + str(fvp) + '-' + str(lvp) + ')_entropy.parquet'
                    dfAux = pd.read_parquet(self.path_pkl + experimentName)
                    dfsAux.append(dfAux)
                    nameExp.append(experimentNametxt)
                for dataFrame in dfsAux:
                    df = keepValidPositions(dataFrame, fvpMayor, lvpMenor)
                    dfs.append(df)
                if self.mvAverage.isChecked() == True:  # type LVRV
                    thread = lvrv_average(dfs, intInput, nameExp)  # Qrunnable to process lvrv moving average
                    thread.signals.finished.connect(self.lvrvOK)
                    thread.signals.error.connect(self.lvrvError)

                    self.loadingLVRV.setMovie(self.movie)
                    self.movie.start()
                    self.threadpool.start(thread)  # start thread
                else:
                    thread = lvrv_poly(dfs, intInput, nameExp)  # Qrunnable to process lvrv poly
                    thread.signals.finished.connect(self.lvrvOK)
                    thread.signals.error.connect(self.lvrvError)
                    self.loadingLVRV.setMovie(self.movie)
                    self.movie.start()
                    self.threadpool.start(thread)  # start thread
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Please enter an integer')
                error_dialog.exec()

    def lvrvError(self):  # error in lvrv process
        self.movie.stop()
        self.loadingLVRV.clear()
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('Error: An error has occurred when calculated LV-RV')
        error_dialog.exec()
        logging.info('An error has occurred when calculated LV-RV')

    def lvrvOK(self, parameters):  # sucess in lvrv process
        self.movie.stop()
        self.loadingLVRV.clear()
        dfs = parameters[0]
        typeLVRV = parameters[1]
        nameExps = parameters[2]
        param = parameters[3]
        if self.lvrv == None:  # first execution
            boxAux = QtWidgets.QVBoxLayout(self.lvrv_frame)  # add to layout
            self.lvrv = FigureLVRV(dfs, self.lvrv_frame, nameExps, typeLVRV, param, width=6, height=5,
                                   dpi=100)  # create lvrv figure to plot and handle events
            boxAux.addWidget(self.lvrv)
        else:
            self.lvrv.updatelvrv(dfs, nameExps, typeLVRV, param)  # update figure
        for ne in nameExps:
            auxStrain = ne.split("_")
            strain = auxStrain[0]
            auxRep = auxStrain[1].split("(")
            repetition = auxRep[0]
            auxfvp = auxRep[1].split("-")
            fvp = auxfvp[0]
            lvp = auxfvp[1].split(")")[0]
            otherexperiments = getExperiments(ne, nameExps)
            log = typeLVRV + ' LV-RV was plotted with parameter ' + str(
                param) + ' with this experiments: ' + otherexperiments
            logging.info(log)
            self.addEntrydb(strain, repetition, fvp, lvp, typeLVRV + ' LV-RV',
                            otherexperiments + ' with parameter = ' + str(param), '')
            self.addFunctions(typeLVRV + ' LV-RV', otherexperiments + ' with parameter = ' + str(param))

        # functions for move stackedWidget(main buttons)

    def entropyPosition(self):
        self.stackedWidget.setCurrentIndex(1)  # plotEntropyPosition

    def entropySurface(self):
        self.stackedWidget.setCurrentIndex(2)

    def codonDecayWidget(self):
        self.stackedWidget.setCurrentIndex(4)

    def tsne(self):
        self.stackedWidget.setCurrentIndex(5)

    def pcaWidget(self):
        self.stackedWidget.setCurrentIndex(3)

    def gumbelWidget(self):
        self.stackedWidget.setCurrentIndex(6)

    def LVRV(self):
        self.stackedWidget.setCurrentIndex(7)

    def Clustering(self):
        self.stackedWidget.setCurrentIndex(8)

    def returnHome(self):
        self.stackedWidget.setCurrentIndex(0)

        # functions to export

    def exportTSNE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        fileName, _ = QFileDialog.getSaveFileName(self, directory=os.getcwd(), caption='Save experiment',
                                                  filter='*.csv',
                                                  options=options)
        if fileName != '':
            if '.csv' not in fileName:  # csv not in filename
                fileName = fileName.replace('.', '') + '.csv'
            if self.tsne == None:  # t-SNE not executed
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Please Plot t-SNE before export')
                error_dialog.exec()
            else:
                nameExp, normal, lr, perp, tsneType = self.tsne.exportCSV(
                    fileName)  # info from export. This is necessary for Data Base
                for ne in nameExp:
                    auxStrain = ne.split("_")
                    strain = auxStrain[0]
                    auxRep = auxStrain[1].split("(")
                    repetition = auxRep[0]
                    auxfvp = auxRep[1].split("-")
                    fvp = auxfvp[0]
                    lvp = auxfvp[1].split(")")[0]
                    otherexperiments = getExperiments(ne, nameExp)
                    if normal:
                        log = tsneType + ' t-SNE executed with this experiments: ' + otherexperiments

                        logging.info(log)
                        self.addEntrydb(strain, repetition, fvp, lvp, 't-SNE ' + tsneType, otherexperiments, fileName)
                    else:
                        log = tsneType + ' t-SNE executed with perplexity = ' + str(
                            perp) + ' and learning rate = ' + str(lr) + ' with this experiments: ' + otherexperiments
                        logging.info(log)
                        self.addEntrydb(strain, repetition, fvp, lvp,
                                        't-SNE ' + tsneType + ' with perp=' + str(perp) + ' and lr=' + str(lr),
                                        otherexperiments, fileName)

    def importTSNE(self):
        try:
            nameExps = []
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            options |= QFileDialog.DontUseCustomDirectoryIcons
            (fileName, aux) = QFileDialog.getOpenFileName(self, directory=os.getcwd(), caption='Select a .csv File',
                                                          filter='*.csv', options=options)
            if fileName != "":  # select experiment
                df = pd.read_csv(fileName)
                strains = df.Strain.unique()  # get strains from csv
                self.addSlidersTSNE(strains)  # add on/off sliders
                columns = df.columns.unique()  # get columns information
                if 'Position' in columns:  # get type of t-SNE
                    tsneType = 'Positions'
                else:
                    tsneType = 'Passages'
                perps = df.Perp.unique()
                lrs = df.LR.unique()

                if len(perps) == 1 and len(
                        lrs) == 1:  # if only had info of add lr and perp(not from normally execution)
                    perp = perps[0]
                    lr = lrs[0]
                else:
                    lr = None
                    perp = None

                if self.tsne == None:  # if is first execution
                    boxAux = QtWidgets.QVBoxLayout(self.tsneFrame)  # add to layout
                    self.tsne = FigureTSNE(None, df, tsneType, nameExps, self.tsneFrame, lr, perp, width=6, height=5,
                                           dpi=100)  # create figure
                    boxAux.addWidget(self.tsne)
                else:
                    self.tsne.newtSNE(None, df, tsneType, nameExps, lr, perp)  # update figure
                self.perplexitySlider.valueChanged.disconnect()
                self.lrSlider.valueChanged.disconnect()
                if tsneType == 'Passages':  # set sliders info for passages type
                    self.perplexitySlider.setValue(0)
                    self.lrSlider.setValue(0)
                    self.perplexitySlider.setMaximum(3)
                    self.lrSlider.setMaximum(3)
                    self.perAux = [3, 6, 12, 15]
                    self.lrAux = [10, 100, 300, 500]
                else:  # set sliders info for positions type

                    self.perplexitySlider.setMaximum(1)
                    self.lrSlider.setMaximum(1)
                    self.perAux = [3, 12]
                    self.lrAux = [10, 300]

                    self.perplexitySlider.setValue(0)
                    self.lrSlider.setValue(0)

                self.perplexitySlider.valueChanged.connect(self.updateTSNE)
                self.lrSlider.valueChanged.connect(self.updateTSNE)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please import a valid t-SNE experiment CSV')
            error_dialog.exec()

    def exportLVRV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        fileName, _ = QFileDialog.getSaveFileName(self, directory=os.getcwd(), caption='Save experiment',
                                                  filter='*.csv',
                                                  options=options)
        if fileName != '':
            if '.csv' not in fileName:
                fileName = fileName.replace('.', '') + '.csv'
            if self.lvrv == None:  # lvrv not executed
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Please getLastResultsPlot LV-RV before export')
                error_dialog.exec()
            else:
                nameExps, typeLVRV, param = self.lvrv.exportCSV(fileName)  # get info for DB
                for ne in nameExps:
                    auxStrain = ne.split("_")
                    strain = auxStrain[0]
                    auxRep = auxStrain[1].split("(")
                    repetition = auxRep[0]
                    auxfvp = auxRep[1].split("-")
                    fvp = auxfvp[0]
                    lvp = auxfvp[1].split(")")[0]

                    otherexperiments = getExperiments(ne, nameExps)

                    log = typeLVRV + ' LV-RV was plotted with parameter ' + str(
                        param) + ' with this experiments: ' + otherexperiments
                    logging.info(log)
                    self.addEntrydb(strain, repetition, fvp, lvp, typeLVRV + ' LV-RV',
                                    otherexperiments + ' with parameter = ' + str(param), fileName)

    def importLVRV(self):
        try:

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            options |= QFileDialog.DontUseCustomDirectoryIcons
            (fileName, aux) = QFileDialog.getOpenFileName(self, directory=os.getcwd(), caption='Select a .csv File',
                                                          filter='*.csv',
                                                          options=options)

            if fileName != "":  # user select csv
                df = pd.read_csv(fileName)
                lvrvType = df.type.unique()[0]  # get type

                if self.lvrv == None:  # first execution
                    boxAux = QtWidgets.QVBoxLayout(self.lvrv_frame)
                    self.lvrv = FigureLVRV(df, self.lvrv_frame, lvrvType, None, width=6, height=5,
                                           dpi=100)  # create figure
                    boxAux.addWidget(self.lvrv)
                else:
                    self.lvrv.updatelvrv(df)  # update figure
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please import a valid LV-RV experiment CSV')
            error_dialog.exec()

    def exportPCA(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        fileName, _ = QFileDialog.getSaveFileName(self, directory=os.getcwd(), caption='Save experiment',
                                                  filter='*.csv',
                                                  options=options)
        if fileName != '':
            if '.csv' not in fileName:
                fileName = fileName.replace('.', '') + '.csv'
            if self.pca == None:  # not pca executed
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Error: Please Plot PCA before export')
                error_dialog.exec()
            else:
                nameExps = self.pca.exportPCA(fileName)  # get info for DB
                for ne in nameExps:
                    auxStrain = ne.split("_")
                    strain = auxStrain[0]
                    auxRep = auxStrain[1].split("(")
                    repetition = auxRep[0]
                    auxfvp = auxRep[1].split("-")
                    fvp = auxfvp[0]
                    lvp = auxfvp[1].split(")")[0]
                    otherexperiments = getExperiments(ne, nameExps)
                    log = 'PCA executed with this experiments ' + otherexperiments
                    logging.info(log)
                    self.addEntrydb(strain, repetition, fvp, lvp, 'PCA', otherexperiments, fileName)

    def importPCA(self):
        try:

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            options |= QFileDialog.DontUseCustomDirectoryIcons
            (fileName, aux) = QFileDialog.getOpenFileName(self, directory=os.getcwd(), caption='Select a .csv File',
                                                          filter='*.csv',
                                                          options=options)

            if fileName != "":  # user select csv
                df = pd.read_csv(fileName)
                if self.pca == None:  # first execution
                    boxAux = QtWidgets.QVBoxLayout(self.widget_image)
                    self.pca = FigurePCA(None, None, None, None, None, self.widget_image, df, width=6,
                                         height=5, dpi=100)  # create figure
                    boxAux.addWidget(self.pca)
                else:
                    self.pca.updatePCA(None, None, None, None, None, df)  # update figure
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Please import a valid PCA experiment CSV')
            error_dialog.exec()

        # data base functions

    def getLastResults(self):
        if self.Online:  # online mode
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            options |= QFileDialog.DontUseCustomDirectoryIcons
            fileName, _ = QFileDialog.getSaveFileName(self, directory=os.getcwd(), caption='Save Results',
                                                      filter='*.csv',
                                                      options=options)
            if fileName != '':
                if '.csv' not in fileName:
                    fileName = fileName.replace('.', '') + '.csv'

                vevExperiments = self.db['ResultsExperiments']  # get table
                results = vevExperiments.find({"_id.user": self.namePC})  # find users results
                csv_columns = ['Strain', 'Repetition', 'fvp', 'lvp', 'function', 'parameters', 'result',
                               'outliers']  # csv columns
                try:
                    csvfile = open(fileName, 'w')  # create csvfile
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)  # set columns
                    writer.writeheader()
                    for experiments in results:  # for every user result experiments in ResultsExperiments
                        data = {"Strain": experiments["_id"]["strain"], "Repetition": experiments["_id"]["repetition"],
                                "fvp": experiments["_id"]["fvp"],
                                "lvp": experiments["_id"]["lvp"], "function": experiments["_id"]["expName"],
                                "parameters": experiments["params"],
                                "result": experiments["result"]}
                        # get data info and add to dict
                        try:
                            data["outliers"] = experiments[
                                "Interest Positions"]  # outliers is not in every entry(added later)
                        except:
                            data["outliers"] = ''
                        writer.writerow(data)  # write data
                    csvfile.close()
                except:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('An Error ocurred while getting last results')
                    error_dialog.exec()
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: VEV Application is in Offline mode')
            error_dialog.exec()

    def addFunctions(self, funcName, params):  # add entry in database for functions
        if self.Online:  # online mode
            functionsCollection = self.db['functions']
            functionEntry = {"_id": funcName, "parameters": params}
            validation = self.validateEntry(functionEntry, 'Function')  # validate schema
            if validation:
                entryD = functionsCollection.find_one({"_id": funcName})
                if entryD == None:  # insert
                    functionsCollection.insert_one(functionEntry)
                else:
                    functionsCollection.update_one({'_id': funcName}, {"$set": functionEntry}, upsert=False)

    def addExperiment(self, strain, repetition, fvp, lvp):  # add entry in database for experiments
        if self.Online:  # online mode
            experimentsCollection = self.db['experiments']
            fvp = int(fvp)
            lvp = int(lvp)
            repetition = int(repetition)
            experimentEntry = {"_id": {"user": self.namePC, "strain": strain, "repetition": repetition, "fvp": fvp,
                                       "lvp": lvp}}
            validation = self.validateEntry(experimentEntry, 'Experiment')  # validate schema
            if validation:
                entryD = experimentsCollection.find_one({"_id": experimentEntry["_id"]})
                if entryD == None:  # insert
                    experimentsCollection.insert_one(experimentEntry)

    def addEntrydb(self, strain, repetition, fvp, lvp, expName, params, result, outliers=None):
        if self.Online:  # online mode
            fvp = int(fvp)
            lvp = int(lvp)
            repetition = int(repetition)
            vevExp = {"_id": {"user": self.namePC, "strain": strain, "repetition": repetition, "fvp": fvp,
                              "lvp": lvp, "expName": expName}, "params": str(params), "result": result}
            validation = self.validateEntry(vevExp, 'ResultsExperiments')  # validate schema
            if validation:
                vevExperiments = self.db['ResultsExperiments']
                vevExp['timestamp'] = datetime.now().strftime("%d-%m-%Y,%H:%M:%S")
                if outliers is not None:  # gumbel or clustering
                    vevExp['Interest Positions'] = outliers

                entryD = vevExperiments.find_one({"_id": vevExp["_id"]})
                if entryD == None:  # insert
                    vevExperiments.insert_one(vevExp)
                else:  # update
                    vevExperiments.update_one({'_id': vevExp["_id"]}, {"$set": vevExp}, upsert=False)

    def addUser(self):
        if self.Online:  # online mode
            userCollection = self.db['users']
            entryD = userCollection.find_one({"_id": self.namePC})
            user = {"_id": self.namePC}
            validation = self.validateEntry(user, 'User')  # validate schema
            if validation:
                if entryD == None:  # insert
                    userCollection.insert_one(user)

    def validateEntry(self, entry, collection):  # validation schema with json-schema
        # first need to select proper schema
        try:
            if collection == 'ResultsExperiments':
                with open('Schema experiments results.json') as j:
                    schema = json.load(j)
            elif collection == 'Experiment':
                with open('Schema experiments.json') as j:
                    schema = json.load(j)
            elif collection == 'Function':
                with open('Schema function.json') as j:
                    schema = json.load(j)
            else:
                with open('Schema user.json') as j:
                    schema = json.load(j)
            validate(instance=entry, schema=schema)  # validate entry
            return True
        except:
            return False
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error: Invalid entry. Not fulfill schema')
            error_dialog.exec()


def main():
    args = sys.argv
    app = QtWidgets.QApplication([])
    args = [x.upper() for x in args]  # upper args to avoid case sensitive
    if 'OFFLINE' in args:
        win = Interface('OFFLINE')
    else:
        win = Interface()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

