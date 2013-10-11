import FWCore.ParameterSet.Config as cms

process = cms.Process("SimpleJetAnalyzer")

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring("file:jetToolbox.root")
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( -1 )
)

## Message logger configuration
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Analyze jets
process.analyzePatJets = cms.EDAnalyzer("SimpleJetAnalyzer",
                                src  = cms.InputTag("CA8JetToolbox"),
                                corrLevel = cms.string("L3Absolute")
                                )

## Define output file
process.TFileService = cms.Service("TFileService",
  fileName = cms.string('out.root')
)

process.p = cms.Path(
    process.analyzePatJets
)
