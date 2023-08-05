import pandas as pd
import numpy as np

def Classify(data,centroids):
    '''Classfies datapoints based on a list of centroids'''
    # Data type checking
    if isinstance(data,pd.DataFrame):
        data = data.values
    if isinstance(centroids,pd.DataFrame):
        centroids = centroids.values
    return np.array([row.index(min(row)) for row in [[np.linalg.norm(item-cent) for cent in centroids] for item in data]])

def MyKmeans(data,iterations,centroids=3):
    '''Kmeans algorithm
    data is a data to cluster (nd-array)
    centroids is initial centroids to start with (nd-array)
    iterations is max number of iterations to run'''
    # Data type checking
    if isinstance(centroids,np.ndarray):
        centroids = pd.DataFrame(centroids)
    elif isinstance(centroids,pd.DataFrame):
        centroids = centroids.values.copy()
    elif isinstance(centroids,int) and isinstance(data,pd.DataFrame):
        centroids = data.sample(centroids).copy()
    elif isinstance(centroids,int) and isinstance(data,np.ndarray):
        centroids = pd.DataFrame(data).sample(centroids)

    if isinstance(data,pd.DataFrame):
        data = data.values

    previous = centroids.copy()
    temp = pd.DataFrame(data)
    for i in range(iterations):
        print(f"Iteration {i + 1}",end='\r')
        # Assignment
        classif = Classify(data,centroids)
        temp['c'] = classif

        # Update
        for j in range(len(centroids)):
            current = temp[temp['c'] == j].drop(columns='c')
            centroids.iloc[j] = current.mean().values
        if np.array_equal(centroids,previous):
            print(f"No points reclassified on iteration {i+1}")
            break
        else:
            previous = centroids.copy()
    return centroids


def KMeans_one_liner(data,centroids,iterations):
    '''Kmeans algorithm but in one line for some reason
       data is a data to cluster (nd-array)
       centroids is initial centroids to start with (nd-array)
       iterations is max number of iterations to run'''
    for iteration in range(iterations):
        centroids = [np.array([np.array([data[index] if np.array([row.index(min(row)) for row in [[np.linalg.norm(item-cent) for cent in centroids] for item in data]])[index] == i else ['r' for time in range(data[0].shape[0])] for index in range(len(data))])[np.array([data[index] if np.array([row.index(min(row)) for row in [[np.linalg.norm(item-cent) for cent in centroids] for item in data]])[index] == i else ['r' for time in range(data[0].shape[0])] for index in range(len(data))]) != ['r' for time in range(data[0].shape[0])]].reshape(int(len(np.array([data[index] if np.array([row.index(min(row)) for row in [[np.linalg.norm(item-cent) for cent in centroids] for item in data]])[index] == i else ['r' for time in range(data[0].shape[0])] for index in range(len(data))])[np.array([data[index] if np.array([row.index(min(row)) for row in [[np.linalg.norm(item-cent) for cent in centroids] for item in data]])[index] == i else ['r' for time in range(data[0].shape[0])] for index in range(len(data))]) != ['r' for time in range(data[0].shape[0])]]) / data[0].shape[0]),data[0].shape[0]).astype('float32')[:,col].mean() for col in range(data[0].shape[0])]) for i in range(len(centroids))]
    return centroids
