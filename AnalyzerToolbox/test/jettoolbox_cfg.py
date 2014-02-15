## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service('Tracer')

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff')

####################################################################################################
#THE JET TOOLBOX

#configure the jet toolbox
inputCollection = cms.InputTag('ak5PFJetsCHS')

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

#---------------------------------------------------------------------------------------------------
#use PAT to turn ValueMaps into userFloats

process.patJets.userData.userFloats.src = ['Njettiness:tau1','Njettiness:tau2','Njettiness:tau3',
                                           'pileupJetIdEvaluator:cutbasedDiscriminant','pileupJetIdEvaluator:fullDiscriminant',
                                           'QGTagger:qgLikelihood','QGTagger:qgMLP',
                                           'QJetsAdder:QjetsVolatility']

process.patJets.userData.userInts.src = ['pileupJetIdEvaluator:cutbasedId','pileupJetIdEvaluator:fullId']

process.out.outputCommands+=['keep *_ak5PFJetsCHS_*_*',
                             'keep *_Njettiness_*_*',
                             'keep *_pileupJetId*_*_*',
                             'keep *_QGTagger_*_*',
                             'keep *_QJetsAdder_*_*']

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
process.maxEvents.input = 500
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'jettoolbox.root'
#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)
