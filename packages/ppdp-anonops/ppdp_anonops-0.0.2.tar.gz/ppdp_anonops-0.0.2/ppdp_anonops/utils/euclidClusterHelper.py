
from math import sqrt
import random
import numpy as np
import numbers

# As by some error some case attributes get safed in the first event of a trace -> Lift these up to become actual case attributes


def liftUniqueEventAttributesToCase(log, attributes):
    for attr in attributes:
        for case_index, case in enumerate(log):
            # Check whether the attribute is a unique event attribute (Only occuring once and in the first event)
            if(attr not in case.attributes.keys()):
                # Ensure the attribute exists, even if it is None
                case.attributes[attr] = None

                move = True
                for event_index, event in enumerate(case):
                    if ((event_index == 0 and attr not in event.keys()) or (event_index > 0 and attr in event.keys())):
                        move = False

                if(move):
                    case.attributes[attr] = case[0][attr]
    return log


def euclidDistCluster_Fit(values, k_clusters, weights, verboose=0):
    # Randomly select k cases to be the centroids of our clustering
    clusterCentroids = []
    try:
        for i in random.sample(range(0, len(values)), k_clusters):
            clusterCentroids.append(values[i])
    except ValueError:
        raise ValueError("Choose a suitable amount of clusters: k < " + str(len(values)))

    # When a selected attribute is not of a numeric type => One-Hot encode it
    oneHotEncodedDict = {}
    for i in range(len(values)):
        for j in range(len(values[i])):
            if not isinstance(values[i][j], numbers.Number) and j not in oneHotEncodedDict:
                oneHotEncodedDict[j] = {'Values': [], 'OneHotEncoded': [], 'OneHotNormalized': [], 'ValueToIndex': {}}

    for j in oneHotEncodedDict.keys():
        for i in range(len(values)):
            if values[i][j] not in oneHotEncodedDict[j]['Values']:
                oneHotEncodedDict[j]['Values'].append(values[i][j])
                oneHotEncodedDict[j]['ValueToIndex'][values[i][j]] = len(oneHotEncodedDict[j]['Values']) - 1

        for k in range(0, len(oneHotEncodedDict[j]['Values'])):
            # Create OneHot-Tuple
            t = [0, ]*len(oneHotEncodedDict[j]['Values'])
            t[k] = 1
            oneHotEncodedDict[j]['OneHotEncoded'].append(tuple(t))
            oneHotEncodedDict[j]['OneHotNormalized'].append(((k * 1.0) / len(oneHotEncodedDict[j]['Values'])))

    caseClusters = []
    for i in range(len(values)):
        val = [(oneHotEncodedDict[j]['OneHotNormalized'][oneHotEncodedDict[j]['ValueToIndex'][values[i][j]]] if j in oneHotEncodedDict.keys() else values[i][j]) for j in range(len(values[i]))]

        centroidDistance = []
        for centroid in clusterCentroids:
            centroidVals = [(oneHotEncodedDict[j]['OneHotNormalized'][oneHotEncodedDict[j]['ValueToIndex'][centroid[j]]] if j in oneHotEncodedDict.keys() else centroid[j]) for j in range(len(values[i]))]
            centroidDistance.append(euclidianDistance(weights, val, centroidVals))
        caseClusters.append(np.argmin(centroidDistance))

    return {"labels": caseClusters, "categories": [clusterCentroids[i][-1] for i in range(len(clusterCentroids))]}


def euclidianDistance(weights, attributesA, attributesB):
    if(len(weights) != len(attributesA) != len(attributesB)):
        raise NotImplementedError("This feature is only available for input arrays of identical length")

    sum = 0

    for i in range(len(weights)):
        sum += weights[i] * ((attributesA[i] - attributesB[i]) ** 2)

        #print(str(weights[i]) + " * " + "((" + str(attributesA[i]) + " - " + str(attributesB[i]) + ") ** 2)) = " + str(weights[i] * ((attributesA[i] - attributesB[i]) ** 2)))
    return sqrt(sum)
