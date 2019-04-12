#ifndef eoverpanalysis_EoverPTreeAlgo_H
#define eoverpanalysis_EoverPTreeAlgo_H

// E/p analysis for run 2
// Joakim Olsson (joakim.olsson@cern.ch)

#include "TTree.h"
#include "TH1.h"

#include "xAODTracking/VertexContainer.h"
#include "xAODTracking/TrackParticleContainer.h"
#include "xAODTruth/TruthParticle.h"


// algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

class EoverPTreeAlgo : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
  public:
    std::string m_inTrackContainerName;

    // configuration variables
    std::string m_detailStr;

    // save output tree of key variables
    bool m_fillOutputTree = false;
    // track isolation settings
    // turn on cutflows
    bool m_useCutFlow = false; 

    // energy calibration, either "ClusterEnergy", "LCWClusterEnergy", or "CellEnergy"
    std::string m_energyCalibCommaList = "ClusterEnergy,CellEnergy,LCWClusterEnergy";
    std::string m_radiusCutCommaList = "100,200";

    // pileup reweighting
    bool m_doCustomPUreweighting = false;
    std::string m_pileupReweightingFile = "pileup_reweighting.root";
    // pt reweighting
    bool m_doTrkPtReweighting = false;
    std::string m_trkPtReweightingFile = "pt_reweighting.root";

  private:

    std::map<std::string, float> m_energyVariablesForTree;
    std::vector<std::string> m_energyCalibList;
    std::vector<std::string> m_radiusCutList;

    // variables to dump to the output ttree
    float trk_etaID;
    float trk_phiID;

    uint8_t m_trkIndex; 
    unsigned long long m_eventNumber; 

    uint8_t trk_nTRT;
    int trk_truthPdgId;

    float trk_truthEnergy;
    float trk_truthP;
    float trk_truthProb;
    char trk_hasTruthParticle;
    TLorentzVector truthPartVec;

    float trk_pt;
    float trk_p;
    float trk_d0;
    float trk_z0sintheta;
    float trk_etaEMB2;
    float trk_phiEMB2;
    float trk_etaTileBar2;
    float trk_phiTileBar2;
    float trk_etaTileExt1;
    float trk_phiTileExt1;
    float trk_etaHEC1;
    float trk_phiHEC1;
    float trk_etaEME2;
    float trk_phiEME2;
    float trk_nearest_dR_EM;
    float trk_nearest_dR_HAD;
    float trkWeight;
    uint8_t trk_NPV_2;
    uint8_t trk_NPV_4;
    uint8_t trk_nclusters;
    uint8_t trk_nclusters_EM;
    uint8_t trk_nclusters_hadlike;
    uint8_t trk_nclusters_HAD;
    uint8_t trk_nclusters_emlike;
    char trk_charge;
    char trk_truthFromPileup;
    char trk_truthIsFake;
    float trk_actualmu;
    float trk_averagemu;
    float trk_corrected_averagemu;



    float trk_ClusterEnergy_EM_200;
    float trk_ClusterEnergy_EM_100;
    float  trk_ClusterEnergy_HAD_200;
    float  trk_ClusterEnergy_HAD_100;
    //float  trk_ClusterEnergy_Pos_Total_200;
    //float  trk_ClusterEnergy_Pos_Total_100;
    //float  trk_ClusterEnergy_Total_200;
    //float  trk_ClusterEnergy_Total_100;

    float trk_LCWClusterEnergy_EM_200;
    float trk_LCWClusterEnergy_EM_100;
    float trk_LCWClusterEnergy_HAD_200;
    float trk_LCWClusterEnergy_HAD_100;
    //float trk_LCWClusterEnergy_Pos_Total_200;
    //float trk_LCWClusterEnergy_Pos_Total_100;
    //float trk_LCWClusterEnergy_Total_200;
    //float trk_LCWClusterEnergy_Total_100;

    float trk_CellEnergy_EM_200;
    float trk_CellEnergy_EM_100;
    float trk_CellEnergy_HAD_200;
    float trk_CellEnergy_HAD_100;
    //float trk_CellEnergy_Pos_Total_200;
    //float trk_CellEnergy_Pos_Total_100;
    //float trk_CellEnergy_Total_200;
    //float trk_CellEnergy_Total_100;
    float trk_CellEnergy_EM_nopresampler_100;
    float trk_CellEnergy_EM_nopresampler_200;
    float trk_CellEnergy_Total_nopresampler_100;
    float trk_CellEnergy_Total_nopresampler_200;


    // cutflow
    TH1D* m_cutflowHist; //!
    TH1D* m_cutflowHistW; //!
    int   m_cutflow_bin; //!

    /* object-level cutflow */

    TH1D* m_trk_cutflowHist_1;  //!
    // list of calo layers

    // variables that don't get filled at submission time should be
    // protected from being send from the submission node to the worker
    // node (done by the //!)
    public:
    // Tree *myTree; //!
    // TH1 *myHist; //!

    // tree for saving some key variables
    TTree *m_tree; //!

    // this is a standard constructor
    EoverPTreeAlgo (std::string className = "EoverPTreeAlgo");

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
    const xAOD::TruthParticle* getTruthPtr(const xAOD::TrackParticle* trackParticle); 

    double deltaR (double trk_eta, double trk_phi, double trk2_eta, double trk2_phi);

    std::vector<double> str2vec(std::string str);

    /// @cond
    // this is needed to distribute the algorithm to the workers
    ClassDef(EoverPTreeAlgo, 1);
    /// @endcond
};

#endif
