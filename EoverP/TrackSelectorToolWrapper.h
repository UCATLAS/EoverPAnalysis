#ifndef EoverP_TrackSelectorToolWrapper_H
#define EoverP_TrackSelectorToolWrapper_H

// EDM include(s):
#include "xAODTracking/VertexContainer.h"
#include "xAODTracking/TrackParticleContainer.h"
#include "InDetTrackSelectionTool/InDetTrackSelectionTool.h"
// #include "TrackVertexAssociationTool/TrackVertexAssociationTool.h"

// algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

// ROOT include(s):
#include "TH1D.h"

class TrackSelectorToolWrapper : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:

  bool m_useCutFlow;            //!

  // configuration variables
  std::string m_inContainerName;      // input container name
  std::string m_outContainerName;     // output container name
  bool  m_decorateSelectedObjects; // decorate selected objects? defaul passSel
  bool  m_createSelectedContainer; // fill using SG::VIEW_ELEMENTS to be light weight
  int   m_nToProcess;               // look at n objects
  int   m_pass_min;                 // minimum number of objects passing cuts
  int   m_pass_max;                 // maximum number of objects passing cuts

  std::string              m_cutLevel; // "NoCut", "Loose", "LoosePrimary", "TightPrimary", "LooseMuon", "LooseElectron", "MinBias", "HILoose", "HITight"
  float m_maxD0;
  float m_maxZ0SinTheta;

  std::string              m_passAuxDecorKeys;
  std::string              m_failAuxDecorKeys;

private:

  std::vector<std::string> m_passKeys;
  std::vector<std::string> m_failKeys;

  int m_numEvent;         //!
  int m_numObject;        //!
  int m_numEventPass;     //!
  int m_numObjectPass;    //!

  // cutflow
  TH1D* m_cutflowHist;          //!
  TH1D* m_cutflowHistW;         //!
  int   m_cutflow_bin;          //!

  // track selection tool
  // https://twiki.cern.ch/twiki/bin/view/AtlasProtected/InDetTrackSelectionTool
  // https://svnweb.cern.ch/trac/atlasoff/browser/InnerDetector/InDetRecTools/InDetTrackSelectionTool
  InDet::InDetTrackSelectionTool *m_selTool; //!
  // CP::LooseTrackVertexAssociationTool *m_trktovxtool; //! 

  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:
  // Tree *myTree; //!
  // TH1 *myHist; //!

  // this is a standard constructor
  TrackSelectorToolWrapper(std::string className = "TrackSelectorToolWrapper");

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

  // these are the functions not inherited from Algorithm
  virtual EL::StatusCode configure ();

  // added functions not from Algorithm
  // why does this need to be virtual?

  /// @cond
  // this is needed to distribute the algorithm to the workers
  ClassDef(TrackSelectorToolWrapper, 1);
  /// @endcond
};

#endif
