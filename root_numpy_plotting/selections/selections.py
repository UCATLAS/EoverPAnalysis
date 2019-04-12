from calculation.calculation import calculation, calculationDataMC
import numpy as np

def NoSelection(trk):
    return np.ones(len(trk)) > 0.0
branches = []
sel_NoSelection = calculation(NoSelection, branches)

def hasHADExtrapolation(trk):
    return (trk["trk_phiHEC1"] > -100) | (trk["trk_phiTileBar2"] > -100) | (trk["trk_phiTileExt1"] > -100)
branches =["trk_phiHEC1", "trk_phiTileBar2", "trk_phiTileExt1"]
sel_hasHADExtrapolation = calculation(hasHADExtrapolation, branches)

#A selection for plotting event-based variables
def Event(trk):
    '''get only the variables associated with the first track in the event.
    This is so that we can reweight variables with an event, and not with individual tracks'''
    return (trk["trkIndex"] < 0.5) & (trk["trkIndex"] > -0.5)
branches = ["trkIndex"]
sel_Event = calculation(Event, branches)

#These are the definitions of the different types of track classifications according to tracking CP
def TruthLink(trk):
    return trk["trk_hasTruthParticle"] == 1

def TruthMatched(trk):
    return trk["trk_truthProb"] > 0.5

def Fake(trk):
    return np.logical_not(TruthMatched(trk))
branches = ["trk_truthProb"]
sel_Fake = calculation(Fake, branches)

def Pileup(trk):
    return TruthMatched(trk) & np.logical_not(TruthLink(trk))
branches = ["trk_truthProb", "trk_hasTruthParticle"]
sel_Pileup = calculation(Pileup, branches)

def HardScatter(trk):
    return TruthMatched(trk) & TruthLink(trk)
branches = ["trk_truthProb", "trk_hasTruthParticle"]
sel_HardScatter = calculation(HardScatter, branches)

def Pion(trk):
    return  (np.abs(trk["trk_truthPdgId"] - 211.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_Pion = calculation(Pion, branches)

def AntiPion(trk):
    return ( np.abs(trk["trk_truthPdgId"] + 211.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_AntiPion = calculation(AntiPion, branches)

def AnyPion(trk):
    return Pion(trk) | AntiPion(trk)
sel_AnyPion = calculation(AnyPion, branches)

def Proton(trk):
    return (np.abs(trk["trk_truthPdgId"] - 2212.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_Proton = calculation(Proton, branches)

def AntiProton(trk):
    return (np.abs(trk["trk_truthPdgId"] + 2212.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_AntiProton = calculation(AntiProton, branches)

def AnyProton(trk):
    return Proton(trk) | AntiProton(trk)
branches = ["trk_truthPdgId"]
sel_AnyProton = calculation(AnyProton, branches)

def Kaon(trk):
    return (np.abs(trk["trk_truthPdgId"] - 321.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_Kaon = calculation(Kaon, branches)

def AntiKaon(trk):
    return (np.abs(trk["trk_truthPdgId"] + 321.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_AntiKaon = calculation(AntiKaon, branches)

def AnyKaon(trk):
    return (Kaon(trk) | AntiKaon(trk))
branches = ["trk_truthPdgId"]
sel_AnyKaon = calculation(AnyKaon, branches)

def Muon(trk):
    return (np.abs(trk["trk_truthPdgId"] - 13.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_Muon = calculation(Muon, branches)

def AntiMuon(trk):
    return (np.abs(trk["trk_truthPdgId"] + 13.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_AntiMuon = calculation(AntiMuon, branches)

def AnyMuon(trk):
    return (Muon(trk) | AntiMuon(trk))
branches = ["trk_truthPdgId"]
sel_AnyMuon = calculation(AnyMuon, branches)

def Electron(trk):
    return (np.abs(trk["trk_truthPdgId"] - 11.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_Electron = calculation(Electron, branches)

def AntiElectron(trk):
    return (np.abs(trk["trk_truthPdgId"] + 11.0) < 0.1)
branches = ["trk_truthPdgId"]
sel_AntiElectron = calculation(AntiElectron, branches)

def AnyElectron(trk):
    return (Electron(trk) | AntiElectron(trk))
branches = ["trk_truthPdgId"]
sel_AnyElectron = calculation(AnyElectron, branches)
##########################################################################

#Define a significant hadron energy deposit with the amount of energy in the HAD calorimeter
def EHadBetween30And90OfMomentum(trk):
    '''At least 30 % of the track momentum and no more than 90 % of the track momentum was found the HAD calorimeter'''
    E_HAD_frac = trk["trk_ClusterEnergy_HAD_200"]/trk["trk_p"]
    return (E_HAD_frac > 0.3) & (E_HAD_frac < 0.9) #This selection only works for EM-scale
branches = ["trk_ClusterEnergy_HAD_200", "trk_p"]
sel_EHadBetween30And90OfMomentum = calculation(EHadBetween30And90OfMomentum, branches)

def Lar1_1GeV(trk):
    return trk["trk_ClusterEnergy_EM_100"] < 1.1
branches = ["trk_ClusterEnergy_EM_100"]
sel_Lar1_1GeV = calculation(Lar1_1GeV, branches)

def Z0SinThetaLess1_5(trk):
    return trk["trk_z0sintheta"] < 1.5
branches = ["trk_z0sintheta"]
sel_Z0SinThetaLess1_5 = calculation(Z0SinThetaLess1_5, branches)

def d0Less1_5(trk):
    return trk["trk_d0"] < 1.5
branches = ["trk_d0"]
sel_d0Less1_5 = calculation(d0Less1_5, branches)

def EM2AcceptanceCalculator(trk, min_cut, max_cut):
    trk_etaEMB = np.abs(trk["trk_etaEMB2"])
    trk_etaEME = np.abs(trk["trk_etaEME2"])

    upper_in_acceptance_EMB = trk_etaEMB < max_cut
    upper_in_acceptance_EME = trk_etaEME < max_cut

    lower_in_acceptance_EMB = trk_etaEMB > min_cut
    lower_in_acceptance_EME = trk_etaEME > min_cut

    return (upper_in_acceptance_EMB | upper_in_acceptance_EME) & (lower_in_acceptance_EMB | lower_in_acceptance_EME)

def NonZeroEnergy(trk):
    return (trk["trk_nclusters_EM"] + trk["trk_nclusters_HAD"]) > 0.5 #there was at least one cluster assocated with the track
branches = ["trk_nclusters_EM", "trk_nclusters_HAD"]
sel_NonZeroEnergy = calculation(NonZeroEnergy, branches)

def ELessEqual0(trk):
    return (trk["trk_ClusterEnergy_EM_200"] + trk["trk_ClusterEnergy_HAD_200"]) <= 1e-6
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_HAD_200"]
sel_ELessEqual0 = calculation(ELessEqual0, branches)

def EHadFracAbove70(trk):
    return ((trk["trk_ClusterEnergy_HAD_200"]) / (trk["trk_ClusterEnergy_EM_200"] + trk["trk_ClusterEnergy_HAD_200"]) >= 0.7) & ((trk["trk_ClusterEnergy_EM_200"] + trk["trk_ClusterEnergy_HAD_200"]) > 0.0)
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_HAD_200"]
sel_EHadFracAbove70 = calculation(EHadFracAbove70, branches)

#A general function to pick different regions of the atlas detector based on track eta in the ID
def IDAcceptanceCalculator(trk, min_cut, max_cut):
    trk_etaID = np.abs(trk["trk_etaID"])
    upper_in_acceptance = trk_etaID < max_cut
    lower_in_acceptance = trk_etaID > min_cut
    return (upper_in_acceptance & lower_in_acceptance)

#You can do fancy things with lambda functions here
def EtaBin(trk, min_cut, max_cut):
    return IDAcceptanceCalculator(trk, min_cut, max_cut)

def PBin(trk, min_cut, max_cut):
    return (trk["trk_p"] > min_cut) & (trk["trk_p"] <= max_cut)

def ECALEta0_6(trk):
    return EM2AcceptanceCalculator(trk, 0.0, 0.6)
branches = ["trk_etaEMB2", "trk_etaEME2"]
sel_ECALEta0_6 = calculation(ECALEta0_6, branches)

#### Here are the eta track selections ###
def IDEta00_06(trk):
    return IDAcceptanceCalculator(trk, 0.0, 0.6)
branches = ["trk_etaID"]
sel_IDEta00_06 = calculation(IDEta00_06, branches)

#### Here are the eta track selections ###
def IDEta00_02(trk):
    return IDAcceptanceCalculator(trk, 0.0, 0.2)
branches = ["trk_etaID"]
sel_IDEta00_02 = calculation(IDEta00_02, branches)

#### Here are the eta track selections ###
def IDEta02_04(trk):
    return IDAcceptanceCalculator(trk, 0.2, 0.4)
branches = ["trk_etaID"]
sel_IDEta02_04 = calculation(IDEta02_04, branches)

#### Here are the eta track selections ###
def IDEta04_06(trk):
    return IDAcceptanceCalculator(trk, 0.4, 0.6)
branches = ["trk_etaID"]
sel_IDEta04_06 = calculation(IDEta04_06, branches)

def IDEta06_11(trk):
    return IDAcceptanceCalculator(trk, 0.6, 1.1)
branches = ["trk_etaID"]
sel_IDEta06_11 = calculation(IDEta06_11, branches)

def IDEta11_14(trk):
    return IDAcceptanceCalculator(trk, 1.1, 1.4)
branches = ["trk_etaID"]
sel_IDEta11_14 = calculation(IDEta11_14, branches)

def IDEta14_15(trk):
    return IDAcceptanceCalculator(trk, 1.4, 1.5)
branches = ["trk_etaID"]
sel_IDEta14_15 = calculation(IDEta14_15, branches)

def IDEta15_18(trk):
    return IDAcceptanceCalculator(trk, 1.5, 1.8)
branches = ["trk_etaID"]
sel_IDEta15_18 = calculation(IDEta15_18, branches)

def IDEta18_23(trk):
    return IDAcceptanceCalculator(trk, 1.8, 2.3)
branches = ["trk_etaID"]
sel_IDEta18_23 = calculation(IDEta18_23, branches)

def IDEta19_23(trk):
    return IDAcceptanceCalculator(trk, 1.9, 2.3)
branches = ["trk_etaID"]
sel_IDEta19_23 = calculation(IDEta19_23, branches)

def PBetween12_18(trk):
    return (1.2 < trk["trk_p"]) & (trk["trk_p"] < 1.8)
branches = ["trk_p"]
sel_PBetween12_18 = calculation(PBetween12_18, branches)

def PBetween22_28(trk):
    return (2.2 < trk["trk_p"]) & (trk["trk_p"] < 2.8)
branches = ["trk_p"]
sel_PBetween22_28 = calculation(PBetween22_28, branches)

def PBetween28_36(trk):
    return (2.8 < trk["trk_p"]) & (trk["trk_p"] < 3.6)
branches = ["trk_p"]
sel_PBetween28_36 = calculation(PBetween28_36, branches)

def NTRT15(trk):
    return (trk["trk_nTRT"] >= 15) | (np.abs(trk["trk_etaID"]) > 2.0)
branches = ["trk_nTRT", "trk_etaID"]
sel_NTRT15 = calculation(NTRT15, branches)

def NTRT20(trk):
    print(trk["trk_nTRT"])
    print("This fraction of tracks in the TRT acceptance, failed the selection")
    print(np.sum(1.0 * np.logical_not((trk["trk_nTRT"] >= 20) & (np.abs(trk["trk_etaID"]) < 2.0)))/ (np.sum(1.0 * np.abs(trk["trk_etaID"]) < 2.0)))
    return (trk["trk_nTRT"] >= 20) | (np.abs(trk["trk_etaID"]) > 2.0)
branches = ["trk_nTRT", "trk_etaID"]
sel_NTRT20 = calculation(NTRT20, branches)

def NTRT25(trk):
    return (trk["trk_nTRT"] >= 25) | (np.abs(trk["trk_etaID"]) > 2.0)
branches = ["trk_nTRT", "trk_etaID"]
sel_NTRT25 = calculation(NTRT25, branches)

def NTRT30(trk):
    return (trk["trk_nTRT"] >= 30) | (np.abs(trk["trk_etaID"]) > 2.0)
branches = ["trk_nTRT", "trk_etaID"]
sel_NTRT30 = calculation(NTRT30, branches)

def NTRT35(trk):
    return (trk["trk_nTRT"] >= 35) | (np.abs(trk["trk_etaID"]) > 2.0)
branches = ["trk_nTRT", "trk_etaID"]
sel_NTRT35 = calculation(NTRT35, branches)

def TwoPV_TwoTracks(trk):
    return (trk["trk_NPV2"] == 2)
branches = ["trk_NPV2"]
sel_TwoPV_TwoTracks = calculation(TwoPV_TwoTracks, branches)

def ThreePV_TwoTracks(trk):
    return (trk["trk_NPV2"] == 3)
branches = ["trk_NPV2"]
sel_ThreePV_TwoTracks = calculation(ThreePV_TwoTracks, branches)

def FourPV_TwoTracks(trk):
    return (trk["trk_NPV2"] == 4)
branches = ["trk_NPV2"]
sel_FourPV_TwoTracks = calculation(FourPV_TwoTracks, branches)

def FivePV_TwoTracks(trk):
    return (trk["trk_NPV2"] == 5)
branches = ["trk_NPV2"]
sel_FivePV_TwoTracks = calculation(FivePV_TwoTracks, branches)

def SixPV_TwoTracks(trk):
    return (trk["trk_NPV2"] == 6)
branches = ["trk_NPV2"]
sel_SixPV_TwoTracks = calculation(SixPV_TwoTracks, branches)

def PGreater1(trk):
    return trk["trk_p"] > 1.0
branches =["trk_p"]
sel_PGreater1 = calculation(PGreater1, branches)

def PGreater1_5(trk):
    return trk["trk_p"] > 1.5
branches =["trk_p"]
sel_PGreater1_5 = calculation(PGreater1_5, branches)

def PGreater2(trk):
    return trk["trk_p"] > 2.0
branches =["trk_p"]
sel_PGreater2 = calculation(PGreater2, branches)

def PGreater2_5(trk):
    return trk["trk_p"] > 2.5
branches =["trk_p"]
sel_PGreater2_5 = calculation(PGreater2_5, branches)

def PGreater3(trk):
    return trk["trk_p"] > 3.0
branches =["trk_p"]
sel_PGreater3 = calculation(PGreater3, branches)


