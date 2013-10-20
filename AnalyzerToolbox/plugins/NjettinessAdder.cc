#include "JetTools/AnalyzerToolbox/plugins/NjettinessAdder.h"
#include "JetTools/AnalyzerToolbox/interface/Njettiness.hh"

#include "FWCore/Framework/interface/MakerMacros.h"

void NjettinessAdder::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  // read input collection
  edm::Handle<edm::View<pat::Jet> > jets;
  iEvent.getByLabel(src_, jets);
  
  
  // prepare room for output
  std::vector<pat::Jet> outJets;   outJets.reserve(jets->size());
  std::vector<float> tau1;         tau1.reserve(jets->size());
  std::vector<float> tau2;         tau2.reserve(jets->size());
  std::vector<float> tau3;         tau3.reserve(jets->size());

  for ( typename edm::View<pat::Jet>::const_iterator jetIt = jets->begin() ; jetIt != jets->end() ; ++jetIt ) {
    pat::Jet newCand(*jetIt);
    edm::Ptr<pat::Jet> jetPtr = jets->ptrAt(jetIt - jets->begin());

    float t1=getTau(1, jetPtr );
    float t2=getTau(2, jetPtr );
    float t3=getTau(3, jetPtr );

    newCand.addUserFloat("tau1", t1);
    newCand.addUserFloat("tau2", t2);
    newCand.addUserFloat("tau3", t3);
    outJets.push_back(newCand);

    tau1.push_back(t1);
    tau2.push_back(t2);
    tau3.push_back(t3);
  }

  std::auto_ptr<std::vector<pat::Jet> > out(new std::vector<pat::Jet>(outJets));
  iEvent.put(out,"jets");

  std::auto_ptr<edm::ValueMap<float> > outT1(new edm::ValueMap<float>());
  std::auto_ptr<edm::ValueMap<float> > outT2(new edm::ValueMap<float>());
  std::auto_ptr<edm::ValueMap<float> > outT3(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler fillerT1(*outT1);
  edm::ValueMap<float>::Filler fillerT2(*outT2);
  edm::ValueMap<float>::Filler fillerT3(*outT3);
  fillerT1.insert(jets, tau1.begin(), tau1.end());
  fillerT2.insert(jets, tau2.begin(), tau2.end());
  fillerT3.insert(jets, tau3.begin(), tau3.end());
  fillerT1.fill();
  fillerT2.fill();
  fillerT3.fill();
  
  iEvent.put(outT1,"tau1");
  iEvent.put(outT2,"tau2");
  iEvent.put(outT3,"tau3");
}

float NjettinessAdder::getTau(int num, edm::Ptr<pat::Jet> object) const
{
  std::vector<const reco::PFCandidate*> all_particles;
  if(object->isPFJet())
    {
      for (unsigned k =0; k < object->getPFConstituents().size(); k++)
	all_particles.push_back( object->getPFConstituent(k).get() );
    } else {
    for (unsigned j = 0; j < object->numberOfDaughters(); j++){
      reco::PFJet const *pfSubjet = dynamic_cast <const reco::PFJet *>(object->daughter(j));
      if (!pfSubjet) break;
          for (unsigned k =0; k < pfSubjet->getPFConstituents().size(); k++)
	    all_particles.push_back( pfSubjet->getPFConstituent(k).get() );	
    }
  }
  std::vector<fastjet::PseudoJet> FJparticles;
  for (unsigned particle = 0; particle < all_particles.size(); particle++){
    const reco::PFCandidate *thisParticle = all_particles.at(particle);
    FJparticles.push_back( fastjet::PseudoJet( thisParticle->px(), thisParticle->py(), thisParticle->pz(), thisParticle->energy() ) );	
  }
  NsubParameters paraNsub = NsubParameters(1.0, cone_); //assume R=0.7 jet clusering used
  Njettiness routine(Njettiness::onepass_kt_axes, paraNsub);
  return routine.getTau(num, FJparticles); 
}



DEFINE_FWK_MODULE(NjettinessAdder);
