## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service("Tracer")

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

####################################################################################################
#THE JET TOOLBOX

#configure the jet toolbox
inputCollection = cms.InputTag("ak5PFJetsCHS")

#---------------------------------------------------------------------------------------------------
#load the various tools

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Njettiness

process.load('JetTools.AnalyzerToolbox.njettinessadder_cfi')
process.Njettiness.src = inputCollection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#pileupJetID

process.load("JetTools.AnalyzerToolbox.pileupjetidproducer_cfi")
process.pileupJetIdCalculator.jets = inputCollection
process.pileupJetIdEvaluator.jets = inputCollection

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#QGTagger

process.load('JetTools.AnalyzerToolbox.QGTagger_RecoJets_cff')
process.QGTagger.srcJets = inputCollection
process.QGTagger.useCHS  = cms.untracked.bool(True)
process.QGTagger.jec     = cms.untracked.string('ak5PFL1FastL2L3')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

process.QJetsAdder = cms.EDProducer("QjetsAdder",
                                    src=inputCollection,
                                    zcut=cms.double(0.1),
                                    dcutfctr=cms.double(0.5),
                                    expmin=cms.double(0.0),
                                    expmax=cms.double(0.0),
                                    rigidity=cms.double(0.1),
                                    ntrial = cms.int32(50),
                                    cutoff=cms.double(10.0),
                                    jetRad= cms.double(0.5),
                                    jetAlgo=cms.string("AK"),
                                    preclustering = cms.int32(50),
                                    )

#---------------------------------------------------------------------------------------------------
#use PAT to turn ValueMaps into userFloats

process.patJets.userData.userFloats.src = ['Njettiness:tau1','Njettiness:tau2','Njettiness:tau3',
                                           'pileupJetIdEvaluator:cutbasedDiscriminant','pileupJetIdEvaluator:fullDiscriminant',
                                           'QGTagger:qgLikelihood','QGTagger:qgMLP',
                                           'QJetsAdder:QjetsVolatility']

process.patJets.userData.userInts.src = ['pileupJetIdEvaluator:cutbasedId','pileupJetIdEvaluator:fullId']

process.out.outputCommands+=["keep *_ak5PFJetsCHS_*_*",
                             "keep *_Njettiness_*_*",
                             "keep *_pileupJetId*_*_*",
                             "keep *_QGTagger_*_*",
                             "keep *_QJetsAdder_*_*"]

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
