import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
                            # replace 'myfile.root' with the source file you want to use
                            fileNames = cms.untracked.vstring('file:jettoolbox.root')
                            )

process.demo = cms.EDAnalyzer('jetAnalyzer',
                              src=cms.InputTag("patJetsAK4PFCHS")
                              #src=cms.InputTag("patJetsCA8PFCHS")
                              #src=cms.InputTag("patJetsAK8PFCHS")
                              )


process.p = cms.Path(process.demo)
