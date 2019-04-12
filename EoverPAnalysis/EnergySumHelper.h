#ifndef eoverpanalysis_EnergySumHelper_H
#define eoverpanalysis_EnergySumHelper_H

#include <map>
#include <xAODTracking/TrackParticleContainer.h>

namespace EnergySumHelper
{

// LAr barrel
//CALOSAMPLING(PreSamplerB, 1, 0) //  0
//CALOSAMPLING(EMB1,        1, 0) //  1
//CALOSAMPLING(EMB2,        1, 0) //  2
//CALOSAMPLING(EMB3,        1, 0) //  3

// LAr EM endcap
//CALOSAMPLING(PreSamplerE, 0, 1) //  4
//CALOSAMPLING(EME1,        0, 1) //  5
//CALOSAMPLING(EME2,        0, 1) //  6
//CALOSAMPLING(EME3,        0, 1) //  7

// Hadronic endcap
//CALOSAMPLING(HEC0,        0, 1) //  8
//CALOSAMPLING(HEC1,        0, 1) //  9
//CALOSAMPLING(HEC2,        0, 1) // 10
//CALOSAMPLING(HEC3,        0, 1) // 11

// Tile barrel
//CALOSAMPLING(TileBar0,    1, 0) // 12
//CALOSAMPLING(TileBar1,    1, 0) // 13
//CALOSAMPLING(TileBar2,    1, 0) // 14

// Tile gap (ITC & scint)
//CALOSAMPLING(TileGap1,    1, 0) // 15
//CALOSAMPLING(TileGap2,    1, 0) // 16
//CALOSAMPLING(TileGap3,    1, 0) // 17

// Tile extended barrel
//CALOSAMPLING(TileExt0,    1, 0) // 18
//CALOSAMPLING(TileExt1,    1, 0) // 19
//CALOSAMPLING(TileExt2,    1, 0) // 20

// Forward EM endcap
//CALOSAMPLING(FCAL0,       0, 1) // 21
//CALOSAMPLING(FCAL1,       0, 1) // 22
//CALOSAMPLING(FCAL2,       0, 1) // 23

// MiniFCAL
//CALOSAMPLING(MINIFCAL0,   0, 1) // 24
//CALOSAMPLING(MINIFCAL1,   0, 1) // 25
//CALOSAMPLING(MINIFCAL2,   0, 1) // 26
//CALOSAMPLING(MINIFCAL3,   0, 1) // 27


    const std::vector<std::string> layer = {
                        "PreSamplerB", //0
					    "EMB1", //1
					    "EMB2", //2
					    "EMB3", //3
					    "PreSamplerE", //4
					    "EME1", //5
					    "EME2", //6
					    "EME3", //7
					    "HEC0", //8
					    "HEC1", //9
					    "HEC2", //10
					    "HEC3", //11
					    "TileBar0", //12
					    "TileBar1", //13
					    "TileBar2", //14
					    "TileGap1", //15
					    "TileGap2", //16
					    "TileGap3", //17
					    "TileExt0", //18
					    "TileExt1", //19
					    "TileExt2" //20
                        }; //! array of all the calo layers
    
    const std::vector<std::string> layer_EM = {
                           "PreSamplerB",
					       "EMB1",
					       "EMB2",
					       "EMB3", 
					       "PreSamplerE", 
					       "EME1",
					       "EME2",
					       "EME3"
                           };

    const std::vector<std::string> layer_HAD = {
                        "TileBar0",
						"TileBar1", 
						"TileBar2",
						"TileGap1",
						"TileGap2",
						"TileGap3",
						"TileExt0",
						"TileExt1",
						"TileExt2", 
						"HEC0",
						"HEC1",
						"HEC2",
						"HEC3"
                        }; //! array of HAD layers only

    const std::map<std::string, unsigned int> layer_to_id = {
                                  {"PreSamplerB", 0},
							      {"EMB1", 1},
							      {"EMB2", 2},
							      {"EMB3", 3},
							      {"PreSamplerE", 4}, 
							      {"EME1", 5},
							      {"EME2", 6}, 
							      {"EME3", 7},
							      {"HEC0", 8},
							      {"HEC1", 9},
							      {"HEC2", 10},
							      {"HEC3", 11},
							      {"TileBar0", 12},
							      {"TileBar1", 13},
							      {"TileBar2", 14},
							      {"TileGap1", 15},
							      {"TileGap2", 16},
							      {"TileGap3", 17},
							      {"TileExt0", 18},
							      {"TileExt1", 19},
							      {"TileExt2", 20}
                                  };

    const std::map<unsigned int, std::string> id_to_layer = { 
                                  {0, "PreSamplerB"},
							      {1, "PreSamplerE"},
							      {2, "EMB1"},
							      {3, "EMB2"},
							      {4, "EMB3"},
							      {5, "EME1"},
							      {6, "EME2"},
							      {7, "EME3"},
							      {8, "HEC0"}, 
							      {9, "HEC1"}, 
							      {10, "HEC2"},
							      {11, "HEC3"},
							      {12, "TileBar0"},
							      {13, "TileBar1"},
							      {14, "TileBar2"},
							      {15, "TileGap1"},
							      {16, "TileGap2"},
							      {17, "TileGap3"},
							      {18, "TileExt0"}, 
							      {19, "TileExt1"}, 
							      {20, "TileExt2"}
                                  };

    extern std::map<unsigned int, float> getEnergySumInLayers(const xAOD::TrackParticle* trk, 
							      std::string variableToSum,
							      std::string radiusCut);
    
    extern std::map<std::string, float> getEnergySumInCalorimeterRegions(const xAOD::TrackParticle* trk,
									 std::string variableToSum, 
									 std::string radiusCut,
									 bool onlyPositiveEnergy = false);
}

#endif
