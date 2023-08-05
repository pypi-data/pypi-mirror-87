import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from src.Format_DF import totalExperimentsToPassages, totalExperimentsToPositions, formatStrains


def tsnePassages(experiments, perp=None, lr=None, df_results=None): #t-SNE for passages

    #calculate t-SNE passages normal with this combinations or if user selected perp and lr
    if ((perp==None) and (lr==None)):
        perps = [3, 6, 12, 15]
        learning_r = [10, 100, 300, 500]
    elif ((perp!=None) and (lr==None)):
        perps=perp
        learning_r = [10, 100, 300, 500]
    elif ((perp==None) and (lr!=None)):
        perps = [3, 6, 12, 15]
        learning_r=lr
    else:
        perps=perp
        learning_r=lr

    data, infos, strains = totalExperimentsToPassages(experiments) #transform experiments
    cant, df_Pas_Strains = formatStrains(strains) #format strains
    df_infos=pd.DataFrame(infos, columns=["Info"]) #create dataframe with info


    data_Aux=pd.DataFrame(columns=["tsne_1", "tsne_2", "Strain", "StrainNumber", "Info", "Perp", "LR"]) #create new dataframe

    data_Tot=pd.DataFrame()

    #calculate every transformation with perp y lerning rate combinations and save in dataframe
    for p in perps:
        for lr in learning_r:
            transformedData = TSNE(perplexity=p, learning_rate=lr, random_state=111).fit_transform(data)
            data_Aux["tsne_1"]=transformedData[:,0]
            data_Aux["tsne_2"]=transformedData[:,1]
            data_Aux["Strain"]=df_Pas_Strains["Strain"]
            data_Aux["StrainNumber"]=df_Pas_Strains["StrainNumber"]
            data_Aux["Info"]=df_infos["Info"]
            data_Aux.loc[:, "Perp"]=p
            data_Aux.loc[:, "LR"]=lr
            data_Aux.loc[:, "Plot"]=0
            data_Tot=data_Tot.append(data_Aux, ignore_index=True)



    if df_results is None: #if normal execution(not perp and lr added by user)
        df_results=data_Tot
    else:
        df_results=df_results.append(data_Tot, ignore_index=True) #add lr and perp to old info

    return df_results #return dataframe

def tsnePositions(experiments, perp=None, lr=None, df_results=None):
    #same as tsnePassages, but with positions. Combinations are less than passages due  the number of points
    if ((perp==None) and (lr==None)):
        perps = [3, 12]
        learning_r = [10, 300]
    elif ((perp!=None) and (lr==None)):
        perps=perp
        learning_r = [10, 100, 300, 500]
    elif ((perp==None) and (lr!=None)):
        perps = [3, 6, 12, 15]
        learning_r=lr
    else:
        perps=perp
        learning_r=lr

    data, infos, strains = totalExperimentsToPositions(experiments)
    cant, df_Pas_Strains = formatStrains(strains)
    df_infos=pd.DataFrame(infos, columns=["Info"])


    data_Aux=pd.DataFrame(columns=["tsne_1", "tsne_2", "Strain", "StrainNumber", "Info", "Perp", "LR"])

    data_Tot=pd.DataFrame()


    for p in perps:
        for lr in learning_r:
            transformedData = TSNE(perplexity=p, learning_rate=lr, random_state=111).fit_transform(data)
            data_Aux["tsne_1"]=transformedData[:,0]
            data_Aux["tsne_2"]=transformedData[:,1]
            data_Aux["Strain"]=df_Pas_Strains["Strain"]
            data_Aux["StrainNumber"]=df_Pas_Strains["StrainNumber"]
            data_Aux["Info"]=df_infos["Info"]
            data_Aux.loc[:, "Perp"]=p
            data_Aux.loc[:, "LR"]=lr
            data_Aux.loc[:, "Plot"]=0
            data_Tot=data_Tot.append(data_Aux, ignore_index=True)



    if df_results is None:
        df_results=data_Tot
    else:
        df_results=df_results.append(data_Tot, ignore_index=True)

    return df_results
