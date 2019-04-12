from PlottingTools.HistogramManager import HistogramManager
import ROOT
from PlottingTools.Plotter import *
from array import array
import os
import time

#ROOT.gROOT.SetBatch(ROOT.kTRUE)

def CloseCanvas(canv):
    canv.Close()
    ROOT.gSystem.ProcessEvents()
    del canv

filename = "testing.root"

HM = HistogramManager(filename)
HM.listHistograms()

base_description = ["P_{T} Reweighted"]
#base_description = []
channelLabels = {"PythiaJetJet" : "Pythia8 MinBias and Dijet", "LowMuData": "2017 Low-<#mu> Data"}
plotter_directory = (filename.split("/")[-1]).replace(".root","") + "plots"

if not os.path.exists("Plots"):
    os.makedirs("Plots")

if not os.path.exists("Plots/" + plotter_directory):
    os.makedirs("Plots/" + plotter_directory)

plotter_directory = "Plots/" + plotter_directory

if False:
        eta_ranges = [(0.0, 0.4), (0.4, 0.8), (0.8, 1.2), (1.2, 1.6), (1.6, 2.0), (2.0, 2.4)]
        for histogramName in ["NClusters","NClusters_EM","NClusters_HAD","NClusters_emlike","NClusters_hadlike"]:
            hist = HM.getHistograms(histogramName)
            description = base_description + ["Inclusive Selection"]
            DataVsMC1 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    extra_description = description)
            DataVsMC1[0].Draw()
            DataVsMC1[0].Print(plotter_directory + "/" + histogramName + ".png")
            for eta_range in eta_ranges:
                histogram_name = histogramName
                histogram_name = histogram_name + "_NonZeroE_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
                hist = HM.getHistograms(histogram_name)
                description = base_description + ["E_{TOTAL} != 0"]
                DataVsMC1 = DrawDataVsMC(hist,\
                                        channelLabels,\
                                        MCKey='PythiaJetJet',\
                                        DataKey='LowMuData',\
                                        extra_description = description)
                DataVsMC1[0].Draw()
                DataVsMC1[0].Print(plotter_directory + "/" + histogram_name + "    .png")
                DataVsMC1[0].Close()



        histogramName = "TwoDTrackPtVsEtaHistogram_HasExtrapolation"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC = Draw2DHistogramOnCanvas(hist["LowMuData"], doLogx = False, doLogy = True)
        DataVsMC.Print(plotter_directory + "/LowMuData" + histogramName + ".png")
        DataVsMC.Close()

        histogramName = "TwoDTrackPtVsEtaHistogram_HasExtrapolation"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC = Draw2DHistogramOnCanvas(hist["PythiaJetJet"], doLogx = False, doLogy = True)
        DataVsMC.Print(plotter_directory + "/PythiaJetJet" + histogramName + ".png")
        DataVsMC.Close()

        histogramName = "TrkEtaPhiEMCal_MomentumBetween3And4GeV_Denomenator"
        hist = HM.getHistograms(histogramName)
        DataVsMC = Draw2DHistogramOnCanvas(hist["PythiaJetJet"], doLogx = False, doLogy = False, x_range = (-1.0, +1.0), zlabel = "N(E!=0)")
        DataVsMC.Print(plotter_directory + "/PythiaJetJet" + histogramName + ".png")
        DataVsMC.Draw()
        DataVsMC.Close()
        DataVsMC = Draw2DHistogramOnCanvas(hist["LowMuData"], doLogx = False, doLogy = False, x_range = (-1.0, +1.0), zlabel = "N(E!=0)")
        DataVsMC.Print(plotter_directory + "/LowMuData" + histogramName + ".png")
        DataVsMC.Draw()
        DataVsMC.Close()
        hist_den = hist

        histogramName = "TrkEtaPhiEMCal_MomentumBetween3And4GeV_Numerator"
        hist = HM.getHistograms(histogramName)
        DataVsMC = Draw2DHistogramOnCanvas(hist["PythiaJetJet"], doLogx = False, doLogy = False, x_range = (-1.0, +1.0), zlabel = "N(E!=0)")
        DataVsMC.Print(plotter_directory + "/PythiaJetJet" + histogramName + ".png")
        DataVsMC.Draw()
        DataVsMC.Close()
        DataVsMC = Draw2DHistogramOnCanvas(hist["LowMuData"], doLogx = False, doLogy = False, x_range = (-1.0, +1.0), zlabel = "N(E!=0)")
        DataVsMC.Print(plotter_directory + "/LowMuData" + histogramName + ".png")
        DataVsMC.Draw()
        DataVsMC.Close()
        hist_num = hist

        ratio = DivideHistograms(hist_num, hist_den)
        DataVsMC = Draw2DHistogramOnCanvas(ratio["PythiaJetJet"], doLogx = False, doLogy = False, x_range = (-1.0, +1.0), zlabel = "N(E!=0)/N(Inclusive)")
        DataVsMC.Draw()
        DataVsMC.Print(plotter_directory + "/PythiaJetJet" + "TrkEtaPhiEMCal_MomentumBetween3And4GeV_ZeroFraction" + ".png")
        DataVsMC.Close()

        DataVsMC = Draw2DHistogramOnCanvas(ratio["LowMuData"], doLogx = False, doLogy = False, x_range = (-1.0, +1.0), zlabel = "N(E!=0)/N(Inclusive)")
        DataVsMC.Draw()
        DataVsMC.Print(plotter_directory + "/LowMuData" + "TrkEtaPhiEMCal_MomentumBetween3And4GeV_ZeroFraction" + ".png")
        DataVsMC.Close()

        histogramName = "trkAverageMu"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC1 = DrawDataVsMC(hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                extra_description = description)
        DataVsMC1[0].Draw()
        DataVsMC1[0].Print(plotter_directory + "/" + histogramName + ".png")
        DataVsMC1[0].Close()


        histogramName = "trkCount"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC2 = DrawDataVsMC(hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                extra_description = description)
        DataVsMC2[0].Draw()
        DataVsMC2[0].Print(plotter_directory + "/" + histogramName + ".png")
        DataVsMC2[0].Close()

        histogramName = "trkNPV2"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC3 = DrawDataVsMC(hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                extra_description = description)
        DataVsMC3[0].Draw()
        DataVsMC3[0].Print(plotter_directory + "/" + histogramName + ".png")
        DataVsMC3[0].Close()

        histogramName =  "eventNPV2Hist"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC5 = DrawDataVsMC(hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                extra_description = description)
        DataVsMC5[0].Draw()
        DataVsMC5[0].Print(plotter_directory + "/" + histogramName + ".png")

        histogramName =  "eventAverageMu"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC6 = DrawDataVsMC(hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                extra_description = description)
        DataVsMC6[0].Draw()
        DataVsMC6[0].Print(plotter_directory + "/" + histogramName + ".png")

        histogramName =  "InclusiveEOP"
        hist = HM.getHistograms(histogramName)
        description = base_description + ["Inclusive Selection"]
        DataVsMC7 = DrawDataVsMC(hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                extra_description = description)
        DataVsMC7[0].Draw()
        DataVsMC7[0].Print(plotter_directory + "/" + histogramName + ".png")


        for extraString in ["", "HasExtrapolation"]:
            histogramName = "trkPtHist" + extraString
            hist = HM.getHistograms(histogramName)
            description = base_description + ["Inclusive Selection"]
            DataVsMC4 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    doLogx = True,\
                                    doLogy = True,\
                                    ratio_min = 0.8,\
                                    ratio_max = 1.2,\
                                    extra_description = description)
            DataVsMC4[0].Draw()
            DataVsMC4[0].Print(plotter_directory + "/" + histogramName + ".png")


            histogramName = "TrkPtHisteta06" + extraString
            hist = HM.getHistograms(histogramName)
            description = base_description + ["|#eta_{ID}|<0.6"]
            DataVsMC8 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    doLogx=True,
                                    ratio_min = 0.6,\
                                    ratio_max = 1.4,\
                                    extra_description = description)
            DataVsMC8[0].Draw()
            DataVsMC8[0].Print(plotter_directory + "/" + histogramName + ".png")

            histogramName = "TrkPtHisteta06_11" + extraString
            hist = HM.getHistograms(histogramName)
            description = base_description + ["0.6<|#eta_{ID}|<1.1"]
            DataVsMC8 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    doLogx=True,
                                    ratio_min = 0.6,\
                                    ratio_max = 1.4,\
                                    extra_description = description)
            DataVsMC8[0].Draw()
            DataVsMC8[0].Print(plotter_directory + "/" + histogramName + ".png")

            histogramName = "TrkPtHisteta11_14" + extraString
            hist = HM.getHistograms(histogramName)
            description = base_description + ["1.1<|#eta_{ID}|<1.4"]
            DataVsMC8 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    doLogx=True,
                                    ratio_min = 0.6,\
                                    ratio_max = 1.4,\
                                    extra_description = description)
            DataVsMC8[0].Draw()
            DataVsMC8[0].Print(plotter_directory + "/" + histogramName + ".png")

            histogramName = "TrkPtHisteta14_15" + extraString
            hist = HM.getHistograms(histogramName)
            description = base_description + ["1.4<|#eta_{ID}|<1.5"]
            DataVsMC8 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    doLogx=True,
                                    ratio_min = 0.6,\
                                    ratio_max = 1.4,\
                                    extra_description = description)
            DataVsMC8[0].Draw()
            DataVsMC8[0].Print(plotter_directory + "/" + histogramName + ".png")

            histogramName =  "TrkPtHisteta15_18" + extraString
            hist = HM.getHistograms(histogramName)
            description = base_description + ["1.5<|#eta_{ID}|<1.8"]
            DataVsMC9 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    doLogx=True,
                                    ratio_min = 0.6,\
                                    ratio_max = 1.4,\
                                    extra_description = description)
            DataVsMC9[0].Draw()
            DataVsMC9[0].Print(plotter_directory + "/" + histogramName + ".png")

            histogramName =  "TrkPtHisteta18_23" + extraString
            hist = HM.getHistograms(histogramName)
            description = base_description + ["1.8<|#eta_{ID}|<2.3"]
            DataVsMC9 = DrawDataVsMC(hist,\
                                    channelLabels,\
                                    MCKey='PythiaJetJet',\
                                    DataKey='LowMuData',\
                                    doLogx=True,
                                    ratio_min = 0.6,\
                                    ratio_max = 1.4,\
                                    extra_description = description)
            DataVsMC9[0].Draw()
            DataVsMC9[0].Print(plotter_directory + "/" + histogramName + ".png")

        histogramName_num =  "InclusiveZeroFractionVsPNumerator"
        hist_num = HM.getHistograms(histogramName_num)

        histogramName_den = "InclusiveZeroFractionVsPDenomenator"
        hist_den = HM.getHistograms(histogramName_den)
        ratio_hist = DivideHistograms(hist_num, hist_den)

        description = base_description + ["Inclusive Selection"]
        DataVsMC9 = DrawDataVsMC(ratio_hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                doLogx=True,
                                doLogy=False,
                                ratio_min = 0.8,\
                                ratio_max = 1.2,\
                                extra_description = description)
        DataVsMC9[0].Draw()
        DataVsMC9[0].Print(plotter_directory + "/" + histogramName_num.replace("Numerator", "") + ".png")
        description = base_description + ["0.2<|#eta_{ID}|<0.4"]
        histogramName_num =  "ZeroFractionVsPetaID02_04Numerator"
        hist_num = HM.getHistograms(histogramName_num)

        histogramName_den = "ZeroFractionVsPetaID02_04Denomenator"
        hist_den = HM.getHistograms(histogramName_den)
        ratio_hist = DivideHistograms(hist_num, hist_den)

        DataVsMC9 = DrawDataVsMC(ratio_hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                doLogx=True,
                                doLogy=False,
                                ratio_min = 0.6,\
                                ratio_max = 1.4,\
                                extra_description = description)
        DataVsMC9[0].Draw()
        DataVsMC9[0].Print(plotter_directory + "/" + histogramName_num.replace("Numerator", "") + ".png")

        description = base_description + ["0.0<|#eta_{ID}|<0.2"]
        histogramName_num =  "ZeroFractionVsPetaID00_02Numerator"
        hist_num = HM.getHistograms(histogramName_num)

        histogramName_den = "ZeroFractionVsPetaID00_02Denomenator"
        hist_den = HM.getHistograms(histogramName_den)
        ratio_hist = DivideHistograms(hist_num, hist_den)

        DataVsMC9 = DrawDataVsMC(ratio_hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                doLogx=True,
                                doLogy=False,
                                ratio_min = 0.6,\
                                ratio_max = 1.4,\
                                extra_description = description)
        DataVsMC9[0].Draw()
        DataVsMC9[0].Print(plotter_directory + "/" + histogramName_num.replace("Numerator", "") + ".png")

        description = base_description + ["0.4<|#eta_{ID}|<0.6"]
        histogramName_num =  "ZeroFractionVsPetaID04_06Numerator"
        hist_num = HM.getHistograms(histogramName_num)

        histogramName_den = "ZeroFractionVsPetaID04_06Denomenator"
        hist_den = HM.getHistograms(histogramName_den)
        ratio_hist = DivideHistograms(hist_num, hist_den)

        DataVsMC9 = DrawDataVsMC(ratio_hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                doLogx=True,
                                doLogy=False,
                                ratio_min = 0.6,\
                                ratio_max = 1.4,\
                                extra_description = description)
        DataVsMC9[0].Draw()
        DataVsMC9[0].Print(plotter_directory + "/" + histogramName_num.replace("Numerator", "") + ".png")

        histogramName = "EtaLess08_TwoDHistTrkPvsPhiInnerToExtrapolEM2"
        description = base_description + ["|#eta_{ID}|<0.8"]
        hist = HM.getHistograms(histogramName)
        DataVsMC10 = Draw2DHistogramOnCanvas(hist["PythiaJetJet"], doLogx = False, doLogy = True)
        DataVsMC10.Draw()
        DataVsMC10.Print(plotter_directory + "/" + histogramName.replace("Numerator", "") + "PythiaJetJet" + ".png")

        histogramName = "EtaLess08_TwoDHistTrkPvsPhiInnerToExtrapolEM2"
        description = base_description + ["|#eta_{ID}|<0.8"]
        hist = HM.getHistograms(histogramName)
        DataVsMC10 = Draw2DHistogramOnCanvas(hist["LowMuData"], doLogx = False, doLogy = True)
        DataVsMC10.Draw()
        DataVsMC10.Print(plotter_directory + "/" + histogramName.replace("Numerator", "") + "LowMuData" + ".png")

        histogramName = "EtaID0_6_PGreater2_0_EOPHist"
        hist = HM.getHistograms(histogramName)
        DataVsMC9 = DrawDataVsMC(hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                doLogx=True,
                                doLogy=False,
                                ratio_min = 0.6,\
                                ratio_max = 1.4,\
                                extra_description = description)
        DataVsMC9[0].Draw()
        DataVsMC9[0].Print(plotter_directory + "/" + histogramName_num.replace("Numerator", "") + ".png")


        description = base_description + ["0.0<|#eta_{ID}|<0.6"]
        histogramName_num =  "ZeroFractionVsPetaID00_06Numerator"
        hist_num = HM.getHistograms(histogramName_num)

        histogramName_den = "ZeroFractionVsPetaID00_06Denomenator"
        hist_den = HM.getHistograms(histogramName_den)
        ratio_hist = DivideHistograms(hist_num, hist_den)

        DataVsMC9 = DrawDataVsMC(ratio_hist,\
                                channelLabels,\
                                MCKey='PythiaJetJet',\
                                DataKey='LowMuData',\
                                doLogx=True,
                                doLogy=False,
                                ratio_min = 0.6,\
                                ratio_max = 1.4,\
                                extra_description = description)
        DataVsMC9[0].Draw()
        DataVsMC9[0].Print(plotter_directory + "/" + histogramName_num.replace("Numerator", "") + ".png")

        description = base_description + ["0.0<|#eta_{ID}|<0.4", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "EOPProfileVsMomentum_MIPSelection_HadFracAbove70_InBin_0_4"
        histograms = HM.getHistograms(histogramName)
        for key in histograms:
            histograms[key] = histograms[key].ProjectionX(histogramName + "_px", "E")

        DataVSMC10 = DrawDataVsMC(histograms,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.9,\
                                  ratio_max = 1.1,\
                                  extra_description = description)
        DataVSMC10[0].Draw()
        DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")

        description = base_description + ["0.4<|#eta_{ID}|<0.8", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "EOPProfileVsMomentum_MIPSelection_HadFracAbove70_InBin_4_8"
        histograms = HM.getHistograms(histogramName)
        for key in histograms:
            histograms[key] = histograms[key].ProjectionX(histogramName + "_px", "E")

        DataVSMC10 = DrawDataVsMC(histograms,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.9,\
                                  ratio_max = 1.1,\
                                  extra_description = description)
        DataVSMC10[0].Draw()
        DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")


        description = base_description + ["0.8<|#eta_{ID}|<1.2", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "EOPProfileVsMomentum_MIPSelection_HadFracAbove70_InBin_8_12"
        histograms = HM.getHistograms(histogramName)
        for key in histograms:
            histograms[key] = histograms[key].ProjectionX(histogramName + "_px", "E")

        DataVSMC10 = DrawDataVsMC(histograms,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.9,\
                                  ratio_max = 1.1,\
                                  extra_description = description)
        DataVSMC10[0].Draw()
        DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")


        description = base_description + ["1.2<|#eta_{ID}|<1.6", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "EOPProfileVsMomentum_MIPSelection_HadFracAbove70_InBin_12_16"
        histograms = HM.getHistograms(histogramName)
        for key in histograms:
            histograms[key] = histograms[key].ProjectionX(histogramName + "_px", "E")

        DataVSMC10 = DrawDataVsMC(histograms,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.9,\
                                  ratio_max = 1.1,\
                                  extra_description = description)
        DataVSMC10[0].Draw()
        DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")

        description = base_description + ["1.6<|#eta_{ID}|<2.0", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "EOPProfileVsMomentum_MIPSelection_HadFracAbove70_InBin_16_20"
        histograms = HM.getHistograms(histogramName)
        for key in histograms:
            histograms[key] = histograms[key].ProjectionX(histogramName + "_px", "E")

        DataVSMC10 = DrawDataVsMC(histograms,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.9,\
                                  ratio_max = 1.1,\
                                  extra_description = description)
        DataVSMC10[0].Draw()
        DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")

        description = base_description + ["2.0<|#eta_{ID}|<2.4", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "EOPProfileVsMomentum_MIPSelection_HadFracAbove70_InBin_20_24"
        histograms = HM.getHistograms(histogramName)
        for key in histograms:
            histograms[key] = histograms[key].ProjectionX(histogramName + "_px", "E")

        DataVSMC10 = DrawDataVsMC(histograms,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.9,\
                                  ratio_max = 1.1,\
                                  extra_description = description)
        DataVSMC10[0].Draw()
        DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")

        description = base_description + ["0.0<|#eta_{ID}|<0.4", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "2DHist_EOPVsMomentum_MIPSelection_HadFracAbove70_InBin_0_4"
        histograms = HM.getHistograms(histogramName)

        MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
        MCCanvas.Draw()
        MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

        DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
        DataCanvas.Draw()
        DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

        description = base_description + ["0.4<|#eta_{ID}|<0.8", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "2DHist_EOPVsMomentum_MIPSelection_HadFracAbove70_InBin_4_8"
        histograms = HM.getHistograms(histogramName)

        MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
        MCCanvas.Draw()
        MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

        DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
        DataCanvas.Draw()
        DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

        description = base_description + ["0.8<|#eta_{ID}|<1.2", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "2DHist_EOPVsMomentum_MIPSelection_HadFracAbove70_InBin_8_12"
        histograms = HM.getHistograms(histogramName)

        MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
        MCCanvas.Draw()
        MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

        DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
        DataCanvas.Draw()
        DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

        description = base_description + ["1.2<|#eta_{ID}|<1.6", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "2DHist_EOPVsMomentum_MIPSelection_HadFracAbove70_InBin_12_16"
        histograms = HM.getHistograms(histogramName)

        MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
        MCCanvas.Draw()
        MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

        DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
        DataCanvas.Draw()
        DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

        description = base_description + ["1.6<|#eta_{ID}|<2.0", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "2DHist_EOPVsMomentum_MIPSelection_HadFracAbove70_InBin_16_20"
        histograms = HM.getHistograms(histogramName)

        MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
        MCCanvas.Draw()
        MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

        DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
        DataCanvas.Draw()
        DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

        description = base_description + ["2.0<|#eta_{ID}|<2.4", "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "MIP Selection"]
        histogramName = "2DHist_EOPVsMomentum_MIPSelection_HadFracAbove70_InBin_20_24"
        histograms = HM.getHistograms(histogramName)

        MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
        MCCanvas.Draw()
        MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

        DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
        DataCanvas.Draw()
        DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

        #histogramNames = ["TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_0_4" , "TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_12_16", "TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_16_20", "TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_20_24", "TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_4_8", "TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_8_12"]
        #
        eta_descriptors = ["0.0<|#eta_{ID}|<0.4", "0.4<|#eta_{ID}|<0.8", "0.8<|#eta_{ID}|<1.2", "1.2<|#eta_{ID}|<1.6", "1.6<|#eta_{ID}|<2.0", "2.0<|#eta_{ID}|<2.4"]
        #
        #for histogramName, descriptor in zip(histogramNames, eta_descriptors):
        #    description = base_description + [descriptor, "#frac{E_{HAD}}{E_{TOTAL}} > 0.7", "E^{dR<0.1}_{EM} < 1.1 GeV"]
        #    histograms = HM.getHistograms(histogramName)
        #
        #    for key in histograms:
        #        histograms[key].Rebin(20)
        #
        #    DataVSMC10 = DrawDataVsMC(histograms,\
        #                          channelLabels,\
        #                          MCKey = "PythiaJetJet",\
        #                          DataKey = "LowMuData",\
        #                          doLogx = True,\
        #                          doLogy = False,
        #                          ratio_min = 0.6,\
        #                          ratio_max = 1.4,\
        #                          extra_description = description)
        #    DataVSMC10.Draw()
        #    DataVSMC10.Print(plotter_directory + "/" + histogramName + ".png")
        eta_ranges = [(0.0, 0.4), (0.4, 0.8), (0.8, 1.2), (1.2, 1.6), (1.6, 2.0), (2.0, 2.4)]
        profileNames = ["EOPProfileVsMomentum", "EOPProfileVsMomentum_MIPSelection_HadBetween30And90OfMomentum", "EOPProfileVsMomentum_MIPSelection_HadFracAbove70", "EOPProfileVsMomentum_NonZeroE"]
        bkgProfileNames = ["EnergyBkgProfileVsMomentum", "EnergyBkgProfileVsMomentum_MIPSelection_HadBetween30And90OfMomentum", "EnergyBkgProfileVsMomentum_MIPSelection_HadFracAbove70", "EnergyBkgProfileVsMomentum_NonZeroE"]
        TwoDHistNames = ["2DHist_EOPVsMomentum", "2DHist_EOPVsMomentum_MIPSelection_HadBetween30And90OfMomentum", "2DHist_EOPVsMomentum_MIPSelection_HadFracAbove70", "2DHist_EOPVsMomentum_NonZeroE"]
        #bkgTwoDHistNames = ["2DHist_EOPBkgVsMomentum", "2DHist_EOPBkgVsMomentum_MIPSelection_HadBetween30And90OfMomentum", "2DHist_EOPBkgVsMomentum_MIPSelection_HadFracAbove70", "2DHist_EOPBkgVsMomentum_NonZeroE"]
        plotDescriptors = [ [], ["0.3 P < E_{HAD} < 0.9 P", "E^{dR<0.1}_{EM} < 1.1 GeV", "N_{TRT} >= 20"], ["E_{HAD}/E_{TOTAL} > 0.7", "E^{dR<0.1}_{EM} < 1.1 GeV", "N_{TRT} >= 20"], ["E_{TOTAL} != 0.0"]]

        for eta_range, eta_descriptor in zip(eta_ranges, eta_descriptors):
            print eta_range
            print eta_descriptor
#TrkMultiplicityVsP_InBin_12_16
#TrkMultiplicityVsP_InBin_16_20
#TrkMultiplicityVsP_InBin_20_24
#TrkMultiplicityVsP_InBin_4_8
#TrkMultiplicityVsP_InBin_8_12
#TrkMultiplicityVsP_Inclusive_InBin_0_4
#TrkMultiplicityVsP_Inclusive_InBin_12_16
#TrkMultiplicityVsP_Inclusive_InBin_16_20
#TrkMultiplicityVsP_Inclusive_InBin_20_24
#TrkMultiplicityVsP_Inclusive_InBin_4_8
#TrkMultiplicityVsP_Inclusive_InBin_8_12
#TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_0_4
#TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_12_16
#TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_16_20
#TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_20_24
#TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_4_8
#TrkMultiplicityVsP_MIPSelection_HadBetween30And90OfMomentum_InBin_8_12
#TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_0_4
#TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_12_16
#TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_16_20
#TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_20_24
#TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_4_8
#TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_8_12
#TrkMultiplicityVsP_NonZeroE_20TRT_InBin_0_4
#TrkMultiplicityVsP_NonZeroE_20TRT_InBin_12_16
#TrkMultiplicityVsP_NonZeroE_20TRT_InBin_16_20
#TrkMultiplicityVsP_NonZeroE_20TRT_InBin_20_24
#TrkMultiplicityVsP_NonZeroE_20TRT_InBin_4_8
#TrkMultiplicityVsP_NonZeroE_20TRT_InBin_8_12
#TrkMultiplicityVsP_NonZeroE_InBin_0_4
#TrkMultiplicityVsP_NonZeroE_InBin_12_16
#TrkMultiplicityVsP_NonZeroE_InBin_16_20
#TrkMultiplicityVsP_NonZeroE_InBin_20_24
#TrkMultiplicityVsP_NonZeroE_InBin_4_8
#TrkMultiplicityVsP_NonZeroE_InBin_8_12
            histogramName = "TrkMultiplicityVsP_NonZeroE" + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
            hist_NonZero = HM.getHistograms(histogramName, rebin = 100)
            histogramName = "TrkMultiplicityVsP" + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
            hist_Inclusive = HM.getHistograms(histogramName, rebin = 100)
            histogramName = "TrkMultiplicityVsP_MIPSelection_HadFracAbove70" + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1])) 
            hist_HadFracAbove70 = HM.getHistograms(histogramName, rebin = 100)

            frac_MIP_of_NonZero = DivideHistograms(hist_HadFracAbove70, hist_NonZero)
            frac_MIP_of_Inclusive = DivideHistograms(hist_HadFracAbove70, hist_Inclusive)

            DataVSMC10 = DrawDataVsMC(frac_MIP_of_NonZero,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.2,\
                                  ratio_max = 1.8,\
                                  ylabel="N(MIP)/N(E!=0)",\
                                  extra_description = base_description  + [eta_descriptor])
            DataVSMC10[0].Draw()
            DataVSMC10[0].Print(plotter_directory + "/" + "FracNonZero_MIP_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1])) + ".png")
            DataVSMC10[0].Close()

            DataVSMC10 = DrawDataVsMC(frac_MIP_of_Inclusive,\
                                  channelLabels,\
                                  MCKey = "PythiaJetJet",\
                                  DataKey = "LowMuData",\
                                  doLogx = True,\
                                  doLogy = False,
                                  ratio_min = 0.6,\
                                  ratio_max = 1.4,\
                                  ylabel="N(MIP)/N(Inclusive)",\
                                  extra_description = base_description +  [eta_descriptor])
            DataVSMC10[0].Draw()
            DataVSMC10[0].Print(plotter_directory + "/" + "FracInclusive_MIP_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1])) + ".png")
            DataVSMC10[0].Close()




            for bkgProfileName, profileName, TwoDHistName, plotDescriptor in zip(bkgProfileNames, profileNames, TwoDHistNames, plotDescriptors):
                description = ["P_{T} Reweighted", eta_descriptor] + plotDescriptor

                histogramName = profileName + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
                histograms = HM.getHistograms(histogramName)
                histograms = ProjectProfiles(histograms)
                histogram_num = histograms
                DataVSMC10 = DrawDataVsMC(histograms,\
                                      channelLabels,\
                                      MCKey = "PythiaJetJet",\
                                      DataKey = "LowMuData",\
                                      doLogx = True,\
                                      doLogy = False,
                                      ratio_min = 0.5,\
                                      ratio_max = 1.5,\
                                      extra_description = description)
                DataVSMC10[0].Draw()
                DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")
                DataVSMC10[0].Close()

                histogramName = bkgProfileName + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
                histograms = HM.getHistograms(histogramName)
                histograms = ProjectProfiles(histograms)
                histogram_den = histograms
                DataVSMC10 = DrawDataVsMC(histograms,\
                                      channelLabels,\
                                      MCKey = "PythiaJetJet",\
                                      DataKey = "LowMuData",\
                                      doLogx = True,\
                                      doLogy = False,
                                      ratio_min = 0.5,\
                                      ratio_max = 1.5,\
                                      extra_description = description)
                DataVSMC10[0].Draw()
                DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")
                DataVSMC10[0].Close()

                EOPCorrHistograms = SubtractHistograms(histogram_num, histogram_den)
                histogramName = "EOPCorrHistogram_" + bkgProfileName + "_"  + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
                DataVSMC10 = DrawDataVsMC(EOPCorrHistograms,\
                                      channelLabels,\
                                      MCKey = "PythiaJetJet",\
                                      DataKey = "LowMuData",\
                                      doLogx = True,\
                                      doLogy = False,\
                                      ylabel = "<E/p>_{Corr}",\
                                      ratio_min = 0.95,\
                                      ratio_max = 1.05,\
                                      extra_description = description)
                DataVSMC10[0].Draw()
                DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")
                DataVSMC10[0].Close()

                histogramName = TwoDHistName + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
                histograms = HM.getHistograms(histogramName)

                DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
                DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

                MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
                MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

            histogram_name =  "TrkMultiplicityVsP_NonZeroE_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
            histograms = HM.getHistograms(histogram_name)
            DataVsMC = DrawDataVsMC(histograms,\
                                    channelLabels,\
                                    MCKey="PythiaJetJet",\
                                    DataKey="LowMuData",\
                                    ratio_min=0.6,\
                                    ratio_max=1.4,\
                                    rebin=100,\
                                    extra_description = ["P_{T} Reweighted", "E_{Total} != 0.0", eta_descriptor])
            DataVsMC[0].Draw()
            DataVsMC[0].Print(plotter_directory + "/" + histogram_name + ".png")
            DataVsMC[0].Close()
        #plot the average energy in the anulus
        profileNames = ["EnergyAnulusProfileVsMomentum_MIPSelection_HadBetween30And90OfMomentum", "EnergyAnulusProfileVsMomentum_MIPSelection_HadFracAbove70"]
        TwoDHistNames = ["2DHist_EnergyAnulusVsMomentum_MIPSelection_HadBetween30And90OfMomentum", "2DHist_EnergyAnulusVsMomentum_MIPSelection_HadFracAbove70"]
        profileDescriptors = [ ["0.3 P < E_{HAD} < 0.9 P", "E^{dR<0.1}_{EM} < 1.1 GeV", "N_{TRT} >= 20"], ["E_{HAD}/E_{TOTAL} > 0.7", "E^{dR<0.1}_{EM} < 1.1 GeV", "N_{TRT} >= 20"], ["E_{TOTAL} != 0.0"] ]

        for eta_range, eta_descriptor in zip(eta_ranges, eta_descriptors):
            eta = eta_range[1]
            p_bins_max = 15.05
            p_bins_min = getP(0.5, eta)
            nBins = 20
            p_bins = getLogBins(p_bins_min, p_bins_max, nBins)
            for profileName, TwoDHistName, profileDescriptor in zip(profileNames, TwoDHistNames,  profileDescriptors):
                description = ["P_{T} Reweighted", eta_descriptor] + profileDescriptor

                histogramName = profileName + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
                histograms = HM.getHistograms(histogramName)
                histograms = ProjectProfiles(histograms)
                DataVSMC10 = DrawDataVsMC(histograms,\
                                      channelLabels,\
                                      MCKey = "PythiaJetJet",\
                                      DataKey = "LowMuData",\
                                      doLogx = True,\
                                      doLogy = False,
                                      ratio_min = 0.4,\
                                      ratio_max = 1.6,\
                                      extra_description = description)
                DataVSMC10[0].Draw()
                DataVSMC10[0].Print(plotter_directory + "/" + histogramName + ".png")
                DataVSMC10[0].Close()

                histogramName = TwoDHistName + "_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
                histograms = HM.getHistograms(histogramName)
                DataCanvas = Draw2DHistogramOnCanvas(histograms["LowMuData"], doLogx = True, doLogy = False)
                DataCanvas.Print(plotter_directory + "/" + histogramName + "LowMuData.png")

                MCCanvas = Draw2DHistogramOnCanvas(histograms["PythiaJetJet"], doLogx = True, doLogy = False)
                MCCanvas.Print(plotter_directory + "/" + histogramName + "PythiaJetJet.png")

                p_ranges = [ (p_bins[i], p_bins[i+1])  for i in range(0, len(p_bins)-1) ]
                for p_range in p_ranges:
                    histogramNames = ["trkEMDR100", "MomentumHadFrac", "HadFrac", "trkTRTHits"]
                    p_high_str = "{:.2f}".format(p_range[1])
                    p_low_str= "{:.2f}".format(p_range[0])
                    for selection_type in ["_NonZeroE_20TRT_InEtaBin_", "_NonZeroE_InEtaBin_", "_MIPSelection_HadFracAbove70_InEtaBin_"]:
                        if "_NonZeroE_20TRT_InEtaBin_" == selection_type:
                            extra_stuff = ["E_{TOTAL} != 0", "N_{TRT Hits} >= 20"]
                        elif "_MIPSelection_HadFracAbove70_InEtaBin_" == selection_type:
                            extra_stuff = ["MIP Seleciton"]
                        else:
                            extra_stuff = ["E_{TOTAL} !=0"]
                        for histogramName in histogramNames:
                            if selection_type == "_MIPSelection_HadFracAbove70_":
                                break
                            histogramName = histogramName + selection_type + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1])) + "_InPBin_" + str(int(100*p_range[0])) + "_" + str(int(100*p_range[1]))
                            histograms = HM.getHistograms(histogramName)
                            DataVSMC = DrawDataVsMC(histograms,\
                                           channelLabels,\
                                           MCKey = "PythiaJetJet",\
                                           DataKey = "LowMuData",\
                                           doLogx = False,\
                                           doLogy = False,
                                           ratio_min = 0.4,\
                                           ratio_max = 1.6,\
                                           extra_description = ["P_{T} Reweighted", eta_descriptor, p_low_str + " < |P/GeV| < " + p_high_str] + extra_stuff)
                            DataVSMC[0].Draw()
                            DataVSMC[0].Print(plotter_directory + "/" + histogramName + ".png")
                            DataVSMC[0].Close()

                        for histogramName in ["NClusters","NClusters_EM","NClusters_HAD","NClusters_emlike","NClusters_hadlike"]:
                            histogram_name = histogramName + selection_type + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1])) + "_InPBin_" +  str(int(100*p_range[0])) + "_" + str(int(100*p_range[1]))
                            hist = HM.getHistograms(histogram_name)
                            DataVsMC1 = DrawDataVsMC(hist,\
                                                    channelLabels,\
                                                    MCKey='PythiaJetJet',\
                                                    DataKey='LowMuData',\
                                                    extra_description =  ["P_{T} Reweighted", eta_descriptor, p_low_str + " < |P/GeV| < " + p_high_str] + extra_stuff)
                            DataVsMC1[0].Draw()
                            DataVsMC1[0].Print(plotter_directory + "/" + histogram_name + ".png")
                            DataVsMC1[0].Close()
                        ROOT.gSystem.ProcessEvents()

raw_input()
#['NTRT20ZeroFractionVsPetaID00_06Denomenator', 'TrkPtHisteta15_18', 'trkNPV2', 'eventAverageMu', 'trkCount', 'trkAverageMu', 'NTRT20ZeroFractionVsPetaID06_11Denomenator', 'NTRT20ZeroFractionVsPetaID02_04Numerator', 'EtaID0_6_PGreater2_0_EOPHist', 'NonZero_EtaID0_6_PBetween12_18_EOPHist', 'NTRT20ZeroFractionVsPetaID00_02Denomenator', 'NonZero_EtaIDBetween19_23_PBetween22_28_EOPHist', 'EtaID0_6_PGreater1_5_EOPHist', 'EtaLess08_TwoDHistTrkPvsPhiInnerToExtrapolEM2', 'InclusiveZeroFractionVsPNumerator', 'TrkPtHisteta06', 'NTRT20ZeroFractionVsPetaID11_14Numerator', 'NTRT20ZeroFractionVsPetaID00_06Numerator', 'NonZeroEnergy_InclusiveEOP', 'TrkPtHisteta18_23', 'InclusiveEOP', 'ZeroFractionVsPetaID06_11Denomenator', 'ZeroFractionVsPetaID02_04Denomenator', 'NTRT20ZeroFractionVsPetaID04_06Numerator', 'trkPtHist', 'NTRT20ZeroFractionVsPetaID00_02Numerator', 'TrkPtHisteta06_11', 'InclusiveZeroFractionVsAbsEtaNumerator', 'ZeroFractionVsPetaID04_06Denomenator', 'NearestDRHist', 'TrackEtaID', 'NonZero_EtaID0_6_PBetween22_28_EOPHist', 'NTRT20ZeroFractionVsPetaID06_11Numerator', 'InclusiveZeroFractionVsEtaNumerator', 'InclusiveZeroFractionVsPDenomenator', 'TwoDTrackPtVsEtaHistogram', 'ZeroFractionVsPetaID11_14Denomenator', 'ZeroFractionVsPetaID00_02Denomenator', 'eventNPV2Hist', 'trkEtaECALHist', 'TrkPtHisteta14_15', 'InclusiveZeroFractionVsEtaDenomenator', 'EtaID0_6_PBetween22_28_EOPHist', 'EtaID0_6_PGreater1_0_EOPHist', 'EtaIDBetween19_23_PBetween28_36_EOPHist', 'NonZero_EtaID0_6_PBetween28_36_EOPHist', 'TrkPtHisteta11_14', 'lowPTLess07_TwoDHistTrkEtavsDEtaInnerToExtrapolEM2', 'NTRT20ZeroFractionVsPetaID04_06Denomenator', 'ZeroFractionVsPetaID00_06Denomenator', 'TwoDHistTrkPvsPhiInnerToExtrapolEM2', 'EtaID0_6_PBetween12_18_EOPHist', 'NTRT20ZeroFractionVsPetaID11_14Denomenator', 'InclusiveZeroFractionVsAbsEtaDenomenator', 'TwoDTrackPvsTrkEtaID', 'NTRT20ZeroFractionVsPetaID02_04Denomenator', 'EtaID0_6_PBetween28_36_EOPHist']

#Loop through the data and MC histograms and perform fits with landau distributions




#create a set of strings that could describe the eta or momentum selections
eta_ranges = [(0.0, 0.4),(0.4,0.8),(0.8,1.2),(1.2,1.6),(1.6,2.0),(2.0,2.4)]

#go and get the average E/P for MIP particles in each of the eta bins.
for eta_range in eta_ranges:

    eta_high_str = "{:.1f}".format(eta_range[1])
    eta_low_str= "{:.1f}".format(eta_range[0])

    #create nbins where there are at least 10,000 entries per bin
    #histogramName = "TrkMultiplicityVsP_MIPSelection_HadFracAbove70_InBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1]))
    #binningHistogram = HM.getHistograms(histogramName)["LowMuData"]
    #FourThousandTracks_pbins = GetBinsFromHistogram(binningHistogram, 4000.0)[0]
    p_bins_max = 15.05
    p_bins_min = getP(0.5, eta_range[1])
    nBins = 20
    p_bins = getLogBins(p_bins_min, p_bins_max, nBins)
    if eta_range[0] < 0.2:
        p_bins = p_bins[1:]

    #loop through the different eta and p bins and perform the fits:
    #p_ranges = [ (FourThousandTracks_pbins[i], FourThousandTracks_pbins[i+1])  for i in range(0, len(FourThousandTracks_pbins)-1) ]

    #create a histogram with each of the bins set to those from the four thousand track histograms

    bin_edges = p_bins
    bin_mpv_data = []
    bin_mpv_error_data = []
    bin_mpv_MC = []
    bin_mpv_error_MC = []

    count = 0
    p_ranges = [ (p_bins[i], p_bins[i+1])  for i in range(0, len(p_bins)-1) ]

    for p_range in p_ranges:
        count += 1

        p_high_str = "{:.2f}".format(p_range[1])
        p_low_str = "{:.2f}".format(p_range[0])

        print "Considering the following range for EOP distributions"
        print p_range[0]
        print p_range[1]

        histogramName = None
        found = False

        #find the histograms
        distFromZero = -1
        while not found:
            distFromZero += 1
            print distFromZero
            for i in range(-1 * distFromZero, distFromZero):
                if found: break
                for j in range(-1 * distFromZero, distFromZero):
                    histogramName = "EOPDistribution_MIPSelection_HadFracAbove70_InEtaBin_" + str(int(10*eta_range[0])) + "_" + str(int(10*eta_range[1])) + "_InPBin_" + str(int(100*(p_range[0]+ (i * 0.01)))) + "_" + str(int(100*(p_range[1] + (j * 0.01))))
                    if HM.hasHistogram(histogramName):
                       found = True
                       break
        print "Getting histogram " + histogramName

        histograms = HM.getHistograms(histogramName, rebin = 2)
        data = histograms["LowMuData"]
        MC = histograms["PythiaJetJet"]
        #loop through the bins with low edges above 0.0 and find the first one with more than 10 entries. Start fitting above that bin
        low_data = 0.0
        high_data = data.GetMean() + 1.5 * data.GetRMS()
        for binx in range(1, data.GetNbinsX() + 1):
            if (data.GetBinContent(binx) > 60 and data.GetBinLowEdge(binx) > 0.15):
                low_data = data.GetBinLowEdge(binx + 1)
                break

        low_MC = 0.0
        high_MC = MC.GetMean() + 1.5 * MC.GetRMS()
        for binx in range(1, MC.GetNbinsX() + 1):
            if (MC.GetBinContent(binx) > 60 and MC.GetBinLowEdge(binx) > 0.15):
                low_MC = MC.GetBinLowEdge(binx + 1)
                break

        for binx in range(data.GetNbinsX(), -1, -1):
            if (data.GetBinContent(binx) > 80):
                high_data = data.GetBinLowEdge(binx)
                break

        for binx in range(MC.GetNbinsX(), -1, -1):
            if (MC.GetBinContent(binx) > 80):
                high_MC = MC.GetBinLowEdge(binx)
                break

        #find the most probable bin and data and MC and use it for the mean of the gaussian distributions
        mpv_data = 0.0
        mpv_value_data= 0.0
        for binx in range(1, data.GetNbinsX() + 1):
            if data.GetBinContent(binx) > mpv_value_data:
                mpv_value_data = data.GetBinContent(binx)
                mpv_data = data.GetBinCenter(binx)

        mpv_MC = 0.0
        mpv_value_MC = 0.0
        for binx in range(1, MC.GetNbinsX() + 1):
            if MC.GetBinContent(binx) > mpv_value_MC:
                mpv_value_MC = MC.GetBinContent(binx)
                mpv_MC = MC.GetBinCenter(binx)

        #this is the landau distribution that will be fit to the histograms
        landau_data = ROOT.TF1("landau_data" + histogramName, "[2]*TMath::Landau(x, [0], [1])", -1.0, 5.0)
        landau_data.SetParName(0, "mpv")
        landau_data.SetParameter(0, mpv_data)
        landau_data.SetParLimits(0, 0.3, 1.1)
        landau_data.SetParName(1, "sigma")
        landau_data.SetParameter(1, data.GetRMS()/4.0)
        landau_data.SetParLimits(1, data.GetRMS()/100.0, data.GetRMS()*2.0)
        landau_data.SetParName(2, "Norm")
        landau_data.SetParameter(2, data.Integral())

        landau_MC = ROOT.TF1("landau_MC" + histogramName, "[2]*TMath::Landau(x, [0], [1])", -1.0, 5.0)
        landau_MC.SetParName(0, "mpv")
        landau_MC.SetParameter(0, mpv_MC)
        landau_MC.SetParLimits(0, 0.3, 1.1)
        landau_MC.SetParName(1, "sigma")
        landau_MC.SetParameter(1, MC.GetRMS()/4.0)
        landau_MC.SetParLimits(1, MC.GetRMS()/100.0, MC.GetRMS()*2.0)
        landau_MC.SetParName(2, "Norm")
        landau_MC.SetParameter(2, MC.Integral())

        #this is the gaus distribution that will be fit to the histograms
        gaus_data = ROOT.TF1("gaus_data" + histogramName, "[2]*TMath::Gaus(x, [0], [1])", -1.0, 5.0)
        gaus_data.SetParName(0, "mu")
        gaus_data.SetParameter(0, mpv_data)
        gaus_data.SetParLimits(0, 0.45, 0.95)
        gaus_data.SetParName(1, "sigma")
        gaus_data.SetParameter(1, data.GetRMS()*0.8)
        gaus_data.SetParLimits(1, data.GetRMS()/3.0, 1.2*data.GetRMS())
        gaus_data.SetParName(2, "Norm")
        gaus_data.SetParameter(2, data.Integral())

        gaus_MC = ROOT.TF1("gaus_MC" + histogramName, "[2]*TMath::Gaus(x, [0], [1])", -1.0, 5.0)
        gaus_MC.SetParName(0, "mu")
        gaus_MC.SetParameter(0, mpv_MC)
        gaus_MC.SetParLimits(0, 0.45, 0.95)
        gaus_MC.SetParName(1, "sigma")
        gaus_MC.SetParameter(1, data.GetRMS() * 0.8)
        gaus_MC.SetParLimits(1, data.GetRMS()/3.0, data.GetRMS()*1.2)
        gaus_MC.SetParName(2, "Norm")
        gaus_MC.SetParameter(2, MC.Integral())

        #Create a gaussian convoluted with a landau histogram
        gaus_forconvolution_MC = ROOT.TF1("gaus_forconvolution_MC" + histogramName, "TMath::Gaus(x, 0.0, [0])", -10.0, +10.0)

        landau_forconvolution_MC = ROOT.TF1("landau_forconvolution_MC" + histogramName, "[2]*TMath::Landau(x, [0], [1])", -1.0, 5.0)

        convolution_MC = ROOT.TF1Convolution(gaus_forconvolution_MC, landau_forconvolution_MC,-1,6,True)
        convolution_MC.SetRange(-1.,5.)
        convolution_MC.SetNofPointsFFT(10000)
        convolution_tofit_MC = ROOT.TF1("f",convolution_MC, -1.0, 5., convolution_MC.GetNpar())
        convolution_tofit_MC.SetName("convolution_MC" + histogramName)

        convolution_tofit_MC.SetParName(0, "SigmaSmear")
        convolution_tofit_MC.SetParLimits(0, -100.0, 100.0)
        convolution_tofit_MC.SetParameter(0, 1.0)

        convolution_tofit_MC.SetParName(1, "mpv")
        convolution_tofit_MC.SetParameter(1, mpv_MC)
        convolution_tofit_MC.SetParLimits(1, 0.3, 1.1)
        convolution_tofit_MC.SetParName(2, "sigma")
        convolution_tofit_MC.SetParameter(2, MC.GetRMS()/4.0)
        convolution_tofit_MC.SetParLimits(2, MC.GetRMS()/100.0, MC.GetRMS()*2.0)
        convolution_tofit_MC.SetParName(3, "Norm")
        convolution_tofit_MC.SetParameter(3, MC.Integral())
        print "Created convolution function"
        convolution_tofit_MC.Print()

        #Create a gaussian convoluted with a landau histogram
        gaus_forconvolution_data = ROOT.TF1("gaus_forconvolution_data" + histogramName, "TMath::Gaus(x, 0.0, [0])", -10.0, +10.0)
        landau_forconvolution_data = ROOT.TF1("landau_forconvolution_data" + histogramName, "[2]*TMath::Landau(x, [0], [1])", -1.0, 5.0)

        convolution_data = ROOT.TF1Convolution(gaus_forconvolution_data, landau_forconvolution_data,-1,6,True)
        convolution_data.SetRange(-1.,5.)
        convolution_data.SetNofPointsFFT(10000)
        convolution_tofit_data = ROOT.TF1("f",convolution_data, -1.0, 5., convolution_data.GetNpar())
        convolution_tofit_data.SetName("convolution_data" + histogramName)
        convolution_tofit_data.SetParName(0, "SigmaSmear")
        convolution_tofit_data.SetParLimits(0, -100.0, 100.0)
        convolution_tofit_data.SetParameter(0, 1.0)

        convolution_tofit_data.SetParName(1, "mpv")
        convolution_tofit_data.SetParameter(1, mpv_data)
        convolution_tofit_data.SetParLimits(1, 0.3, 1.1)
        convolution_tofit_data.SetParName(2, "sigma")
        convolution_tofit_data.SetParameter(2, data.GetRMS()/4.0)
        convolution_tofit_data.SetParLimits(2, data.GetRMS()/100.0, data.GetRMS()*2.0)
        convolution_tofit_data.SetParName(3, "Norm")
        convolution_tofit_data.SetParameter(3, data.Integral())
        print "Created convolution function"
        convolution_tofit_data.Print()

        #choose the fit funciton that you want to use
        fit_function = "convolution"
        fit_function_data_string = fit_function + "_data"
        fit_function_MC_string = fit_function + "_MC"

        #Good settings for a landau x gaus
        data.GetXaxis().SetRange(data.FindBin(0.15), data.FindBin(1.3))
        MC.GetXaxis().SetRange(MC.FindBin(0.15), MC.FindBin(1.3))

        #good settings for a gaus
        #data.GetXaxis().SetRange(data.FindBin(0.3), data.FindBin(1.0))
        #MC.GetXaxis().SetRange(MC.FindBin(0.3), MC.FindBin(1.0))

        mean_data = data.GetMean()
        sigma_data = data.GetRMS()
        mean_MC = MC.GetMean()
        sigma_MC = MC.GetRMS()

        data.GetXaxis().SetRange()
        MC.GetXaxis().SetRange()

        #good setting for a landau x gaus
        low = min(mean_data - 1.2*sigma_data, mean_MC - 1.2*sigma_MC)
        high = max(mean_data + 1.0*sigma_data, mean_MC + 1.0*sigma_MC)

        #good settings for a gaus
        #low = min(mean_data - 1.2*sigma_data, mean_MC - 1.2*sigma_MC)
        #high = max(mean_data + 0.5*sigma_data, mean_MC + 0.5*sigma_MC)

        #re-do the fit in the +- 1 sigma window
        data.Fit(fit_function_data_string + histogramName, "", "", low, high)
        MC.Fit(fit_function_MC_string + histogramName, "", "", low, high)

        fit_function_data = data.GetFunction(fit_function_data_string + histogramName)
        fit_function_data.SetLineColor(ROOT.kBlack)

        fit_function_MC = MC.GetFunction(fit_function_MC_string + histogramName)
        fit_function_MC.SetLineColor(ROOT.kRed)

        description = ["P_{T} Reweighted", "MIP Selection", eta_low_str + " < |#eta| < " + eta_high_str , p_low_str + " < P/GeV < " + p_high_str]

        DataVsMC = DrawDataVsMC(histograms,\
                              channelLabels,\
                              MCKey = "PythiaJetJet",\
                              DataKey = "LowMuData",\
                              doLogx = False,\
                              doLogy = False,
                              ratio_min = 0.4,\
                              ratio_max = 1.6,\
                              xAxis_range = (0.0, 2.0),\
                              extra_description = description)
        DataVsMC[0].Draw()
        DataVsMC[0].cd()
        raw_input()
        top_pad = DataVsMC[1]
        top_pad.cd()
        fit_function_MC.Draw("Same")

        if fit_function_MC.GetNDF() <= 1:
            continue

        #draw a little text thing describing the fit result
        chisq_MC_str = "{:.3f}".format(fit_function_MC.GetChisquare()/fit_function_MC.GetNDF())
        prob_MC_str = "{:.3f}".format(fit_function_MC.GetProb())
        mpv_MC_str = "{:.3f}".format(fit_function_MC.GetParameter(1))
        mpvErr_MC_str = "{:.3f}".format(fit_function_MC.GetParError(1))
        sigma_MC_str = "{:.3f}".format(fit_function_MC.GetParameter(1))
        sigmaErr_MC_str = "{:.3f}".format(fit_function_MC.GetParError(1))

        chisq_data_str = "{:.3f}".format(fit_function_data.GetChisquare()/fit_function_data.GetNDF())
        prob_data_str = "{:.3f}".format(fit_function_data.GetProb())
        mpv_data_str = "{:.3f}".format(fit_function_data.GetParameter(1))
        mpvErr_data_str = "{:.3f}".format(fit_function_data.GetParError(1))
        sigma_data_str = "{:.3f}".format(fit_function_data.GetParameter(1))
        sigmaErr_data_str = "{:.3f}".format(fit_function_data.GetParError(1))

        chisq_MC = fit_function_MC.GetChisquare()/fit_function_MC.GetNDF()
        prob_MC = fit_function_MC.GetProb()

        if fit_function == "convolution":
            mpv_MC = fit_function_MC.GetParameter(1)
            mpvErr_MC = fit_function_MC.GetParError(1)

        else:
            mpv_MC = fit_function_MC.GetParameter(0)
            mpvErr_MC = fit_function_MC.GetParError(0)

        sigma_MC = fit_function_MC.GetParameter(1)
        sigmaErr_MC = fit_function_MC.GetParError(1)

        chisq_data = fit_function_data.GetChisquare()/fit_function_data.GetNDF()
        prob_data = fit_function_data.GetProb()
        if fit_function == "convolution":
            mpv_data = fit_function_data.GetParameter(1)
            mpvErr_data = fit_function_data.GetParError(1)
        else:
            mpv_data = fit_function_data.GetParameter(0)
            mpvErr_data = fit_function_data.GetParError(0)

        sigma_data = fit_function_data.GetParameter(1)
        sigmaErr_data = fit_function_data.GetParError(1)

        bin_mpv_data.append(mpv_data)
        bin_mpv_error_data.append(mpvErr_data)
        bin_mpv_MC.append(mpv_MC)
        bin_mpv_error_MC.append(mpvErr_MC)

        if fit_function != "convolution":
            dataResult = "Data: #mu=" + mpv_data_str + "#pm" + mpvErr_data_str + " #sigma=" + sigma_data_str + "#pm" + sigmaErr_data_str + " #Chi^2/NDOF=" + chisq_data_str + " Prob=" + prob_data_str
            MCResult = "MC: #mu=" + mpv_MC_str + "#pm" + mpvErr_MC_str + " #sigma=" + sigma_MC_str + "#pm" + sigmaErr_MC_str + " #Chi^2/NDOF=" + chisq_MC_str + " Prob=" + prob_MC_str
        else:
            dataResult = "Data: #mu=" + mpv_data_str + "#pm" + mpvErr_data_str + " #Chi^2/NDOF=" + chisq_data_str + " Prob=" + prob_data_str
            MCResult = "MC: #mu=" + mpv_MC_str + "#pm" + mpvErr_MC_str + " #Chi^2/NDOF=" + chisq_MC_str + " Prob=" + prob_MC_str

        DrawText(0.5, 0.55, dataResult, size=0.035)
        DrawText(0.5, 0.5, MCResult, size=0.035)

        print "Creating the histogram for"
        print plotter_directory + "/" + histogramName + ".png"

        DataVsMC[0].Modified()
        DataVsMC[0].Update()
        DataVsMC[0].Print(plotter_directory + "/" + histogramName + ".png")
        raw_input()
    #create an MC and data histogram with each bin set to the result from the fit

    data_hist = ROOT.TH1D("DataFitResults" + str(eta_range[0]) + "_" + str(eta_range[1]),"DataFitResults" + str(eta_range[0]) + "_" + str(eta_range[1]), len(p_bins[1:])-1, array('d', p_bins[1:]))
    MC_hist = ROOT.TH1D("MCFitResults" + str(eta_range[0]) + "_" + str(eta_range[1]),"DataFitResults" + str(eta_range[0]) + "_" + str(eta_range[1]), len(p_bins[1:])-1, array('d', p_bins[1:]))

    for i in range(1, data_hist.GetNbinsX() + 1):
        data_hist.SetBinContent(i, bin_mpv_data[i-1])
        data_hist.SetBinError(i, bin_mpv_error_MC[i-1])
        MC_hist.SetBinContent(i, bin_mpv_MC[i-1])
        MC_hist.SetBinError(i, bin_mpv_error_MC[i-1])

    histograms = {"PythiaJetJet":MC_hist, "LowMuData":data_hist}

    description = ["P_{T} Reweighted", "MIP Selection", eta_low_str + " < |#eta| < " + eta_high_str]
    DataVsMC = DrawDataVsMC(histograms,\
                          channelLabels,\
                          MCKey = "PythiaJetJet",\
                          DataKey = "LowMuData",\
                          doLogx = True,\
                          doLogy = False,
                          ratio_min = 0.9,\
                          ratio_max = 1.1,\
                          extra_description = description)

    DataVsMC[0].Draw()
    DataVsMC[0].Print("DataFitResults" + str(eta_range[0]) + "_" + str(eta_range[1]) + ".png")
