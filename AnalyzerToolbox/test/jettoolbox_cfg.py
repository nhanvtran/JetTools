## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

process.source.fileNames = [
    '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0076C8E3-9AE1-E111-917C-003048D439AA.root'
    ]

#-------------------------------------------------------------------------------

from PhysicsTools.PatAlgos.tools.pfTools import *

postfix = "PFlow"
jetAlgo="AK5"
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=True, postfix=postfix)

#-------------------------------------------------------------------------------

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJetsCA8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsCA8PF")
                                        )

#-------------------------------------------------------------------------------

###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(rParam = cms.double(0.8),
                                         src = cms.InputTag('pfNoElectron'+postfix),
                                         doAreaFastjet = cms.bool(True),
                                         doRhoFastjet = cms.bool(True),
                                         Rho_EtaMax = cms.double(6.0),
                                         Ghost_EtaMax = cms.double(7.0)
                                         )

addJetCollection(process,
                 cms.InputTag('ca8PFJetsPFlow'),
                 'CA8', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 doJetID = False
                 )


process.load('JetTools.AnalyzerToolbox.AnalyzerJetToolbox_cff')
process.Njettiness.src = cms.InputTag("selectedPatJetsCA8PF")
process.Njettiness.cone = cms.double(0.8)
process.QGTagger.srcJets = cms.InputTag("selectedPatJetsCA8PF")
process.QGTagger.useCHS  = cms.untracked.bool(True)
process.QGTagger.isPatJet = cms.untracked.bool(True)

#-------------------------------------------------------------------------------

# Let it run
process.p = cms.Path(
    getattr(process,"patPF2PATSequence"+postfix)
    + process.ca8PFJetsPFlow
    + process.patDefaultSequence
    + process.goodPatJetsPFlow
    + process.selectedPatJetsCA8PF
    + process.AnalyzerJetToolbox
)

#-------------------------------------------------------------------------------

# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
#process.load("CommonTools.ParticleFlow.PF2PAT_EventContent_cff")
#process.out.outputCommands =  cms.untracked.vstring('drop *')
process.out.outputCommands = cms.untracked.vstring('drop *',
                                                   'keep *_selectedPatJetsCA8PF_*_*',
                                                   'keep *_Njettiness_tau*_*',
                                                   'keep *_QGTagger_*_*'
                                                   )

#-------------------------------------------------------------------------------

process.GlobalTag.globaltag =  'START53_V7E::All'    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
process.maxEvents.input = 10
process.out.fileName = 'jettoolbox.root'
