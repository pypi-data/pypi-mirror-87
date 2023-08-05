import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import KMeans
import os

def ClusterImage(image,numClusters):
    '''image is the filepath to the image
       numClusters is how many centroids to have'''
    img = np.asarray(mpimg.imread(image))
    y_size, x_size, dim = img.shape
    newName = os.path.splitext(image)[0][os.path.splitext(image)[0].find('/') + 1:]

    flat = np.reshape(img.flatten(),(y_size * x_size, dim))

    KM = KMeans(n_clusters=numClusters,max_iter=50)
    KM.fit(flat)
    if dim == 4:
        new_img = [KM.cluster_centers_[x] for x in KM.predict(flat)]
    else:
        new_img = [KM.cluster_centers_[x].astype('int') for x in KM.predict(flat)]
    test = np.reshape(np.array(new_img),(y_size,x_size,dim))
    fig = plt.figure(figsize=(x_size/72,y_size/72),frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(test,aspect='auto')
    plt.savefig(f'{newName}_{numClusters}.png')


ClusterImage('./horse.jpg',3)
