// -*- C++ -*-
//
// Package:    JetToolbox
// Class:      JetToolbox
// 
/**\class JetToolbox JetToolbox.cc JetTools/JetToolbox/src/JetToolbox.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  john stupak
//         Created:  Thu Oct 10 16:52:18 CDT 2013
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

#include <fastjet/JetDefinition.hh>
#include <fastjet/PseudoJet.hh>
#include <fastjet/ClusterSequence.hh>

#include "JetTools/AnalyzerToolbox/src/JetPruner.cc"
#include "JetTools/AnalyzerToolbox/src/WTagger.cc"

//
// class declaration
//

class JetToolbox : public edm::EDProducer {
   public:
      explicit JetToolbox(const edm::ParameterSet&);
      ~JetToolbox();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------

  edm::InputTag jetSrc_;
  fastjet::JetAlgorithm jetAlg_;
  double jetSize_;

  bool doPruning_;
  JetPruner pruner_;
  WTagger wTagger_;

  bool doTrimming_;
  bool doFiltering_;

  bool doWTagging_;
  bool doTopTagging_;

  bool doPileupID_;
  bool doQuarkGluonDisc_;
  bool doSubstructAnalysis_;
  bool doSubjetBTagging_;

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
JetToolbox::JetToolbox(const edm::ParameterSet& iConfig)
{
  produces<std::vector<pat::Jet>>();
  
  jetSrc_=iConfig.getParameter<edm::InputTag>("jetSrc");

  std::string jetAlgString=iConfig.getParameter<std::string>("jetAlg");
  /*fastjet::JetAlgorithm {                                                                                                                                                        
    fastjet::kt_algorithm = 0, fastjet::cambridge_algorithm = 1, fastjet::antikt_algorithm = 2, fastjet::genkt_algorithm = 3,                                                      
    fastjet::cambridge_for_passive_algorithm = 11, fastjet::genkt_for_passive_algorithm = 13, fastjet::ee_kt_algorithm = 50, fastjet::ee_genkt_algorithm = 53,                     
    fastjet::plugin_algorithm = 99                                                                                                                                                 
    }                                                                                                                                                                              
  */
  if(jetAlgString=="KT") jetAlg_=fastjet::kt_algorithm;
  if (jetAlgString=="CA") jetAlg_=fastjet::cambridge_algorithm;
  if (jetAlgString=="AK") jetAlg_=fastjet::antikt_algorithm;

  jetSize_=iConfig.getParameter<double>("jetSize");

  doPruning_=iConfig.getParameter<bool>("doPruning");
  doTrimming_=iConfig.getParameter<bool>("doTrimming");
  doFiltering_=iConfig.getParameter<bool>("doFiltering");

  doWTagging_=iConfig.getParameter<bool>("doWTagging");
  doTopTagging_=iConfig.getParameter<bool>("doTopTagging");

  doPileupID_=iConfig.getParameter<bool>("doPielupID");
  doQuarkGluonDisc_=iConfig.getParameter<bool>("doQuarkGluonDisc");
  doSubstructAnalysis_=iConfig.getParameter<bool>("doSubstructAnalysis");
  doSubjetBTagging_=iConfig.getParameter<bool>("doSubjetBTagging");

  std::cout<<"JetToolbox: doPruning: "<<doPruning_<<std::endl;
  std::cout<<"JetToolbox: doWTagging: "<<doWTagging_<<std::endl;

  //Instantiate helpers                                                                                                                                                            
  if(doPruning_)
    {
      pruner_=JetPruner(iConfig);
    }

  if(doWTagging_)
    {
      doPruning_=true;
      wTagger_=WTagger(iConfig);
    }
}


JetToolbox::~JetToolbox()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
JetToolbox::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   edm::Handle<edm::View<pat::Jet> > inputJets;
   iEvent.getByLabel(jetSrc_,inputJets);

   std::vector<pat::Jet> outputJets;   
   outputJets.reserve(inputJets->size());

   for ( typename edm::View<pat::Jet>::const_iterator jetIt = inputJets->begin() ; jetIt != inputJets->end() ; ++jetIt ) {
     pat::Jet* theJet=new pat::Jet(*jetIt);
     
     // Store the particle flow constituents of this jet in a vector
     std::vector<edm::Ptr<reco::PFCandidate> > pfConstituents = theJet->getPFConstituents();
     
     // initialize vector
     std::vector<fastjet::PseudoJet> pseudoJets;
     
     //loop over all constituents of jet
     for (unsigned lp = 0; lp < pfConstituents.size (); ++lp){
       float px = pfConstituents[lp]->px();
       float py = pfConstituents[lp]->py();
       float pz = pfConstituents[lp]->pz();
       float e = pfConstituents[lp]->energy();
       
       pseudoJets.push_back( fastjet::PseudoJet(px, py, pz, e));
     }
     
     // Recluster
     fastjet::JetDefinition jetDef(jetAlg_, jetSize_);
     fastjet::ClusterSequence clusterSeq(pseudoJets, jetDef);
     
     const std::vector<fastjet::PseudoJet> reclusteredJet = sorted_by_pt(clusterSeq.inclusive_jets(0.0));
     
     if(doPruning_){
       pruner_.prune(theJet,reclusteredJet);
     }
     
     if(doWTagging_){
       wTagger_.wTag(theJet);
     }

     outputJets.push_back(*theJet);
   }
   std::auto_ptr<std::vector<pat::Jet> > output(new std::vector<pat::Jet>(outputJets));
   iEvent.put(output);
}

// ------------ method called once each job just before starting event loop  ------------
void 
JetToolbox::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
JetToolbox::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
JetToolbox::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
JetToolbox::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
JetToolbox::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
JetToolbox::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
JetToolbox::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetToolbox);
