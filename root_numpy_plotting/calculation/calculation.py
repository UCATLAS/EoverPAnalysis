from pyximport import install

import numpy as np
install(setup_args={"include_dirs":np.get_include()},reload_support=True)
from util import getWeightsFromBins

class calculationDataMC:
    def __init__(self, function, list_of_branches):
        self.function = function
        self.name = function.__name__
        self.needsDataFlag = True
        self.branches = list_of_branches

    def eval(self, data, dataFlag):
        return self.function(data, dataFlag)

class calculation:
    def __init__(self, function, list_of_branches):
        self.function = function
        self.name = function.__name__
        self.needsDataFlag = False
        self.branches = list_of_branches

    def eval(self, data):
        return self.function(data)

def WeightsToNormalizeToHistogram(variable_in_histogram, histogram):
    '''normalize the weights to the histogram'''
    low_edges = []
    high_edges = []
    normalizations = []
    #get the low bin edges of the histograms
    for bin in range(1, histogram.GetNbinsX() + 1):
        low_edges.append(histogram.GetBinLowEdge(bin))
        high_edges.append(histogram.GetBinLowEdge(bin + 1))
        normalizations.append(histogram.GetBinContent(bin))

    low_edges = np.array(low_edges, np.float)
    high_edges = np.array(high_edges, np.float)
    hist_weights = np.array(normalizations, np.float)

    weights = getWeightsFromBins(variable_in_histogram, low_edges, high_edges, hist_weights)

    return weights

class weightCalculation:
    def __init__(self, function, list_of_branches):
        self.function = function
        self.name = function.__name__
        self.branches = list_of_branches
        self.reweightDictionary = {}

    def eval(self, data, isData, channel):
        weights = self.function(data, isData)
        if channel in self.reweightDictionary:
            for variable, histogram in zip(self.reweightDictionary[channel]["variables"], self.reweightDictionary[channel]["histograms"]):
                print("Reweighting variable " + variable.name + " in channel " + channel)
                extra_weight = WeightsToNormalizeToHistogram(variable.eval(data), histogram)
                weights *= extra_weight
        return weights

    def addReweightHistogram(self, channel, variable, histogram):
        histogram.SetDirectory(0)
        if channel not in self.reweightDictionary:
            self.reweightDictionary[channel] = {}
            self.reweightDictionary[channel]["variables"] = []
            self.reweightDictionary[channel]["histograms"] = []
            self.reweightDictionary[channel]["variables"].append(variable)
            self.reweightDictionary[channel]["histograms"].append(histogram)
            ##make sure that we always read the variable that we need for the histogram reweighting
            for branch_name in variable.branches:
                if branch_name not in self.branches:
                    self.branches.append(branch_name)
        else:
            self.reweightDictionary[channel]["variables"].append(variable)
            self.reweightDictionary[channel]["histograms"].append(histogram)
            ##make sure that we always read the variable that we need for the histogram reweighting
            for branch_name in variable.branches:
                if branch_name not in self.branches:
                    self.branches.append(branch_name)




