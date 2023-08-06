
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import hashlib
from cryptography.fernet import Fernet
from ppdp_anonops import Condensation, Swapping, Addition
import base64
from math import sqrt
from ppdp_anonops.utils import *
from sklearn.cluster import KMeans
import random
import numpy as np
from kmodes.kmodes import KModes
import numbers

from sklearn.preprocessing import OneHotEncoder

from ppdp_anonops.utils import euclidClusterHelper
from ppdp_anonops.utils.euclidClusterHelper import liftUniqueEventAttributesToCase


def main():
    c = Condensation()
    log = xes_importer.apply("resources/Sepsis Cases - Event Log.xes")
    xes_exporter.export_log(c.CondenseCaseAttributeByEuclidianDistance(log, "Age", ["concept:name", "Diagnose"], [0.1, 0.15, 0.75], 5), "tmpEuclid.xes")

    # log = c.CondenseEventAttributeBykModeCluster(log, "concept:name", ["org:group", "CRP", "LacticAcid"], 5)
    # xes_exporter.export_log(log, "tmp.xes")

    # kModes()

    # oneHot()

    log = xes_importer.apply("resources/Sepsis Cases - Event Log.xes")
    #euclidDistClusterCase(log, "Age", ["concept:name", "Diagnose"], 5, verboose=1)

    # Move Unique-Event-Attributes up to trace attributes
    attributes = ["concept:name", "Diagnose"]
    attributes.append("Age")
    log = euclidClusterHelper.liftUniqueEventAttributesToCase(log, attributes)

    values = []
    for case_index, case in enumerate(log):
        caseValues = []
        for attr in attributes:
            caseValues.append(case.attributes[attr])
        values.append(caseValues)

    cluster = euclidClusterHelper.euclidDistCluster_Fit(values, 5, [0.1, 0.15, 0.75])
    print(cluster["labels"])
    print(cluster["categories"])

    #log = xes_importer.apply("resources/running_example_caseAttributes.xes")
    #euclidDistClusterCase(log, "Age", ["Zip", "Salary", "concept:name"], 3, verboose=1)


def kModes():
    log = xes_importer.apply("resources/Sepsis Cases - Event Log.xes")
    vals = []
    for case_index, case in enumerate(log):
        for eIdx, e in enumerate(case):
            if((e["concept:name"], e["org:group"]) not in vals):
                vals.append((e["concept:name"], e["org:group"]))

    km = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)

    # clusters = km.fit_predict(np.array(vals).reshape(-1, 1))
    clusters = km.fit_predict(vals)

    # Print the cluster centroids
    print(km.cluster_centroids_)
    print(km.labels_)

    for i in range(len(vals)):
        print(str(km.cluster_centroids_[km.labels_[i]]) + " => " + str(vals[i]))


def oneHot():
    log = xes_importer.apply("resources/Sepsis Cases - Event Log.xes")
    attribute = "concept:name"
    # attribute = "org:group"

    vals = []
    for case_index, case in enumerate(log):
        for eIdx, e in enumerate(case):
            if(e[attribute] not in vals):
                vals.append(e[attribute])

    enc = OneHotEncoder(handle_unknown='ignore')
    vals = np.array(vals).reshape(-1, 1)
    enc.fit(vals)

    encDict = {}
    decDict = {}
    data = enc.transform(vals).toarray()
    cat = enc.categories_[0]
    for i in range(len(cat)):
        encDict[cat[i]] = data[i]
        # decDict[data[i]] = cat[i]

    print(encDict)
    print('###############')
    print(decDict)

    # initialize KMeans object specifying the number of desired clusters
    kmeans = KMeans(n_clusters=5)

    # reshape data to make them clusterable
    readyData = data  # np.array(data).reshape(-1, 1)

    # learning the clustering from the input date
    kmeans.fit(readyData)

    print(kmeans.labels_)
    print(vals.reshape(1, -1)[0])


def euclidDistClusterCase(log, sensitiveAttribute, descriptiveAttributes, k, verboose=0):
    # Move Unique-Event-Attributes up to trace attributes
    attributes = descriptiveAttributes
    attributes.append(sensitiveAttribute)
    log = liftUniqueEventAttributesToCase(log, attributes)

    # Randomly select k cases to be the centroids of our clustering
    clusterCentroids = []
    try:
        for i in random.sample(range(0, len(log)), k):
            clusterCentroids.append(log[i])
    except ValueError:
        raise ValueError("Choose a suitable amount of clusters: k < " + str(len(log)))

    # When a selected attribute is not of a numeric type => One-Hot encode it
    oneHotEncodedDict = {}
    for attr in attributes:
        for case_index, case in enumerate(log):
            if not isinstance(case.attributes[attr], numbers.Number) and attr not in oneHotEncodedDict:
                oneHotEncodedDict[attr] = {'Values': [], 'OneHotEncoded': [], 'OneHotSkalar': [], 'ValueToIndex': {}}
    for attr in oneHotEncodedDict.keys():
        for case_index, case in enumerate(log):
            if case.attributes[attr] not in oneHotEncodedDict[attr]['Values']:
                oneHotEncodedDict[attr]['Values'].append(case.attributes[attr])
                oneHotEncodedDict[attr]['ValueToIndex'][case.attributes[attr]] = len(oneHotEncodedDict[attr]['Values']) - 1
        for i in range(0, len(oneHotEncodedDict[attr]['Values'])):
            # Create OneHot-Tuple
            t = [0, ]*len(oneHotEncodedDict[attr]['Values'])
            t[i] = 1
            oneHotEncodedDict[attr]['OneHotEncoded'].append(tuple(t))
            #oneHotEncodedDict[attr]['OneHotSkalar'].append(2 * i)
            #oneHotEncodedDict[attr]['OneHotSkalar'].append((2 + i) * i)
            oneHotEncodedDict[attr]['OneHotSkalar'].append(1 + ((i * 1.0) / len(oneHotEncodedDict[attr]['Values'])))

    if(verboose == 1):
        print("######################### OneHot-Encoding #########################")
        print(oneHotEncodedDict.keys())
        print("###################################################################")

    caseClusters = []
    for case_index, case in enumerate(log):
        val = [(oneHotEncodedDict[i]['OneHotSkalar'][oneHotEncodedDict[i]['ValueToIndex'][case.attributes[i]]] if i in oneHotEncodedDict.keys() else case.attributes[i]) for i in attributes]

        centroidDistance = []
        for centroid in clusterCentroids:
            centroidVals = [(oneHotEncodedDict[i]['OneHotSkalar'][oneHotEncodedDict[i]['ValueToIndex'][centroid.attributes[i]]] if i in oneHotEncodedDict.keys() else centroid.attributes[i]) for i in attributes]
            centroidDistance.append(euclidianDistance([0.1, 0.1, 0.8], val, centroidVals))
        caseClusters.append(np.argmin(centroidDistance))

    if(verboose == 1):
        print("######################### Cluster of Case (Array-Index is Case-Index) #########################")
        print(caseClusters)
        print("###############################################################################################")


def euclidianDistance(weights, attributesA, attributesB):
    if(len(weights) != len(attributesA) != len(attributesB)):
        raise NotImplementedError("This feature is only available for input arrays of identical length")

    sum = 0

    for i in range(len(weights)):
        sum += weights[i] * ((attributesA[i] - attributesB[i]) ** 2)

        print(str(weights[i]) + " * " + "((" + str(attributesA[i]) + " - " + str(attributesB[i]) + ") ** 2)) = " + str(weights[i] * ((attributesA[i] - attributesB[i]) ** 2)))
    return sqrt(sum)


def getAttr(xes_log):
    case_attribs = []
    for case_index, case in enumerate(xes_log):
        for key in case.attributes.keys():
            if key not in case_attribs:
                case_attribs.append(key)
    event_attribs = []
    for case_index, case in enumerate(xes_log):
        for event_index, event in enumerate(case):
            for key in event.keys():
                if key not in event_attribs:
                    event_attribs.append(key)
    return case_attribs, event_attribs

# Identity (Case) Disclosure
# def calculateIdentityCaseDisclosure():


# Attribute (Trace) Disclosure
# def calculateAttributeTraceDisclosure():


# def calculateUtilityLoss():

def __getMode(self, valueList):
    if len(valueList) == 0:
        return 0

    s = {}
    for v in valueList:
        if v in s:
            s[v] += 1
        else:
            s[v] = 1

    # Sort dict by value
    s = {k: v for k, v in sorted(s.items(), key=lambda item: item[1])}
    return next(iter(s.keys()))


if __name__ == "__main__":
    main()
