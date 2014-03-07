## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service('Tracer')

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff')
process.load("RecoJets.Configuration.RecoGenJets_cff")
process.load("RecoJets.Configuration.GenJetParticles_cff")

process.ca8GenJetsNoNu = process.ca6GenJetsNoNu.clone( rParam = 0.8 )

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection

addJetCollection(
    process,
    labelName = 'CA8PFCHS',
    jetSource = cms.InputTag('ca8PFJetsCHS'),
    algo='ca8',
    jetCorrections = ('AK7PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None')
    )

addJetCollection(
    process,
    labelName = 'AK8PFCHS',
    jetSource = cms.InputTag('ak8PFJetsCHS'),
    algo='ak8',
    jetCorrections = ('AK7PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None')
    )

switchJetCollection(
    process,
    jetSource = cms.InputTag('ak5PFJets'),
    jetCorrections = ('AK5PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-1'),
    btagDiscriminators = ['jetBProbabilityBJetTags',
                          'jetProbabilityBJetTags',
                          'trackCountingHighPurBJetTags',
                          'trackCountingHighEffBJetTags',
                          'simpleSecondaryVertexHighEffBJetTags',
                          'simpleSecondaryVertexHighPurBJetTags',
                          'combinedSecondaryVertexBJetTags'
                          ],
    )

####################################################################################################
#THE JET TOOLBOX

#configure the jet toolbox

inputCollection = cms.InputTag("ca8PFJetsCHS")
#inputCollection = cms.InputTag('ak8PFJetsCHS')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if inputCollection.value().startswith("ca"):
    alg='ca'
elif inputCollection.value().startswith("ak"):
    alg='ak'
    
if '5PFJets' in inputCollection.value():
    distPar=0.5
elif '8PFJets' in inputCollection.value():
    distPar=0.8

try: alg,distPar
except:
    "inputCollection not recognized"
    exit(1)
            
#---------------------------------------------------------------------------------------------------
#load the various tools

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Njettiness

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",QJetsAdder = cms.PSet(initialSeed = cms.untracked.uint32(7)))

process.load('RecoJets.JetProducers.nJettinessAdder_cfi')
process.Njettiness.src = inputCollection
process.Njettiness.cone=cms.double(distPar)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#pileupJetID

process.load('RecoJets.JetProducers.pileupjetidproducer_cfi')
process.pileupJetIdCalculator.jets = inputCollection
process.pileupJetIdEvaluator.jets = inputCollection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#QGTagger

process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets = inputCollection
process.QGTagger.useCHS  = cms.bool(True)
process.QGTagger.jec     = cms.string('')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#QJetsAdder

process.load('RecoJets.JetProducers.qjetsadder_cfi')
process.QJetsAdder.src=inputCollection
process.QJetsAdder.jetRad = cms.double(distPar)
process.QJetsAdder.jetAlgo=cms.string(alg.upper())

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Grooming valueMaps
process.load('RecoJets.Configuration.RecoPFJets_cff')

#process.ca8PFJetsCHSPrunedLinks.src = inputCollection
#process.ca8PFJetsCHSPrunedLinks.matched = cms.InputTag(inputCollection.value()+"Pruned")

#process.ca8PFJetsCHSTrimmedLinks.src = inputCollection
#process.ca8PFJetsCHSTrimmedLinks.matched = cms.InputTag(inputCollection.value()+"Trimmed")

#process.ca8PFJetsCHSFilteredLinks.src = inputCollection
#process.ca8PFJetsCHSFilteredLinks.matched = cms.InputTag(inputCollection.value()+"Filtered")

#---------------------------------------------------------------------------------------------------
#use PAT to turn ValueMaps into userFloats

if inputCollection.value()=="ca8PFJetsCHS": patJets=process.patJetsCA8PFCHS
elif inputCollection.value()=="ak8PFJetsCHS": patJets=process.patJetsAK8PFCHS

patJets.userData.userFloats.src = ['Njettiness:tau1','Njettiness:tau2','Njettiness:tau3',
                                   'pileupJetIdEvaluator:fullDiscriminant',
                                   'QGTagger:qgLikelihood',
                                   'QJetsAdder:QjetsVolatility',
                                   ]

patJets.userData.userInts.src = ['pileupJetIdEvaluator:cutbasedId','pileupJetIdEvaluator:fullId']

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from JetMETAnalyses.TestValueMap.makeTooledJets_cfi import tooledJets

if inputCollection.value()=="ca8PFJetsCHS":
    process.ca8PFJetsCHSTooled = tooledJets.clone()
    process.ca8PFJetsCHSTooled.src = 'selectedPatJetsCA8PFCHS'
    process.ca8PFJetsCHSTooled.doubleValueMaps = cms.VInputTag(["ca8PFJetsCHSPrunedLinks",
                                                                "ca8PFJetsCHSTrimmedLinks",
                                                                "ca8PFJetsCHSFilteredLinks"
                                                                ]
                                                               )
    process.ca8PFJetsCHSTooled.doubleValueMapIDStrings = cms.vstring(['prunedMass',
                                                                      'trimmedMass',
                                                                      'filteredMass'
                                                                      ]
                                                                 )

elif inputCollection.value()=="ak8PFJetsCHS":
    process.ak8PFJetsCHSTooled = tooledJets.clone()
    process.ak8PFJetsCHSTooled.src = 'selectedPatJetsAK8PFCHS'
    process.ak8PFJetsCHSTooled.doubleValueMaps = cms.VInputTag(["ak8PFJetsCHSPrunedLinks",
                                                                "ak8PFJetsCHSTrimmedLinks",
                                                                "ak8PFJetsCHSFilteredLinks"
                                                                ]
                                                               )
    process.ak8PFJetsCHSTooled.doubleValueMapIDStrings = cms.vstring(['prunedMass',
                                                                      'trimmedMass',
                                                                      'filteredMass'
                                                                      ]
                                                                     )

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

#process.out.outputCommands+=['keep *_ak5PFJetsCHS_*_*',
process.out.outputCommands=['drop *',
                            'keep *_Njettiness_*_*',
                            'keep *_pileupJetId*_*_*',
                            'keep *_QGTagger_*_*',
                            'keep *_QJetsAdder_*_*']

if inputCollection.value()=="ca8PFJetsCHS":
    process.out.outputCommands+=['keep *_ca8PFJetsCHS__PAT',
                                 'keep *_ca8PFJetsCHSTooled__PAT',
                                 'keep *_ca8PFJetsCHSPrunedLinks__PAT',
                                 'keep *_ca8PFJetsCHSTrimmedLinks__PAT',
                                 'keep *_ca8PFJetsCHSFilteredLinks__PAT',
                                 ]
    
elif inputCollection.value()=="ak8PFJetsCHS":
    process.out.outputCommands+=['keep *_ak8PFJetsCHS__PAT',
                                 'keep *_ak8PFJetsCHSTooled__PAT',
                                 'keep *_ak8PFJetsCHSPrunedLinks__PAT',
                                 'keep *_ak8PFJetsCHSTrimmedLinks__PAT',
                                 'keep *_ak8PFJetsCHSFilteredLinks__PAT',
                                 ]

####################################################################################################

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
#from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarAODSIM
#process.source.fileNames = filesRelValProdTTbarAODSIM
process.source.fileNames = cms.untracked.vstring('/store/relval/CMSSW_7_0_0_pre11/RelValRSKKGluon_m3000GeV_13/GEN-SIM-RECO/POSTLS162_V4-v1/00000/1CCFFDA6-846A-E311-9E61-0025905964C2.root')
#                                         ##
process.maxEvents.input = 5
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'jettoolbox.root'
#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)
