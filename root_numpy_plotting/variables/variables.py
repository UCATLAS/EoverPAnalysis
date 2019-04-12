from calculation.calculation import calculation, calculationDataMC, weightCalculation
from selections.selections import NonZeroEnergy
import numpy as np
from math import pi

def HadFrac(trk):
    return (trk["trk_ClusterEnergy_HAD_200"]) / (trk["trk_ClusterEnergy_EM_200"] + trk["trk_ClusterEnergy_HAD_200"])
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_HAD_200"]
calc_HadFrac = calculation(HadFrac, branches)

def MomentumHadFrac(trk):
    return (trk["trk_ClusterEnergy_HAD_200"])/trk["trk_p"]
branches = ["trk_ClusterEnergy_HAD_200", "trk_p"]
calc_MomentumHadFrac = calculation(MomentumHadFrac, branches)

def EnergyEMDR100(trk):
    return (trk["trk_ClusterEnergy_EM_100"])
branches = ["trk_ClusterEnergy_EM_100"]
calc_EnergyEMDR100 = calculation(EnergyEMDR100, branches)

def nTRT(trk):
    return trk["trk_nTRT"]
branches = ["trk_nTRT"]
calc_nTRT = calculation(nTRT, branches)

def trkCount(trk):
    return np.zeros(len(trk))
branches = []
calc_trkCount = calculation(trkCount, branches)

def trkNClusters(trk):
    return trk["trk_nclusters"]
calc_trkNClusters = calculation(trkNClusters, ["trk_nclusters"])

def trkNClusters_EM(trk):
    return trk["trk_nclusters_EM"]
calc_trkNClusters_EM = calculation(trkNClusters_EM, ["trk_nclusters_EM"])

def trkNClusters_emlike(trk):
    return trk["trk_nclusters_emlike"]
calc_trkNClusters_emlike = calculation(trkNClusters_emlike, ["trk_nclusters_emlike"])

def trkNClusters_HAD(trk):
    return trk["trk_nclusters_HAD"]
calc_trkNClusters_HAD = calculation(trkNClusters_HAD, ["trk_nclusters_HAD"])

def trkNClusters_hadlike(trk):
    return trk["trk_nclusters_hadlike"]
calc_trkNClusters_hadlike = calculation(trkNClusters_hadlike, ["trk_nclusters_hadlike"])

def trkHADFraction(trk):
    trk_total_nonzero = NonZeroEnergy(trk)
    return_value = np.zeros(len(trk))
    return_value[trk_total_nonzero] = ((trk["trk_ClusterEnergy_HAD_200"])[trk_total_nonzero])/((trk["trk_ClusterEnergy_HAD_200"] + trk["trk_ClusterEnergy_EM_200"])[trk_total_nonzero])
    return return_value
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_HAD_200"]
calc_trkHADFraction = calculation(trkHADFraction, branches)

def trkEMFraction(trk):
    trk_total_nonzero = NonZeroEnergy(trk)
    return_value = np.zeros(len(trk))
    return_value[trk_total_nonzero] = trk["trk_ClusterEnergy_EM_200"]/(trk["trk_ClusterEnergy_EM_200"] + trk["trk_ClusterEnergy_HAD_200"])[trk_total_nonzero]
    return return_value
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_HAD_200"]
calc_trkEMFraction = calculation(trkEMFraction, branches)

def trkPt(trk):
    return trk["trk_pt"]
branches = ["trk_pt"]
calc_trkPt = calculation(trkPt, branches)

def trkEtaID(trk):
    return trk["trk_etaID"]
branches = ["trk_etaID"]
calc_trkEta = calculation(trkEtaID, branches)

def trkEtaID_ABS(trk):
    return np.abs(trk["trk_etaID"])
branches = ["trk_etaID"]
calc_trkEta_ABS = calculation(trkEtaID_ABS, branches)

def hasExtrapolationEMCal(trk):
    trk_etaEMB = np.abs(trk["trk_etaEMB2"])
    trk_etaEME = np.abs(trk["trk_etaEME2"])
    hasEMB = trk_etaEMB < 100.0
    hasEME = trk_etaEME < 100.0
    return hasEMB, hasEME

def trkEtaECAL(trk):
    hasEMB, hasEME = hasExtrapolationEMCal(trk)
    hasEME = np.logical_not(hasEMB) & (hasEME)
    print "This many tracks had extensions to both the barrel and the emec " + str(np.sum(1*(hasEMB & hasEME)))
    trkEtaECAL = np.ones(len(hasEMB)) * 100000.0
    trkEtaECAL[hasEMB] = trk["trk_etaEMB2"][hasEMB]
    trkEtaECAL[hasEME] = trk["trk_etaEME2"][hasEME]

    print(np.logical_not(hasEMB | hasEME))

    if (np.sum(1.0*np.logical_not(hasEMB | hasEME) > 1.5)):
        print(trk_etaEMB[np.logical_not(hasEMB | hasEME)])
        print(np.sum( 1 * np.logical_not(hasEMB | hasEME)))
        raise ValueError("one of the trakc did not have an extrapolation to the electromagnetic calorimeter")

    return trkEtaECAL

branches = ["trk_etaEMB2","trk_etaEME2"]
calc_trkEtaECAL = calculation(trkEtaECAL, branches)

def trkPhiECAL(trk):
    hasEMB, hasEME = hasExtrapolationEMCal(trk)
    hasEME = np.logical_not(hasEMB) & (hasEME)
    print "This many tracks had extensions to both the barrel and the emec " + str(np.sum(1*(hasEMB & hasEME)))

    trkPhiECAL = np.ones(len(hasEMB)) * 100000.0
    trkPhiECAL[hasEMB] = trk["trk_phiEMB2"][hasEMB]
    trkPhiECAL[hasEME] = trk["trk_phiEME2"][hasEME]

    print(np.logical_not(hasEMB | hasEME))

    if (np.sum(1.0*np.logical_not(hasEMB | hasEME) > 1.5)):
        print(trk_phiEMB[np.logical_not(hasEMB | hasEME)])
        print(np.sum( 1 * np.logical_not(hasEMB | hasEME)))
        raise ValueError("one of the trakc did not have an extrapolation to the electromagnetic calorimeter")

    return trkPhiECAL
branches = ["trk_phiEMB2","trk_phiEME2", "trk_etaEMB2","trk_etaEME2"]
calc_trkPhiECAL = calculation(trkPhiECAL, branches)

def trkNearestNeighbourEM2(trk):
    return trk["trk_nearest_dR_EM"]
branches = ["trk_nearest_dR_EM"]
calc_trkNearestNeighbourEM2 =  calculation(trkNearestNeighbourEM2, branches)

def trkNPV2(trk):
    return trk["trk_NPV_2"]
branches = ["trk_NPV_2"]
calc_trkNPV2 = calculation(trkNPV2, branches)

def trkNPV4(trk):
    return trk["trk_NPV_4"]
branches = ["trk_NPV_4"]
calc_trkNPV4 = calculation(trkNPV4, branches)

def trkAverageMu(trk):
    return trk["trk_averagemu"]
branches = ["trk_averagemu"]
calc_trkAverageMu = calculation(trkAverageMu, branches)

def trkP(trk):
    return trk["trk_p"]
branches = ["trk_p"]
calc_trkP = calculation(trkP, branches)

def trkEtaID(trk):
    return trk["trk_etaID"]
branches = ["trk_etaID"]
calc_trkEtaID = calculation(trkEtaID, branches)

def trkEtaEME2(trk):
    return trk["trk_etaEME2"]
branches = ["trk_etaEME2"]
calc_trkEtaEME2 = calculation(trkEtaEME2, branches)

def trkEtaEMB2(trk):
    return trk["trk_etaEMB2"]
branches = ["trk_etaEMB2"]
calc_trkEtaEMB2 = calculation(trkEtaEMB2, branches)

def EnergyAnulus(trk):
    return trk["trk_ClusterEnergy_EM_200"] - trk["trk_ClusterEnergy_EM_100"]
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_EM_100"]
calc_EnergyAnulus = calculation(EnergyAnulus, branches)

def EOPBkg(trk):
    return (1./trk["trk_p"]) * (4.0/3.0) * (EnergyAnulus(trk))
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_EM_100", "trk_p"]
calc_EOPBkg = calculation(EOPBkg, branches)

def EOP(trk):
    return (trk["trk_ClusterEnergy_EM_200"] + trk["trk_ClusterEnergy_HAD_200"])/trk["trk_p"]
branches = ["trk_ClusterEnergy_EM_200", "trk_ClusterEnergy_HAD_200", "trk_p"]
calc_EOP = calculation(EOP, branches)

def DPhi(trk):
    dphi = np.ones(len(trk)) * 100000000.0
    hasEMB2 = np.abs(trk["trk_phiEMB2"]) < 40
    hasEME2 = np.abs(trk["trk_phiEME2"]) < 40
    if np.any(hasEMB2 & hasEME2):
        print("This many tracks had an extrapolation to both EME and EMB " + str(np.sum(1.0 * (hasEMB2 & hasEME2))))
    dphi[hasEME2] = np.abs(trk["trk_phiID"] - trk["trk_phiEME2"])[hasEME2]
    dphi[hasEMB2] = np.abs(trk["trk_phiID"] - trk["trk_phiEMB2"])[hasEMB2]
    greater_than_pi = dphi > pi

    dphi[greater_than_pi] = 2.0 * pi - dphi[greater_than_pi]
    return dphi
branches = ["trk_phiEMB2", "trk_phiEME2","trk_phiID"]
calc_trkDPhi = calculation(DPhi, branches)

def DEta(trk):
    deta = np.ones(len(trk)) * 100000000.0
    hasEMB2 = np.abs(trk["trk_etaEMB2"]) < 40
    hasEME2 = np.abs(trk["trk_etaEME2"]) < 40
    if np.any(hasEMB2 & hasEME2):
        print("This many tracks had an extrapolation to both EME and EMB " + str(np.sum(1.0 * (hasEMB2 & hasEME2))))
    deta[hasEME2] = np.abs(trk["trk_etaID"] - trk["trk_etaEME2"])[hasEME2]
    deta[hasEMB2] = np.abs(trk["trk_etaID"] - trk["trk_etaEMB2"])[hasEMB2]
    return deta

branches = ["trk_etaEMB2", "trk_etaEME2","trk_etaID"]
calc_trkDEta = calculation(DEta, branches)

def weight(trk, isData):
    if not isData:
        return trk["trkWeight"]
    return np.ones(len(trk))
branches = ["trkWeight"]
calc_weight = weightCalculation(weight, branches)
