from ROOT import TFile, TH1D, TTree, TChain
from root_numpy import tree2array
import time
import os
import glob

#These are python JZW samples. I normalize to the number of generated events, the cross section and the filter efficiency
weight_dictionary = {\
"361020" : (1./(1000000.0)) * 78420000 * 0.9755,
"361021" : (1./(1000000.0)) * 78420000 * 0.00067143,
"361022" : (1./(999000.0)) *  2433200 * 0.00033423,
}

#particle_labels_dictionary = {\
#""#pi^+"

import os
import psutil
process = psutil.Process(os.getpid())

def branchDresser(branches):
    '''this is a function that dresses the branches to extend the branches'''
    return branches #No extension necessary

def getXSectionWeight(filename):
    weight = None
    for dsid in weight_dictionary:
        if dsid in filename:
            weight = weight_dictionary[dsid]

    if weight == None:
        raise ValueError("Can't find the dataset id in the weight file")
    return weight

def getIsData(filename):
    return "Data" in filename or "data" in filename

def GetData(partition = (0, 0), bare_branches = [], channel = "", filename = None, tree = None, treename = None, variables = [], weightCalculator = None, selections = [], selection_string = "",  verbose = False):
    '''a function used for multiprocessing. It makes all of the selections used by the analysis'''
    global process

    isData = getIsData(filename)
    for branch in weightCalculator.branches:
        if branch not in bare_branches:
            bare_branches.append(branch)
    branches = branchDresser(bare_branches)
    if verbose: print branches

    if verbose: print "Reading from file " + filename

    data = None
    for i in range(1, 50):
        try:
            data = tree2array(tree, branches, selection_string, start = partition[0], stop = partition[1])
        except Exception as e:
            print "Catching a failed attempt to retrieve data error. Trying agagin in 5 seconds"
            print e
            time.sleep(5) #try again in 5 seconds
        else:
            break

    if data == None:
        raise ValueError("Could not retrieve the data.")

    if verbose: print "Got the data for parition " + str(partition)

    # a dictionary of selections
    selection_dict = {}
    # a dictionary of variables = {}
    variable_dict = {}

    print("Evaluating weights")
    weights = weightCalculator.eval(data, isData, channel)

    if not isData:
        print("getting the xsection weight")
        xsec_weight = getXSectionWeight(filename)
        if verbose: print("X Section Weight Set To " + str(xsec_weight))
        weights = weights * xsec_weight

    ##calculate everything we need in one go!
    for variable in variables:
        if verbose: print("calculating variables for " + variable.name)
        variable_dict[variable.name] = variable.eval(data)

    #selection_dict is a dictionary of numpy arrays that have dimension # of events
    #each entry in the numpy array tells you if the event passed the selection
    for selection in selections:
        if verbose: print("calculating selection " + selection.name)
        if not selection.name in selection_dict:
            selection_dict[selection.name] = selection.eval(data)

    return_dict = {}
    return_dict["selection_dict"] = selection_dict
    return_dict["variable_dict"] = variable_dict
    return_dict["weights"] = weights
    f = tree.GetCurrentFile()
    tree.SetDirectory(0)
    f.Close()
    
    return return_dict
