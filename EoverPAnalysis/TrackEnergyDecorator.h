#ifndef eoverpanalysis_TrackEnergyDecorator_H
#define eoverpanalysis_TrackEnergyDecorator_H

// E/p analysis for run 2
// Lukas Adamek (lukas.adamek@cern.ch)

#include "TTree.h"
#include "TH1.h"

#include "EoverPAnalysis/EnergySumHelper.h"
#include "xAODTracking/VertexContainer.h"
#include "xAODTracking/TrackParticleContainer.h"
#include "xAODTruth/TruthParticle.h"

// algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

class TrackEnergyDecorator : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
  public:
    std::string m_inTrackContainerName;

    // energy calibration, either "ClusterEnergy", "LCWClusterEnergy", or "CellEnergy"
    std::string m_energyCalibCommaList = "ClusterEnergy,CellEnergy,LCWClusterEnergy";
    std::string m_radiusCutCommaList = "100,200,300";
    std::string m_energySumName = "Energy";

  private:

    std::vector<std::string> m_energyCalibList;
    std::vector<std::string> m_radiusCutList;

    public:
    TrackEnergyDecorator (std::string className = "TrackEnergyDecorator");
    // these are the functions inherited from Algorithm
    virtual EL::StatusCode setupJob (EL::Job& job);
    virtual EL::StatusCode fileExecute ();
    virtual EL::StatusCode histInitialize ();
    virtual EL::StatusCode changeInput (bool firstFile);
    virtual EL::StatusCode initialize ();
    virtual EL::StatusCode execute ();
    virtual EL::StatusCode postExecute ();
    virtual EL::StatusCode finalize ();
    virtual EL::StatusCode histFinalize ();
    std::vector<double> str2vec(std::string str);
    /// @cond
    // this is needed to distribute the algorithm to the workers
    ClassDef(TrackEnergyDecorator, 1);
    /// @endcond
};

#endif
