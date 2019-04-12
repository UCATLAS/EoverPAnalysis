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

eta_bins_runII_general = ".0, .6, 1.1, 1.4, 1.5, 1.8, 1.9, 2.3"
# OLD  p_bins_runII_general = ".5, .8, 1.2, 1.8, 2.2, 2.8, 3.6, 4.6, 6., 10., 15., 20., 25., 30., 40., 50., 100., 200., 1000., 10000."
p_bins_runII_general = ".5, .8, 1.2, 1.8, 2.2, 2.8, 3.4, 4.2, 5., 6., 7., 9., 12., 15., 20., 30." #, 40., 50., 100., 200., 1000., 10000."

# E/p for comparisons with the Run 1 paper
# ''' E/p histograms with LoosePrimary track selection'''
# c.setalg("EoverPAnalysis", {"m_name": "EoverP_Run1paper_noSelection",
#                            "m_inTrackContainerName": trks,
#                            "m_energyCalib": "ClusterEnergy",
#                            "m_doCaloTotal": True,
#                            "m_doCaloEM": True,
#                            "m_doCaloHAD": True,
#                            "m_doBgSubtr" : True,
#                            "m_doTileLayer": False,
#                            "m_trkIsoDRmax": .4,
#                            "m_trkIsoPfrac": 0.,
#                            "m_doTrkPcut": True,
#                            "m_trkPmin": 0.,
#                            "m_trkPmax": 1e8,
#                            "m_doTrkEtacut": True,
#                            "m_trkEtamin": 0.,
#                            "m_trkEtamax": 1e8,
#                            "m_doTileCuts": False,
#                            "m_LarEmax": 1e8,
#                            "m_TileEfracmin": -1,
#                            "m_Pbins": "500, 0, 50",
#                            "m_doPbinsArray": True,
#                            "m_PbinsArray": p_bins_runII_general,
#                            "m_Etabins": "50, 0., 2.5",
#                            "m_doEtabinsArray": True,
#                            "m_EtabinsArray": eta_bins_runII_general,
#                            "m_doExtraEtaEnergyBinHists": False,
#                            "m_doGlobalTileEfracRanges": False,
#                            "m_doGlobalEnergyRanges": False,
#                            "m_doGlobalEtaRanges": False,
#                            "m_doGlobalExtraRanges": False,
#                            "m_detailStr": "all",
#                            "m_useCutFlow": False,
#                            "m_debug": False})

''' Set up all the algorithms '''
c.setalg("BasicEventSelection", {"m_name": "BasicEventSelection",
                                 "m_applyGRLCut": True,
                                 "m_GRLxml": "$WorkDir_DIR/data/EoverPAnalysis/data15_13TeV.periodB1_DetStatus-v62-pro18_DQDefects-00-01-02_PHYS_StandardModel_MinimuBias2010.xml",
                                 "m_doPUreweighting": False,
                                 "m_applyPrimaryVertexCut": True,
                                 "m_PVNTrack": 2,
                                 "m_applyEventCleaningCut": True,
                                 "m_applyCoreFlagsCut": True,
                                 "m_applyTriggerCut": True,
                                 "m_triggerSelection": "HLT_noalg_mb_L1MBTS_1",
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
# ''' Fill histograms with tracking details, after LoosePrimary and with TRT selection '''
# c.setalg("TrackHistsAlgo", {"m_name": "Tracks_LoosePrimaryTRT",
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
#                                   "m_maxAbsEta": 2.5,
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

for energy_calib in ["ClusterEnergy", "ClusterEnergyLCW", "CellEnergy"]:
# for energy_calib in ["ClusterEnergy", "ClusterEnergyLCW"]:
# for energy_calib in ["ClusterEnergy"]:

    # # E/p for comparisons with the Run 1 paper
    # ''' E/p histograms with LoosePrimary track selection'''
    # c.setalg("EoverPAnalysis", {"m_name": "EoverP_LoosePrimaryTrks_"+energy_calib+"_Run1paper_noTrkIsolation",
    #                             "m_inTrackContainerName": trks_loose,
    #                             "m_energyCalib": energy_calib, # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
    #                             "m_doCaloTotal": True,
    #                             "m_doCaloEM": True,
    #                             "m_doCaloHAD": True,
    #                             "m_doBgSubtr" : True,
    #                             "m_doTileLayer": False,
    #                             "m_trkIsoDRmax": .0,
    #                             "m_trkIsoPfrac": 0.,
    #                             "m_doTrkPcut": True,
    #                             "m_trkPmin": 0.,
    #                             "m_trkPmax": 1e8,
    #                             "m_doTrkEtacut": True,
    #                             "m_trkEtamin": 0.,
    #                             "m_trkEtamax": 1e8,
    #                             "m_doTrkPtReweighting": False,
    #                             "m_doTileCuts": False,
    #                             "m_LarEmax": 1e8,
    #                             "m_TileEfracmin": -1,
    #                             "m_Pbins": "500, 0, 50",
    #                             "m_doPbinsArray": True,
    #                             "m_PbinsArray": p_bins_runII_general,
    #                             "m_Etabins": "50, 0., 2.5",
    #                             "m_doEtabinsArray": True,
    #                             "m_EtabinsArray": eta_bins_runII_general,
    #                             "m_doExtraEtaEnergyBinHists": True,
    #                             "m_doGlobalTileEfracRanges": False,
    #                             "m_doGlobalEnergyRanges": False,
    #                             "m_doGlobalEtaRanges": False,
    #                             "m_doGlobalExtraRanges": False,
    #                             "m_detailStr": "all",
    #                             "m_useCutFlow": False,
    #                             "m_debug": False})

    if energy_calib == "ClusterEnergy":
        useCutFlow = True
    else:
        useCutFlow = False
    # E/p for comparisons with the Run 1 paper
    ''' E/p histograms with LoosePrimary track selection'''
    c.setalg("EoverPAnalysis", {"m_name": "EoverP_LoosePrimaryTrks_"+energy_calib+"_Run1paper",
                                "m_inTrackContainerName": trks_loose,
                                "m_energyCalib": energy_calib, # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
                                "m_doCaloTotal": True,
                                "m_doCaloEM": False,
                                "m_doCaloHAD": False,
                                "m_doBgSubtr" : True,
                                "m_doTileLayer": False,
                                "m_trkIsoDRmax": .4,
                                "m_trkIsoPfrac": 0.,
                                "m_doTrkPcut": True,
                                "m_trkPmin": 0.,
                                "m_trkPmax": 1e8,
                                "m_doTrkEtacut": True,
                                "m_trkEtamin": 0.,
                                "m_trkEtamax": 2.3,
                                "m_doTrkPtReweighting": False,
                                "m_doTileCuts": False,
                                "m_LarEmax": 1e8,
                                "m_TileEfracmin": -1,
                                "m_Pbins": "500, 0, 50",
                                "m_doPbinsArray": True,
                                "m_PbinsArray": p_bins_runII_general,
                                "m_Etabins": "50, 0., 2.5",
                                "m_doEtabinsArray": True,
                                "m_EtabinsArray": eta_bins_runII_general,
                                "m_doProfileEta": True,
                                "m_doProfileP": True,
                                "m_doExtraEtaEnergyBinHists": True,
                                "m_doGlobalTileEfracRanges": False,
                                "m_doGlobalEnergyRanges": False,
                                "m_doGlobalEtaRanges": False,
                                "m_doGlobalExtraRanges": False,
                                "m_detailStr": "all",
                                "m_useCutFlow": useCutFlow,
                                "m_debug": False})
