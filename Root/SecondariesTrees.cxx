/*
  Root/SecondariesTrees.cxx

  M. LeBlanc (Arizona) <matt.leblanc@cern.ch>
  for Run 2 E/p studies on identified resonances.
*/

#include "AsgTools/MessageCheck.h"
#include "EoverPAnalysis/SecondariesTrees.h"
#include "EoverPAnalysis/EnergySumHelper.h"

#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include "TFile.h"
#include "TSystem.h"
#include "TLorentzVector.h"

// EDM include(s):
#include "xAODCaloEvent/CaloClusterContainer.h"
#include "xAODCaloEvent/CaloCluster.h"
#include "xAODCore/ShallowCopy.h"
#include "AthContainers/ConstDataVector.h"
#include "xAODTracking/Vertex.h"

#include "xAODTracking/VertexContainer.h"
#include "xAODJet/JetContainer.h"
#include "xAODJet/JetAuxContainer.h"
#include "xAODTracking/TrackParticleContainer.h"
#include "xAODTruth/TruthParticle.h"
#include "xAODTruth/TruthParticleContainer.h"
#include "xAODEventInfo/EventInfo.h"

SecondariesTrees :: SecondariesTrees (const std::string& name,
					  ISvcLocator *pSvcLocator)
  : EL::AnaAlgorithm (name, pSvcLocator)
{
  declareProperty( "label", m_label = "nominal",
                   "A label for the histograms" );

  declareProperty( "isData", m_isData = false,
                   "Is this data?" );

  declareProperty( "MessageFrequency", m_MessageFrequency = 1000,
		   "Frequency of debug messages" );

  declareProperty( "VertexContainer", m_VertexContainer = "PrimaryVertices",
                   "Input vertex container?" );

  declareProperty( "TrackContainer", m_TrackContainer = "InDetTrackParticlesLoose",
		   "Input track container?" );
}

SecondariesTrees :: ~SecondariesTrees()
{
  // vector output branches need to be cleaned up
  //delete m_jetPt;
}

StatusCode SecondariesTrees :: initialize ()
{
  m_event = wk()->xaodEvent();

  // Histogram booking

  std::string a;
  for(std::stringstream sst(m_energyCalibCommaList); getline(sst, a, ','); )  // that's all ! 
    m_energyCalibList.push_back(a);

  for(std::stringstream sst(m_radiusCutCommaList); getline(sst, a, ','); )  // that's all ! 
    m_radiusCutList.push_back(a);


  ANA_CHECK (book (TH1F ("h_npv_"+m_label, "h_npv_"+m_label, 60, 0, 60))); // NPV
  ANA_CHECK (book (TH1F ("h_mu_"+m_label, "h_mu_"+m_label, 80, 0, 80))); // mu

  ANA_CHECK (book (TH1F ("h_nConstituents_"+m_label, "h_nConstituents_"+m_label, 60, 0, 60))); // nConstituents

  ANA_CHECK (book (TH2F ("h2_DTRatioVsClusterE_"+m_label, "h2_DTRatioVsClusterE_"+m_label, 40, 0, 20, 120, 0, 1.2))); // DigiTruth bread-n-butter
  
  // Output tree
  // This left mostly as an example

  ANA_CHECK (book (TTree(TString("Tree_"+m_label).Data(), "Output Tree")) );
  TTree* t = tree (TString("Tree_"+m_label).Data());

  t->Branch("DSID",&m_DSID);
  t->Branch("weight",&m_weight);
  t->Branch("mcWeight",&m_mcWeight);
  t->Branch("mu",&m_mu);
  t->Branch("npv",&m_npv);
  
  t->Branch("vertex_N",&m_vertex_N);
  t->Branch("vertex_pt",&m_vertex_pt);
  t->Branch("vertex_eta",&m_vertex_eta);
  t->Branch("vertex_phi",&m_vertex_phi);
  t->Branch("vertex_mass",&m_vertex_mass);
  t->Branch("vertex_massErr",&m_vertex_massErr);
  t->Branch("vertex_Rxy",&m_vertex_Rxy);
  t->Branch("vertex_chiSquared",&m_vertex_chiSquared);
  t->Branch("vertex_numberDoF",&m_vertex_numberDoF);
  t->Branch("vertex_dr",&m_vertex_dr);
  t->Branch("vertex_isIsolatedPairEM",&m_vertex_isIsolatedPairEM);
  t->Branch("vertex_isIsolatedPairHAD",&m_vertex_isIsolatedPairHAD);

  // 
  t->Branch("trk1Index",      &m_trk1Index);
  t->Branch("trk1_etaID", &trk1_etaID);
  t->Branch("trk1_phiID", &trk1_phiID);
  t->Branch("trk1_pt", &trk1_pt);
  t->Branch("trk1_d0", &trk1_d0);
  t->Branch("trk1_nTRT", &trk1_nTRT);
  t->Branch("trk1_charge", &trk1_charge);
  t->Branch("trk1_z0sintheta", &trk1_z0sintheta);
  t->Branch("trk1_p", &trk1_p);
  t->Branch("trk1_iso1_EM2", &trk1_iso1_EM2);
  t->Branch("trk1_iso1_HAD2", &trk1_iso1_HAD2);
  t->Branch("trk1_iso2_EM2", &trk1_iso2_EM2);
  t->Branch("trk1_iso2_HAD2", &trk1_iso2_HAD2);
  t->Branch("trk1_etaEMB2", &trk1_etaEMB2);
  t->Branch("trk1_phiEMB2", &trk1_phiEMB2);
  t->Branch("trk1_etaEME2", &trk1_etaEME2);
  t->Branch("trk1_phiEME2", &trk1_phiEME2);
  t->Branch("trk1_etaTileBar2", &trk1_etaTileBar2);
  t->Branch("trk1_phiTileBar2", &trk1_phiTileBar2);
  t->Branch("trk1_etaTileExt1", &trk1_etaTileExt1);
  t->Branch("trk1_phiTileExt1", &trk1_phiTileExt1);
  t->Branch("trk1_etaHEC1", &trk1_etaHEC1);
  t->Branch("trk1_phiHEC1", &trk1_phiHEC1);
  t->Branch("trk1_nearest_dR_EM", &trk1_nearest_dR_EM);
  t->Branch("trk1_nearest_dR_HAD", &trk1_nearest_dR_HAD);
  t->Branch("trk1_nclusters", &trk1_nclusters);
  t->Branch("trk1_nclusters_EM", &trk1_nclusters_EM);
  t->Branch("trk1_nclusters_hadlike", &trk1_nclusters_hadlike);
  t->Branch("trk1_nclusters_HAD", &trk1_nclusters_HAD);
  t->Branch("trk1_nclusters_emlike", &trk1_nclusters_emlike);
  t->Branch("trk1Weight", &trk1Weight);
  t->Branch("trk1_NPV_2", &trk1_NPV_2);
  t->Branch("trk1_NPV_4", &trk1_NPV_4);
  t->Branch("trk1_hasTruthParticle", &trk1_hasTruthParticle);
  t->Branch("trk1_truthPdgId", &trk1_truthPdgId);
  t->Branch("trk1_truthEnergy", &trk1_truthEnergy);
  t->Branch("trk1_truthP", &trk1_truthP);
  t->Branch("trk1_truthProb", &trk1_truthProb);
  t->Branch("trk1_actualmu", &trk1_actualmu);
  t->Branch("trk1_averagemu", &trk1_averagemu);
  t->Branch("trk1_corrected_averagemu", &trk1_corrected_averagemu);

  t->Branch("trk2Index",      &m_trk2Index);
  t->Branch("trk2_etaID", &trk2_etaID);
  t->Branch("trk2_phiID", &trk2_phiID);
  t->Branch("trk2_pt", &trk2_pt);
  t->Branch("trk2_d0", &trk2_d0);
  t->Branch("trk2_nTRT", &trk2_nTRT);
  t->Branch("trk2_charge", &trk2_charge);
  t->Branch("trk2_z0sintheta", &trk2_z0sintheta);
  t->Branch("trk2_p", &trk2_p);
  t->Branch("trk2_iso1_EM2", &trk2_iso1_EM2);
  t->Branch("trk2_iso1_HAD2", &trk2_iso1_HAD2);
  t->Branch("trk2_iso2_EM2", &trk2_iso2_EM2);
  t->Branch("trk2_iso2_HAD2", &trk2_iso2_HAD2);
  t->Branch("trk2_etaEMB2", &trk2_etaEMB2);
  t->Branch("trk2_phiEMB2", &trk2_phiEMB2);
  t->Branch("trk2_etaEME2", &trk2_etaEME2);
  t->Branch("trk2_phiEME2", &trk2_phiEME2);
  t->Branch("trk2_etaTileBar2", &trk2_etaTileBar2);
  t->Branch("trk2_phiTileBar2", &trk2_phiTileBar2);
  t->Branch("trk2_etaTileExt1", &trk2_etaTileExt1);
  t->Branch("trk2_phiTileExt1", &trk2_phiTileExt1);
  t->Branch("trk2_etaHEC1", &trk2_etaHEC1);
  t->Branch("trk2_phiHEC1", &trk2_phiHEC1);
  t->Branch("trk2_nearest_dR_EM", &trk2_nearest_dR_EM);
  t->Branch("trk2_nearest_dR_HAD", &trk2_nearest_dR_HAD);
  t->Branch("trk2_nclusters", &trk2_nclusters);
  t->Branch("trk2_nclusters_EM", &trk2_nclusters_EM);
  t->Branch("trk2_nclusters_hadlike", &trk2_nclusters_hadlike);
  t->Branch("trk2_nclusters_HAD", &trk2_nclusters_HAD);
  t->Branch("trk2_nclusters_emlike", &trk2_nclusters_emlike);
  t->Branch("trk2Weight", &trk2Weight);
  t->Branch("trk2_NPV_2", &trk2_NPV_2);
  t->Branch("trk2_NPV_4", &trk2_NPV_4);
  t->Branch("trk2_hasTruthParticle", &trk2_hasTruthParticle);
  t->Branch("trk2_truthPdgId", &trk2_truthPdgId);
  t->Branch("trk2_truthEnergy", &trk2_truthEnergy);
  t->Branch("trk2_truthP", &trk2_truthP);
  t->Branch("trk2_truthProb", &trk2_truthProb);
  t->Branch("trk2_actualmu", &trk2_actualmu);
  t->Branch("trk2_averagemu", &trk2_averagemu);
  t->Branch("trk2_corrected_averagemu", &trk2_corrected_averagemu);

  //All energy deposits in EM-Calorimeter and HAD-Calorimeter
  for (std::string energyCalib : m_energyCalibList)
    {
      for (std::string radiusCut : m_radiusCutList)
	{
	  ANA_MSG_INFO("Made ttree branches for energy of clusters at scale " + energyCalib + " and cut " + radiusCut);
	  std::string key1_EM = "trk1_" + energyCalib + "_EM_" + radiusCut;
	  m_energyVariablesForTree[key1_EM] = 0.0;
	  std::string key1_HAD = "trk1_" + energyCalib + "_HAD_" + radiusCut;
	  m_energyVariablesForTree[key1_HAD] = 0.0;
	  std::string key2_EM = "trk2_" + energyCalib + "_EM_" + radiusCut;
	  m_energyVariablesForTree[key2_EM] = 0.0;
	  std::string key2_HAD = "trk2_" + energyCalib + "_HAD_" + radiusCut;
	  m_energyVariablesForTree[key2_HAD] = 0.0;
	  t->Branch(("trk1_" + energyCalib + "_EM_" + radiusCut).c_str(), &(m_energyVariablesForTree[key1_EM]));
	  t->Branch(("trk1_" + energyCalib + "_HAD_" + radiusCut).c_str(), &(m_energyVariablesForTree[key1_HAD]));
	  t->Branch(("trk2_" + energyCalib + "_EM_" + radiusCut).c_str(), &(m_energyVariablesForTree[key2_EM]));
	  t->Branch(("trk2_" + energyCalib + "_HAD_" + radiusCut).c_str(), &(m_energyVariablesForTree[key2_HAD]));
	}
    }
    
  return StatusCode::SUCCESS;
}

StatusCode SecondariesTrees :: execute ()
{
  static int count = 0;
  bool debug=false;
  if(count==0)
    {
      debug = true;
      std::cout << "SecondariesTrees :: execute() BEGIN" << std::endl;
    }
  count++;
  if(count % m_MessageFrequency == 0) debug = true; // Defaults to print every 1000 events

  if(debug) std::cout << "SecondariesTrees :: execute()\tProcessing event " << count << ". "  << std::endl;

  // NPV and mu
  int npv = 0;
  const xAOD::VertexContainer* PrimaryVertices = 0;
  m_event->retrieve(PrimaryVertices,m_VertexContainer.Data());
  for(const auto vertex : *PrimaryVertices)
    if(vertex->trackParticleLinks().size() >= 2)
      npv++;  
  m_npv = npv;
  m_vertex_N = npv;

  if(debug) std::cout << "SecondariesTrees :: execute()\t" << npv << " primary vertices!" << std::endl; 

  // Track particles
  const xAOD::TrackParticleContainer* TrackParticles = 0;
  m_event->retrieve(TrackParticles, m_TrackContainer.Data());

  // Truth particles
  const xAOD::TruthParticleContainer* TruthParticles = 0;
  if(!m_isData) m_event->retrieve(TruthParticles, "TruthParticles");
  
  // Event weights
  const xAOD::EventInfo* eventInfo = 0;
  if( !m_event->retrieve( eventInfo, "EventInfo" ).isSuccess()) return EL::StatusCode::FAILURE;
  
  Float_t weight = 1.0;

  if(!m_isData)
    {
      Float_t mc_weight = eventInfo->mcEventWeight();
      Int_t dsid = eventInfo->mcChannelNumber();
      
      weight *= mc_weight;
      
      float xs = 1.;
      
      // R21
      if(dsid==361020) xs=(78420000000000./15527000.); // xSec*FE/evnts in fb !!!!!
      if(dsid==361021) xs=(78420000000000./15997000.);
      if(dsid==361022) xs=(2433200000000.*3.3423E-04/15983000.);
      if(dsid==361023) xs=(2433200000000.*3.3423E-04/15983000.);
      if(dsid==361024) xs=(254630000.*5.3138E-04/15978500.);
      if(dsid==361025) xs=(4553500.*9.2409E-04/15991500.);
      if(dsid==361026) xs=(257530.000*9.4092E-04/17834000.);
      if(dsid==361027) xs=(16215.*3.9280E-04/15118500.);
      if(dsid==361028) xs=(625.030*6.2503E-04/15997000.);
      if(dsid==361029) xs=(19.639*1.2076E-02/14552500.);
      if(dsid==361030) xs=(1.196*5.9087E-03/15998000.);
      if(dsid==361031) xs=(0.042*2.6761E-03/15973000.);
      if(dsid==361032) xs=(0.0010367*4.2592E-04/15070000.);
      
      weight *= xs;

      m_mcWeight = mc_weight;
      m_weight = weight;
    }
  
  for(const auto vertex : *PrimaryVertices)
    {
      //std::cout << vertex->trackParticleLinks().size() << " tracks on vertex" << std::endl;         
      TLorentzVector tlv_vertex;
      if(vertex->trackParticleLinks().size()!=2) continue;
      else
	{
	  //This is the track pT, and coordinates of the track in the ID	  	  	  
	  trk1_pt = vertex->trackParticle(0)->pt()/1.e3;
	  trk1_etaID = vertex->trackParticle(0)->eta();
	  trk1_phiID = vertex->trackParticle(0)->phi();
	  //m_track1_m = vertex->trackParticle(0)->m()/1.e3;
	  trk1_p = 0.0; //get the track momentum from q/p
	  if (fabs(vertex->trackParticle(0)->qOverP())>0.) trk1_p = (1./fabs(vertex->trackParticle(0)->qOverP()))/1e3; 
	  trk1_charge = (vertex->trackParticle(0)->qOverP()>0.) ? 1 : -1;
	  
	  trk2_pt = vertex->trackParticle(1)->pt()/1.e3;
	  trk2_etaID = vertex->trackParticle(1)->eta();
          trk2_phiID = vertex->trackParticle(1)->phi();
	  //m_track2_m = vertex->trackParticle(1)->m()/1.e3;
	  trk2_p = 0.0; //get the track momentum from q/p
	  if (fabs(vertex->trackParticle(1)->qOverP())>0.) trk2_p = (1./fabs(vertex->trackParticle(1)->qOverP()))/1e3;
          trk2_charge = (vertex->trackParticle(1)->qOverP()>0.) ? 1 : -1;

	  if(m_label=="Lambda")
	    {
	      if(trk1_pt > trk2_pt) trk1_m = 0.938272;
	      else if (trk1_pt < trk2_pt) trk2_m = 0.938272;
	    }
	  if(m_label=="Ks")
            {
              trk1_m = 0.13957;
              trk2_m = 0.13957;
            }
	  if(m_label=="Phi")
            {
              trk1_m = 0.493677;
              trk2_m = 0.493677;
            }
	}

      TLorentzVector tlv_track1;
      tlv_track1.SetPtEtaPhiM(trk1_pt, 
			      trk1_etaID,
			      trk1_phiID,
			      trk1_m);
      
      TLorentzVector tlv_track2;
      tlv_track2.SetPtEtaPhiM(trk2_pt,
                              trk2_etaID,
                              trk2_phiID,
                              trk2_m);

      static SG::AuxElement::ConstAccessor< float > acc_iso1_EM2("dRToNearestTrackInEM");
      static SG::AuxElement::ConstAccessor< float > acc_iso1_HAD2("dRToNearestTrackInHAD");
      static SG::AuxElement::ConstAccessor< float > acc_iso2_EM2("dRToSecondNearestTrackInEM");
      static SG::AuxElement::ConstAccessor< float > acc_iso2_HAD2("dRToSecondNearestTrackInHAD");

      if( acc_iso1_EM2.isAvailable(*vertex->trackParticle(0)))  trk1_iso1_EM2  = acc_iso1_EM2(*vertex->trackParticle(0));
      if( acc_iso1_HAD2.isAvailable(*vertex->trackParticle(0))) trk1_iso1_HAD2 = acc_iso1_HAD2(*vertex->trackParticle(0));
      if( acc_iso2_EM2.isAvailable(*vertex->trackParticle(0)))  trk1_iso2_EM2  = acc_iso2_EM2(*vertex->trackParticle(0));
      if( acc_iso2_HAD2.isAvailable(*vertex->trackParticle(0))) trk1_iso2_HAD2 = acc_iso2_HAD2(*vertex->trackParticle(0));

      if( acc_iso1_EM2.isAvailable(*vertex->trackParticle(1)))  trk2_iso1_EM2  = acc_iso1_EM2(*vertex->trackParticle(1));
      if( acc_iso1_HAD2.isAvailable(*vertex->trackParticle(1))) trk2_iso1_HAD2 = acc_iso1_HAD2(*vertex->trackParticle(1));
      if( acc_iso2_EM2.isAvailable(*vertex->trackParticle(1)))  trk2_iso2_EM2  = acc_iso2_EM2(*vertex->trackParticle(1));
      if( acc_iso2_HAD2.isAvailable(*vertex->trackParticle(1))) trk2_iso2_HAD2 = acc_iso2_HAD2(*vertex->trackParticle(1));

      if(debug)
	{
	  std::cout << "track 1 isolation: nearest\tEM " << trk1_iso1_EM2 << " HAD " << trk1_iso1_HAD2 
		    << "\tnext\tEM " << trk1_iso2_EM2 << " HAD " << trk1_iso2_HAD2 << std::endl
		    << "track 2 isolation: nearest\tEM " << trk2_iso1_EM2 << " HAD " <<trk2_iso1_HAD2
		    << "\tnext\tEM " <<trk2_iso2_EM2 << " HAD " << trk2_iso2_HAD2 << std::endl;	   
	}

      tlv_vertex.Clear();
      tlv_vertex += tlv_track1;
      tlv_vertex += tlv_track2;

      if(debug) std::cout << "Track1 4vec:\tpt: " << tlv_track1.Pt() <<"\teta: "
			  << tlv_track1.Eta() << "\tphi: " << tlv_track1.Phi()
			  << "\tm: " << tlv_track1.M()
			  << std::endl;
      
      if(debug) std::cout << "Track2 4vec:\tpt: " << tlv_track2.Pt() <<"\teta: "
                          << tlv_track2.Eta() << "\tphi: " << tlv_track2.Phi()
                          << "\tm: " << tlv_track2.M()
                          << std::endl;
    
      if(debug) std::cout << "Vertex 4vec:\tpt: " << tlv_vertex.Pt() <<"\teta: "
			  << tlv_vertex.Eta() << "\tphi: " << tlv_vertex.Phi()
			  << "\tm: " << tlv_vertex.M()
			  << std::endl;

      static SG::AuxElement::ConstAccessor< float > acc_chiSquared("chiSquared");
      if(acc_chiSquared.isAvailable(*vertex) ) m_vertex_chiSquared = acc_chiSquared(*vertex);
      
      static SG::AuxElement::ConstAccessor< float > acc_numberDoF("numberDoF");
      if(acc_numberDoF.isAvailable(*vertex) ) m_vertex_numberDoF = acc_numberDoF(*vertex);

      if(m_label=="Lambda")
	{
	  static SG::AuxElement::ConstAccessor< float > acc_Lambda_mass("Lambda_mass");
	  static SG::AuxElement::ConstAccessor< float > acc_Lambda_massErr("Lambda_massErr");
	  if( acc_Lambda_mass.isAvailable(*vertex) ) m_vertex_mass = acc_Lambda_mass(*vertex);
	  if( acc_Lambda_massErr.isAvailable(*vertex) ) m_vertex_massErr = acc_Lambda_massErr(*vertex);
	}

      if(m_label=="Ks")
	{
          static SG::AuxElement::ConstAccessor< float > acc_Ks_mass("Ks_mass");
          static SG::AuxElement::ConstAccessor< float > acc_Ks_massErr("Ks_massErr");
          if( acc_Ks_mass.isAvailable(*vertex) ) m_vertex_mass = acc_Ks_mass(*vertex);
          if( acc_Ks_massErr.isAvailable(*vertex) ) m_vertex_massErr = acc_Ks_massErr(*vertex);
	}
      
      if(m_label=="Phi")
	{
          static SG::AuxElement::ConstAccessor< float > acc_Phi_mass("Phi_mass");
          static SG::AuxElement::ConstAccessor< float > acc_Phi_massErr("Phi_massErr");
          if( acc_Phi_mass.isAvailable(*vertex) ) m_vertex_mass = acc_Phi_mass(*vertex);
          if( acc_Phi_massErr.isAvailable(*vertex) ) m_vertex_massErr = acc_Phi_massErr(*vertex);
	}

      m_vertex_pt = tlv_vertex.Pt();
      m_vertex_eta = tlv_vertex.Eta();
      m_vertex_phi = tlv_vertex.Phi();

      m_vertex_dr = tlv_track1.DeltaR(tlv_track2);

      m_vertex_Rxy = vertex->position().perp();
     
      m_vertex_isIsolatedPairEM = 0;      
      static SG::AuxElement::ConstAccessor< ElementLink<xAOD::TrackParticleContainer > > acc_nearestEMLink("LinkToNearestTrackInEM");
      if(acc_nearestEMLink.isAvailable(*vertex->trackParticle(0)) && acc_nearestEMLink.isAvailable(*vertex->trackParticle(1)))
	if(acc_nearestEMLink(*vertex->trackParticle(0)).isValid() && acc_nearestEMLink(*vertex->trackParticle(1)).isValid())	 
	  if( (*acc_nearestEMLink(*vertex->trackParticle(0)) == vertex->trackParticle(1))
	      && (*acc_nearestEMLink(*vertex->trackParticle(1)) == vertex->trackParticle(0)))
	    m_vertex_isIsolatedPairEM=1;
	  
      m_vertex_isIsolatedPairHAD = 0;
      static SG::AuxElement::ConstAccessor< ElementLink<xAOD::TrackParticleContainer > > acc_nearestHADLink("LinkToNearestTrackInHAD");
      if(acc_nearestHADLink.isAvailable(*vertex->trackParticle(0)) && acc_nearestHADLink.isAvailable(*vertex->trackParticle(1)))
	if(acc_nearestHADLink(*vertex->trackParticle(0)).isValid() && acc_nearestHADLink(*vertex->trackParticle(1)).isValid())
	  if( (*acc_nearestHADLink(*vertex->trackParticle(0)) == vertex->trackParticle(1))
	      && (*acc_nearestHADLink(*vertex->trackParticle(1)) == vertex->trackParticle(0)) )
	    m_vertex_isIsolatedPairHAD=1;

      // Track e/p stuff

      //Sum all energy deposits in the EM calorimeter and the HAD caloriemter with different radius cuts
      for (std::string energyCalib : m_energyCalibList)
	{
	  for (std::string radiusCut : m_radiusCutList)
	    {
	      std::string key_EM1 = "trk1_" + energyCalib + "_EM_" + radiusCut;
	      m_energyVariablesForTree[key_EM1] = 0.0;
	      std::string key_HAD1 = "trk1_" + energyCalib + "_HAD_" + radiusCut;
	      m_energyVariablesForTree[key_HAD1] = 0.0;

	      std::string key_EM2 = "trk2_" + energyCalib + "_EM_" + radiusCut;
	      m_energyVariablesForTree[key_EM2] = 0.0;
	      std::string key_HAD2 = "trk2_" + energyCalib + "_HAD_" + radiusCut;
              m_energyVariablesForTree[key_HAD2] = 0.0;

	      std::map<std::string, float> energySum1 = EnergySumHelper::getEnergySumInCalorimeterRegions(vertex->trackParticle(0),energyCalib,radiusCut,false);
	      std::map<std::string, float> energySum2 = EnergySumHelper::getEnergySumInCalorimeterRegions(vertex->trackParticle(1),energyCalib,radiusCut,false);
	      m_energyVariablesForTree[key_HAD1] = energySum1["HAD"];
	      m_energyVariablesForTree[key_EM1] = energySum1["EM"];
	      m_energyVariablesForTree[key_HAD2] = energySum2["HAD"];
              m_energyVariablesForTree[key_EM2] = energySum2["EM"];
	    }
	}

      ///////////////////////////////////////Information about the # of clusters ////////////////////////////////////////////////////////////////
      trk1_nclusters_EM = 0;
      trk1_nclusters_HAD = 0;
      trk1_nclusters_hadlike = 0;
      trk1_nclusters_emlike = 0;

      trk2_nclusters_EM = 0;
      trk2_nclusters_HAD = 0;
      trk2_nclusters_hadlike = 0;
      trk2_nclusters_emlike = 0;

      SG::AuxElement::ConstAccessor< std::vector<float> > acc_ClusterEnergy_Energy("CALO_ClusterEnergy_Energy");
      SG::AuxElement::ConstAccessor< std::vector<int> > acc_ClusterEnergy_maxEnergyLayer("CALO_ClusterEnergy_maxEnergyLayer");
      SG::AuxElement::ConstAccessor< std::vector<float> > acc_ClusterEnergy_emProbability("CALO_ClusterEnergy_emProbability");

      // TRACK ONE
      //make sure that the information is available
      if (acc_ClusterEnergy_Energy.isAvailable(*vertex->trackParticle(0)) 
	  && acc_ClusterEnergy_maxEnergyLayer.isAvailable(*vertex->trackParticle(0)) 
	  && acc_ClusterEnergy_emProbability.isAvailable(*vertex->trackParticle(0)) )
	{
	  std::vector<float> trk_cluster_energies = acc_ClusterEnergy_Energy(*vertex->trackParticle(0));
	  std::vector<int> trk_cluster_maxEnergyLayer = acc_ClusterEnergy_maxEnergyLayer(*vertex->trackParticle(0));
	  std::vector<float> trk_cluster_emProbability = acc_ClusterEnergy_emProbability(*vertex->trackParticle(0));
	  
	  //make sure that number of clusters is consistent between different decorations
	  if (trk_cluster_energies.size() != trk_cluster_maxEnergyLayer.size())
	    {
	      ANA_MSG_ERROR("The cluster vectors do not all have the same length for a given track");
	      return EL::StatusCode::FAILURE;
	    }
	  
	  trk1_nclusters = trk_cluster_energies.size();
	  ANA_MSG_DEBUG("The number of clusters associated with the track was " + std::to_string(trk1_nclusters));
	  
	  //Where were the clusters that are associated with the track
	  ANA_MSG_DEBUG("Printing out the layer of maximum energy of the clusters");
	  for (unsigned int i = 0; i < trk_cluster_maxEnergyLayer.size(); i ++)
	    {
	      int max_layer = trk_cluster_maxEnergyLayer.at(i);
	      ANA_MSG_DEBUG(EnergySumHelper::id_to_layer.at(max_layer));
	      
	      if (std::find(EnergySumHelper::layer_EM.begin(),
			    EnergySumHelper::layer_EM.end(),
			    EnergySumHelper::id_to_layer.at(max_layer)) != EnergySumHelper::layer_EM.end())
		trk1_nclusters_EM += 1;
	      if (std::find(EnergySumHelper::layer_HAD.begin(),
			    EnergySumHelper::layer_HAD.end(),
			    EnergySumHelper::id_to_layer.at(max_layer)) != EnergySumHelper::layer_HAD.end())
		trk1_nclusters_HAD += 1;
	      
	      float em_probability = trk_cluster_emProbability.at(i);
	      if (em_probability > 0.5) trk1_nclusters_emlike += 1;
	      else trk1_nclusters_hadlike += 1;
	    }
	  
	  ANA_MSG_DEBUG("Track 1 clusters in the EM calorimeters: "  + std::to_string(trk1_nclusters_EM));
	  ANA_MSG_DEBUG("Track 1 clusters in the HAD calorimeters: "  + std::to_string(trk1_nclusters_HAD));
	  ANA_MSG_DEBUG("Track 1 clusters with EM prob greater than 0.5 : "  + std::to_string(trk1_nclusters_emlike));
	  ANA_MSG_DEBUG("Track 1 clusters with EM prob less than 0.5 : " + std::to_string(trk1_nclusters_hadlike));
	}

      // TRACK TWO
      //make sure that the information is available
      if (acc_ClusterEnergy_Energy.isAvailable(*vertex->trackParticle(1))
          && acc_ClusterEnergy_maxEnergyLayer.isAvailable(*vertex->trackParticle(1))
          && acc_ClusterEnergy_emProbability.isAvailable(*vertex->trackParticle(1)) )
	{
	  std::vector<float> trk_cluster_energies = acc_ClusterEnergy_Energy(*vertex->trackParticle(1));
	  std::vector<int> trk_cluster_maxEnergyLayer = acc_ClusterEnergy_maxEnergyLayer(*vertex->trackParticle(1));
	  std::vector<float> trk_cluster_emProbability = acc_ClusterEnergy_emProbability(*vertex->trackParticle(1));
	  
          //make sure that number of clusters is consistent between different decorations
          if (trk_cluster_energies.size() != trk_cluster_maxEnergyLayer.size())
            {
              ANA_MSG_ERROR("The cluster vectors do not all have the same length for a given track");
              return EL::StatusCode::FAILURE;
            }

          trk2_nclusters = trk_cluster_energies.size();
          ANA_MSG_DEBUG("The number of clusters associated with the track was " + std::to_string(trk2_nclusters));

          //Where were the clusters that are associated with the track
          ANA_MSG_DEBUG("Printing out the layer of maximum energy of the clusters");
	  for (unsigned int i = 0; i < trk_cluster_maxEnergyLayer.size(); i ++)
            {
              int max_layer = trk_cluster_maxEnergyLayer.at(i);
              ANA_MSG_DEBUG(EnergySumHelper::id_to_layer.at(max_layer));

              if (std::find(EnergySumHelper::layer_EM.begin(),
                            EnergySumHelper::layer_EM.end(),
                            EnergySumHelper::id_to_layer.at(max_layer)) != EnergySumHelper::layer_EM.end())
		trk2_nclusters_EM += 1;
              if (std::find(EnergySumHelper::layer_HAD.begin(),
                            EnergySumHelper::layer_HAD.end(),
                            EnergySumHelper::id_to_layer.at(max_layer)) != EnergySumHelper::layer_HAD.end())
		trk2_nclusters_HAD += 1;

              float em_probability = trk_cluster_emProbability.at(i);
              if (em_probability > 0.5) trk2_nclusters_emlike += 1;
              else trk2_nclusters_hadlike += 1;
            }

	  ANA_MSG_DEBUG("Track 2 clusters in the EM calorimeters: "  + std::to_string(trk2_nclusters_EM));
          ANA_MSG_DEBUG("Track 2 clusters in the HAD calorimeters: "  + std::to_string(trk2_nclusters_HAD));
	  ANA_MSG_DEBUG("Track 2 clusters with EM prob greater than 0.5 : "  + std::to_string(trk2_nclusters_emlike));
          ANA_MSG_DEBUG("Track 2 clusters with EM prob less than 0.5 : " + std::to_string(trk2_nclusters_hadlike));
	}

	// Fill for every vertex??
      tree (TString("Tree_"+m_label).Data())->Fill ();
    }  
    
  // fill the branches  
  //tree (TString("Tree_"+m_label).Data())->Fill (); 

  return StatusCode::SUCCESS;
}


StatusCode SecondariesTrees :: finalize ()
{
  return StatusCode::SUCCESS;
}
