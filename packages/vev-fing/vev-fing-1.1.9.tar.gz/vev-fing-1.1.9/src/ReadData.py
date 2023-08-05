
import pandas as pd
import numpy as np
import os
import glob
from src.NumericalSort import numericalSort
import re

def readData(parameters):
    i = 0
    strainControl = ''
    repetitionControl = ''
    path=parameters[0]
    fvp=parameters[1]
    lvp=parameters[2]

    df_list = []
    for filename in sorted(glob.glob(os.path.join(path, '*.csv')) , key=numericalSort): #every csv in directory sorted
        #checks name of .csv
        auxInfo = filename.split('/')
        auxInfo = auxInfo[len(auxInfo)-1]
        auxInfo = auxInfo.split('_')
        auxPassage = auxInfo[1]
        strain = auxInfo[2]
        auxRepetition = auxInfo[3]
        repetition = re.sub("\D+", '', auxRepetition)
        passage = re.sub("\D+",'',auxPassage)
        if i == 0: # check only one type of strain and repetition
            strainControl = strain
            repetitionControl = repetition
            i = i +1
        if repetition != repetitionControl or strainControl != strain:
            raise Exception("Error, there are csv files from other experiment")
        df=pd.read_csv(filename) #get csv
        df['Passage']=passage #passage information is csv passage
        df_list.append(df) #add dataframe to array



    df_T = pd.concat(df_list) #concat all DataFrame passages in one
    df_T['Strain']=strain #add info of strain
    df_T['Repetition']=repetition #add info of repetition
    df_T['info'] = df_T.apply(lambda row: str(row.Strain) + ',' + str(row.Repetition) + "," + str(row.Passage) + "," + str(row.Position),axis=1) #create column info


    positions = df_T['Position'].unique() #get positions
    lvpAux = positions[len(positions) - 1] #get last positions of experiment
    if lvp ==0 or lvpAux < lvp: #control lvp value
        lvp = lvpAux
    df_T =keepValidPositions(df_T,fvp,lvp) #keep valid positions of experiment


    return df_T, strain, repetition, lvp


def keepValidPositions(dfE, fvp, lvp):
    # Function that takes the dataframe and keeps only the valid positions

    # look for the value of the positions in the dataframe
    posiciones = dfE.Position.unique()

    # Find the index where the positions are valid
    idx = np.where((posiciones >= fvp) & (posiciones <= lvp))

    #save valid positions
    posVal = posiciones[idx]


    dfE_val = dfE[dfE.Position.isin(posVal)].copy() #get new dataframe only with valid positions

    return dfE_val
