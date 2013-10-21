// -*- C++ -*-
//
// Package:    JetTools/AnalyzerToolbox
// Class:      WTagAdder
// 
/**\class WTagAdder WTagAdder.cc JetTools/AnalyzerToolbox/src/WTagAdder.cc
   
Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  john stupak
//         Created:  Thu Sep 19 22:03:29 CDT 2013
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


//
// class declaration
//

class WTagAdder : public edm::EDProducer {
public:
  explicit WTagAdder(const edm::ParameterSet&);

  ~WTagAdder();
  
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
private:
  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  virtual void beginRun(edm::Run&, edm::EventSetup const&);
  virtual void endRun(edm::Run&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
  
  bool isWTagged(edm::Ptr<pat::Jet>) const;

  // ----------member data ---------------------------
  
  edm::InputTag src_ ;

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
WTagAdder::WTagAdder(const edm::ParameterSet& iConfig):src_(iConfig.getParameter<edm::InputTag>("src"))

{
  produces<std::vector<pat::Jet> >();

  massDropMax_=iConfig.getParameter<double>("massDropMax");
  prunedMassMin_=iConfig.getParameter<double>("prunedMassMin");
  prunedMassMax_=iConfig.getParameter<double>("prunedMassMax");
}


WTagAdder::~WTagAdder()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
WTagAdder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
/* This is an event example
   //Read 'ExampleData' from the Event
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);

   //Use the ExampleData to create an ExampleData2 which 
   // is put into the Event
   std::auto_ptr<ExampleData2> pOut(new ExampleData2(*pIn));
   iEvent.put(pOut);
*/

/* this is an EventSetup example
   //Read SetupData from the SetupRecord in the EventSetup
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
*/
 
   // read input collection
   edm::Handle<edm::View<pat::Jet> > jets;
   iEvent.getByLabel(src_, jets);
  
   // prepare room for output
   std::vector<pat::Jet> outJets;   outJets.reserve(jets->size());

   for ( typename edm::View<pat::Jet>::const_iterator jetIt = jets->begin() ; jetIt != jets->end() ; ++jetIt ) {
     //pat::Jet newCand(*jetIt);
     //edm::Ptr<pat::Jet> jetPtr = jets->ptrAt(jetIt - jets->begin());
     //newCand.addUserFloat("isWTagged", isWTagged(jetPtr));
     //outJets.push_back(newCand);
   }

   std::auto_ptr<std::vector<pat::Jet> > out(new std::vector<pat::Jet>(outJets));
   iEvent.put(out);
}

bool WTagAdder::isWTagged(edm::Ptr<pat::Jet> theJet) const
{
  bool result = (theJet->userFloat("massDrop")<massDropMax_) && (theJet->userFloat("prunedMass")>prunedMassMin_) && (theJet->userFloat("prunedMass")<prunedMassMax_);

  return result;
}



// ------------ method called once each job just before starting event loop  ------------
void 
WTagAdder::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
WTagAdder::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
WTagAdder::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
WTagAdder::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
WTagAdder::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
WTagAdder::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
WTagAdder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;

  //desc.add<double>("massDropMax", 0.4);
  //desc.add<double>("prunedMassMin", 60.);
  //desc.add<double>("prunedMassMax", 100.);

  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(WTagAdder);
