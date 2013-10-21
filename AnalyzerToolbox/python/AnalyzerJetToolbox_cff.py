import FWCore.ParameterSet.Config as cms

from JetTools.AnalyzerToolbox.QGTagger_RecoJets_cff import *

Njettiness = cms.EDProducer("NjettinessAdder",
                               src=cms.InputTag("selectedPatJetsCA8PF"),
                               cone=cms.double(0.5)
                               )

AnalyzerJetToolbox = cms.Sequence( Njettiness + QuarkGluonTagger )

