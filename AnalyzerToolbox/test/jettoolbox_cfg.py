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

#from JetTools.AnalyzerToolbox.puJetIDAlgo_cff import *
process.load("JetTools.AnalyzerToolbox.pileupjetidproducer_cfi")
process.pileupJetIdCalculator.jets = inputCollection
process.pileupJetIdEvaluator.jets = inputCollection

#---------------------------------------------------------------------------------------------------
#use PAT to turn ValueMaps into userFloats

process.patJets.userData.userFloats.src = ['Njettiness:tau1','Njettiness:tau2','Njettiness:tau3',
                                           'pileupJetIdEvaluator:cutbasedDiscriminant','pileupJetIdEvaluator:fullDiscriminant']

process.patJets.userData.userInts.src = ['pileupJetIdEvaluator:cutbasedId','pileupJetIdEvaluator:fullId']

process.out.outputCommands+=["keep *_*ak5PFJets*_*_*",
                             "keep *_Njettiness_*_*",
                             "keep *_pileupJetId*_*_*"]

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
