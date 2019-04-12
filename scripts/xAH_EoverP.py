# E/p analysis for run 2
# Lukas Adamek (lukas.adamek@cern.ch)

from xAH_config import xAH_config
c = xAH_config()

import shlex,argparse

# Parser for options passed through xAH_run.py --extraOptions="(...)"
parser = argparse.ArgumentParser("MLBJESJER")
parser.add_argument('--isData', action='store_true', default=False)
args = parser.parse_args(shlex.split(args.extra_options))

c.output("ANALYSIS")

# input containers
trks = "InDetTrackParticles"
trks_loose = trks + "Loose"
trks_tight = trks + "Tight"
trks_loose_isolated = trks_loose + "Isolated"
trks_tight_isolated = trks_tight + "Isolated"
trks_loose_isolated_vertex = trks_loose_isolated + "VertexAssociated"
trks_tight_isolated_vertex = trks_tight_isolated + "VertexAssociated"
radiusCuts = "100,200,300"

# Set up the Basic Event Selection for 2017 low-mu data
c.setalg("BasicEventSelection", {"m_name": "BasicEventSelection",
                                 "m_applyGRLCut": args.isData,
                                 "m_doPUreweighting": False,
                                 "m_applyPrimaryVertexCut": True,
                                 "m_applyEventCleaningCut": True,
                                 "m_applyCoreFlagsCut": args.isData,
                                 "m_applyTriggerCut": args.isData,
                                 "m_GRLxml": "EoverPAnalysis/data17_13TeV.periodN_DetStatus-v98-pro21-16_Unknown_PHYS_StandardGRL_All_Good_25ns_ignore_GLOBAL_LOWMU_for_specific_run341294.xml",
                                 "m_lumiCalcFileNames": "EoverPAnalysis/ilumicalc_histograms_HLT_mb_sptrk_341294_OflLumi-13TeV-010.root",
                                 "m_PRWFileNames": "EoverPAnalysis/ntup_prw_36102_JZ012.root",
                                 "m_triggerSelection": "HLT_mb_sptrk",
                                 "m_applyPrimaryVertexCut": True,
                                 "m_PVNTrack": 2,
                                 "m_useMetaData": False,
                                 "m_checkDuplicatesData": False,
                                 "m_checkDuplicatesMC": False
				 })

# Fill histograms with tracking details, passing only basic event selection
c.setalg("TrackHistsAlgo", {"m_name": "Tracks_BasicEvtSel",
                            "m_inContainerName": trks,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_msgLevel": "info"
			    })



# track selection algorithm
c.setalg("InDetTrackSelectionToolAlgo", {"m_name": "Sel_" + trks_loose,
					 "m_inputTrackContainer": trks,
					 "m_minPt": 0.5,
					 "m_CutLevel": "Loose",
					 "m_outputTrackContainer": trks_loose,
					 "m_msgLevel": "info"
					 })

# Create new energy sum decorations for the tracks
c.setalg("TrackEnergyDecorator", {"m_name": "TrackEnergyDecoratorAlgoUno",
				  "m_energySumName":"TotalCalibHitEnergy",
                                  "m_inTrackContainerName": trks_loose,
                                  "m_radiusCutCommaList":radiusCuts,
                                  "m_energyCalibCommaList":"ClusterEMActiveCalibHitEnergy,ClusterNonEMActiveCalibHitEnergy,ClusterEscapedActiveCalibHitEnergy,ClusterInvisibleActiveCalibHitEnergy,ClusterEMInactiveCalibHitEnergy,ClusterNonEMInactiveCalibHitEnergy,ClusterEscapedInactiveCalibHitEnergy,ClusterInvisibleInactiveCalibHitEnergy",
				  })

# Create new energy sum decorations for the tracks
c.setalg("TrackEnergyDecorator", { "m_name": "TrackEnergyDecoratorAlgoDos",
				   "m_energySumName":"TotalPhotonBackgroundCalibHitEnergy",
                                  "m_inTrackContainerName": trks_loose,
				   "m_radiusCutCommaList":radiusCuts,
				   "m_energyCalibCommaList":"ClusterPhotonBackgroundEMActiveCalibHitEnergy,ClusterPhotonBackgroundNonEMActiveCalibHitEnergy,ClusterPhotonBackgroundEscapedActiveCalibHitEnergy,ClusterPhotonBackgroundInvisibleActiveCalibHitEnergy,ClusterPhotonBackgroundEMInactiveCalibHitEnergy,ClusterPhotonBackgroundNonEMInactiveCalibHitEnergy,ClusterPhotonBackgroundEscapedInactiveCalibHitEnergy,ClusterPhotonBackgroundInvisibleInactiveCalibHitEnergy",
				  })

# Create new energy sum decorations for the tracks
c.setalg("TrackEnergyDecorator", { "m_name": "TrackEnergyDecoratorAlgoTres",
				   "m_energySumName":"TotalHadronicBackgroundCalibHitEnergy",
				   "m_inTrackContainerName": trks_loose,
				   "m_radiusCutCommaList":radiusCuts,
				   "m_energyCalibCommaList":"ClusterHadronicBackgroundEMActiveCalibHitEnergy,ClusterHadronicBackgroundNonEMActiveCalibHitEnergy,ClusterHadronicBackgroundEscapedActiveCalibHitEnergy,ClusterHadronicBackgroundInvisibleActiveCalibHitEnergy,ClusterHadronicBackgroundEMInactiveCalibHitEnergy,ClusterHadronicBackgroundNonEMInactiveCalibHitEnergy,ClusterHadronicBackgroundEscapedInactiveCalibHitEnergy,ClusterHadronicBackgroundInvisibleInactiveCalibHitEnergy",
				  })

# Fill histograms with tracking details, after LoosePrimary selection
c.setalg("TrackHistsAlgo", {"m_name": "TrackHist_" + trks_loose,
                            "m_inContainerName": trks_loose,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_msgLevel": "info"
			    })

c.setalg("TrackExtrapolationIsolationTool", {"m_name": "TrackIso_" + trks_loose,
					     "m_inputTrackContainer": trks_loose,
					     "m_outputTrackContainer": trks_loose_isolated,
					     "m_trkIsoDRmax": 0.4,
					     "m_msgLevel": "info"
					     })

# Fill histograms with tracking details, after LoosePrimary + Isolation selection
c.setalg("TrackHistsAlgo", {"m_name": "TrackHist_" + trks_loose_isolated,
                            "m_inContainerName": trks_loose_isolated,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_msgLevel": "info"
			    })

c.setalg("InDetTrackSelectionToolAlgo", {"m_name": "Sel_" + trks_tight_isolated ,
					 "m_inputTrackContainer": trks_loose_isolated,
					 "m_outputTrackContainer": trks_tight_isolated,
					 "m_CutLevel": "TightPrimary",
					 "m_msgLevel": "info"
					 })

# Fill histograms with tracking details, after LoosePrimary + Isolation + tight primary selection
c.setalg("TrackHistsAlgo", {"m_name": "TrackHist_" + trks_tight_isolated,
                            "m_inContainerName": trks_tight_isolated,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_msgLevel": "info"
			    })

c.setalg("TightTrackVertexAssociationToolAlgo", {"m_name":"TrackVertexAssociationTool",
						 "m_inputTrackContainer": trks_loose_isolated,
						 "m_outputTrackContainer": trks_loose_isolated_vertex,
						 "m_dzSinTheta_cut": 0.5,
						 "m_d0_cut": 0.5,
						 "m_msgLevel": "info",
						 })

# Fill histograms with tracking details, after LoosePrimary + Isolation + vertex association cut
c.setalg("TrackHistsAlgo", {"m_name": "TrackHist_" + trks_loose_isolated_vertex,
                            "m_inContainerName": trks_loose_isolated_vertex,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_msgLevel": "info"
			    })

c.setalg("TightTrackVertexAssociationToolAlgo", {"m_name":"TrackVertexAssociatedTool",
						 "m_inputTrackContainer": trks_tight_isolated,
						 "m_outputTrackContainer": trks_tight_isolated_vertex,
						 "m_dzSinTheta_cut":0.5,
						 "m_d0_cut":0.5,
						 "m_msgLevel": "info",
						 })

# Fill histograms with tracking details, after LoosePrimary + Isolation + Tight Primary + vertex association cut
c.setalg("TrackHistsAlgo", {"m_name": "TrackHist_" + trks_tight_isolated_vertex,
                            "m_inContainerName": trks_tight_isolated_vertex,
                            "m_detailStr": "2D IPDetails HitCounts Chi2Details",
                            "m_msgLevel": "info"
			    })

#### Make E/p ttree
for track_container in [trks_loose_isolated, trks_loose_isolated_vertex, trks_tight_isolated, trks_tight_isolated_vertex]:
        # E/p histograms with LoosePrimary track selection
        c.setalg("EoverPTreeAlgo", {"m_name": "LA_EoverP_" + track_container,
				    "m_inTrackContainerName": track_container,
				    "m_energyCalibCommaList": "ClusterEnergy,CellEnergy,LCWClusterEnergy,ClusterEMActiveCalibHitEnergy,TotalCalibHitEnergy,TotalPhotonBackgroundCalibHitEnergy,TotalHadronicBackgroundCalibHitEnergy",
				    "m_radiusCutCommaList": radiusCuts,
				    "m_useCutFlow": True,
                                    "m_msgLevel": "info"
				    })

for sv in ['Lambda','Ks','Phi']:
	c.algorithm("SecondariesTrees", {"m_name": "MLB_EoverP_" + sv,
					 "label": sv,
					 "isData": True,
					 "MessageFrequency": 10000,
					 "VertexContainer" : sv+"Candidates",
					 "TrackContainer" : trks_loose
					 })
	
