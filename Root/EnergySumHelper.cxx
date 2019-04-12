#include "EoverPAnalysis/EnergySumHelper.h"

std::map<unsigned int, float> EnergySumHelper::getEnergySumInLayers(const xAOD::TrackParticle* trk, 
								    std::string variableToSum, 
								    std::string radiusCut)
{
  std::map<unsigned int, float> energySum;

  for (std::string layerName: layer) 
    {
      float trk_E_tmp = trk->auxdata<float>(std::string("CALO_"+variableToSum+"_"+layerName+"_" +radiusCut))/1.e3; 
      unsigned int i = layer_to_id.at(layerName);
      energySum[i] += trk_E_tmp;
    }
  return energySum;
}

std::map<std::string, float> EnergySumHelper::getEnergySumInCalorimeterRegions(const xAOD::TrackParticle* trk, 
									       std::string variableToSum, 
									       std::string radiusCut, 
									       bool onlyPositiveEnergy)
{
  std::map<unsigned int, float> energySum =  getEnergySumInLayers(trk, variableToSum, radiusCut);  
  std::map<std::string, float> energySumInCaloRegion;

  energySumInCaloRegion["HAD"] = 0.0;
  energySumInCaloRegion["EM"] = 0.0;

  for (std::string layerName: layer_HAD) 
    {
      float energy = energySum[layer_to_id.at(layerName)];
      if (onlyPositiveEnergy and (energy < 0.0))
	continue;
      energySumInCaloRegion["HAD"] += energy;
    }
  
  for (std::string layerName: layer_EM) 
    {
      float energy = energySum[layer_to_id.at(layerName)];
      if (onlyPositiveEnergy and (energy < 0.0))
	continue;
      energySumInCaloRegion["EM"] += energy;
    }

  return energySumInCaloRegion;
}
