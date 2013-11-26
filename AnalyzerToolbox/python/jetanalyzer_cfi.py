import FWCore.ParameterSet.Config as cms

jetAnalyzer = cms.EDAnalyzer('jetAnalyzer',
                             src  = cms.InputTag("patJets")
                             
)
