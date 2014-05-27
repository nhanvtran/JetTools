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

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TFile.h"

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

  TH1F* h_tau1 = new TH1F("tau1",";#tau_{1}",25,0,1);
  TH1F* h_tau2 = new TH1F("tau2",";#tau_{2}",25,0,1);
  TH1F* h_tau3 = new TH1F("tau3",";#tau_{3}",25,0,1);

  TH1F* h_fullDiscriminant = new TH1F("fullDiscriminant",";fullDiscriminant",25,0,1);

  TH1F* h_cutbasedId = new TH1F("cutbasedId",";cutbasedId",8,-0.5,7.5);
  TH1F* h_fullId = new TH1F("fullId",";fullId",8,-0.5,7.5);

  TH1F* h_qgLikelihood = new TH1F("qgLikelihood",";qgLikelihood",25,0,1);

  TH1F* h_QjetsVolatility = new TH1F("QjetsVolatility",";QjetsVolatility",25,0,2);

  TH1F* h_prunedMass = new TH1F("prunedMass",";pruned mass",50,0,500);
  TH1F* h_trimmedMass = new TH1F("trimmedMass",";trimmed mass",50,0,500);
  TH1F* h_filteredMass = new TH1F("filteredMass",";filtered mass",50,0,500);

  TH1F* h_topJetMass = new TH1F("topJetMass",";top jet mass",50,0,500);

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

  for( edm::View<pat::Jet>::const_iterator jet_iter = jets->begin();
       jet_iter !=jets->end(); ++jet_iter)
    {
      float pt = jet_iter->pt();
      float eta = jet_iter->eta();

      int cutbasedId=0, fullId=0;
      float fullDiscriminant=0, qgLikelihood=0, tau1=0, tau2=0, tau3=0, QjetsVolatility=0, prunedMass=0, trimmedMass=0, filteredMass=0, topJetMass;

      if ( jets_->label().compare("patJetsAK5PFCHS")==0 || jets_->label().compare("patJetsAK4PFCHS")==0){
	cutbasedId = jet_iter->userInt("pileupJetIdEvaluator:cutbasedId");
	
	fullDiscriminant = jet_iter->userFloat("pileupJetIdEvaluator:fullDiscriminant");
	fullId = jet_iter->userInt("pileupJetIdEvaluator:fullId");
	
	qgLikelihood = jet_iter->userFloat("QGTagger:qgLikelihood");
	
	h_fullDiscriminant->Fill(fullDiscriminant);
	
	h_cutbasedId->Fill(cutbasedId);
	h_fullId->Fill(fullId);
	
	h_qgLikelihood->Fill(qgLikelihood);
      }
      else if (jets_->label().compare("patJetsCA8PFCHS")==0 ){
	
	tau1 = jet_iter->userFloat("NjettinessCA8:tau1");
	tau2 = jet_iter->userFloat("NjettinessCA8:tau2");
	tau3 = jet_iter->userFloat("NjettinessCA8:tau3");
	
	QjetsVolatility = jet_iter->userFloat("QJetsAdderCA8:QjetsVolatility");
	
	prunedMass = jet_iter->userFloat("ca8PFJetsCHSPrunedLinks");
	trimmedMass = jet_iter->userFloat("ca8PFJetsCHSTrimmedLinks");
	filteredMass = jet_iter->userFloat("ca8PFJetsCHSFilteredLinks");
	
	topJetMass = jet_iter->userFloat("cmsTopTagPFJetsCHSLinksCA8");
	
	h_tau1->Fill(tau1);
	h_tau2->Fill(tau2);
	h_tau3->Fill(tau3);
	
	h_QjetsVolatility->Fill(QjetsVolatility);
	
	h_prunedMass->Fill(prunedMass);
	h_trimmedMass->Fill(trimmedMass);
	h_filteredMass->Fill(filteredMass);
	
	h_topJetMass->Fill(topJetMass);
      }
      
      else if (jets_->label().compare("patJetsAK8PFCHS")==0 ){
	
	tau1 = jet_iter->userFloat("NjettinessAK8:tau1");
	tau2 = jet_iter->userFloat("NjettinessAK8:tau2");
	tau3 = jet_iter->userFloat("NjettinessAK8:tau3");
	
	QjetsVolatility = jet_iter->userFloat("QJetsAdderAK8:QjetsVolatility");
	
	prunedMass = jet_iter->userFloat("ak8PFJetsCHSPrunedLinks");
	trimmedMass = jet_iter->userFloat("ak8PFJetsCHSTrimmedLinks");
	filteredMass = jet_iter->userFloat("ak8PFJetsCHSFilteredLinks");
	
	topJetMass = jet_iter->userFloat("cmsTopTagPFJetsCHSLinksAK8");
	
	h_tau1->Fill(tau1);
	h_tau2->Fill(tau2);
	h_tau3->Fill(tau3);
	
	h_QjetsVolatility->Fill(QjetsVolatility);
	
	h_prunedMass->Fill(prunedMass);
	h_trimmedMass->Fill(trimmedMass);
	h_filteredMass->Fill(filteredMass);
	
	h_topJetMass->Fill(topJetMass);
      }

      std::cout<<"pt: "<<pt<<std::endl;
      std::cout<<"eta: "<<eta<<std::endl;

      std::cout<<"tau1: "<<tau1<<std::endl;
      std::cout<<"tau2: "<<tau2<<std::endl;
      std::cout<<"tau3: "<<tau3<<std::endl;

      std::cout<<"cutbasedId: "<<cutbasedId<<std::endl;

      std::cout<<"fullDiscriminant: "<<fullDiscriminant<<std::endl;
      std::cout<<"fullId: "<<fullId<<std::endl;

      std::cout<<"qgLikelihood: "<<qgLikelihood<<std::endl;

      std::cout<<"QjetsVolatility: "<<QjetsVolatility<<std::endl;

      std::cout<<"prunedMass: "<<prunedMass<<std::endl;
      std::cout<<"trimmedMass: "<<trimmedMass<<std::endl;
      std::cout<<"filteredMass: "<<filteredMass<<std::endl;

      std::cout<<"topJetMass:"<<topJetMass<<std::endl;

      std::cout<<std::endl;
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
  TFile* f=new TFile("hists.root","RECREATE");

  h_tau1->Write();
  h_tau2->Write();
  h_tau3->Write();

  h_fullDiscriminant->Write();

  h_cutbasedId->Write();
  h_fullId->Write();

  h_qgLikelihood->Write();

  h_QjetsVolatility->Write();

  h_prunedMass->Write();
  h_trimmedMass->Write();
  h_filteredMass->Write();

  h_topJetMass->Write();

  f->Close();
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
