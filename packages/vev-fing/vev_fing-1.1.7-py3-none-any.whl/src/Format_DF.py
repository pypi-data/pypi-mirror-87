import numpy as np
import pandas as pd


def experimentToPassages(df):
    # Function that takes the experiment (dataframe df) and converts each passage into a row

    passages = df['Passage'].unique()  # get passages

    info_df = str(df['info'].iloc[0])  # get info
    strain_df = info_df.split(',')[0]
    repetition_df = info_df.split(',')[1]

    arrayDF_P = []
    arrayInfo = []
    arrayStrain = []

    for p in passages:  # every passage

        dfP = df[df.Passage.eq(p)]  # get dataframe for this passage
        dfPE = dfP[['Entropy']]  # get entropy
        passageArray = np.array(dfPE)  # convert to numpy array
        pA = np.squeeze(np.array([passageArray]))  # reduce dimension
        arrayDF_P.append(pA)  # add pasage to array
        arrayInfo.append(str(strain_df) + ',' + str(repetition_df) + ',' + str(p))
        arrayStrain.append(str(strain_df))
    return np.array(arrayDF_P), np.array(arrayInfo), np.array(arrayStrain)


def totalExperimentsToPassages(parameters):
    # Function that takes all the experiments you have loaded in parameters and converts each experiment to one row per passage

    # Arrays where the passages are stored as rows and the info
    arrayT_DF_P = []
    arrayT_Info = []
    arrayT_Strain = []

    for df in parameters:  # every experiment
        arrayP, arrayI, arrayS = experimentToPassages(df)  # convert each passage into a row
        arrayT_DF_P.append(arrayP)
        arrayT_Info.append(arrayI)
        arrayT_Strain.append(arrayS)

    totalArrayData = np.concatenate(arrayT_DF_P)
    totalArrayInfo = np.concatenate(arrayT_Info)
    totalArrayStrain = np.concatenate(arrayT_Strain)

    return totalArrayData, totalArrayInfo, totalArrayStrain


def experimentToPositions(df):
    # Function that takes the experiment (dataframe df) and converts each position into a row
    # same as experimentsToPassage but with positions

    positions = df['Position'].unique()  # get positions

    info_df = str(df['info'].iloc[0])  # get info
    strain_df = info_df.split(',')[0]
    repetition_df = info_df.split(',')[1]

    arrayDF_P = []
    arrayInfo = []
    arrayStrain = []

    for p in positions:
        dfP = df[df.Position.eq(p)]
        dfPE = dfP[['Entropy']]
        positionArray = np.array(dfPE)

        pA = np.squeeze(np.array([positionArray]))
        arrayDF_P.append(pA)
        arrayInfo.append(str(strain_df) + ',' + str(repetition_df) + ',' + str(p))
        arrayStrain.append(str(strain_df))
    return np.array(arrayDF_P), np.array(arrayInfo), np.array(arrayStrain)


def totalExperimentsToPositions(parameters):
    # same as totalExperimentsToPassages but with positions
    arrayT_DF_P = []
    arrayT_Info = []
    arrayT_Strain = []

    for df in parameters:
        arrayP, arrayI, arrayS = experimentToPositions(df)
        arrayT_DF_P.append(arrayP)
        arrayT_Info.append(arrayI)
        arrayT_Strain.append(arrayS)

    totalArrayData = np.concatenate(arrayT_DF_P)
    totalArrayInfo = np.concatenate(arrayT_Info)
    totalArrayStrain = np.concatenate(arrayT_Strain)

    return totalArrayData, totalArrayInfo, totalArrayStrain


def formatStrains(strainT):
    # Function that takes the array of strains and assigns each one an int from 0
    # It also calculates the value that the perplexity parameter of tSNE should take according to the number of points of each stra

    # Pass the strains of the loaded experiments to dataframe
    df = pd.DataFrame(strainT, columns=["Strain"])
    df = df.assign(StrainNumber=df['Strain'])

    strainsU = df.Strain.unique()  # getthe number of passages of each strain
    dataRows = []
    i = 0
    for s in strainsU:
        n = df[df.Strain.eq(s)].count()
        dataRows.append(n)
        df.loc[df['Strain'] == s, 'StrainNumber'] = i
        i += 1
    arNum = np.array(dataRows)

    return arNum, df