#!/bin/bash
if [ $# -eq 0 ]

  then
    echo "Usage: source run_condor_all_eop_pileup.sh tag"

  else

    cd $WorkDir_DIR/../run

    tag=$1
    today=$(date +"%Y%m%d")
    files_data15=EoverPAnalysis/filelists/data15_13TeV_pileup_all.txt
    files_data16=EoverPAnalysis/filelists/data16_13TeV_pileup_all.txt

    mkdir -p results

    echo xAH_run.py --files ${files_data15} --inputList --config EoverPAnalysis/scripts/config_eop_data_pileup.py --submitDir results/condor_all_eop_pileup_data15_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_data15} --inputList --config EoverPAnalysis/scripts/config_eop_data_pileup.py --submitDir results/condor_all_eop_pileup_data15_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    echo xAH_run.py --files ${files_data16} --inputList --config EoverPAnalysis/scripts/config_eop_data_pileup_2016.py --submitDir results/condor_all_eop_pileup_data16_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    xAH_run.py --files ${files_data16} --inputList --config EoverPAnalysis/scripts/config_eop_data_pileup_2016.py --submitDir results/condor_all_eop_pileup_data16_${today}_${tag} --verbose --force condor --optFilesPerWorker 10

    echo "---> Write to logfile:"
    echo ${files_data15} > results/run_condor_eop_pileup_2016.log
    echo results/condor_all_eop_pileup_data15_${today}_${tag} >> results/run_condor_eop_pileup_2016.log
    echo ${files_data16} >> results/run_condor_eop_pileup_2016.log
    echo results/condor_all_eop_pileup_data16_${today}_${tag} >> results/run_condor_eop_pileup_2016.log

    echo "--> Jobs submitted!"
    echo "source $TestArea/EoverPAnalysis/scripts/merge_condor_eop.sh $WorkDir_DIR/../run/results/run_condor_eop_pileup.log # when condor jobs are finished to merge output files"

fi
