import pandas as pd
import numpy as np
import math
import os



def getEntropyExperiment(strain,repetition,fvp,lvp,dataFrame):
    pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
    path_pkl = pathPip + 'src/data_experiments/'
    filePath=path_pkl +str(strain)+'_' +str(repetition)+'('+str(fvp)+'-'+str(lvp)+')_entropy.parquet'

    if os.path.isfile(filePath): #if entropy exists
        return pd.read_parquet(filePath)
    else:
        entropyList = []
        epsilon = 2.2204e-16
        for index, row in dataFrame.iterrows():
            i = 0
            entropy = float(0)
            for freq in row:
                i += 1
                if i > 2 and i < 67: # i = 1 is passage, i = 2 is coverage and from i = 3 you have the 64 codons
                    entropy -= np.multiply(freq, (math.log(freq + epsilon)))  # logarithm to base e of the frequency
            entropyList.append(entropy)

        dataFrame['Entropy'] = np.asarray(entropyList) #add entropy to dataframe
        df = dataFrame[['Position','Coverage','Strain','Repetition','Passage','Entropy','info']] #drop frequencies

        return df

def getEntropyExperimentAminos(strain,repetition,fvp,lvp,dataFrame):
    pathPip = str(os.path.dirname(pd.__file__)).split('pandas')[0]
    path_pkl = pathPip + 'src/data_experiments/'
    filePath=path_pkl +str(strain)+'_' +str(repetition)+'('+str(fvp)+'-'+str(lvp)+')_aminos_entropy.parquet'

    if os.path.isfile(filePath):
        return pd.read_parquet(filePath)
    else:

        entropyList = []
        epsilon = 2.2204e-16
        for index, row in dataFrame.iterrows():
            i = 0
            entropy = float(0)
            for freq in row:
                i += 1
                if i > 1 and i < 23: # aminos
                    entropy -= np.multiply(freq, (math.log(freq + epsilon)))  # # logarithm to base e of the frequency
            entropyList.append(entropy)

        dataFrame['Entropy'] = np.asarray(entropyList)
        dataFrame.to_parquet(filePath)
        return dataFrame
