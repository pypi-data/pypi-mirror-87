import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter



def getEntropySurface(dataFrame,strain,repetition):
    pathPip = str(os.path.dirname(np.__file__)).split('numpy')[0]
    positions = np.array(dataFrame['Position'].astype(int))  # get positions
    passages = np.array(dataFrame['Passage'].astype(int))  # get passages
    entropy = np.array(dataFrame['Entropy'])  # get entropy

    cols = np.unique(positions).shape[0]  # get unique positions

    y = positions.reshape(-1, cols)  # reshape 1-D to dimension 2-D with passages,positions
    x = passages.reshape(-1, cols)  # reshape 1-D to dimension 2-D with passages,positions
    z = entropy.reshape(-1, cols)  # reshape 1-D to dimension 2-D with passages,positions

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.grid(True)

    surf = ax.contour3D(x, y, z, 100, cmap='twilight_shifted')  # plot surface

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)  # colorbar

    # labls
    ax.set_xlabel('Passages')
    ax.set_ylabel('Positions')
    ax.set_zlabel('Entropy')
    # save image
    name =pathPip+ 'src/plot_images/entropySurface_' +strain+'_' +repetition+ '.png'
    plt.savefig(name)
    plt.close()


