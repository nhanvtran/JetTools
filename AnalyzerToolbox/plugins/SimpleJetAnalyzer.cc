#include <map>
#include <string>
#include <iomanip>
#include <sstream>
#include <iostream>

#include "TH1.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"


class SimpleJetAnalyzer : public edm::EDAnalyzer {

public:
  /// default contructor
  explicit SimpleJetAnalyzer(const edm::ParameterSet& cfg);
  /// default destructor
  ~SimpleJetAnalyzer(){};
  
private:
  /// everything that needs to be done during the even loop
  virtual void analyze(const edm::Event& event, const edm::EventSetup& setup);

  /// check if histogram was booked
  bool booked(const std::string histName) const { return hists_.find(histName.c_str())!=hists_.end(); };
  /// fill histogram if it had been booked before
  void fill(const std::string histName, double value) const { if(booked(histName.c_str())) hists_.find(histName.c_str())->second->Fill(value); };
private:  
  /// pat jets
  edm::InputTag jets_;
  /// management of 1d histograms
  std::map<std::string,TH1F*> hists_; 
};


SimpleJetAnalyzer::SimpleJetAnalyzer(const edm::ParameterSet& cfg):
  jets_(cfg.getParameter<edm::InputTag>("src"))
{
  // register TFileService
  edm::Service<TFileService> fs;
  // jet multiplicity
  hists_["mult" ]=fs->make<TH1F>("mult" , "N_{Jet}"          ,   15,   0.,   15.);
  // jet pt (for all jets)
  hists_["pt"   ]=fs->make<TH1F>("pt"   , "p_{T}(Jet) [GeV]" ,   60,   0.,  300.);
  // jet eta (for all jets)
  hists_["eta"  ]=fs->make<TH1F>("eta"  , "#eta (Jet)"       ,   60,  -3.,    3.);
}

void
SimpleJetAnalyzer::analyze(const edm::Event& event, const edm::EventSetup& setup)
{
  edm::Handle<edm::View<pat::Jet> > jets;
  event.getByLabel(jets_,jets);

  edm::Handle<edm::ValueMap<float> > tau1;
  event.getByLabel("Njettiness","tau1",tau1);

  edm::Handle<edm::ValueMap<float> > qgLikelihood;
  event.getByLabel("QGTagger","qgLikelihood",qgLikelihood);

  // loop jets
  for(edm::View<pat::Jet>::const_iterator jet=jets->begin(); jet!=jets->end(); ++jet){

    int ijet = jet - jets->begin();
    edm::RefToBase<pat::Jet> jetRef(edm::Ref<edm::View<pat::Jet>>(jets,ijet));

    std::cout<<"jet->eta(): "<<jet->eta()<<std::endl;
    std::cout<<"tau1: "<<(*tau1)[jetRef]<<std::endl;
    std::cout<<"qgLikelihood: "<<(*qgLikelihood)[jetRef]<<std::endl;
    std::cout<<std::endl;
  }
  // jet multiplicity
  fill( "mult" , jets->size());
  // invariant dijet mass for first two leading jets
  if(jets->size()>1){ fill( "mass", ((*jets)[0].p4()+(*jets)[1].p4()).mass());}
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimpleJetAnalyzer);
