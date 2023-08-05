import matplotlib.pyplot as plt
import os


def plotEntropyPosition(position, dataFrame,strain,repetition,color = 'red'):
    pathPip = str(os.path.dirname(plt.__file__)).split('matplotlib')[0]
    passage=dataFrame.loc[dataFrame.Position==position,'Passage'] #get passage information for that position
    entropy=dataFrame.loc[dataFrame.Position==position,'Entropy'] #get entropy information for that position
    fig1, ax = plt.subplots()
    ax.plot(passage, entropy,color=color) #plot image
    #labels
    ax.set_xlabel('Passages')
    ax.set_ylabel('Entropy')
    ax.set_title("Entropy over passages for position "+str(position))
    plt.grid()
    name =pathPip+ 'src/plot_images/Entropy_' + str(position) +'_'+strain+'_'+repetition+ '.png'
    plt.savefig(name)
    plt.close()


def plotEntropiesPosition(position, dataFrames): #plot entropy * position for every experiment in PCA
    pathPip = str(os.path.dirname(plt.__file__)).split('matplotlib')[0]
    ffig1, ax = plt.subplots()
    for df in dataFrames: #every experiment
        strain = df.Strain.unique()[0]
        repetition = df.Repetition.unique()[0]
        passage=df.loc[df.Position==position,'Passage'] #get info
        entropy = df.loc[df.Position == position, 'Entropy'] #get info
        line,=ax.plot(passage, entropy)
        auxLabel = strain + '-' +str(repetition) #labels
        line.set_label(auxLabel)
        ax.legend()
    #labels
    ax.set_xlabel('Passages')
    ax.set_ylabel('Entropy')
    ax.set_title("Entropy over passages for position " + str(position))
    plt.grid()
    name = pathPip+'src/plot_images/Entropy_' + str(position) +'.png'
    plt.savefig(name)
    plt.close()

    
    
    
