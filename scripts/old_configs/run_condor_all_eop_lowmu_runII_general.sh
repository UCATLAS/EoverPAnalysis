#!/bin/bash
if [ $# -eq 0 ]

  then
    echo "Usage: source run_condor_all_eop_lowmu_runII_general.sh tag"

  else

    cd $WorkDir_DIR/../run

    tag=$1
    today=$(date +"%Y%m%d")
    files_data=EoverPAnalysis/filelists/data15_13TeV_lowmu_all.txt
    files_mc_ND=EoverPAnalysis/filelists/mc15_13TeV_lowmu_ND.txt
    files_mc_SD=EoverPAnalysis/filelists/mc15_13TeV_lowmu_SD.txt
    files_mc_DD=EoverPAnalysis/filelists/mc15_13TeV_lowmu_DD.txt

    mkdir -p results

    echo "---> Running data:"
    echo xAH_run.py --files ${files_data} --inputList --config EoverPAnalysis/scripts/config_eop_data_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_data_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_data} --inputList --config EoverPAnalysis/scripts/config_eop_data_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_data_${today}_${tag} --verbose --force condor --optFilesPerWorker 10

    # echo "---> Running MC:"
    echo xAH_run.py --files ${files_mc_ND} --inputList --config EoverPAnalysis/scripts/config_eop_mc_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_mc_ND_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    echo xAH_run.py --files ${files_mc_SD} --inputList --config EoverPAnalysis/scripts/config_eop_mc_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_mc_SD_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    echo xAH_run.py --files ${files_mc_DD} --inputList --config EoverPAnalysis/scripts/config_eop_mc_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_mc_DD_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_mc_ND} --inputList --config EoverPAnalysis/scripts/config_eop_mc_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_mc_ND_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_mc_SD} --inputList --config EoverPAnalysis/scripts/config_eop_mc_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_mc_SD_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_mc_DD} --inputList --config EoverPAnalysis/scripts/config_eop_mc_lowmu_runII_general.py --submitDir results/condor_all_eop_lowmu_runII_general_mc_DD_${today}_${tag} --verbose --force condor --optFilesPerWorker 10

    echo "---> Write to logfile:"
    echo ${files_data} > results/run_condor_eop_lowmu_runII_general.log
    echo results/condor_all_eop_lowmu_runII_general_data_${today}_${tag} >> results/run_condor_eop_lowmu_runII_general.log
    echo ${files_mc_ND} >> results/run_condor_eop_lowmu_runII_general.log
    echo results/condor_all_eop_lowmu_runII_general_mc_ND_${today}_${tag} >> results/run_condor_eop_lowmu_runII_general.log
    echo ${files_mc_SD} >> results/run_condor_eop_lowmu_runII_general.log
    echo results/condor_all_eop_lowmu_runII_general_mc_SD_${today}_${tag} >> results/run_condor_eop_lowmu_runII_general.log
    echo ${files_mc_DD} >> results/run_condor_eop_lowmu_runII_general.log
    echo results/condor_all_eop_lowmu_runII_general_mc_DD_${today}_${tag} >> results/run_condor_eop_lowmu_runII_general.log

    echo "--> Jobs submitted!"
    echo "source $TestArea/EoverPAnalysis/scripts/merge_condor_eop.sh $WorkdDir_DIR/../run/results/run_condor_eop_lowmu_runII_general.log # when condor jobs are finished to merge output files"

fi
