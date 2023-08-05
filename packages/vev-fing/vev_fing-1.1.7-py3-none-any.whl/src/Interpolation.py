import pandas as pd
import numpy as np



def interpolationPassageFreq(passage, dataframe):
    passages = dataframe.Passage.unique().tolist() #get unique passages
    i = passages.index(passage) #get index
    auxPassagePlus = passages[i + 1] #get passage before
    auxPassageMinus = passages[i - 1] #get passage after
    columns = dataframe.columns
    i=0
    for c in columns:
       if i > 1 and i < 66: #all the codons
           dataframe.loc[dataframe.Passage == passage, c] = None #new info in passage to interpolate
           df1 = dataframe.loc[dataframe.Passage == auxPassageMinus, c].tolist()  #codon freq passage before
           df3 = dataframe.loc[dataframe.Passage == auxPassagePlus, c].tolist() #codon freq passage after
           df2 = dataframe.loc[dataframe.Passage == passage, c].tolist() #codon in passage to interpolate = None
           dfs = [df1, df2, df3]
           dfAux = pd.DataFrame(dfs)
           dfAux = dfAux.interpolate() #create linear interpolation
           aux = dfAux.iloc[[1]].values.tolist() #get new value
           dataframe.loc[dataframe.Passage == passage, c] = np.asarray(aux[0]) #change info
       i=i+1



    return dataframe

def interpolationPassage(passage, dataframe):
    #same as interpolationPassageFreq but insted of codons, this function interpolate only entropy
    passages = dataframe.Passage.unique().tolist()
    i = passages.index(passage)
    auxPassagePlus = passages[i + 1]
    auxPassageMinus = passages[i - 1]
    dataframe.loc[dataframe.Passage == passage, 'Entropy'] = None
    df1 = dataframe.loc[dataframe.Passage == auxPassageMinus, 'Entropy'].tolist()
    df3 = dataframe.loc[dataframe.Passage == auxPassagePlus, 'Entropy'].tolist()
    df2 = dataframe.loc[dataframe.Passage == passage, 'Entropy'].tolist()
    dfs = [df1, df2, df3]
    dfAux = pd.DataFrame(dfs)
    dfAux = dfAux.interpolate()
    aux = dfAux.iloc[[1]].values.tolist()
    dataframe.loc[dataframe.Passage == passage, 'Entropy'] = np.asarray(aux[0])

    return dataframe
