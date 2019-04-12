// E/p analysis for run 2
// Lukas Adamek (lukas.adamek@cern.ch)

#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>
#include "AthContainers/ConstDataVector.h"
#include "xAODEventInfo/EventInfo.h"
#include "xAODTruth/TruthParticle.h"
#include "xAODAnaHelpers/HelperFunctions.h"
#include <EoverPAnalysis/EoverPTreeAlgo.h>
#include "AsgTools/MessageCheck.h"
#include "TMath.h"

#include "xAODTruth/TruthParticleContainer.h"
#include "xAODTruth/TruthParticle.h"
#include "AthLinks/ElementLink.h"
#include "AthContainers/AuxElement.h"
#include "EoverPAnalysis/EnergySumHelper.h"

// this is needed to distribute the algorithm to the workers
ClassImp(EoverPTreeAlgo)

  EoverPTreeAlgo :: EoverPTreeAlgo (std::string className) :
    Algorithm(className),
    // cutflows
    m_cutflowHist(nullptr),
    m_cutflowHistW(nullptr),
    m_trk_cutflowHist_1(nullptr),
    m_eventNumber(0),
    m_trkIndex(0),
    m_tree(nullptr)
{
  m_inTrackContainerName    = "";
  m_debug                   = false;
}

EL::StatusCode EoverPTreeAlgo :: setupJob (EL::Job& job)
{
  job.useXAOD();
  xAOD::Init("EoverPTreeAlgo").ignore();

  EL::OutputStream outForTree("tree");
  if(!job.outputHas("tree") ){ job.outputAdd ( outForTree ); }

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode EoverPTreeAlgo :: histInitialize ()
{

  Info("histInitialize()", "%s", m_name.c_str() );
  ANA_CHECK(xAH::Algorithm::algInitialize());
  // needed here and not in initalize since this is called first
  if( m_inTrackContainerName.empty()){
    Error("configure()", "One or more required configuration values are empty");
    return EL::StatusCode::FAILURE;
  }

  if(m_useCutFlow) {
    TFile *file = wk()->getOutputFile ("cutflow");
    m_trk_cutflowHist_1  = (TH1D*)file->Get("cutflow_trks_1");
  }

  return EL::StatusCode::SUCCESS;
}

typedef ElementLink<xAOD::TruthParticleContainer> TruthLink_t;
static SG::AuxElement::Accessor<TruthLink_t> LINKTOTRUTH("truthParticleLink");
const xAOD::TruthParticle* EoverPTreeAlgo :: getTruthPtr(const xAOD::TrackParticle* trackParticle) {
  const xAOD::TruthParticle *result = nullptr;
  if ( LINKTOTRUTH.isAvailable(*trackParticle) ) {
    const TruthLink_t link = trackParticle->auxdata<TruthLink_t>("truthParticleLink");
    if ( link.isValid() ) {
      result = *link;
    }
  }
  return result;
}


EL::StatusCode EoverPTreeAlgo :: fileExecute () { return EL::StatusCode::SUCCESS; }
EL::StatusCode EoverPTreeAlgo :: changeInput (bool /*firstFile*/) { return EL::StatusCode::SUCCESS; }

EL::StatusCode EoverPTreeAlgo :: initialize ()
{
  std::string a;
  for(std::stringstream sst(m_energyCalibCommaList); getline(sst, a, ','); )  // that's all ! 
     m_energyCalibList.push_back(a);

  for(std::stringstream sst(m_radiusCutCommaList); getline(sst, a, ','); )  // that's all ! 
     m_radiusCutList.push_back(a);

  Info("initialize()", "EoverPTreeAlgo");
  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  // setup the tree output
  ANA_MSG_DEBUG("Registering Output Tree");
  TFile* treeFile = wk()->getOutputFile ("tree");
  treeFile->mkdir(m_name.c_str());
  treeFile->cd(m_name.c_str());

  ANA_MSG_DEBUG("Tree Regiestered");
  std::string treeName = m_name+"_tree";
  if (m_tree == nullptr)
    m_tree = new TTree(treeName.c_str(),treeName.c_str());
  if (m_tree ==  nullptr) {
    Error("execute()","Failed to instantiate output tree!");
    return EL::StatusCode::FAILURE;
  }

  ANA_MSG_DEBUG("Adding a tree with name " + treeName);
  treeFile->ls(m_name.c_str());

  ANA_MSG_DEBUG("Setting the directory of the tree");
  TDirectory *dir = treeFile->GetDirectory(m_name.c_str());
  if (dir) m_tree->SetDirectory(dir);
  else ANA_MSG_ERROR("The output directory doesn't exist!");
      
  ANA_MSG_DEBUG("Adding the tree to the output");
  wk()->addOutput( m_tree );

  ANA_MSG_DEBUG("Registering Tree Branches");
  //m_tree->Branch("eventNumber",   &m_eventNumber,   "EventNumber/l"); I don't think we need this variable
  m_tree->Branch("trkIndex",      &m_trkIndex);
  m_tree->Branch("trk_etaID", &trk_etaID);
  m_tree->Branch("trk_phiID", &trk_phiID);
  m_tree->Branch("trk_pt", &trk_pt);
  m_tree->Branch("trk_d0", &trk_d0);
  m_tree->Branch("trk_nTRT", &trk_nTRT);
  m_tree->Branch("trk_charge", &trk_charge);
  m_tree->Branch("trk_z0sintheta", &trk_z0sintheta);
  m_tree->Branch("trk_p", &trk_p);
  m_tree->Branch("trk_etaEMB2", &trk_etaEMB2);
  m_tree->Branch("trk_phiEMB2", &trk_phiEMB2);
  m_tree->Branch("trk_etaEME2", &trk_etaEME2);
  m_tree->Branch("trk_phiEME2", &trk_phiEME2);
  m_tree->Branch("trk_etaTileBar2", &trk_etaTileBar2);
  m_tree->Branch("trk_phiTileBar2", &trk_phiTileBar2);
  m_tree->Branch("trk_etaTileExt1", &trk_etaTileExt1);
  m_tree->Branch("trk_phiTileExt1", &trk_phiTileExt1);
  m_tree->Branch("trk_etaHEC1", &trk_etaHEC1);
  m_tree->Branch("trk_phiHEC1", &trk_phiHEC1);
  m_tree->Branch("trk_nearest_dR_EM", &trk_nearest_dR_EM);
  m_tree->Branch("trk_nearest_dR_HAD", &trk_nearest_dR_HAD);
  m_tree->Branch("trk_nclusters", &trk_nclusters);
  m_tree->Branch("trk_nclusters_EM", &trk_nclusters_EM);
  m_tree->Branch("trk_nclusters_hadlike", &trk_nclusters_hadlike);
  m_tree->Branch("trk_nclusters_HAD", &trk_nclusters_HAD);
  m_tree->Branch("trk_nclusters_emlike", &trk_nclusters_emlike);
  m_tree->Branch("trkWeight", &trkWeight);
  m_tree->Branch("trk_NPV_2", &trk_NPV_2);
  m_tree->Branch("trk_NPV_4", &trk_NPV_4);
  m_tree->Branch("trk_hasTruthParticle", &trk_hasTruthParticle);
  m_tree->Branch("trk_truthPdgId", &trk_truthPdgId);
  m_tree->Branch("trk_truthEnergy", &trk_truthEnergy);
  m_tree->Branch("trk_truthP", &trk_truthP);
  m_tree->Branch("trk_truthProb", &trk_truthProb);
  m_tree->Branch("trk_actualmu", &trk_actualmu);
  m_tree->Branch("trk_averagemu", &trk_averagemu);
  m_tree->Branch("trk_corrected_averagemu", &trk_corrected_averagemu);

  //All energy deposits in EM-Calorimeter and HAD-Calorimeter
  for (std::string energyCalib : m_energyCalibList){
      for (std::string radiusCut : m_radiusCutList){
          ANA_MSG_INFO("Made ttree branches for energy of clusters at scale " + energyCalib + " and cut " + radiusCut);
          std::string key_EM = "trk_" + energyCalib + "_EM_" + radiusCut;
          m_energyVariablesForTree[key_EM] = 0.0;
          std::string key_HAD = "trk_" + energyCalib + "_HAD_" + radiusCut;
          m_energyVariablesForTree[key_HAD] = 0.0;
          m_tree->Branch(("trk_" + energyCalib + "_EM_" + radiusCut).c_str(), &(m_energyVariablesForTree[key_EM]));
          m_tree->Branch(("trk_" + energyCalib + "_HAD_" + radiusCut).c_str(), &(m_energyVariablesForTree[key_HAD]));
      }
  }

  ANA_MSG_DEBUG("Getting the cuflows");
  if(m_useCutFlow) {
    TFile *file = wk()->getOutputFile ("cutflow");
    // retrieve the object cutflow
    m_trk_cutflowHist_1  = (TH1D*)file->Get("cutflow_trks_1");
  }

  const xAOD::EventInfo* eventInfo(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, m_eventInfoContainerName, m_event, m_store));
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode EoverPTreeAlgo :: execute ()
{
  // retrieve event
  const xAOD::EventInfo* eventInfo(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, m_eventInfoContainerName, m_event, m_store ));
  //  1.) the PU weight ("PileupWeight")
  //  2.) the corrected mu ("corrected_averageInteractionsPerCrossing")
  float eventWeight(1.);
  if( eventInfo->isAvailable< float >( "mcEventWeight" ) ) {
    eventWeight = eventInfo->auxdecor< float >( "mcEventWeight" );
    static SG::AuxElement::ConstAccessor< float > weight_pileup ("PileupWeight");
    if (weight_pileup.isAvailable(*eventInfo)){
        float pileupWeight(0.);
        pileupWeight = weight_pileup(*eventInfo);
        eventWeight *= pileupWeight;
    }
  }
  else {ANA_MSG_ERROR("No Event Weight Available");}

  m_eventNumber = -1;
  m_trkIndex = -1;

  const xAOD::VertexContainer *vtxs(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(vtxs, "PrimaryVertices", m_event, m_store) );

  const xAOD::TrackParticleContainer* trks(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(trks, m_inTrackContainerName, m_event, m_store) );

  SG::AuxElement::ConstAccessor< float > acc_dRToNearestTrackInEM("dRToNearestTrackInEM");
  SG::AuxElement::ConstAccessor< float > acc_dRToNearestTrackInHAD("dRToNearestTrackInHAD");

  // loop over all tracks only once
  for(auto trk: *trks){
    ANA_MSG_DEBUG("Beginning track loop");

    if (trk->auxdata<int>("CALO_extrapolation") == 0) continue;
    ANA_MSG_DEBUG("Track has CALO extrapolation");
    if (m_useCutFlow) m_trk_cutflowHist_1->Fill("Has calo extrapolation", 1.0);

    if (acc_dRToNearestTrackInEM.isAvailable(*trk)) trk_nearest_dR_EM = acc_dRToNearestTrackInEM(*trk);
    else {ANA_MSG_WARNING("Coulnd't find the decorator for the dR to the nearest track"); trk_nearest_dR_EM = -1.0;}

    if (acc_dRToNearestTrackInHAD.isAvailable(*trk)) trk_nearest_dR_HAD= acc_dRToNearestTrackInHAD(*trk);
    else {ANA_MSG_WARNING("Coulnd't find the decorator for the dR to the nearest track"); trk_nearest_dR_HAD = -1.0;}

    //This is the track pT
    trk_pt = trk->pt()/1e3;

    //Get the value of the eta and phi co-ordinates when extrapolated to the EMB/EME
    trk_etaEMB2 = trk->auxdata<float>("CALO_trkEta_EMB2");
    trk_phiEMB2 = trk->auxdata<float>("CALO_trkPhi_EMB2");

    // EME2
    trk_etaEME2 = trk->auxdata<float>("CALO_trkEta_EME2");
    trk_phiEME2 = trk->auxdata<float>("CALO_trkPhi_EME2");

    //TileBar2
    trk_etaTileBar2 = trk->auxdata<float>("CALO_trkEta_TileBar2");
    trk_phiTileBar2 = trk->auxdata<float>("CALO_trkPhi_TileBar2");

    //TileExt1
    trk_etaTileExt1 = trk->auxdata<float>("CALO_trkEta_TileExt1");
    trk_phiTileExt1 = trk->auxdata<float>("CALO_trkPhi_TileExt1");

    //HEC1
    trk_etaHEC1 = trk->auxdata<float>("CALO_trkEta_HEC1");
    trk_phiHEC1 = trk->auxdata<float>("CALO_trkPhi_HEC1");

    trk_d0 = trk->d0(); //This is the correct d0
    trk_z0sintheta = trk->z0() * TMath::Sin(trk->theta()); //This isn't the correct impact parameter w.r.t the primary vertex

    //get the track momentum from q/p
    trk_p = 0.0;
    if (fabs(trk->qOverP())>0.) trk_p = (1./fabs(trk->qOverP()))/1e3; 
    trk_charge = (trk->qOverP()>0.) ? 1 : -1;

    // coordinates of the track in the ID
    trk_etaID = trk->eta();
    trk_phiID = trk->phi();

    trkWeight = eventWeight;//The track weight is just the event weight

    //Sum all energy deposits in the EM calorimeter and the HAD caloriemter with different radius cuts
    for (std::string energyCalib : m_energyCalibList){
        for (std::string radiusCut : m_radiusCutList){
            std::string key_EM = "trk_" + energyCalib + "_EM_" + radiusCut;
            m_energyVariablesForTree[key_EM] = 0.0;
            std::string key_HAD = "trk_" + energyCalib + "_HAD_" + radiusCut;
            m_energyVariablesForTree[key_HAD] = 0.0;
            std::map<std::string, float> energySum = EnergySumHelper::getEnergySumInCalorimeterRegions(trk,energyCalib,radiusCut,false);
            m_energyVariablesForTree[key_HAD] = energySum["HAD"];
            m_energyVariablesForTree[key_EM] = energySum["EM"];
        }
    }

    ///////////////////////////////////////Information about the # of clusters ////////////////////////////////////////////////////////////////
    trk_nclusters_EM = 0;
    trk_nclusters_HAD = 0;
    trk_nclusters_hadlike = 0;
    trk_nclusters_emlike = 0;

    SG::AuxElement::ConstAccessor< std::vector<float> > acc_ClusterEnergy_Energy("CALO_ClusterEnergy_Energy");
    SG::AuxElement::ConstAccessor< std::vector<int> > acc_ClusterEnergy_maxEnergyLayer("CALO_ClusterEnergy_maxEnergyLayer");
    SG::AuxElement::ConstAccessor< std::vector<float> > acc_ClusterEnergy_emProbability("CALO_ClusterEnergy_emProbability");
    SG::AuxElement::ConstAccessor< std::vector<float> > acc_ClusterEnergy_dRToTrack("CALO_ClusterEnergy_dRToTrack");

    //make sure that the information is available
    if (acc_ClusterEnergy_Energy.isAvailable(*trk) && acc_ClusterEnergy_maxEnergyLayer.isAvailable(*trk) && acc_ClusterEnergy_emProbability.isAvailable(*trk) ){
      std::vector<float> trk_cluster_energies = acc_ClusterEnergy_Energy(*trk);
      std::vector<int> trk_cluster_maxEnergyLayer = acc_ClusterEnergy_maxEnergyLayer(*trk);
      std::vector<float> trk_cluster_emProbability = acc_ClusterEnergy_emProbability(*trk);
      std::vector<float> trk_cluster_dRToTrack = acc_ClusterEnergy_dRToTrack(*trk);

      //make sure that number of clusters is consistent between different decorations
      if (trk_cluster_energies.size() != trk_cluster_maxEnergyLayer.size()){
         ANA_MSG_ERROR("The cluster vectors do not all have the same length for a given track");
         return EL::StatusCode::FAILURE;
      }

      trk_nclusters = trk_cluster_energies.size();
      ANA_MSG_DEBUG("The number of clusters associated with the track was " + std::to_string(trk_nclusters));

      //Where were the clusters that are associated with the track
      ANA_MSG_DEBUG("Printing out the layer of maximum energy of the clusters");
      for (unsigned int i = 0; i < trk_cluster_maxEnergyLayer.size(); i ++)
      {
         if (trk_cluster_dRToTrack.at(i) > 0.2){continue;} //only count those clsuters within a dR cut of 0.2
         int max_layer = trk_cluster_maxEnergyLayer.at(i);
         ANA_MSG_DEBUG(EnergySumHelper::id_to_layer.at(max_layer));

         if (std::find(EnergySumHelper::layer_EM.begin(), EnergySumHelper::layer_EM.end(), EnergySumHelper::id_to_layer.at(max_layer)) != EnergySumHelper::layer_EM.end()) trk_nclusters_EM += 1;
         if (std::find(EnergySumHelper::layer_HAD.begin(), EnergySumHelper::layer_HAD.end(), EnergySumHelper::id_to_layer.at(max_layer)) != EnergySumHelper::layer_HAD.end()) trk_nclusters_HAD += 1;

         float em_probability = trk_cluster_emProbability.at(i);
         if (em_probability > 0.5) trk_nclusters_emlike += 1;
         else trk_nclusters_hadlike += 1;
      }
      ANA_MSG_DEBUG("This many clusters in the EM calorimeters: "  + std::to_string(trk_nclusters_EM));
      ANA_MSG_DEBUG("This many clusters in the HAD calorimeters: "  + std::to_string(trk_nclusters_HAD));
      ANA_MSG_DEBUG("This many clusters with EM prob greater than 0.5 : "  + std::to_string(trk_nclusters_emlike));
      ANA_MSG_DEBUG("This many clusters with EM prob less than 0.5 : "  + std::to_string(trk_nclusters_hadlike));
    }
    else ANA_MSG_DEBUG("There was no information about the number of clusters associated with the track");

    ///////////////////////////////////////TRUTH INFORMATION ////////////////////////////////////////////////////////////////

    //reset the truth information
    trk_truthPdgId = 0;
    trk_truthEnergy = -999.0;
    trk_truthP = -999.0;
    trk_truthProb = -1.0;
    trk_hasTruthParticle = 0;

    //Get the truth match probability of the track
    static SG::AuxElement::ConstAccessor< float > tmpAcc("truthMatchProbability"); //What is the name of the truth match probabily cut variable?
    if (tmpAcc.isAvailable(*trk)){
        const xAOD::TruthParticle* truthPart = getTruthPtr(trk);
        trk_truthProb = tmpAcc(*trk);
        //check if the track passes the truth match probaility cut
        if (!truthPart) {trk_hasTruthParticle = 0;} //there was a truth match, but the link is broken (or truth particle has energy < 100MeV!)
        else { 
            trk_hasTruthParticle = 1;
            trk_truthPdgId = truthPart->pdgId();
            trk_truthEnergy = truthPart->e()/1000.0;
            truthPartVec.SetPtEtaPhiE(truthPart->pt()/1000.0, truthPart->eta(), truthPart->phi(), truthPart->e()/1000.0);
            trk_truthP = truthPartVec.P()/1000.0;
        }
    }

    ///////////////////////////////////////TRT HITS ////////////////////////////////////////////////////////////////

    // set ttree variables
    m_eventNumber = eventInfo->eventNumber();
    if (!trk->summaryValue(trk_nTRT, xAOD::numberOfTRTHits))ANA_MSG_ERROR("TRT hits not filled");
    ANA_MSG_DEBUG(TString("The number of TRT hits was " + std::to_string (trk_nTRT)));

    ///////////////////////////////////////EVENT VARIABLES ////////////////////////////////////////////////////////////////

    trk_NPV_2 = HelperFunctions::countPrimaryVertices(vtxs, 2);
    trk_NPV_4 = HelperFunctions::countPrimaryVertices(vtxs, 4);
    trk_averagemu = -1;
    trk_actualmu = -1;
    trk_corrected_averagemu = -1;

    // get pileup
    if( eventInfo->isAvailable< float >( "actualInteractionsPerCrossing" ) ) {
      trk_actualmu = eventInfo->actualInteractionsPerCrossing();
    }
    if( eventInfo->isAvailable< float >( "corrected_averageInteractionsPerCrossing" ) && !eventInfo->eventType( xAOD::EventInfo::IS_SIMULATION )) 
      trk_corrected_averagemu = eventInfo->auxdata< float >( "corrected_averageInteractionsPerCrossing" );
    else if( eventInfo->isAvailable< float >( "averageInteractionsPerCrossing" ) )
      trk_averagemu = eventInfo->averageInteractionsPerCrossing();

    m_trkIndex += 1;
    ANA_MSG_DEBUG("Filling Tree");
    m_tree->Fill();
  } // END looping trk

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode EoverPTreeAlgo :: postExecute () { return EL::StatusCode::SUCCESS; }

EL::StatusCode EoverPTreeAlgo :: finalize () { 

  return EL::StatusCode::SUCCESS; 
}

EL::StatusCode EoverPTreeAlgo :: histFinalize ()
{
  ANA_CHECK(xAH::Algorithm::algFinalize());
  return EL::StatusCode::SUCCESS;
}

