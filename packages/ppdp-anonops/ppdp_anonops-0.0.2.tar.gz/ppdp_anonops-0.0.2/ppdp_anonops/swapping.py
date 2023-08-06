from .anonymizationOperationInterface import AnonymizationOperationInterface
import collections
import random

# k-means
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import numbers


class Swapping(AnonymizationOperationInterface):
    def __init__(self):
        super(Swapping, self).__init__()

    def SwapEventAttributeValuesBykMeanCluster(self, xesLog, sensitiveAttribute, k_clusters):
        values = self._getEventAttributeValues(xesLog, sensitiveAttribute)

        self.__checkNumericAttributes(values)

        kmeans = self.__clusterizeData(values, k_clusters)

        valueClusterDict, clusteredValues = self.__getClusterHelpers(kmeans, values)

        # Choose random new value from clustered data
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(sensitiveAttribute in event.keys()):
                    # Get possible values from current values cluster
                    listOfValues = clusteredValues[valueClusterDict[event[sensitiveAttribute]]]

                    # Generate new random index
                    rnd = random.randint(0, len(listOfValues) - 1)

                    # Overwrite old attribute value with new one
                    event[sensitiveAttribute] = listOfValues[rnd]

        self.AddExtension(xesLog, 'swa', 'event', sensitiveAttribute)
        return xesLog

    def SwapCaseAttributeValuesBykMeanCluster(self, xesLog, sensitiveAttribute, k_clusters):
        values = self._getCaseAttributeValues(xesLog, sensitiveAttribute)

        self.__checkNumericAttributes(values)

        kmeans = self.__clusterizeData(values, k_clusters)

        valueClusterDict, clusteredValues = self.__getClusterHelpers(kmeans, values)

        # Choose random new value from clustered data
        for case_index, case in enumerate(xesLog):
            if(sensitiveAttribute in case.attributes.keys()):
                # Get possible values from current values cluster
                listOfValues = clusteredValues[valueClusterDict[case.attributes[sensitiveAttribute]]]

                # Generate new random index
                rnd = random.randint(0, len(listOfValues) - 1)

                # Overwrite old attribute value with new one
                case.attributes[sensitiveAttribute] = listOfValues[rnd]

        self.AddExtension(xesLog, 'swa', 'case', sensitiveAttribute)
        return xesLog

    # Make sure all values provided are actually numeric
    def __checkNumericAttributes(self, values):
        numCheck = [x for x in values if not isinstance(x, numbers.Number)]
        if(len(numCheck) > 0):
            raise NotImplementedError("Use a numeric attribute")
        pass

    def __clusterizeData(self, values, k_clusters):
        # initialize KMeans object specifying the number of desired clusters
        kmeans = KMeans(n_clusters=k_clusters)

        # reshape data to make them clusterable
        readyData = np.array(values).reshape(-1, 1)

        # learning the clustering from the input date
        kmeans.fit(readyData)

        return kmeans

    def __getClusterHelpers(self, kmeans, values):
        # Provides a cluster number for every key
        valueClusterDict = {}
        for i in range(len(kmeans.labels_)):
            if values[i] not in valueClusterDict:
                valueClusterDict[values[i]] = kmeans.labels_[i]

        clusterValues = {}
        for i in range(kmeans.n_clusters):
            clusterValues[i] = [x for x in valueClusterDict.keys() if valueClusterDict[x] == i]

        return valueClusterDict, clusterValues
