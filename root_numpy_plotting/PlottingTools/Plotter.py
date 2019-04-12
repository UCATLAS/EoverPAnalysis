import numpy as np
from array import array
from root_numpy import fill_hist, fill_profile
import ROOT
from DataPrep import GetData
import imp

try:
    imp.find_module('atlasplots')
    foundAtlasPlots = True
    print "Found atlas plots module. Setting atlas style"
except ImportError:
    foundAtlasPlots = False
    print "Didn't find atlas plots module. Did NOT set atlas style. Continuing"

if foundAtlasPlots:
    from atlasplots import atlas_style as astyle
    astyle.SetAtlasStyle()

global_scope = []
CANVAS_COUNTER = 1

def GetBinsFromHistogram(hist, entriesPerBin):
    ''' Get bins with # of entries entriesPerBin inside of it'''
    bins = [] #a list of floats to store the bin edges of the new histograms
    bins.append(hist.GetBinLowEdge(1)) #append the bin edge of the lowest bin
    tracks = [] # list of the number of tracks in each bin
    runningCount = 0.0 #keep a running count of the number of tracks
    for binx in range(1,hist.GetNbinsX() + 1):
        runningCount += hist.GetBinContent(binx)
        if runningCount > entriesPerBin or binx == hist.GetNbinsX():
            bins.append(hist.GetBinLowEdge(binx) + hist.GetBinWidth(binx))
            tracks.append(runningCount)
            runningCount = 0.0

    return bins, tracks

def getLogBins(minBin, maxBin, nBins):
    '''Get nBins logarithmically-evenly spaced bins ranging from minBin to maxBin'''
    bins = []
    base = (float(maxBin)/float(minBin)) ** (1.0/float(nBins))
    for i in range(0, nBins+1):
        bins.append(minBin * (base) ** i)
    return bins

def getBins(minBin, maxBin, nBins):
    '''Get nBins evenly spaced bins ranging from minBin to maxBin'''
    bins = []
    step = float(maxBin - minBin)/float(nBins)
    for i in range(0, nBins+1):
        bins.append(minBin + (i*step))
    return bins

def getP(Pt, eta):
    '''Given a value of pT and eta, return the momentum'''
    return Pt*np.cosh(eta)

def toGlobalScope(obj):
    '''Keep TObjects alive at global scope'''
    global_scope.append(obj)

def Draw2DHistogramOnCanvas(TwoDHist, doLogx = False, doLogy = False, x_range = None, rebin=None, zlabel = None):
     '''Take a 2-D histogram and plot it on a canvas. Options for a logarithmic x and y axis are available.'''
     global CANVAS_COUNTER
     ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
     canvas_name = TwoDHist.GetName() + "_" + str(CANVAS_COUNTER)
     CANVAS_COUNTER += 1
     canvas = ROOT.TCanvas(canvas_name, canvas_name, 1300, 800)
     canvas.SetRightMargin(0.25)
     TwoDHist.Draw("colz")
     #TwoDHist.GetZaxis().SetTitleSize(0.035)
     TwoDHist.GetZaxis().SetTitleOffset(3.5)
     TwoDHist.GetXaxis().SetTitleOffset(1.0)
     TwoDHist.GetZaxis().SetTitleOffset(0.8)
     TwoDHist.GetYaxis().SetTitleOffset(1.0)
     if x_range:
         TwoDHist.GetXaxis().SetRangeUser(x_range[0], x_range[1])

     if doLogx:
         canvas.SetLogx()
     if doLogy:
         canvas.SetLogy()
     if rebin:
         TwoDHist.Rebin2D(rebin, rebin)
     if zlabel:
         TwoDHist.GetZaxis().SetTitle(zlabel)
     canvas.Draw()
     #TwoDHist.GetXaxis().SetRange(15, 300)
     canvas.Modified()
     canvas.Update()
     global_scope.append(canvas)
     return canvas

def DrawText(x, y, text, color=1, size=0.05):
    '''Draw text.

    Parameters
    ----------
    x : float
        x position in NDC coordinates
    y : float
        y position in NDC coordinates
    text : string, optional
        The text
    color : int, optional
        Text colour (the default is 1, i.e. black).
        See https://root.cern.ch/doc/master/classTColor.html.
        If you know the hex code, rgb values, etc., use ``ROOT.TColor.GetColor()``
    size : float, optional
        Text size
        See https://root.cern.ch/doc/master/classTLatex.html
    '''
    l = ROOT.TLatex()
    l.SetTextSize(size)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x, y, text)

def handle_underflow_overflow(h):
    '''
    add the underflow and overflow (underflow = 0, overflow=nbins+1)
    '''

    # underflow
    underflow = h.GetBinContent(0)
    first_bin = h.GetBinContent(1)
    h.SetBinContent(1, first_bin+underflow)
    h.SetBinContent(0, 0) # remove underflow
    # underflow error
    underflow_error = h.GetBinError(0)
    first_bin_error = h.GetBinError(1)
    h.SetBinError(1, (underflow_error**2 + first_bin_error**2)**0.5)

    # overflow
    last_bin = h.GetNbinsX()
    last_bin_content = h.GetBinContent(last_bin)
    overflow = h.GetBinContent(last_bin+1)
    h.SetBinContent(last_bin, last_bin_content+overflow)
    h.SetBinContent(last_bin+1, 0) # remove overflow
    # overflow error
    last_bin_error = h.GetBinError(last_bin)
    overflow_error = h.GetBinError(last_bin+1)
    h.SetBinError(last_bin, (last_bin_error**2 + overflow_error**2)**0.5)

    return h

def cleanUpHistograms(h):
    '''Create a histogram with it's characteristics set to standard values.'''
    h.SetLineStyle(1)
    h.SetLineWidth(3)
    h.SetFillStyle(0)
    h.SetFillColor(0)
    h.SetMarkerSize(0)
    return h

MCColor = ROOT.kRed
DataColor = ROOT.kBlack

def GetHistogramOfErrors(hist_dict):
    '''Given an input dictionary of histograms, return a dictionary of histograms with the bin content set to the error of the bin'''
    dict_keys = hist_dict.keys()

    for key in dict_keys:
        if key not in dict_keys:
            raise ValueError("The two dictionaries do not have the same keys")

    return_dict = {}
    for channel in dict_keys:
        Hist_clone = hist_dict[channel].Clone(hist_dict[channel].GetName() + "Errors")
        Hist_clone.GetXaxis().SetTitle(hist_dict[channel].GetXaxis().GetTitle())
        Hist_clone.GetYaxis().SetTitle(hist_dict[channel].GetYaxis().GetTitle())
        Hist_clone.Sumw2()
        for bin in range(0, Hist_clone.GetNbinsX() + 1):
            hist_clone.SetBinContent(bin, hist_dict[channel])
            hist_clone.SetBinError(bin, 0.0)

        return_dict[channel] = Hist_clone

    return return_dict

def ProjectProfiles(hist_dict):
    '''Get the X Projection of a TProfile histogram. This is useful for dividing TProfile histograms later'''
    for channel in hist_dict:
        hist_dict[channel] = hist_dict[channel].ProjectionX()
    return hist_dict

def DrawDataVsMC(histogram_dict, LegendLabels = {}, MCKey = "", DataKey = "", doLogy = True, doLogx = False, ratio_min= 0.0, ratio_max = 2.0, extra_description = None, extra_desx = 0.37, extra_desy = 0.87, scale_factor = 1000, xTicksNumber = None, yTicksNumber = 505, rebin=None, ylabel = None, xAxis_range = None):
    '''
    This function returns a canvas with a data and MC histogram drawn acoording to configurable settings.

    inputs
    -----------------------------------------------------------------------------------------------------
    histogram_dict: a dictionary of string channel name to TH1 or TProfile
    LegendLabels: a dictionary of string channel name to string description of channel to be used in the legend.
    MCKey: A string corresponding to the key for the MC histogram
    DataKey: a string correponding to the key for the data histogram
    doLogy: Bool. When true, the y axis is drawn with logarithmic scale
    doLogx: Bool. When true, the x axis is drawn with logarithmic scale
    ratio_min: the minimum value of the range of the y-axis in the data/MC ratio plot
    ratio_max: the maximum value of the range of the y-axis in the data/MC ratio plot
    extra_desction: list of strings corresponding to be drawn on the plot. These are used to describe what is being plotted.
    extra_desx: the x co-ordinate of the extra descriptions in NDC coordinates
    extra_desy: the y co-ordinate of the extra descriptions in NDC coordinates
    scale_dactor: the maximual value of the y-axis is set to scale_factor * (largest bin entry)
    xTicksNumber: change the number of ticks on the x-axis
    yTicksNumber: set the number of ticks on the y-axis
    -----------------------------------------------------------------------------------------------------
    '''
    title_offset = 1.2
    MCHist = histogram_dict[MCKey]
    DataHist = histogram_dict[DataKey]
    MCHist = cleanUpHistograms(MCHist)
    MCHist.SetLineColor(MCColor)
    DataHist.SetLineColor(DataColor)

    if rebin != None:
        MCHist.Rebin(rebin)
        DataHist.Rebin(rebin)

    if xAxis_range != None:
        #find the bin to use to set the range
        x_low = None
        x_high = None
        for bin in range(0, MCHist.GetNbinsX() + 1):
            cent = MCHist.GetBinCenter(bin)
            if cent >= xAxis_range[0] and x_low == None:
                x_low = bin
            elif cent > xAxis_range[1] and x_high == None:
                x_high = bin -1
        MCHist.GetXaxis().SetRange(x_low, x_high)
        DataHist.GetXaxis().SetRange(x_low, x_high)

    legend = ROOT.TLegend(0.60, 0.65, 0.92, 0.89)
    legend.SetBorderSize(0)
    toGlobalScope(legend)

    global CANVAS_COUNTER #This is to make sure that no two canvases ever get the same name. Otherwise root complains...
    canvas_name = "Canvas" + MCKey + DataKey + MCHist.GetTitle() + str(CANVAS_COUNTER)
    CANVAS_COUNTER = CANVAS_COUNTER + 1
    canvas = ROOT.TCanvas(canvas_name, canvas_name, 1300, 800)

    top_pad = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    top_pad.Draw()
    top_pad.cd()
    top_pad.SetBottomMargin(0)

    filename = MCHist.GetTitle() + "histogram"

    if (type(extra_description) == list and len(extra_description) > 3):
        scale_factor *= 10.0

    maximum_bin = 0.0
    minimum_bin = 10000000000000000.0
    for bin in range(1, MCHist.GetNbinsX() + 1):
        content = MCHist.GetBinContent(bin)
        if content > maximum_bin:
            maximum_bin = content
        if content < minimum_bin and content > 0.0:
            minimum_bin = content

    for bin in range(1, DataHist.GetNbinsX() + 1):
        content = DataHist.GetBinContent(bin)
        if content > maximum_bin:
            maximum_bin = content
        if content < minimum_bin and content > 0.0:
            minimum_bin = content

    if doLogy:
        filename += "logy"

    if doLogy:
        if minimum_bin <= 0.0:
            minimum_bin = 1
        MCHist.SetMaximum(maximum_bin * scale_factor)
        MCHist.SetMinimum(minimum_bin * 0.5)
        DataHist.SetMaximum(maximum_bin * scale_factor)
        DataHist.SetMinimum(minimum_bin * 0.5)

    else:
        MCHist.SetMaximum(maximum_bin * 1.5)
        MCHist.SetMinimum(minimum_bin * 0.5)
        DataHist.SetMaximum(maximum_bin * 1.5)
        DataHist.SetMinimum(minimum_bin * 0.5)

    MCHist.GetYaxis().SetTitleOffset(1.3)
    if ylabel:
        MCHist.GetYaxis().SetTitle(ylabel)
    MCHist.Draw("HIST")
    DataHist.Draw("SAME")

    legend.AddEntry(MCHist, LegendLabels[MCKey])
    legend.AddEntry(DataHist, LegendLabels[DataKey])
    legend.SetTextSize(0.04)
    legend.Draw()

    if extra_description:
        if not type(extra_description) == list:
            DrawText(extra_desx, extra_desy, extra_description)
        else:
            top = extra_desy
            for descr in extra_description:
                DrawText(extra_desx, top, descr)
                top -= 0.08

    if doLogy:
        top_pad.SetLogy()
    if doLogx:
        top_pad.SetLogx()

    ROOT.gROOT.SetStyle("ATLAS")
    #astyle.ATLASLabel(0.2, 0.87, "Internal")
    top_pad.Modified()
    top_pad.Update()
    toGlobalScope(top_pad)

    canvas.cd()
    bottom_pad = ROOT.TPad("pad2", "pad2", 0, 0.01, 1, 0.3)
    if doLogx:
        bottom_pad.SetLogx()
    #bottom_pad.SetRightMargin(0.15)
    bottom_pad.Draw()
    bottom_pad.cd()
    toGlobalScope(bottom_pad)

    data_ratio = DataHist.Clone("data_histogram")
    data_ratio.Divide(MCHist)
    data_ratio = cleanUpHistograms(data_ratio)
    data_ratio.SetLineColor(ROOT.kBlack)
    data_ratio.Draw("HIST E")

    MCHist_label_size = MCHist.GetXaxis().GetLabelSize()
    variableLabel = MCHist.GetXaxis().GetTitle()

    data_ratio.GetYaxis().SetNdivisions(yTicksNumber)

    data_ratio.GetYaxis().SetTitle("Data/MC")
    scale_ratio = (top_pad.GetWh()*top_pad.GetAbsHNDC())/(bottom_pad.GetWh() * bottom_pad.GetAbsHNDC())
    data_ratio.GetXaxis().SetLabelSize(MCHist_label_size*(scale_ratio))
    data_ratio.GetYaxis().SetLabelSize(MCHist_label_size*(scale_ratio))
    data_ratio.GetXaxis().SetTitle(variableLabel)
    data_ratio.GetXaxis().SetTitleOffset(1.2)
    data_ratio.SetMaximum(ratio_max - 0.0001)
    data_ratio.SetMinimum(ratio_min + 0.0001)
    data_ratio.GetXaxis().SetTitleSize(MCHist_label_size*scale_ratio)
    data_ratio.GetYaxis().SetTitleSize(MCHist_label_size*scale_ratio)
    data_ratio.GetYaxis().SetTitleOffset(title_offset/scale_ratio)
    data_ratio.SetMaximum(ratio_max - 0.0001)
    data_ratio.SetMinimum(ratio_min + 0.0001)
    data_ratio.Draw("HIST E")
    toGlobalScope(data_ratio)

    ##Draw a set of solid and dotted lines on the ratio plot to guide the reader's eyes
    straight_line = ROOT.TF1("line1", str(1.0) , -10e6, + 10e6)
    straight_line.SetLineWidth(2)
    straight_line.Draw("Same")
    toGlobalScope(straight_line)

    straight_line_up = ROOT.TF1("line2",  str(1.0 + (2.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_up.SetLineWidth(1)
    straight_line_up.SetLineStyle(1)
    straight_line_up.Draw("Same")
    toGlobalScope(straight_line_up)

    straight_line_up2 = ROOT.TF1("line3",  str(1.0 + (1.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_up2.SetLineWidth(1)
    straight_line_up2.SetLineStyle(3)
    straight_line_up2.Draw("Same")
    toGlobalScope(straight_line_up2)

    straight_line_up3 = ROOT.TF1("line4",  str(1.0 + (3.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_up3.SetLineWidth(1)
    straight_line_up3.SetLineStyle(3)
    straight_line_up3.Draw("Same")
    toGlobalScope(straight_line_up3)

    straight_line_down3 = ROOT.TF1("line5",  str(1.0 - (3.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_down3.SetLineWidth(1)
    straight_line_down3.SetLineStyle(3)
    straight_line_down3.Draw("Same")
    toGlobalScope(straight_line_down3)

    straight_line_down = ROOT.TF1("line6",  str(1.0 - (2.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_down.SetLineWidth(1)
    straight_line_down.SetLineStyle(1)
    straight_line_down.Draw("Same")
    toGlobalScope(straight_line_down)

    straight_line_down2 = ROOT.TF1("line7",  str(1.0 - (1.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_down2.SetLineWidth(1)
    straight_line_down2.SetLineStyle(3)
    straight_line_down2.Draw("Same")
    toGlobalScope(straight_line_down2)

    bottom_pad.Modified()
    bottom_pad.Update()

    bottom_pad.Draw()
    bottom_pad.cd()
    bottom_pad.SetTopMargin(0)
    bottom_pad.SetBottomMargin(0.45)

    if xTicksNumber != None:
        data_ratio.GetXaxis().SetNdivisions(xTicksNumber)

    bottom_pad.Modified()
    bottom_pad.Update()

    top_pad.Modified()
    top_pad.Update()

    canvas.SetRightMargin(0.15);
    canvas.Modified()
    canvas.Update()

    return canvas, top_pad, bottom_pad

def GetListOfNeededBranches(variables, selections):
    '''given a list of variables and selections, get all of the branches that should be read from the tree'''
    branches = []

    for variable in variables:
        for branch in variable.branches:
            if branch not in branches:
                branches.append(branch)

    for selection in selections:
        for branch in selection.branches:
            if branch not in branches:
                branches.append(branch)

    return branches

def DivideHistograms(hist_dict1, hist_dict2):
    '''take the histograms from two dictionaries hist_dict1 and hist_dict2, and divide them by matching keys. Return a dictionary with each key corresponding to the divided histogram.'''
    dict1_keys = hist_dict1.keys()
    dict2_keys = hist_dict2.keys()

    for key in dict1_keys:
        if key not in dict2_keys:
            raise ValueError("The two dictionaries do not have the same keys")
    for key in dict2_keys:
        if key not in dict1_keys:
            raise ValueError("The two dictionaries do not have the same keys")

    return_dict = {}
    for channel in dict1_keys:
        Hist_clone1 = hist_dict1[channel].Clone(hist_dict1[channel].GetName() + "divided" + hist_dict2[channel].GetName())
        Hist_clone1.GetXaxis().SetTitle(hist_dict1[channel].GetXaxis().GetTitle())
        Hist_clone1.GetYaxis().SetTitle(hist_dict1[channel].GetYaxis().GetTitle())
        Hist_clone1.Divide(hist_dict2[channel])
        return_dict[channel] = Hist_clone1

    return return_dict

def SubtractHistograms(hist_dict1, hist_dict2):
    '''take the histograms from two dictionaries hist_dict1 and hist_dict2, and divide them by matching keys. Return a dictionary with each key corresponding to the divided histogram.'''
    dict1_keys = hist_dict1.keys()
    dict2_keys = hist_dict2.keys()

    for key in dict1_keys:
        if key not in dict2_keys:
            raise ValueError("The two dictionaries do not have the same keys")
    for key in dict2_keys:
        if key not in dict1_keys:
            raise ValueError("The two dictionaries do not have the same keys")

    return_dict = {}
    for channel in dict1_keys:
        Hist_clone1 = hist_dict1[channel].Clone(hist_dict1[channel].GetName() + "subtracted" + hist_dict2[channel].GetName())
        Hist_clone1.GetXaxis().SetTitle(hist_dict1[channel].GetXaxis().GetTitle())
        Hist_clone1.GetYaxis().SetTitle(hist_dict1[channel].GetYaxis().GetTitle())
        Hist_clone1.Add(hist_dict2[channel], -1.0)
        return_dict[channel] = Hist_clone1

    return return_dict

def DivideTwoChannels(hist_dict, channel_numerator, channel_denomenator, new_zlabel = "", z_low = 0.0, z_high = 2.0):
    '''Given a dictionary string channel to TH1D or TProfile histogram, divide the histogram with key channel_numerator by the histogram with key channel denomenator'''
    hist_numerator = hist_dict[channel_numerator]
    hist_denomenator = hist_dict[channel_denomenator]

    Hist_clone = hist_numerator.Clone(hist_dict[channel_numerator].GetName() + "divided" + hist_dict[channel_numerator].GetName())

    Hist_clone.Divide(hist_denomenator)

    Hist_clone.SetMaximum(z_high)
    Hist_clone.SetMinimum(z_low)
    Hist_clone.GetXaxis().SetTitle(new_zlabel)

    return Hist_clone


class Plotter:
    '''
    '''
    def __init__(self, inputs, treeName, weightCalculator, base_selections = "", partition_dictionary = None):
        self.channelFiles = {}
        self.channelLabels = {}
        self.binningHistograms = {}
        self.AddInputDictionary(inputs)
        self.treeName = treeName
        self.partition_dictionary = partition_dictionary
        self.normalization_dictionary = {}
        self.test = False
        self.verbose = False
        self.total_selections = []
        self.total_variables =[]
        self.HistogramCallDictionary = {}
        self.base_selections = base_selections
        self.NormalizationWeightsDictionary = {} # A dictionary of channel to variable to the weights needed for the reweighting of this variable
        self.object_counter = 0
        self.weightCalculator = weightCalculator

    def BookHistogramForBinning(self, histogram, histogramName):
        '''This saves a histogram that can be used later to determine bin sizes. This could be a track multiplicity distribution, for example'''
        histogram.SetDirectory(0)
        self.binningHistograms[histogramName] = histogram
        toGlobalScope(histogram) #keep the histogram alive at the global scope

    def AddInputDictionary(self, dictionary):
        '''Take an input dictionary of channel names to: tuple of (channel descriptor for legend, list of [input root filename strings])'''
        self.channels = dictionary.keys()
        for channel in self.channels:
            self.channelFiles[channel] = dictionary[channel][1]
            self.channelLabels[channel] = dictionary[channel][0]

    def GetVariablesAndWeights(self, channel, filename, variables, list_selections):
        '''Given a string channel, string filename, a list of calculation variables and a list of calculations list_selections, return a dictionary keys selection_dict, variable_dict and weights. selection_dict is a dictionary of key selection name to numpy array of bool. variable_dict is a dictionary of string variable name to numpy array variable. weights is a numpy array of floats'''
        branches = GetListOfNeededBranches(variables, list_selections)

        #get the parition of the ttree to be read
        partition = None
        if self.partition_dictionary == None:
            partition = (0, total_entries)
        else:
            partition = self.partition_dictionary[filename]
            print("Found a partition")

        tree = self.tree_dict[filename]

        print("Getting data for partition " + str(partition))
        result = GetData(partition = partition, bare_branches = branches, channel = channel, filename = filename, tree = tree, treename = self.treeName, variables=variables, weightCalculator = self.weightCalculator, selections = list_selections, selection_string = self.base_selections, verbose = self.verbose)

        #Get the selections, variables and weights
        selection_dict = result["selection_dict"]
        variable_dict = result["variable_dict"]
        weights = result["weights"]

        print "The following selections have been evaluated "
        for selection in selection_dict:
            print selection
        print "The following variables have be evaluated " 
        for variable in variable_dict:
            print variable

        #prepare to loop through the selections and apply all of them
        #if self.verbose: print("\n\n\n\n\n===============\nPreselections are being applied")
        #if self.verbose: print("Pre-selection event count" + str(len(weights)))
        #total_selection = np.ones(len(weights)) > 0.0
        #for selection in list_selections:
        #    if self.verbose: print("applying selection " + str(selection.name))
            #if self.verbose: print(selection_dict[selection.name])
        #    total_selection &= selection_dict[selection.name]
            #cutflowsWeighted.Fill(selection_name, np.sum(weights[total_selection]))
            #cutflows.Fill(selection_name, np.sum(1*total_selection))
        #if self.verbose: print("post preselection event count" + str(np.sum(1*total_selection)))

        #Apply the selections to the variables and return them.
        #weights = weights[total_selection]
        #for variable in variable_dict:
        #    print "applying selection to variable " + variable
        #    variable_dict[variable] = variable_dict[variable][total_selection]

        return variable_dict, selection_dict, weights


    def GetHistograms(self, histogram_name, data_dictionary, variable, list_selections = [], bins = 1, range_low = 0.000001, range_high=1. - 0.00001,  xlabel ="", ylabel = "", HistogramPerFile=False, useWeights = True):
        '''Get the histogram for variable after list_selections is applied.'''

        variableNameToFill = variable.name
        variables = [variable]
        histogram_dictionary = {}
        if not HistogramPerFile:
            for channel in self.channels:
                if (type(bins) == list):
                    bins_array = array('d',bins)
                    histogram_dictionary[channel] = ROOT.TH1D(histogram_name + channel, histogram_name + channel, len(bins_array)-1, bins_array)
                else:
                    histogram_dictionary[channel] = ROOT.TH1D(histogram_name + channel, histogram_name + channel, bins, range_low + 0.0000001, range_high - 0.000001)
                histogram_dictionary[channel].GetXaxis().SetTitle(xlabel)
                histogram_dictionary[channel].GetYaxis().SetTitle(ylabel)
                histogram_dictionary[channel].Sumw2()

            for channel in self.channels:
                normalization_weight = 0.0
                for filename in self.channelFiles[channel]:
                    variable_dict, selection_dict, weights = data_dictionary[channel][filename]
                    total_selection = np.ones(len(weights)) > 0.0
                    for selection in list_selections:
                        total_selection &= selection_dict[selection.name]
                    to_fill = variable_dict[variableNameToFill][total_selection]
                    to_weight = weights[total_selection]
                    if self.verbose: print(len(to_fill))
                    if self.verbose: print(len(to_weight))
                    if self.verbose: print to_fill
                    if self.verbose: print to_weight
                    if self.verbose: print("Filling Variable " + variable.name)
                    if useWeights:
                        fill_hist(histogram_dictionary[channel], to_fill, to_weight)
                    else:
                        fill_hist(histogram_dictionary[channel], to_fill)

            return histogram_dictionary

    def Get2DHistograms(self, histogram_name, data_dictionary, variable_x, variable_y, list_selections = [], bins_x = 1, range_low_x = 0.000001, range_high_x=1. - 0.00001,  xlabel ="", bins_y=1, range_low_y=0.000001, range_high_y=1. - 0.00001, ylabel = "", zlabel="",):
        '''the 2-d histgram with variable_x and variable_y drawn'''
        variableNameToFill_x = variable_x.name
        variableNameToFill_y = variable_y.name
        variables = [variable_x, variable_y]
        histogram_dictionary = {}
        for channel in self.channels:
            if (type(bins_x) == list and type(bins_y) == list):
                bins_array_x = array('d',bins_x)
                bins_array_y = array('d',bins_y)
                histogram_dictionary[channel] = ROOT.TH2D(histogram_name + channel, histogram_name + channel, len(bins_array_x)-1, bins_array_x, len(bins_array_y)-1, bins_array_y)
            elif (type(bins_x) != list and type(bins_y) != list):
                histogram_dictionary[channel] = ROOT.TH2D(histogram_name + channel, histogram_name + channel, bins_x, range_low_x + 0.0000001, range_high_x - 0.000001, bins_y, range_low_y+0.0000001, range_high_y + 0.0000001)
            else:
                raise ValueError("both of the bins_x and bins_y variables need to be the same type. Both integers, or both lists")
            histogram_dictionary[channel].GetXaxis().SetTitle(xlabel)
            histogram_dictionary[channel].GetYaxis().SetTitle(ylabel)
            histogram_dictionary[channel].GetZaxis().SetTitle(zlabel)
            histogram_dictionary[channel].GetZaxis().SetTitleSize(0.035)
            histogram_dictionary[channel].GetZaxis().SetTitleOffset(1.35)
            histogram_dictionary[channel].Sumw2()

        for channel in self.channels:
            normalization_weight = 0.0
            for filename in self.channelFiles[channel]:
                variable_dict, selection_dict, weights = data_dictionary[channel][filename]
                total_selection = np.ones(len(weights)) > 0.0
                for selection in list_selections:
                    total_selection &= selection_dict[selection.name]
                to_weight = weights[total_selection]
                n_sel = len(to_weight)
                to_fill = np.zeros((n_sel,2))
                to_fill[:,0] = variable_dict[variableNameToFill_x][total_selection]
                to_fill[:,1] = variable_dict[variableNameToFill_y][total_selection]
                if self.verbose: print to_fill
                if self.verbose: print to_weight
                if self.verbose: print("Filling Variable " + variable.name)
                fill_hist(histogram_dictionary[channel], to_fill, to_weight)
        return histogram_dictionary


    def GetTProfileHistograms(self, histogram_name, data_dictionary, variable_x, variable_y, list_selections = [], bins = 1, range_low = 0.000001, range_high=1. - 0.00001,  xlabel ="", ylabel="",):
        '''Get a TProfile histogram with variable_y profiled against variable_x, after selections list_selections have been applied'''

        variableNameToFill_x = variable_x.name
        variableNameToFill_y = variable_y.name
        variables = [variable_x, variable_y]
        histogram_dictionary = {}
        for channel in self.channels:
            if (type(bins) == list):
                bins_array = array('d',bins)
                histogram_dictionary[channel] = ROOT.TProfile(histogram_name + channel, histogram_name + channel, len(bins_array)-1, bins_array)
            else:
                histogram_dictionary[channel] = ROOT.TProfile(histogram_name + channel, histogram_name + channel, bins, range_low + 0.0000001, range_high - 0.000001)
            histogram_dictionary[channel].Sumw2()

        for channel in self.channels:
            for filename in self.channelFiles[channel]:
                variable_dict, selection_dict, weights = data_dictionary[channel][filename]
                total_selection = np.ones(len(weights)) > 0.0
                for selection in list_selections:
                    total_selection &= selection_dict[selection.name]
                to_weight = weights[total_selection]
                n_sel = len(to_weight)
                to_fill = np.zeros((n_sel,2))
                to_fill[:,0] = variable_dict[variableNameToFill_x][total_selection]
                to_fill[:,1] = variable_dict[variableNameToFill_y][total_selection]
                if self.verbose: print to_fill
                if self.verbose: print to_weight
                if self.verbose: print("Filling Variable " + variable.name)
                print("Filling Histogram")
                fill_profile(histogram_dictionary[channel], to_fill, to_weight)
                print("Finished filling histogram")

            histogram_dictionary[channel].GetXaxis().SetTitle(xlabel)
            histogram_dictionary[channel].GetYaxis().SetTitle(ylabel)
        return histogram_dictionary

    def BookHistograms(self, histogram_name, variable, list_selections = [], bins = 1, range_low = 0.000001, range_high=1. - 0.00001,  xlabel ="", ylabel = "", HistogramPerFile=False, useWeights = True):
        if histogram_name not in self.HistogramCallDictionary:
            self.HistogramCallDictionary[histogram_name] = lambda data_dictionary : self.GetHistograms(histogram_name, data_dictionary, variable, list_selections = list_selections, bins = bins, range_low = range_low, range_high=range_high,  xlabel = xlabel, ylabel = ylabel, HistogramPerFile=HistogramPerFile, useWeights = useWeights)
        else:
            raise ValueError("histogram name already exists")
        for selection in list_selections:
            if selection.name not in [sel.name for sel in self.total_selections]:
                self.total_selections.append(selection)

        if variable.name not in [var.name for var in self.total_variables]:
            self.total_variables.append(variable)

    def Book2DHistograms(self, histogram_name, variable_x, variable_y, list_selections = [], bins_x = 1, range_low_x = 0.000001, range_high_x=1. - 0.00001,  xlabel ="", bins_y=1, range_low_y=0.000001, range_high_y=1. - 0.00001, ylabel = "", zlabel=""):
        if histogram_name not in self.HistogramCallDictionary:
            self.HistogramCallDictionary[histogram_name] = lambda data_dictionary : self.Get2DHistograms(histogram_name, data_dictionary, variable_x, variable_y, list_selections = list_selections, bins_x = bins_x, range_low_x =range_low_x, range_high_x=range_high_x,  xlabel =xlabel, bins_y=bins_y, range_low_y=range_low_y, range_high_y=range_high_y, ylabel = ylabel, zlabel=zlabel)
        else:
            raise ValueError("histogram name already exists")

        for selection in list_selections:
            if selection.name not in [sel.name for sel in self.total_selections]:
                self.total_selections.append(selection)

        if variable_x.name not in [var.name for var in self.total_variables]:
            self.total_variables.append(variable_x)

        if variable_y.name not in [var.name for var in self.total_variables]:
            self.total_variables.append(variable_y)

    def BookTProfileHistograms(self, histogram_name,  variable_x, variable_y, list_selections = [], bins = 1, range_low = 0.000001, range_high=1. - 0.00001,  xlabel ="", ylabel = ""):
        if histogram_name not in self.HistogramCallDictionary:
            self.HistogramCallDictionary[histogram_name] = lambda data_dictionary : self.GetTProfileHistograms(histogram_name, data_dictionary, variable_x, variable_y, list_selections = list_selections, bins = bins, range_low = range_low, range_high=range_high,  xlabel =xlabel, ylabel=ylabel)
        else:
            raise ValueError("histogram name already exists")

        for selection in list_selections:
            if selection.name not in [sel.name for sel in self.total_selections]:
                self.total_selections.append(selection)

        if variable_x.name not in [var.name for var in self.total_variables]:
            self.total_variables.append(variable_x)

        if variable_y.name not in [var.name for var in self.total_variables]:
            self.total_variables.append(variable_y)

    def DumpHistograms(self):
        data_dictionary = {}
        for channel in self.channels:
            data_dictionary[channel] = {}
            for filename in self.channelFiles[channel]:
                data_dictionary[channel][filename] = self.GetVariablesAndWeights(channel,filename, self.total_variables, self.total_selections)

        histogram_dictionary = {}
        for histogram_name in self.HistogramCallDictionary:
            histogram_dictionary[histogram_name] = self.HistogramCallDictionary[histogram_name](data_dictionary)

        return histogram_dictionary
