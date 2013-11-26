// -*- C++ -*-
//
// Package:    tmp/jetAnalyzer
// Class:      jetAnalyzer
// 
/**\class jetAnalyzer jetAnalyzer.cc tmp/jetAnalyzer/plugins/jetAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  John Stupak
//         Created:  Mon, 25 Nov 2013 16:39:03 GMT
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

class jetAnalyzer : public edm::EDAnalyzer {
   public:
      explicit jetAnalyzer(const edm::ParameterSet&);
      ~jetAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
  edm::InputTag* jets_;
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
jetAnalyzer::jetAnalyzer(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
  jets_=new edm::InputTag(iConfig.getParameter<edm::InputTag>("src"));


}


jetAnalyzer::~jetAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
jetAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   edm::Handle<edm::View<pat::Jet> > jets;
   iEvent.getByLabel(*jets_,jets);
   //iEvent.getByLabel(iConfig.getParameter<edm::InputTag>("src"),jets);
   for( edm::View<pat::Jet>::const_iterator jet_iter = jets->begin();
	jet_iter !=jets->end(); ++jet_iter)
     {
       float tau1 = jet_iter->userFloat("Njettiness:tau1");
       std::cout<<tau1<<std::endl;
     }
   /*
#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
   */
}


// ------------ method called once each job just before starting event loop  ------------
void 
jetAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
jetAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
jetAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
jetAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
jetAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
jetAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
jetAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(jetAnalyzer);
