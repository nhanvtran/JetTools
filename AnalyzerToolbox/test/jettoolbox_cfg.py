
# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('doPruning',
                  True,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  'Apply jet pruning')

options.register('doWTagging',
                 True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 'Apply W-tagging')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  'Run this on real data')

options.register ('globalTag',
                  '',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  'Overwrite defaul globalTag')

options.register ('forceCheckClosestZVertex',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Force the check of the closest z vertex")

options.register('doJetTauCrossCleaning',
                 False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Enable cleaning the jet collections based on taus")

options.parseArguments()


if not options.useData :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

    process.source.fileNames = [
        '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0076C8E3-9AE1-E111-917C-003048D439AA.root'
    ]

else :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
    process.source.fileNames = [
        '/store/data/Run2012A/Jet/AOD/23May2012-v2/0000/FCCBC3B4-C2A5-E111-B4E8-00A0D1EE8ECC.root'
    ]

print options

print 'Running jet corrections: '
print inputJetCorrLabel

import sys


###############################
####### Global Setup ##########
###############################

if options.useData :
    if options.globalTag is '':
        process.GlobalTag.globaltag = cms.string( 'GR_P_V40_AN1::All' )
    else:
        process.GlobalTag.globaltag = cms.string( options.globalTag )
else :
    if options.globalTag is '':
        process.GlobalTag.globaltag = cms.string( 'START53_V7E::All' )
    else:
        process.GlobalTag.globaltag = cms.string( options.globalTag )


from PhysicsTools.PatAlgos.patTemplate_cfg import *

###############################
####### DAF PV's     ##########
###############################

pvSrc = 'offlinePrimaryVertices'

## The good primary vertex filter ____________________________________________||
process.primaryVertexFilter = cms.EDFilter(
    "VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake & ndof > 4 & abs(z) <= 24 & position.Rho <= 2"),
    filter = cms.bool(True)
    )


from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0),
                                     minNdof = cms.double(4.0) # this is >= 4
                                     ),
    src=cms.InputTag(pvSrc)
    )

###############################
#### Jet RECO includes ########
###############################

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *
#from RecoJets.JetProducers.GenJetParameters_cfi import *


###############################
########## PF Setup ###########
###############################

# Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff. 
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix,
	  jetCorrections=inputJetCorrLabel, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), typeIMetCorrections=False)
#useGsfElectrons(process,postfix,dR="03")
if not options.forceCheckClosestZVertex :
    process.pfPileUpPFlow.checkClosestZVertex = False

# change the cone size of electron isolation to 0.3 as default.
process.pfIsolatedElectronsPFlow.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFIdPFlow"))
process.pfIsolatedElectronsPFlow.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFIdPFlow")
process.pfIsolatedElectronsPFlow.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("elPFIsoValueNeutral03PFIdPFlow"), cms.InputTag("elPFIsoValueGamma03PFIdPFlow"))

process.pfElectronsPFlow.isolationValueMapsCharged  = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFIdPFlow"))
process.pfElectronsPFlow.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFIdPFlow" )
process.pfElectronsPFlow.isolationValueMapsNeutral  = cms.VInputTag(cms.InputTag( "elPFIsoValueNeutral03PFIdPFlow"), cms.InputTag("elPFIsoValueGamma03PFIdPFlow"))

process.patElectronsPFlow.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFIdPFlow"),
        pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFIdPFlow"),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFIdPFlow"),
        pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFIdPFlow"),
        pfPhotons = cms.InputTag("elPFIsoValueGamma03PFIdPFlow")
        )

# enable/disable tau cleaning
if not options.doJetTauCrossCleaning:
    # if jetCrossCleaning is false, we want to disable
    # the cross cleaning (which is on by default)
    getattr(process,"pfNoTau"+postfix).enable = False
    #getattr(process,"pfNoTau"+postfixLoose).enable = False
else:
    getattr(process,"pfNoTau"+postfix).enable = False
    #getattr(process,"pfNoTau"+postfixLoose).enable = False

# Keep additional PF information for taus
# embed in AOD externally stored leading PFChargedHadron candidate
process.patTausPFlow.embedLeadPFChargedHadrCand = cms.bool(True)  
# embed in AOD externally stored signal PFChargedHadronCandidates
process.patTausPFlow.embedSignalPFChargedHadrCands = cms.bool(True)  
# embed in AOD externally stored signal PFGammaCandidates
process.patTausPFlow.embedSignalPFGammaCands = cms.bool(True) 
# embed in AOD externally stored isolation PFChargedHadronCandidates
process.patTausPFlow.embedIsolationPFChargedHadrCands = cms.bool(True) 
# embed in AOD externally stored isolation PFGammaCandidates
process.patTausPFlow.embedIsolationPFGammaCands = cms.bool(True)
# embed in AOD externally stored leading PFChargedHadron candidate
process.patTaus.embedLeadPFChargedHadrCand = cms.bool(True)  
# embed in AOD externally stored signal PFChargedHadronCandidates 
process.patTaus.embedSignalPFChargedHadrCands = cms.bool(True)  
# embed in AOD externally stored signal PFGammaCandidates
process.patTaus.embedSignalPFGammaCands = cms.bool(True) 
# embed in AOD externally stored isolation PFChargedHadronCandidates 
process.patTaus.embedIsolationPFChargedHadrCands = cms.bool(True) 
# embed in AOD externally stored isolation PFGammaCandidates
process.patTaus.embedIsolationPFGammaCands = cms.bool(True)

# turn to false when running on data
if options.useData :
    removeMCMatching( process, ['All'] )

###############################
###### Electron ID ############
###############################

process.load('EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi') 
process.eidMVASequence = cms.Sequence(  process.mvaTrigV0 + process.mvaNonTrigV0 )
#Electron ID
process.patElectronsPFlow.electronIDSources.mvaTrigV0    = cms.InputTag("mvaTrigV0")
process.patElectronsPFlow.electronIDSources.mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0") 
process.patPF2PATSequencePFlow.replace( process.patElectronsPFlow, process.eidMVASequence * process.patElectronsPFlow )

#process.patElectronsPFlowLoose.electronIDSources.mvaTrigV0    = cms.InputTag("mvaTrigV0")
#process.patElectronsPFlowLoose.electronIDSources.mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0") 
#process.patPF2PATSequencePFlowLoose.replace( process.patElectronsPFlowLoose, process.eidMVASequence * process.patElectronsPFlowLoose )

#Convesion Rejection
# this should be your last selected electron collection name since currently index is used to match with electron later. We can fix this using reference pointer.
process.patConversionsPFlow = cms.EDProducer("PATConversionProducer",
                                             electronSource = cms.InputTag("selectedPatElectronsPFlow")      
                                             )
process.patPF2PATSequencePFlow += process.patConversionsPFlow
#process.patConversionsPFlowLoose = cms.EDProducer("PATConversionProducer",
#                                                  electronSource = cms.InputTag("selectedPatElectronsPFlowLoose")  
#                                                  )
#process.patPF2PATSequencePFlowLoose += process.patConversionsPFlowLoose

"""
###############################
###### Bare KT 0.6 jets #######
###############################

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
from RecoJets.JetProducers.kt4PFJets_cfi import *
process.kt6PFJetsForIsolation =  kt4PFJets.clone(
    rParam = 0.6,
    doRhoFastjet = True,
    Rho_EtaMax = cms.double(2.5)
    )
"""

###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    Ghost_EtaMax = cms.double(7.0)
    )

#-------------------------------------------------------------------------------

from JetTools.AnalyzerToolbox.jettoolbox_cfi import *

process.CA8JetToolbox=JetToolbox.clone(
    jetSrc=cms.InputTag('goodPatJetsCA8PF'),
    doPruning=cms.bool(True),
    )

#-------------------------------------------------------------------------------

"""
###############################
###### AK 0.7 jets ############
###############################
process.ak7PFlow = process.pfJetsPFlow.clone(
	rParam = cms.double(0.7)
    )
"""

# CATopJet PF Jets

for ipostfix in [postfix] :
    for module in (
        getattr(process,"ca8PFJets" + ipostfix),
        #getattr(process,"CATopTagInfos" + ipostfix),
        #getattr(process,"CATopTagInfosHEPTopTag" + ipostfix),
        #getattr(process,"caTopTag" + ipostfix),
        #getattr(process,"caHEPTopTag" + ipostfix),
        #getattr(process,"caPruned" + ipostfix)
        ) :
        getattr(process,"patPF2PATSequence"+ipostfix).replace( getattr(process,"pfNoElectron"+ipostfix), getattr(process,"pfNoElectron"+ipostfix)*module )

# Use the good primary vertices everywhere. 
for imod in [process.patMuonsPFlow,
             #process.patMuonsPFlowLoose,
             process.patElectronsPFlow,
             #process.patElectronsPFlowLoose,
             process.patMuons,
             process.patElectrons] :
    imod.pvSrc = "goodOfflinePrimaryVertices"
    imod.embedTrack = True
    
addJetCollection(process, 
                 cms.InputTag('ca8PFJetsPFlow'),
                 'CA8', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=True,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 #genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )

switchJetCollection(process,cms.InputTag('ak5PFJets'),
		    doJTA        = False,
		    doBTagging   = False,
		    jetCorrLabel = inputJetCorrLabel,
		    doType1MET   = True,
		    #genJetCollection=cms.InputTag("ak5GenJetsNoNu"),
		    doJetID      = False
		    )

for icorr in [process.patJetCorrFactors,
	      #process.patJetCorrFactorsCATopTagPF,
	      #process.patJetCorrFactorsCAHEPTopTagPF,
              #process.patJetCorrFactorsCA8PrunedPF,
              process.patJetCorrFactorsCA8PF ] :
    icorr.rho = cms.InputTag("kt6PFJets", "rho")

###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
for jetcoll in (process.patJetsPFlow,
		#process.patJets,
                process.patJetsCA8PF,
                #process.patJetsCA8PrunedPF,
                #process.patJetsCATopTagPF,
                #process.patJetsCAHEPTopTagPF
                ) :

    # Add the calo towers and PFCandidates.
    # I'm being a little tricksy here, because I only
    # actually keep the products if the "writeFat" switch
    # is on. However, this allows for overlap checking
    # with the Refs so satisfies most use cases without
    # having to add to the object size
    jetcoll.addBTagInfo = False
    jetcoll.embedCaloTowers = True
    jetcoll.embedPFCandidates = True

# Add CATopTag and b-tag info... piggy-backing on b-tag functionality
process.patJetsPFlow.addBTagInfo = True
#process.patJetsCATopTagPF.addBTagInfo = True
#process.patJetsCAHEPTopTagPF.addBTagInfo = True
#process.patJetsCA8PrunedPF.addBTagInfo = True

#################################################
#### Fix the PV collections for the future ######
#################################################
for module in [#process.patJetCorrFactors,
               process.patJetCorrFactorsPFlow,
               #process.patJetCorrFactorsCATopTagPF,
               #process.patJetCorrFactorsCAHEPTopTagPF,
               #process.patJetCorrFactorsCA8PrunedPF,
               process.patJetCorrFactorsCA8PF
               ]:
    module.primaryVertices = "goodOfflinePrimaryVertices"

###############################
#### Selections Setup #########
###############################

# AK5 Jets
process.selectedPatJetsPFlow.cut = cms.string("pt > 5")
process.patJetsPFlow.addTagInfos = True
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAODPFlow")
    )
process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')

# CA8 jets
process.selectedPatJetsCA8PF.cut = cms.string("pt > 20")

# electrons
process.selectedPatElectrons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectrons.embedTrack = cms.bool(True)
process.selectedPatElectronsPFlow.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectronsPFlow.embedTrack = cms.bool(True)
#process.selectedPatElectronsPFlowLoose.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
#process.patElectronsPFlowLoose.embedTrack = cms.bool(True)
# muons
process.selectedPatMuons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patMuons.embedTrack = cms.bool(True)
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 2.5")
process.patMuonsPFlow.embedTrack = cms.bool(True)
#process.selectedPatMuonsPFlowLoose.cut = cms.string("pt > 10.0 & abs(eta) < 2.5")
#process.patMuonsPFlowLoose.embedTrack = cms.bool(True)
# taus
process.selectedPatTausPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.selectedPatTaus.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.patTausPFlow.isoDeposits = cms.PSet()
process.patTaus.isoDeposits = cms.PSet()
# photons
process.patPhotonsPFlow.isoDeposits = cms.PSet()
process.patPhotons.isoDeposits = cms.PSet()


# Apply jet ID to all of the jets upstream. We aren't going to screw around
# with this, most likely. So, we don't really to waste time with it
# at the analysis level. 
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJetsCA8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsCA8PF")
                                        )

## IVF and BCandidate producer for Vbb cross check analysis
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')

process.patseq = cms.Sequence(
    process.goodOfflinePrimaryVertices*
    process.softElectronCands*
    process.inclusiveVertexing*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.patDefaultSequence*
    process.goodPatJetsPFlow*
    process.goodPatJetsCA8PF*
    process.CA8JetToolbox
    )

process.p0 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p0')

process.out.fileName = cms.untracked.string('jetToolbox.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

# process all the events
process.maxEvents.input = 10
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")

"""
process.out.outputCommands = [
    'drop *',
    'keep *_*_*_*'
    ]
"""

process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',
    'drop patJets_selectedPat*_*_*',
    'keep patJets_selectedPatJetsCA12MassDropFilteredSubjetsPF*_*_*',
    'drop *_selectedPatJets_*_*',    
    'keep *_patMETs*_*_*',
#    'keep *_offlinePrimaryVertices*_*_*',
#    'keep *_kt6PFJets*_*_*',
    'keep *_goodOfflinePrimaryVertices*_*_*',    
    'drop patPFParticles_*_*_*',
#    'drop patTaus_*_*_*',
    'keep recoPFJets_caPruned*_*_*',
    'keep recoPFJets_ca*Filtered*_*_*',
    'keep recoPFJets_caTopTag*_*_*',
    'keep recoPFJets_caHEPTopTag*_*_*',
    'keep patTriggerObjects_patTriggerPFlow_*_*',
    'keep patTriggerFilters_patTriggerPFlow_*_*',
    'keep patTriggerPaths_patTriggerPFlow_*_*',
    'keep patTriggerEvent_patTriggerEventPFlow_*_*',
    'keep *_cleanPatPhotonsTriggerMatch*_*_*',
    'keep *_cleanPatElectronsTriggerMatch*_*_*',
    'keep *_cleanPatMuonsTriggerMatch*_*_*',
    'keep *_cleanPatTausTriggerMatch*_*_*',
    'keep *_cleanPatJetsTriggerMatch*_*_*',
    'keep *_patMETsTriggerMatch*_*_*',
    'keep double_*_*_PAT',
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_caTopTagPFlow_*_*',
    'keep *_caPrunedPFlow_*_*',
    'keep *_CATopTagInfosPFlow_*_*',
    'keep *_prunedGenParticles_*_*',
    'drop recoPFCandidates_selectedPatJets*_*_*',
    'keep recoPFCandidates_selectedPatJetsPFlow_*_*',
    'drop CaloTowers_selectedPatJets*_*_*',
    'drop recoBasicJets_*_*_*',
    'keep *_*Lite_*_*',
    'drop patJets_goodPatJetsAK5FilteredPF_*_*',
    'drop patJets_goodPatJetsAK5PrunedPF_*_*',
    'drop patJets_goodPatJetsAK5TrimmedPF_*_*',
    'drop patJets_goodPatJetsAK7PF_*_*',
    'drop patJets_goodPatJetsAK7FilteredPF_*_*',
    'drop patJets_goodPatJetsAK7PrunedPF_*_*',
    'drop patJets_goodPatJetsAK7TrimmedPF_*_*',
    'drop patJets_goodPatJetsAK8PF_*_*',
    'drop patJets_goodPatJetsAK8FilteredPF_*_*',
    'drop patJets_goodPatJetsAK8PrunedPF_*_*',
    'drop patJets_goodPatJetsAK8TrimmedPF_*_*',
    'drop recoGenJets_selectedPatJets*_*_*',
    'keep *_*_rho_*',
    'drop *_*PFlowLoose*_*_*',
    'keep patElectrons_selected*PFlowLoose*_*_*',
    'keep patMuons_selected*PFlowLoose*_*_*',
    'keep *_patConversions*_*_*',
    #'keep patTaus_*PFlowLoose*_*_*',
    'keep *_offlineBeamSpot_*_*',
    'drop *_*atTaus_*_*',
    'keep *_pfType1CorrectedMet_*_*',
    'keep *_pfType1p2CorrectedMet_*_*',
    #'keep recoTracks_generalTracks_*_*',
    'keep *_CA8JetToolbox_*_*'
    ]

open('junk.py','w').write(process.dumpPython())
