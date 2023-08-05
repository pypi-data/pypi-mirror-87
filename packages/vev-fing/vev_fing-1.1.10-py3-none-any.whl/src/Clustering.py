import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import numpy as np
    import pandas as pd
    import math
    import itertools
    import matplotlib.pyplot as plt
    from matplotlib import gridspec
    from tslearn.clustering import TimeSeriesKMeans
    from pyts.decomposition import SingularSpectrumAnalysis
    from tslearn.utils import to_time_series
    from sklearn.manifold import TSNE
    from src.Format_DF import totalExperimentsToPassages, formatStrains, experimentToPositions, totalExperimentsToPositions


def clustering(data,num_of_clus,metrica):
    """Function that returns the clustering
     Parameters:
     data: Array of data where each row is the entropy path at a position
     num_of_clus: Number of clusters
     metric: Metric to be used by TimeSeriesKMeans

     Returns array of size (quantity_of_ts,) and tslearn.clustering object
    """


    tslearn_time_series = to_time_series(data)

    km = TimeSeriesKMeans(n_clusters=num_of_clus, metric=metrica,random_state=0)
    labels_clus= km.fit_predict(tslearn_time_series)

    barycenters = km.cluster_centers_

    return labels_clus, barycenters

def listPositions(labels_clus, num_of_clus):
    """Function that returns a list with both objects and num_of_clus
     Parameters:
     labels_clus: The labels returned by the clustering method
     num_of_clas: Number of clusters

     Returns: List with as many objects as num_of_clus where each component is a list with the positions of each cluster
    """

    pos=labels_clus.size
    positions=[]

    for j in range(num_of_clus):
        aux=[]
        for i in range(pos):

            if labels_clus[i]==j: aux.append(i)

        positions.append(aux)

    return positions




def plotClustersCurves(data,pos, bary,nroCluster,directory):
    """Function that plots the trajectories of the entropies of arr, indicated in pos
     Parameters:
     data: Array of data where each row is the entropy path at a position
     pos: Positions to plot (labels returned by the tslearn.clustering object)
     bary: Center of gravity of the clusters
    """

    x=np.arange(data[0].size)

    total_fig = bary.shape[0]

    if total_fig >= 3:
        cols = 3
        rows = int(math.ceil(total_fig / cols))
    else:
        cols = 1
        rows = 2


    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure()

    for cent in range(bary.shape[0]):
        ax = fig.add_subplot(gs[cent])
        for p in pos[cent]:
                y=data[p,:]
                ax.plot(x, y, 'k', alpha=0.1)
        ax.plot(x, bary[cent], 'r', linewidth=2)

    fig.set_size_inches(10, 8)
    fig.tight_layout()
    plt.savefig(directory+'/Curves'+str(nroCluster))
    plt.close()


def plotClustersDimRed(data_DR,pos, bary,nroCluster,directory):
    """Function that plots in the 2D plane the positions according to the cluster to which they belong (indicated in pos)
     Parameters:
     data_DR: Array of data with the transformation components (PCA, tSNE, etc)
     pos: List with as many objects as the number of clusters with all positions belonging to the cluster (corresponds to positions returned by listPositions)
     bary: barycenters of the clusters (corresponds to barycenters returned by clustering. It is an array with a time series for each barycenter)
    """

    fig, ax = plt.subplots()
    i=0

    for cent in range(bary.shape[0]):

        x=data_DR[pos[cent],0]
        y=data_DR[pos[cent],1]
        i+=1
        ax.scatter(x, y, alpha=0.3)

    fig.set_size_inches(12, 10)
    plt.show()


def plotClustersCentDimRed(data_DR,pos, bary_DR,nroCluster,directory):
    """Function that plots in the plane of reduced dimension the positions according to the cluster to which they belong (indicated in pos)
     Parameters:
     data_DR: Array of data with the transformation components (PCA, tSNE, etc)
     pos: List with as many objects as the number of clusters with all positions belonging to the cluster (corresponds to positions returned by listPositions)
     bary: Center of gravity of the clusters
    """

    fig, ax = plt.subplots()
    i=0

    for cent in range(bary_DR.shape[0]):
        x=data_DR[pos[cent],0]
        y=data_DR[pos[cent],1]
        i+=1
        ax.scatter(x, y, alpha=0.3)
        ax.scatter(bary_DR[[cent],0],bary_DR[[cent],1], marker='x', c='k', s=60)


    fig.set_size_inches(12, 10)
    plt.show()



def getClustering(list_df_entropy, metrica, perp=3, lr=100):

    number_clusters=[2,4,6] #number of clusters to plot

    df_Aux=pd.DataFrame(columns=["tsne_1", "tsne_2", "2", "4", "6"]) #create data frame to save information

    array_data_Pos, array_Pos_Info, array_Pos_Strain=totalExperimentsToPositions(list_df_entropy)

    array_Data_Pos_TSNE = TSNE(perplexity=perp, learning_rate=lr, random_state=111).fit_transform(array_data_Pos) #t-SNE with every position

    df_Aux["tsne_1"]=array_Data_Pos_TSNE[:,0] #save in dataframe
    df_Aux["tsne_2"]=array_Data_Pos_TSNE[:,1]

    df_I = pd.DataFrame([sub.split(",") for sub in array_Pos_Info]) #split info column
    df_I.columns=["Strain", "Repetition", "Position"]  #create tree columns with this info

    pos_s = []
    bary_s = []

    for c in number_clusters:
        labels_clust, bary = clustering(array_data_Pos,c,metrica) #calls clustering
        list_posiciones = listPositions(labels_clust, c)
        pos_s.append(list_posiciones)
        bary_s.append(bary)
        df_Aux[str(c)] = labels_clust #add label in dataframe

    df_T = pd.concat([df_Aux, df_I], axis=1)



    return array_data_Pos, df_T, pos_s, bary_s

def getClusteringSSA(list_df_entropy, metrica, perp=3, lr=100, ssa_components=2):
    #same as function above usingin in this case SingularSpectrumAnalysis to transform array_data_Pos
    number_clusters=[2,4,6]

    df_Aux=pd.DataFrame(columns=["tsne_1", "tsne_2", "2", "4", "6"])

    #Format all data to obtain an array where each row is a time series for each position
    array_data_Pos, array_Pos_Info, array_Pos_Strain=totalExperimentsToPositions(list_df_entropy)

    #SSA descomposition to all time series
    transformer = SingularSpectrumAnalysis(window_size=ssa_components)
    array_data_Pos_SSA = transformer.transform(array_data_Pos)
    array_data_Pos_SSA_firstComp = array_data_Pos_SSA[:,0,:]


    array_data_Pos_SSA_TSNE = TSNE(perplexity=perp, learning_rate=lr, random_state=111).fit_transform(array_data_Pos_SSA_firstComp)

    df_Aux["tsne_1"]=array_data_Pos_SSA_TSNE[:,0]
    df_Aux["tsne_2"]=array_data_Pos_SSA_TSNE[:,1]

    df_I = pd.DataFrame([sub.split(",") for sub in array_Pos_Info])
    df_I.columns=["Strain", "Repetition", "Position"]

    pos_s = []
    bary_s = []

    for c in number_clusters:
        labels_clust, bary = clustering(array_data_Pos_SSA_firstComp,c,metrica)
        list_posiciones = listPositions(labels_clust, c)
        pos_s.append(list_posiciones)
        bary_s.append(bary)
        df_Aux[str(c)] = labels_clust

    df_T = pd.concat([df_Aux, df_I], axis=1)

    return array_data_Pos, df_T, pos_s, bary_s

def plot_confusion_matrix(cm,nroCluster,directory, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    tick_marks_x = np.arange(len(classes)-2)
    plt.xticks(tick_marks_x, classes[:-2], rotation=45)
    plt.yticks(tick_marks, classes)


    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('New cluster label')
    plt.xlabel('Old cluster label')
    plt.savefig(directory + '/confMatrix' + str(nroCluster) + '.png')
    plt.close()

