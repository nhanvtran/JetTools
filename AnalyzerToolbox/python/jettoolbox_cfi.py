import FWCore.ParameterSet.Config as cms

JetToolbox = cms.EDProducer(
    'JetToolbox',
    jetSrc = cms.string(""),

    jetAlg = cms.string("CA"),
    jetSize = cms.double(0.8),

    doPruning = cms.bool(False),
    doTrimming = cms.bool(False),
    doFiltering = cms.bool(False),
    
    doWTagging = cms.bool(False),
    doTopTagging = cms.bool(False),
    
    doPielupID = cms.bool(False),
    doQuarkGluonDisc = cms.bool(False),
    doSubstructAnalysis = cms.bool(False),
    doSubjetBTagging = cms.bool(False),

    pruningJetAlg = cms.string("CA"),
    pruningJetSize = cms.double(0.2),
    RcutFactor = cms.double(0.5),
    zCut = cms.double(0.1),

    massDropMax = cms.double(0.4),
    prunedMassMin = cms.double(60),
    prunedMassMax = cms.double(100)
)
