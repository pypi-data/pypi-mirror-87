import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter1d
from src.Format_DF import totalExperimentsToPassages, formatStrains, experimentToPositions



def movingAverage_1D(arr, n=3):
    y_f = uniform_filter1d(arr, mode='constant', size=n)
    r=int(np.floor(n/2)+1)
    for i in range(r-1):
        d=((np.floor(n/2)+1)+i)
        y_f[i]=n*y_f[i]/d


    for i in range(y_f.shape[0]-r+1,y_f.shape[0]):
        d=y_f.shape[0]-i+np.floor(n/2)
        y_f[i]=n*y_f[i]/d

    return y_f


def movingAverage(arr, n=3):

    arr_MA = np.zeros_like(arr)

    for i in range(arr.shape[0]):
        arr_MA[i]=movingAverage_1D(arr[i],n)
    return arr_MA


def decomposition_PM_LV_RV(df, window):

    ar_Data, ar_Info, ar_Strain = experimentToPositions(df)

    df_I = pd.DataFrame([sub.split(",") for sub in ar_Info])
    df_I.columns=["Strain", "Repetition", "Position"]

    arr_Low = movingAverage(ar_Data, n=window)
    arr_High=np.abs(ar_Data-arr_Low)

    ar_Data_Sum=np.sum(ar_Data, axis=1)
    arr_Low_Sum=np.sum(arr_Low, axis=1)
    arr_HighSum=np.sum(arr_High, axis=1)

    data_Aux=pd.DataFrame(columns=["Info", "Position", "Strain", "Repetition", "Entropy_Acum", "Entropy_Low", "Entropy_High"])

    data_Aux['Info']=ar_Info
    data_Aux['Position']=df_I.Position
    data_Aux['Strain']=df_I.Strain
    data_Aux['Repetition']=df_I.Repetition
    data_Aux['Entropy_Acum']=ar_Data_Sum
    data_Aux['Entropy_Low']=arr_Low_Sum
    data_Aux['Entropy_High']=arr_HighSum

    return data_Aux



def decomposition_Poly_LV_RV(df, grade): #lv_rv poly

    ar_Data, ar_Info, ar_Strain = experimentToPositions(df) #get info

    df_I = pd.DataFrame([sub.split(",") for sub in ar_Info])
    df_I.columns=["Strain", "Repetition", "Position"] #split info column

    passages=df['Passage'].unique() #get passages

    passages = list(map(int, passages)) #cast to int

    arr_Low = np.zeros_like(ar_Data)

    for i in range(ar_Data.shape[0]):
        z = np.polyfit(passages, ar_Data[i], grade) #Least squares
        p = np.poly1d(z)
        arr_Low[i]=p(passages)

    arr_High=np.abs(ar_Data-arr_Low)

    ar_Data_Sum=np.sum(ar_Data, axis=1)
    arr_Low_Sum=np.sum(arr_Low, axis=1)
    arr_HighSum=np.sum(arr_High, axis=1)

    data_Aux=pd.DataFrame(columns=["Info", "Position", "Strain", "Repetition", "Entropy_Acum", "Entropy_Low", "Entropy_High"])

    data_Aux['Info']=ar_Info
    data_Aux['Position']=df_I.Position
    data_Aux['Strain']=df_I.Strain
    data_Aux['Repetition']=df_I.Repetition
    data_Aux['Entropy_Acum']=ar_Data_Sum
    data_Aux['Entropy_Low']=arr_Low_Sum
    data_Aux['Entropy_High']=arr_HighSum

    return data_Aux
