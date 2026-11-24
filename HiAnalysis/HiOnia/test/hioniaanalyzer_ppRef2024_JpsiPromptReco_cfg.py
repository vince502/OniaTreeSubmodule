import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras


HLTProcess = "HLT"
isMC = False
muonSelection = "GlbOrTrk"
applyEventSel = True
OnlySoftMuons = False
applyCuts = False
SumETvariables = False
SofterSgMuAcceptance = False
doTrimuons = False
doDimuonTrk = False
atLeastOneCand = False
OneMatchedHLTMu = -1
keepExtraColl = False
miniAOD = True
UsePropToMuonSt = True
pdgId = 443
useMomFormat = "vector"


process = cms.Process("HIOnia", eras.Run3_2024_ppRef)

options = VarParsing.VarParsing("analysis")
options.outputFile = "Oniatree_Jpsi_ppRef2024Data_141X.root"
options.secondaryOutputFile = "Jpsi_DataSet.root"
options.inputFiles = [
    "/store/data/Run2024J/PPRefDoubleMuon0/MINIAOD/PromptReco-v1/000/387/445/00000/fe6e7398-7787-4ef1-b3c9-495e937c3bcc.root",
]
options.maxEvents = -1
options.parseArguments()

triggerList = {
    "DoubleMuonTrigger": cms.vstring(
        "HLT_PPRefL1DoubleMu0_Open_v",
        "HLT_PPRefL1DoubleMu0_v",
        "HLT_PPRefL1DoubleMu0_SQ_v",
        "HLT_PPRefL1DoubleMu2_v",
        "HLT_PPRefL1DoubleMu2_SQ_v",
        "HLT_PPRefL2DoubleMu0_Open_v",
        "HLT_PPRefL2DoubleMu0_v",
        "HLT_PPRefL3DoubleMu0_Open_v",
        "HLT_PPRefL3DoubleMu0_v",
    ),
    "SingleMuonTrigger": cms.vstring(
        "HLT_PPRefL1SingleMu7_v",
        "HLT_PPRefL1SingleMu12_v",
        "HLT_PPRefL2SingleMu7_v",
        "HLT_PPRefL2SingleMu12_v",
        "HLT_PPRefL2SingleMu15_v",
        "HLT_PPRefL3SingleMu3_v",
        "HLT_PPRefL3SingleMu5_v",
        "HLT_PPRefL3SingleMu7_v",
        "HLT_PPRefL3SingleMu12_v",
        "HLT_PPRefL3SingleMu15_v",
        "HLT_PPRefL3SingleMu20_v",
    ),
}

process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load("Configuration.Geometry.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, "141X_dataRun3_Prompt_v3", "")

from HiAnalysis.HiOnia.oniaTreeAnalyzer_cff import oniaTreeAnalyzer

oniaTreeAnalyzer(
    process,
    muonTriggerList=triggerList,
    HLTProName=HLTProcess,
    muonSelection=muonSelection,
    L1Stage=2,
    isMC=isMC,
    pdgID=pdgId,
    outputFileName=options.outputFile,
    doTrimu=doTrimuons,
    doDimuTrk=doDimuonTrk,
)

process.onia2MuMuPatGlbGlb.dimuonSelection = cms.string(
    "(2.4 < mass && mass < 5.0) && charge == 0 && pt > 4.0 && "
    "abs(rapidity) < 2.4 && "
    "abs(daughter('muon1').innerTrack.dz - daughter('muon2').innerTrack.dz) < 25 && "
    "daughter('muon1').muonID('TMOneStationTight') && "
    "daughter('muon2').muonID('TMOneStationTight') && "
    "daughter('muon1').isPFMuon() && daughter('muon2').isPFMuon()"
)
process.onia2MuMuPatGlbGlb.LateDimuonSel = cms.string('userFloat("vProb") > 0.01')
process.onia2MuMuPatGlbGlb.dimuonMassHypothesis = cms.double(3.096916)
process.onia2MuMuPatGlbGlb.onlySoftMuons = cms.bool(OnlySoftMuons)

process.hionia.minimumFlag = cms.bool(keepExtraColl)
process.hionia.useGeTracks = cms.untracked.bool(keepExtraColl)
process.hionia.fillRecoTracks = cms.bool(keepExtraColl)
process.hionia.SofterSgMuAcceptance = cms.bool(SofterSgMuAcceptance)
process.hionia.SumETvariables = cms.bool(SumETvariables)
process.hionia.applyCuts = cms.bool(applyCuts)
process.hionia.AtLeastOneCand = cms.bool(atLeastOneCand)
process.hionia.OneMatchedHLTMu = cms.int32(OneMatchedHLTMu)
process.hionia.checkTrigNames = cms.bool(False)
process.hionia.mom4format = cms.string(useMomFormat)
process.hionia.isHI = cms.untracked.bool(False)
process.hionia.useBeamSpot = cms.bool(False)

if applyEventSel:
    process.load("HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff")

    import HLTrigger.HLTfilters.hltHighLevel_cfi

    process.hltHI = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
    process.hltHI.HLTPaths = ["HLT_PPRefL*DoubleMu*_v*", "HLT_PPRefL*SingleMu*_v*"]
    process.hltHI.throw = False
    process.hltHI.andOr = True

    process.oniaTreeAna.replace(
        process.patMuonSequence,
        process.primaryVertexFilter * process.hltHI * process.patMuonSequence,
    )

if atLeastOneCand:
    if doTrimuons:
        process.oniaTreeAna.replace(
            process.onia2MuMuPatGlbGlb,
            process.onia2MuMuPatGlbGlb * process.onia2MuMuPatGlbGlbFilterTrimu,
        )
        process.oniaTreeAna.replace(
            process.patMuonSequence,
            process.filter3mu * process.pseudoDimuonFilterSequence * process.patMuonSequence,
        )
    elif doDimuonTrk:
        process.oniaTreeAna.replace(
            process.onia2MuMuPatGlbGlb,
            process.onia2MuMuPatGlbGlb * process.onia2MuMuPatGlbGlbFilterDimutrk,
        )
        process.oniaTreeAna.replace(
            process.patMuonSequence,
            process.pseudoDimuonFilterSequence * process.patMuonSequence,
        )
    else:
        process.oniaTreeAna.replace(
            process.onia2MuMuPatGlbGlb,
            process.onia2MuMuPatGlbGlb * process.onia2MuMuPatGlbGlbFilter,
        )
        process.oniaTreeAna.replace(
            process.patMuonSequence,
            process.pseudoDimuonFilterSequence * process.patMuonSequence,
        )

process.oniaTreeAna = cms.Path(process.oniaTreeAna)

if miniAOD:
    from HiSkim.HiOnia2MuMu.onia2MuMuPAT_cff import changeToMiniAOD

    changeToMiniAOD(process)
    process.unpackedMuons.addPropToMuonSt = cms.bool(UsePropToMuonSt)

process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(options.inputFiles),
)
process.TFileService = cms.Service("TFileService", fileName=cms.string(options.outputFile))
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(options.maxEvents))
process.options = cms.untracked.PSet(
    wantSummary=cms.untracked.bool(True),
    numberOfThreads=cms.untracked.uint32(1),
)
process.schedule = cms.Schedule(process.oniaTreeAna)
