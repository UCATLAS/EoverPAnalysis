# E/p analysis for run 2
# Joakim Olsson (joakim.olsson@cern.ch)

from xAH_config import xAH_config
c = xAH_config()

# input containers
trks = "InDetTrackParticles"

# selected version
trks_loose = trks+"LoosePrimary"
trks_loose_ntrtG20 = trks+"LoosePrimary_nTRTG20"
trks_tight = trks+"TightPrimary"
trks_run1 = trks+"Run1"

doCustomPUreweighting = True
pileupReweightingFile = "pileup_reweighting.root";

do_trkPtRewighting = True
trkPtReweightingFile = "pt_reweighting_pileup.root"


c.setalg("EoverPAnalysis", {"m_name": "EoverP_LoosePrimaryTrks_ClusterEnergy_noCuts",
                            "m_inTrackContainerName": trks,
                            "m_energyCalib": "ClusterEnergy", # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
                            "m_doCaloTotal": True,
                            "m_doCaloEM": False,
                            "m_doCaloHAD": False,
                            "m_doBgSubtr" : False,
                            "m_doTileLayer": False,
                            "m_trkIsoDRmax": .4,
                            "m_trkIsoPfrac": 0.,
                            "m_doTrkPcut": True,
                            "m_trkPmin": 2,
                            "m_trkPmax": 1e8,
                            "m_doTrkEtacut": True,
                            "m_trkEtamin": 0.,
                            "m_trkEtamax": 1.7,
                            "m_doTileCuts": True,
                            "m_LarEmax": 1.,
                            "m_TileEfracmin": 0.7,
                            "m_Pbins": "30, 0., 30.",
                            "m_doPbinsArray": True,
                            "m_PbinsArray": "0., 2.5, 3., 3.5, 4., 4.5, 5., 6., 7., 8., 9., 10., 12., 14., 16., 20., 30.",
                            "m_Etabins": "17, -1.7, 1.7",
                            "m_doEtabinsArray": False,
                            "m_EtabinsArray": "",
                            "m_doExtraEtaEnergyBinHists": False,
                            "m_doGlobalTileEfracRanges": False,
                            "m_doGlobalEnergyRanges": False,
                            "m_doGlobalEtaRanges": False,
                            "m_pileupReweightingFile": pileupReweightingFile,
                            "m_doCustomPUreweighting": doCustomPUreweighting,
                            "m_trkPtReweightingFile": trkPtReweightingFile,
                            "m_doTrkPtReweighting": do_trkPtRewighting,
                            "m_detailStr": "all",
                            "m_useCutFlow": False,
                            "m_debug": False})

''' Set up all the algorithms '''
c.setalg("BasicEventSelection", {"m_name": "BasicEventSelection",
                                 "m_applyGRLCut": False,
                                 "m_doPUreweighting": False,
                                 # "m_doPUreweighting": True,
                                 # # "m_doCustomPUreweighting": False,
                                 # # "m_PRWHistName": "pileup_chan361021_run284500",
                                 # "m_PRWFileNames": "$WorkDir_DIR/data/EoverPAnalysis/group.phys-susy.PRW.mc15c.3_METADATA.merged.root",
                                 # "m_lumiCalcFileNames": "$WorkDir_DIR/data/EoverPAnalysis/ilumicalc_histograms_HLT_noalg_zb_L1ZB_276262-284484_OflLumi-13TeV-005.root",
                                 "m_useMetaData" : True,
                                 "m_applyPrimaryVertexCut": True,
                                 "m_applyEventCleaningCut": True,
                                 "m_applyCoreFlagsCut": False,
                                 "m_applyTriggerCut": False,
                                 "m_PVNTrack": 2,
                                 "m_useMetaData": False,
                                 "m_checkDuplicatesData": False,
                                 "m_checkDuplicatesMC": False})

''' Fill histograms with tracking details, passing only basic event selection'''
c.setalg("TrackHistsAlgo", {"m_name": "Tracks_BasicEvtSel",
                            "m_inContainerName": trks,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_debug": False})

''' Select tracks passing the "LoosePrimary" Tracking CP Recommendations (Moriond 2016)'''
# https://twiki.cern.ch/twiki/bin/view/AtlasProtected/TrackingCPMoriond2016
c.setalg("TrackVertexSelection", {"m_name": "TrackSel_LoosePrimary",
                                  "m_inContainerName": trks,
                                  "m_decorateSelectedObjects": False,
                                  "m_createSelectedContainer": True,
                                  "m_pass_min": 1,
                                  "m_cutLevel": "LoosePrimary",
                                  "m_minPt": 0.4,
                                  "m_maxAbsEta": 2.5,
                                  "m_maxD0": 2.0,
                                  "m_maxZ0SinTheta": 3.0,
                                  "m_minNTrtHits": -1,
                                  "m_outContainerName": trks_loose,
                                  "m_useCutFlow": True,
                                  "m_debug": False})

''' Fill histograms with tracking details, after LoosePrimary selection '''
c.setalg("TrackHistsAlgo", {"m_name": "Tracks_LoosePrimary",
                            "m_inContainerName": trks_loose,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_debug": False})

# ''' Select tracks passing the "LoosePrimary" Tracking CP Recommendations (Moriond 2016), with nTRT > 20'''
# # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/TrackingCPMoriond2016
# c.setalg("TrackVertexSelection", {"m_name": "TrackSel_LoosePrimary_nTRTG20",
#                                   "m_inContainerName": trks,
#                                   "m_decorateSelectedObjects": False,
#                                   "m_createSelectedContainer": True,
#                                   "m_pass_min": 1,
#                                   "m_cutLevel": "LoosePrimary",
#                                   "m_minPt": 0.4,
#                                   "m_maxAbsEta": 2.5,
#                                   "m_maxD0": 2.0,
#                                   "m_maxZ0SinTheta": 3.0,
#                                   "m_minNTrtHits": 20,
#                                   "m_outContainerName": trks_loose_ntrtG20,
#                                   "m_useCutFlow": False,
#                                   "m_debug": False})
#
# ''' Fill histograms with tracking details, after LoosePrimary but with *NO TRT cut* selection '''
# c.setalg("TrackHistsAlgo", {"m_name": "Tracks_LoosePrimaryNoTRT",
#                             "m_inContainerName": trks_loose_ntrtG20,
#                             "m_detailStr": "2D IPDetails HitCounts Chi2Details",
#                             "m_debug": False})
#
# ''' Select tracks passing the "TightPrimary" Tracking CP Recommendations (Moriond 2016)'''
# # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/TrackingCPMoriond2016
# c.setalg("TrackVertexSelection", {"m_name": "TrackSel_TightPrimary",
#                                   "m_inContainerName": trks,
#                                   "m_decorateSelectedObjects": False,
#                                   "m_createSelectedContainer": True,
#                                   "m_pass_min": 1,
#                                   "m_cutLevel": "TightPrimary",
#                                   "m_minPt": 0.4,
#                                   "m_maxAbsEta": 2.5,
#                                   "m_maxD0": 2.0,
#                                   "m_maxZ0SinTheta": 3.0,
#                                   "m_minNTrtHits": -1,
#                                   "m_outContainerName": trks_tight,
#                                   "m_useCutFlow": False,
#                                   "m_debug": False})
#
# ''' Fill histograms with tracking details, after TightPrimary selection '''
# c.setalg("TrackHistsAlgo", {"m_name": "Tracks_TightPrimary",
#                             "m_inContainerName": trks_tight,
#                             "m_detailStr": "2D IPDetails HitCounts Chi2Details",
#                             "m_debug": False})
#
# ''' Tracks with the same selections as in the ATLAS Run 1 paper '''
# # https://cds.cern.ch/record/2006570
# c.setalg("TrackVertexSelection", {"m_name": "TrackSel_Run1",
#                                   "m_inContainerName": trks,
#                                   "m_decorateSelectedObjects": False,
#                                   "m_createSelectedContainer": True,
#                                   "m_pass_min": 1,
#                                   "m_cutLevel": "NoCut",
#                                   "m_minPt": 0.4,
#                                   "m_maxAbsEta": 2.3,
#                                   "m_maxD0": 1.5,
#                                   "m_maxZ0SinTheta": 1.5,
#                                   "m_minNPixelHits": 1,
#                                   "m_minNSctHits": 6,
#                                   "m_minNTrtHits": 20,
#                                   "m_outContainerName": trks_run1,
#                                   "m_useCutFlow": False,
#                                   "m_debug": False})
#
# ''' Fill histograms with tracking details, after Run1 selection '''
# c.setalg("TrackHistsAlgo", {"m_name": "Tracks_Run1",
#                             "m_inContainerName": trks_run1,
#                             "m_detailStr": "2D IPDetails HitCounts Chi2Details",
#                             "m_debug": False})

#### Make E/p plots

#E/p with TileCal selections
''' E/p histograms with LoosePrimary track selection'''
c.setalg("EoverPAnalysis", {"m_name": "EoverP_LoosePrimaryTrks_ClusterEnergy_Tile_notrkP_noLar_noTileEfrac",
                            "m_inTrackContainerName": trks_loose,
                            "m_energyCalib": "ClusterEnergy", # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
                            "m_doCaloTotal": True,
                            "m_doCaloEM": True,
                            "m_doCaloHAD": True,
                            "m_doBgSubtr" : False,
                            "m_doTileLayer": True,
                            "m_trkIsoDRmax": .4,
                            "m_trkIsoPfrac": 0.,
                            "m_doTrkPcut": True,
                            "m_trkPmin": 0.,
                            "m_trkPmax": 1e8,
                            "m_doTrkEtacut": True,
                            "m_trkEtamin": 0.,
                            "m_trkEtamax": 1.7,
                            "m_doTileCuts": True,
                            "m_LarEmax": 1e8,
                            "m_TileEfracmin": -1,
                            "m_Pbins": "30, 0., 30.",
                            "m_doPbinsArray": True,
                            "m_PbinsArray": "0., 2.5, 3., 3.5, 4., 4.5, 5., 6., 7., 8., 9., 10., 12., 14., 16., 20., 30.",
                            "m_Etabins": "17, -1.7, 1.7",
                            "m_doEtabinsArray": False,
                            "m_EtabinsArray": "",
                            "m_doExtraEtaEnergyBinHists": False,
                            "m_doGlobalTileEfracRanges": False,
                            "m_doGlobalEnergyRanges": False,
                            "m_doGlobalEtaRanges": False,
                            "m_pileupReweightingFile": pileupReweightingFile,
                            "m_doCustomPUreweighting": doCustomPUreweighting,
                            "m_trkPtReweightingFile": trkPtReweightingFile,
                            "m_doTrkPtReweighting": do_trkPtRewighting,
                            "m_detailStr": "all",
                            "m_useCutFlow": False,
                            "m_debug": False})

# ''' E/p histograms with LoosePrimary track selection'''
# c.setalg("EoverPAnalysis", {"m_name": "EoverP_LoosePrimaryTrks_ClusterEnergy_Tile_2GeVTrkP_noLar_noTileEfrac",
#                             "m_inTrackContainerName": trks_loose,
#                             "m_energyCalib": "ClusterEnergy", # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
#                             "m_doCaloTotal": True,
#                             "m_doCaloEM": True,
#                             "m_doCaloHAD": True,
#                             "m_doBgSubtr" : False,
#                             "m_doTileLayer": True,
#                             "m_trkIsoDRmax": .4,
#                             "m_trkIsoPfrac": 0.,
#                             "m_doTrkPcut": True,
#                             "m_trkPmin": 2.,
#                             "m_trkPmax": 1e8,
#                             "m_doTrkEtacut": True,
#                             "m_trkEtamin": 0.,
#                             "m_trkEtamax": 1.7,
#                             "m_doTileCuts": True,
#                             "m_LarEmax": 1e8,
#                             "m_TileEfracmin": -1,
#                             "m_Pbins": "30, 0., 30.",
#                             "m_doPbinsArray": True,
#                             "m_PbinsArray": "0., 2.5, 3., 3.5, 4., 4.5, 5., 6., 7., 8., 9., 10., 12., 14., 16., 20., 30.",
#                             "m_Etabins": "17, -1.7, 1.7",
#                             "m_doEtabinsArray": False,
#                             "m_EtabinsArray": "",
#                             "m_doExtraEtaEnergyBinHists": False,
#                             "m_doGlobalTileEfracRanges": False,
#                             "m_doGlobalEnergyRanges": False,
#                             "m_doGlobalEtaRanges": False,
#                             "m_trkPtReweightingFile": trkPtReweightingFile,
#                             "m_doTrkPtReweighting": do_trkPtRewighting,
#                             "m_detailStr": "all",
#                             "m_useCutFlow": False,
#                             "m_debug": False})
#
# ''' E/p histograms with LoosePrimary track selection'''
# c.setalg("EoverPAnalysis", {"m_name": "EoverP_LoosePrimaryTrks_ClusterEnergy_Tile_2GeVTrkP_1GeVLar_noTileEfrac",
#                             "m_inTrackContainerName": trks_loose,
#                             "m_energyCalib": "ClusterEnergy", # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
#                             "m_doCaloTotal": True,
#                             "m_doCaloEM": True,
#                             "m_doCaloHAD": True,
#                             "m_doBgSubtr" : False,
#                             "m_doTileLayer": True,
#                             "m_trkIsoDRmax": .4,
#                             "m_trkIsoPfrac": 0.,
#                             "m_doTrkPcut": True,
#                             "m_trkPmin": 2.,
#                             "m_trkPmax": 1e8,
#                             "m_doTrkEtacut": True,
#                             "m_trkEtamin": 0.,
#                             "m_trkEtamax": 1.7,
#                             "m_doTileCuts": True,
#                             "m_LarEmax": 1,
#                             "m_TileEfracmin": -1,
#                             "m_Pbins": "30, 0., 30.",
#                             "m_doPbinsArray": True,
#                             "m_PbinsArray": "0., 2.5, 3., 3.5, 4., 4.5, 5., 6., 7., 8., 9., 10., 12., 14., 16., 20., 30.",
#                             "m_Etabins": "17, -1.7, 1.7",
#                             "m_doEtabinsArray": False,
#                             "m_EtabinsArray": "",
#                             "m_doExtraEtaEnergyBinHists": False,
#                             "m_doGlobalTileEfracRanges": False,
#                             "m_doGlobalEnergyRanges": False,
#                             "m_doGlobalEtaRanges": False,
#                             "m_trkPtReweightingFile": trkPtReweightingFile,
#                             "m_doTrkPtReweighting": do_trkPtRewighting,
#                             "m_detailStr": "all",
#                             "m_useCutFlow": False,
#                             "m_debug": False})

# for energy_calib in ["ClusterEnergy", "ClusterEnergyLCW", "CellEnergy"]:
for energy_calib in ["ClusterEnergy"]:

    if energy_calib == "ClusterEnergy":
        useCutFlow = True
    else:
        useCutFlow = False
    ''' E/p histograms with LoosePrimary track selection'''
    c.setalg("EoverPAnalysis", {"m_name": "EoverP_LoosePrimaryTrks_"+energy_calib+"_Tile_defaultCuts",
                                "m_inTrackContainerName": trks_loose,
                                "m_energyCalib": energy_calib, # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
                                "m_doCaloTotal": True,
                                "m_doCaloEM": True,
                                "m_doCaloHAD": True,
                                "m_doBgSubtr" : False,
                                "m_doTileLayer": True,
                                "m_trkIsoDRmax": .4,
                                "m_trkIsoPfrac": 0.,
                                "m_doTrkPcut": True,
                                "m_trkPmin": 2,
                                "m_trkPmax": 1e8,
                                "m_doTrkEtacut": True,
                                "m_trkEtamin": 0.,
                                "m_trkEtamax": 1.7,
                                "m_doTileCuts": True,
                                "m_LarEmax": 1.,
                                "m_TileEfracmin": 0.7,
                                "m_Pbins": "30, 0., 30.",
                                "m_doPbinsArray": True,
                                "m_PbinsArray": "0., 2.5, 3., 3.5, 4., 4.5, 5., 6., 7., 8., 9., 10., 12., 14., 16., 20., 30.",
                                "m_Etabins": "17, -1.7, 1.7",
                                "m_doEtabinsArray": False,
                                "m_EtabinsArray": "",
                                "m_doExtraEtaEnergyBinHists": False,
                                "m_doGlobalTileEfracRanges": False,
                                "m_doGlobalEnergyRanges": True,
                                "m_doGlobalEtaRanges": True,
                                "m_pileupReweightingFile": pileupReweightingFile,
                                "m_doCustomPUreweighting": doCustomPUreweighting,
                                "m_trkPtReweightingFile": trkPtReweightingFile,
                                "m_doTrkPtReweighting": do_trkPtRewighting,
                                "m_detailStr": "all",
                                "m_useCutFlow": useCutFlow,
                                "m_debug": False})
