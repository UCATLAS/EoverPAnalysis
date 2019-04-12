# E/p analysis for run 2
# Joakim Olsson (joakim.olsson@cern.ch)

from xAH_config import xAH_config
c = xAH_config()

# input containers
trks = "InDetTrackParticles"

# selected version
trks_loose = trks+"LoosePrimary"
trks_loose_ntrtG20 = trks+"LoosePrimary_nTRTG20"

eta_bins_runII_general = ".0, .6, 1.1, 1.4, 1.5, 1.7, 1.9, 2.3"
# OLD  p_bins_runII_general = ".5, .8, 1.2, 1.8, 2.2, 2.8, 3.6, 4.6, 6., 10., 15., 20., 25., 30., 40., 50., 100., 200., 1000., 10000."
#p_bins_runII_general = ".5, .8, 1.2, 1.8, 2.2, 2.8, 3.4, 4.2, 5., 6., 7., 9., 12., 15., 20., 30." #, 40., 50., 100., 200., 1000., 10000."
p_bins_runII_general = ".5, .8, 1.2, 1.8, 2.2, 2.8, 3.4, 4.2, 5., 6., 7., 9., 12., 15., 20., 30. , 40., 50., 100., 200., 1000., 10000."


''' Set up all the algorithms '''
c.setalg("BasicEventSelection", {"m_name": "BasicEventSelection",
                                 "m_applyGRLCut": False,
                                 "m_doPUreweighting": False,
                                 "m_applyPrimaryVertexCut": True,
                                 "m_applyEventCleaningCut": False,
                                 "m_applyCoreFlagsCut": False,
                                 "m_applyTriggerCut": False,
                                 "m_PVNTrack": 4,
                                 "m_useMetaData": False,
                                 "m_checkDuplicatesData": False,
                                 "m_checkDuplicatesMC": False})

''' Fill histograms with tracking details, passing only basic event selection'''
c.setalg("TrackHistsAlgo", {"m_name": "Tracks_BasicEvtSel",
                            "m_inContainerName": trks,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_debug": False})

''' Select tracks passing the "LoosePrimary" Tracking CP Recommendations (Moriond 2017)'''
c.setalg("TrackVertexSelection", {"m_name": "TrackSel_LoosePrimary",
                                  "m_inContainerName": trks,
                                  "m_decorateSelectedObjects": False,
                                  "m_createSelectedContainer": True,
                                  "m_pass_min": 1,
                                  "m_minPt": 0.5,
                                  "m_cutLevel": "LoosePrimary",
                                  "m_outContainerName": trks_loose,
                                  "m_useCutFlow": True,
                                  "m_debug": False})

''' Fill histograms with tracking details, after LoosePrimary selection '''
c.setalg("TrackHistsAlgo", {"m_name": "Tracks_LoosePrimary",
                            "m_inContainerName": trks_loose,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_debug": False})

#''' Select tracks passing the "LoosePrimary" Tracking CP Recommendations (Moriond 2016), with nTRT > 20'''
# https://twiki.cern.ch/twiki/bin/view/AtlasProtected/TrackingCPMoriond2016
#c.setalg("TrackVertexSelection", {"m_name": "TrackSel_LoosePrimary_nTRTG20",
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

#''' Fill histograms with tracking details, after LoosePrimary and with TRT selection '''
#c.setalg("TrackHistsAlgo", {"m_name": "Tracks_LoosePrimaryTRT",
#                             "m_inContainerName": trks_loose_ntrtG20,
#                             "m_detailStr": "2D IPDetails HitCounts Chi2Details",
#                             "m_debug": False})

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

#### Make E/p plots

for track_container in [trks_loose]:

    for energy_calib in ["ClusterEnergy", "ClusterEnergyLCW", "CellEnergy"]:
        ''' E/p histograms with LoosePrimary track selection'''
        c.setalg("EoverPAnalysis", {"m_name": "EoverP_"+energy_calib + track_container,
                                    "m_inTrackContainerName": track_container,
                                    "m_energyCalib": energy_calib, # ClusterEnergy, ClusterEnergyLCW, or CellEnergy
                                    "m_LarEmax": 1.0, #This selection is applied if m_applyTileCuts is true
                                    "m_applyTileCuts": True, #whether or not to cut on TileEfracMin
                                    "m_TileEfracmin": 0.7, #the fraction of energy that should be deposited in the tile calorimeter
                                    "m_doGlobalTileEfracRanges": True, #plots of different TileEfrac selections that could be applied
                                    "m_doGlobalEtaRanges": True, #plots with eta < 0.5, 0.5 < eta < 0.7, and eta < 0.7
                                    "m_doExtraEtaEnergyBinHists": False, 
                                    "m_doGlobalExtraRanges": False,
                                    "m_doGlobalEnergyRanges": False,
                                    "m_doCaloTotal": True,
                                    "m_doCaloEM": True,
                                    "m_doCaloHAD": True,
                                    "m_doBgSubtr" : False,
                                    "m_doTileLayer": True,
                                    "m_trkIsoDRmax": .4,
                                    "m_trkIsoPfrac": 0.,
                                    "m_doTrkPcut": True,
                                    "m_trkPmin": 2.0,
                                    "m_trkPmax": 1e8,
                                    "m_doTrkEtacut": True,
                                    "m_trkEtamin": 0.,
                                    "m_trkEtamax": 1.7,
                                    "m_doTrkPtReweighting": False, # do_trkPtRewighting,
                                    "m_trkPtReweightingFile": "",
                                    "m_Pbins": "500, 0, 50",
                                    "m_doPbinsArray": True,
                                    "m_PbinsArray": p_bins_runII_general,
                                    "m_Etabins": "50, 0., 2.5",
                                    "m_doEtabinsArray": True,
                                    "m_EtabinsArray": eta_bins_runII_general,
                                    "m_doProfileEta": True,
                                    "m_doProfileP": True,
                                    "m_detailStr": "all",
                                    "m_useCutFlow": False,
                                    "m_debug": False})

