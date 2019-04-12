#ifndef eoverpanalysis_TrackSorter_H
#define eoverpanalysis_TrackSorter_H

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

class TrackSorter : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
  public:
    std::string m_inTrackContainerName;

    // energy calibration, either "ClusterEnergy", "LCWClusterEnergy", or "CellEnergy"
    std::string m_sort;
    std::string m_sortedTrackContainerName;

  private:

    public:
    TrackSorter (std::string className = "TrackSorter");
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
    static bool sort_p(const xAOD::TrackParticle* A, const xAOD::TrackParticle* B);
    static bool sort_pt(const xAOD::TrackParticle* A, const xAOD::TrackParticle* B);
    std::vector<double> str2vec(std::string str);
    /// @cond
    // this is needed to distribute the algorithm to the workers
    ClassDef(TrackSorter, 1);
    /// @endcond
};

#endif
