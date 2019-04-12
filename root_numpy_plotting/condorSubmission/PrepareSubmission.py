#First get the number of entries in each of the trees in inputs
from sys import path as sys_path
from os import path as os_path
Curr_DIR = os_path.expandvars('$EOPPlottingDir')
sys_path.insert(1, Curr_DIR)
import os
from inputs.samples import INPUT
from PlottingTools.Plotter import Plotter
from variables.variables import calc_weight
import ROOT
import pickle
import glob

import argparse
parser = argparse.ArgumentParser(description='Submit plotting batch jobs for the EoverPAnalysis plotting')
parser.add_argument('--treeName', '-tn', dest="treeName", type=str, required=True, help='the name of the tree to read from')
parser.add_argument('--NPartitions', '-np', dest="NPartitions", type=int, default='0', help='the number of plotting jobs to submit')
parser.add_argument('--jobName', '-jobName', dest="jobName", type=str, default='""', help='the name of the job to be submitted')

args = parser.parse_args()

#Create a pickle file and list for each submission
treeName = args.treeName
jobName = args.jobName
NPartitions = args.NPartitions

submission_list = []
EntriesPerFile = {}
tree_dict = {}

for key in INPUT:
    filenames = INPUT[key][1]
    for filename in filenames:
        print "Adding files in " + filename
        isFile = os.path.isfile(filename)
        tree = ROOT.TChain(treeName)
        if not isFile:
            if filename[-1] != "/":
                search_for = filename + "/*.root"
            else:
                search_for = filename + "*.root*"
            files =  glob.glob(search_for)
            files.sort()
            for f in files:
                if "eos" in f:
                     tfile = ROOT.TFile.Open("root://eosatlas/" + f, "READ")
                else:
                     tfile = ROOT.TFile.Open(f, "READ")
                print "Adding "+f
                tree.Add(f)
                tfile.Close()
        else:
            tree.Add("root://eosatlas/" + filename)

        EntriesPerFile[filename] = tree.GetEntries()
        f = tree.GetCurrentFile()
        tree.SetDirectory(0)
        f.Close()

        tree_dict[filename] = tree

def GeneratePartitions(Entries, NPartitions):
    return_list = []
    if Entries <= NPartitions * 10:
        raise ValueError("The number of events per partition is so small. What is the point?")
    step = int(Entries/NPartitions) - 10

    #print(step)
    count = 1
    for i in range(0, NPartitions):
        return_list.append( ( (i * step), (i+1) * step) )
        count += 1
    return_list.append((return_list[-1][1],Entries))

    if return_list[-1][0] > return_list[-1][1]:
        raise ValueError("The order of the last partition doesn't makse sense")

    #print(len(return_list))

    if len(return_list) != NPartitions + 1:
        raise ValueError("The number of partitions for this file was not NPartions = " + str(NPartitions))

    return return_list

def GenerateListOfPartitions(EntriesPerFile, NPartitions):
    return_list = []
    for i in range(0, NPartitions + 1):
        return_list.append({})

    for key in EntriesPerFile:
        partitions_for_file = GeneratePartitions(EntriesPerFile[key], NPartitions)
        for partition, dictionary in zip(partitions_for_file, return_list):
            dictionary[key] = partition

    return return_list

partitions = GenerateListOfPartitions(EntriesPerFile, NPartitions)
leading_script = file("condor_" + jobName + ".sub", "w")
cwd = os.getcwd()

#Create a plotter for each partition, and also a submission script:
#get the reweighting histograms
from variables.variables import calc_trkCount, calc_trkNPV2, calc_trkPt
trkCount_histogram_file = ROOT.TFile("reweightHistograms/TrkCountReweight_LoosePrimary_VertexAssociated.root", "READ")
trkCount_histogram = trkCount_histogram_file.Get("trkCountLowMuData")
calc_weight.addReweightHistogram("PythiaJetJet", calc_trkCount, trkCount_histogram)

#eventNPV2_histogram_file = ROOT.TFile("reweightHistograms/EventNPV2Reweight_LoosePrimary_VertexAssociated.root", "READ")
#eventNPV2_histogram = eventNPV2_histogram_file.Get("eventNPV2HistLowMuDatadividedeventNPV2HistLowMuData")
#calc_weight.addReweightHistogram("PythiaJetJet", calc_trkNPV2, eventNPV2_histogram)

trkPtReweight_file = ROOT.TFile("reweightHistograms/PTReweight.root", "READ")
trkPtReweight_histogram = trkPtReweight_file.Get("DataMCRatioPTSpectrium")
calc_weight.addReweightHistogram("PythiaJetJet", calc_trkPt, trkPtReweight_histogram)

#get the histograms used for detemining the bin sizes:
#histogramList = [\
#"LowMuData/TrkMultiplicityVsP_NonZeroE_InBin_20_24LowMuData",\
#"LowMuData/TrkMultiplicityVsP_NonZeroE_InBin_16_20LowMuData",\
#"LowMuData/TrkMultiplicityVsP_NonZeroE_InBin_12_16LowMuData",\
#"LowMuData/TrkMultiplicityVsP_NonZeroE_InBin_8_12LowMuData",\
#"LowMuData/TrkMultiplicityVsP_NonZeroE_InBin_4_8LowMuData",\
#"LowMuData/TrkMultiplicityVsP_NonZeroE_InBin_0_4LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_20_24LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_16_20LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_12_16LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_8_12LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_4_8LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_0_4LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_20_24LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_16_20LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_12_16LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_8_12LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_4_8LowMuData",\
#"LowMuData/TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_0_4LowMuData",\
#]
#
#f = ROOT.TFile("binningHistograms/binning.root", "READ")
#binningHistogramDictionary = {}
#for histogramNameInFile in histogramList:
#    hist = f.Get(histogramNameInFile)
#    histogramName = histogramNameInFile.replace("LowMuData/","").replace("LowMuData","")
#    binningHistogramDictionary[histogramName] = hist
#    hist.GetBinContent(1) #test that the histogram was retrieved 
#    hist.SetDirectory(0)
#f.Close()

leading_script.write("Universe = vanilla\n")
leading_script.write("Executable = condorSubmission/plot.sh\n")

#create the output directories for then job
if not os.path.exists(jobName):
    os.makedirs(jobName)
if not os.path.exists(jobName+"/Output"):
    os.makedirs(jobName+"/Output")
if not os.path.exists(jobName+"/Error"):
    os.makedirs(jobName+"/Error")
if not os.path.exists(jobName+"/Log"):
    os.makedirs(jobName+"/Log")
if not os.path.exists(jobName+"/Submission"):
    os.makedirs(jobName+"/Submission")
submission_pickle_file = jobName + "/Submission/" + jobName + ".pickle"

leading_script.write("Error = " +jobName + "/Error/job.$(Process)\n")
leading_script.write("Output = " +jobName + "/Output/job.$(Process)\n")
leading_script.write("Log = "+jobName+"/Log/job.$(Process)\n")
leading_script.write("+ProjectName='atlas-eopplotting'\n")
leading_script.write('+JobFlavour = "tomorrow"\n')
leading_script.write("should_transfer_files = YES\n")
leading_script.write("when_to_transfer_output = ON_Exit\n")
leading_script.write("transfer_output         = True\n")
leading_script.write("transfer_input_files    = CondorPythonLocal, variables, PlottingTools, selections, condorSubmission/submit.py ,calculation, FillingScript.py, " + submission_pickle_file + "\n")
leading_script.write("transfer_output_files   = " + jobName + "_$(Process).root\n")
leading_script.write("\n")

for i in range(0, len(partitions)):
    partition = partitions[i]
    plots = Plotter(INPUT, treeName, calc_weight, base_selections = "", partition_dictionary = partition)
    plots.tree_dict = tree_dict

#    for histogramName in binningHistogramDictionary:
#        plots.BookHistogramForBinning(binningHistogramDictionary[histogramName], histogramName)

    submission_list.append(plots)
    leading_script.write("Arguments = $(Process) "  +  submission_pickle_file.split("/")[-1] + " " + jobName + "\n")
    leading_script.write("Queue 1\n")
    leading_script.write("\n")

#create a pickle file for each submission
pickle.dump( submission_list, open(submission_pickle_file, "wb" ) )
