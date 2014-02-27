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

## uncomment the following line to add different jet collections
## to the event content
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection

addJetCollection(
    process,
    labelName = 'CA8PFCHS',
    jetSource = cms.InputTag('ca8PFJetsCHS'),
    algo='ca8',
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
#inputCollection = cms.InputTag('ak5PFJetsCHS')
inputCollection = cms.InputTag("ca8PFJetsCHS")

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

process.load('RecoJets.JetProducers.njettinessadder_cfi')
process.Njettiness.src = inputCollection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#pileupJetID

process.load('RecoJets.JetProducers.pileupjetidproducer_cfi')
process.pileupJetIdCalculator.jets = inputCollection
process.pileupJetIdEvaluator.jets = inputCollection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#QGTagger

process.load('RecoJets.JetProducers.QGTagger_RecoJets_cff')
process.QGTagger.srcJets = inputCollection
process.QGTagger.useCHS  = cms.untracked.bool(True)
process.QGTagger.jec     = cms.untracked.string('ak5PFL1FastL2L3')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#QJetsAdder

process.load('RecoJets.JetProducers.qjetsadder_cfi')
process.QJetsAdder.src=inputCollection
process.QJetsAdder.jetAlgo=cms.string(alg.upper())
process.QJetsAdder.jetRad = cms.double(distPar)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Grooming valueMaps

process.load('RecoJets.JetProducers.ca8PFJetsCHS_groomingValueMaps_cfi')
process.ca8PFJetsCHSPrunedLinks.src = inputCollection
process.ca8PFJetsCHSPrunedLinks.matched = cms.InputTag(inputCollection.value()+"Pruned")

#process.ca8PFJetsCHSTrimmedLinks.src = inputCollection
#process.ca8PFJetsCHSTrimmedLinks.matched = cms.InputTag(inputCollection.value()+"Trimmed")

#process.ca8PFJetsCHSFilteredLinks.src = inputCollection
#process.ca8PFJetsCHSFilteredLinks.matched = cms.InputTag(inputCollection.value()+"Filtered")

#---------------------------------------------------------------------------------------------------
#use PAT to turn ValueMaps into userFloats

process.patJetsCA8PFCHS.userData.userFloats.src = ['Njettiness:tau1','Njettiness:tau2','Njettiness:tau3',
                                                   'pileupJetIdEvaluator:cutbasedDiscriminant','pileupJetIdEvaluator:fullDiscriminant',
                                                   'QGTagger:qgLikelihood','QGTagger:qgMLP',
                                                   'QJetsAdder:QjetsVolatility',
                                                   ]

process.patJetsCA8PFCHS.userData.userInts.src = ['pileupJetIdEvaluator:cutbasedId','pileupJetIdEvaluator:fullId']

from JetMETAnalyses.TestValueMap.makeTooledJets_cfi import tooledJets
process.ca8PFJetsCHSTooled = tooledJets.clone()
process.ca8PFJetsCHSTooled.src = 'selectedPatJetsCA8PFCHS'
process.ca8PFJetsCHSTooled.doubleValueMaps = cms.VInputTag(["ca8PFJetsCHSPrunedLinks",
                                                            #"ca8PFJetsCHSTrimmedLinks",
                                                            #"ca8PFJetsCHSFilteredLinks"
                                                            ]
                                                           )
process.ca8PFJetsCHSTooled.doubleValueMapIDStrings = cms.vstring(['prunedMass',
                                                                  #'trimmedMass',
                                                                  #'filteredMass'
                                                                  ]
                                                                 )

process.out.outputCommands+=['keep *_ak5PFJetsCHS_*_*',
                             'keep *_Njettiness_*_*',
                             'keep *_pileupJetId*_*_*',
                             'keep *_QGTagger_*_*',
                             'keep *_QJetsAdder_*_*',
                             'keep *_ca8PFJetsCHS_*_*',
                             'keep *_ca8PFJetsCHSTooled_*_*',
                             'keep *_ca8PFJetsCHSPrunedLinks_*_*',
                             #'keep *_ca8PFJetsCHSTrimmedLinks_*_*',
                             #'keep *_ca8PFJetsCHSFilteredLinks_*_*',
                             ]

####################################################################################################

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarAODSIM
process.source.fileNames = filesRelValProdTTbarAODSIM
#                                         ##
process.maxEvents.input = 5
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'jettoolbox.root'
#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)
