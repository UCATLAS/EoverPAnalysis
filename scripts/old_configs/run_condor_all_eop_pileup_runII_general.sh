#!/bin/bash
if [ $# -eq 0 ]

  then
    echo "Usage: source run_condor_all_eop_pileup_runII_general.sh tag"

  else

    cd $WorkDir_DIR/../run

    tag=$1
    today=$(date +"%Y%m%d")
    files_data=EoverPAnalysis/filelists/data15_13TeV_pileup_all.txt
    # files_JZ0W=EoverPAnalysis/filelists/mc15_13TeV_pileup_JZ0W_test200k.txt
    files_JZ1W=EoverPAnalysis/filelists/mc15_13TeV_pileup_JZ1W_all.txt

    mkdir -p results

    echo "---> Running JZxW pileup MC samples:"
    echo xAH_run.py --files ${files_data} --inputList --config EoverPAnalysis/scripts/config_eop_data_pileup_runII_general.py --submitDir results/condor_all_eop_pileup_runII_general_data_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_data} --inputList --config EoverPAnalysis/scripts/config_eop_data_pileup_runII_general.py --submitDir results/condor_all_eop_pileup_runII_general_data_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    # echo xAH_run.py --files ${files_JZ0W} --inputList --config EoverPAnalysis/scripts/config_eop_mc_pileup_runII_general.py --submitDir results/condor_all_eop_pileup_runII_general_JZ0W_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    # xAH_run.py --files ${files_JZ0W} --inputList --config EoverPAnalysis/scripts/config_eop_mc_pileup_runII_general.py --submitDir results/condor_all_eop_pileup_runII_general_JZ0W_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    echo xAH_run.py --files ${files_JZ1W} --inputList --config EoverPAnalysis/scripts/config_eop_mc_pileup_runII_general.py --submitDir results/condor_all_eop_pileup_runII_general_JZ1W_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_JZ1W} --inputList --config EoverPAnalysis/scripts/config_eop_mc_pileup_runII_general.py --submitDir results/condor_all_eop_pileup_runII_general_JZ1W_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    #
    echo "---> Write to logfile:"
    echo ${files_data} > results/run_condor_eop_pileup_runII_general.log
    echo results/condor_all_eop_pileup_runII_general_data_${today}_${tag} >> results/run_condor_eop_pileup_runII_general.log
    # echo ${files_JZ0W} >> results/run_condor_eop_pileup_runII_general.log
    # echo results/condor_all_eop_pileup_runII_general_JZ0W_${today}_${tag} >> results/run_condor_eop_pileup_runII_general.log
    echo ${files_JZ1W} >> results/run_condor_eop_pileup_runII_general.log
    echo results/condor_all_eop_pileup_runII_general_JZ1W_${today}_${tag} >> results/run_condor_eop_pileup_runII_general.log

    echo "--> Jobs submitted!"
    echo "source $TestArea/EoverPAnalysis/scripts/merge_condor_eop.sh $WorkDir_DIR/../run/results/run_condor_eop_pileup_runII_general.log # when condor jobs are finished to merge output files"

fi
