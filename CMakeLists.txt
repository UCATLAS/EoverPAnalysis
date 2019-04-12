################################################################################
# Package: EoverPAnalysis
################################################################################

# Declare the package name:
atlas_subdir( EoverPAnalysis )

# Declare the package's dependencies:
atlas_depends_on_subdirs( PUBLIC
                          xAODAnaHelpers
                          Control/AthLinks
                          Control/AthContainers
                          AsgExternal/Asg_FastJet
                          PhysicsAnalysis/D3PDTools/EventLoop
                          PhysicsAnalysis/D3PDTools/AnaAlgorithm
                          Control/xAODRootAccess
                          Event/xAOD/xAODEventInfo
                          Event/xAOD/xAODJet
                          Event/xAOD/xAODTracking
                          Event/xAOD/xAODCaloEvent
                          Event/xAOD/xAODTruth
                          Control/AthToolSupport/AsgTools
                          InnerDetector/InDetRecTools/InDetTrackSelectionTool
                          InnerDetector/InDetRecTools/TrackVertexAssociationTool
)

# Find the needed external(s):
find_package( ROOT COMPONENTS Core RIO Hist Tree )
find_package( Eigen REQUIRED )

# build a dictionary for the library
atlas_add_root_dictionary ( EoverPAnalysisLib EoverPAnalysisDictSource
			    ROOT_HEADERS EoverPAnalysis/EoverPTreeAlgo.h EoverPAnalysis/TrackExtrapolationIsolationTool.h EoverPAnalysis/SecondariesTrees.h Root/LinkDef.h
                            EXTERNAL_PACKAGES ROOT
)

# build a shared library
atlas_add_library( EoverPAnalysisLib EoverPAnalysis/*.h Root/*.cxx ${EoverPAnalysisDictSource}
                   PUBLIC_HEADERS EoverPAnalysis
                   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} ${EIGEN_INCLUDE_DIRS}
                   LINK_LIBRARIES ${ROOT_LIBRARIES} 
                   xAODAnaHelpersLib 
)

# Install files from the package:
atlas_install_scripts( scripts/*.py )
atlas_install_data( data/* )
