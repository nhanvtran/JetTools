## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service("Tracer")

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

process.load('JetTools.AnalyzerToolbox.AnalyzerJetToolbox_cff')
process.Njettiness.src = cms.InputTag("ak5PFJetsCHS")
process.Njettiness.cone = cms.double(0.5)

process.patJets.userData.userFloats.src = ['Njettiness:tau1','Njettiness:tau2','Njettiness:tau3']

process.out.outputCommands+=["keep *_*Njettiness*_*_*",
                             "keep *_*ak5PFJets*_*_*"]

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
process.maxEvents.input = 10
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'jettoolbox.root'
#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)
