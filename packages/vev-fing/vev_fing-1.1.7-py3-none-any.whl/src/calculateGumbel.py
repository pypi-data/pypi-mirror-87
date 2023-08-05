import pandas as pd
import math
import matplotlib.pyplot as plt
import scipy
import os



def dgumbel(x,mu,s): #density function
    return math.exp((mu - x)/s - math.exp((mu - x)/s))/s

def pgumbel(q,mu,s): #distribution function
    return math.exp(-(math.exp(-((q - mu)/s))))

def qgumbel(p,mu,s): #Quantile function
    return (mu - s) * math.log(-math.log(p))

def gumbelPlot(df,strain,repetition):
    dataframe,positions= extractMaximums(df)
    outlieres =gumbelAdjust(dataframe,positions,strain,repetition)
    return outlieres

def extractMaximums(df):
    df_positions =df.Position.unique() #get positions
    entropies = []
    for position in df_positions:
        entropy=df.loc[df.Position==position,'Entropy'].max() #maximum entropy
        entropies.append(entropy)

    df = pd.DataFrame(entropies, columns=['Entropy']) #create df with entropies maxiumums
    return df,df_positions


def get_hist(ax):
    n,bins = [],[]
    for rect in ax.patches:
        ((x0, y0), (x1, y1)) = rect.get_bbox().get_points()
        n.append(y1-y0)
        bins.append(x0) # left edge of each bin
    bins.append(x1) # also get right edge of last bin

    return n,bins




def gumbelAdjust(dfMax,positions,strain,repetition):
    pathPip=str(os.path.dirname(pd.__file__)).split('pandas')[0]
    sub = dfMax.quantile(.95, axis = 0)
    quantile= sub.iloc[0] #get quantile number
    listDF = dfMax.values.tolist()
    subsample=[]
    subpos = []
    index = 0
    for value in listDF: #every value in dfMax
        if value <= quantile: #if not in left tail
            subsample.append(value)
            subpos.append(positions[index])
        index +=1

    mu, sigma = scipy.stats.gumbel_r.fit(subsample) #fit subsample with gumbel

    #points of interest
    distribution = []
    dfMax['Position'] = positions

    for p in positions:
        distribution.append(1-pgumbel(dfMax.loc[dfMax.Position==p,'Entropy'].values.tolist(),mu,sigma)) #calcule p-value and add to distribution list
    dfDist = pd.DataFrame(distribution,columns=['dist']) #create DataFrame
    dfDist['positions'] = positions
    df =dfDist.nsmallest(10,'dist') #10 smallest p-value
    outliers = df['positions'].values.tolist()
    i = 0
    auxlen = len(outliers)
    pos = 'Positions of interest: ' #create string with every outlier
    while i < auxlen:
        if (i+1) == auxlen: #last position
            pos += str(outliers[i])
        else:
            pos += str(outliers[i]) + ', '
        i +=1



    dfHist = pd.DataFrame(subsample,columns=['Entropy'])
    dfAux = pd.DataFrame(subsample,columns=['Entropy'])
    axsub=dfHist['Entropy'].hist(bins=20,grid=False, xlabelsize=12, ylabelsize=12, density=True) #create histogram
    n, bins = get_hist(axsub) #get points from histogram


    plt.xlabel("Entropy ", fontsize=15)
    plt.ylabel("Frequency", fontsize=15)
    plt.xlim([0.0, 0.2])

    dfAux['Position']=subpos

    x=[]

    y=[]
    for point in bins: #x,y from gumble
        x.append(point)
        a=dgumbel(point,mu,sigma)
        y.append(a)
        #plt.plot(a,x,'bo')
        #aux=aux+sum



    plt.plot(x,y, 'r-', label='density gumbel', linewidth=1) #plot gumble
    name = pathPip+'src/plot_images/Gumbel'+'_'+strain+'_'+repetition + '.png'
    plt.savefig(name)
    plt.close()
    return pos #return positions of interest



