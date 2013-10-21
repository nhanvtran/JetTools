// -*- C++ -*-
//
// Package:    WTagger
// Class:      WTagger
// 
/**\class WTagger WTagger.cc JetTools/AnalyzerToolboxsrc/WTagger.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  john stupak
//         Created:  Fri Oct 11 16:25:21 CDT 2013
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

//
// class declaration
//

class WTagger : public edm::EDAnalyzer {
public:
  WTagger();
  explicit WTagger(const edm::ParameterSet&);
  ~WTagger();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  void wTag(pat::Jet *theJet);

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  virtual void endRun(edm::Run const&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

  // ----------member data ---------------------------
  double massDropMax_;
  double prunedMassMin_;
  double prunedMassMax_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
WTagger::WTagger(){}

WTagger::WTagger(const edm::ParameterSet& iConfig){
  massDropMax_=iConfig.getParameter<double>("massDropMax");
  prunedMassMin_=iConfig.getParameter<double>("prunedMassMin");
  prunedMassMax_=iConfig.getParameter<double>("prunedMassMax");
}


WTagger::~WTagger()
{
 
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
WTagger::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;



#ifdef THIS_IS_AN_EVENT_EXAMPLE
  Handle<ExampleData> pIn;
  iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  ESHandle<SetupData> pSetup;
  iSetup.get<SetupRecord>().get(pSetup);
#endif
}

void WTagger::wTag(pat::Jet *theJet){
  bool result = (theJet->userFloat("massDrop")<massDropMax_) && (theJet->userFloat("prunedMass")>prunedMassMin_) && (theJet->userFloat("prunedMass")<prunedMassMax_);
  theJet->addUserFloat("isWTagged", result);
}

// ------------ method called once each job just before starting event loop  ------------
void 
WTagger::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
WTagger::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
WTagger::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
WTagger::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
WTagger::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
WTagger::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
WTagger::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(WTagger);
