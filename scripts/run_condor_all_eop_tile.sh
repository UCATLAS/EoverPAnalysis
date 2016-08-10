#!/bin/bash
if [ $# -eq 0 ]

  then
    echo "Usage: source run_condor_all_eop_tile.sh tag"

  else

    cd $ROOTCOREBIN/..

    tag=$1
    today=$(date +"%Y%m%d")
    files_COF=EoverPAnalysis/filelists/mc15_13TeV_tile_COF.txt
    files_OF1=EoverPAnalysis/filelists/mc15_13TeV_tile_OF1.txt
    files_OF2=EoverPAnalysis/filelists/mc15_13TeV_tile_OF2.txt

    mkdir -p results

    echo "---> Running tile COF, OF1, and OF2 samples:"
    echo xAH_run.py --files ${files_COF} --inputList --config EoverPAnalysis/scripts/config_eop_mc.py --submitDir results/condor_all_eop_tile_COF_mc_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    echo xAH_run.py --files ${files_OF1} --inputList --config EoverPAnalysis/scripts/config_eop_mc.py --submitDir results/condor_all_eop_tile_OF1_mc_${today}_${tag} --verbose --force condor --optFilesPerWorker 10
    echo xAH_run.py --files ${files_OF2} --inputList --config EoverPAnalysis/scripts/config_eop_mc.py --submitDir results/condor_all_eop_tile_OF2_mc_${today}_${tag} --verbose --force condor --optFilesPerWorker 10

    echo "---> Write to logfile:"
    echo "# ---> "$(date +"%Y-%m-%d:%H:%M:%S") >> results/run_condor_eop_tile.log
    echo ${files_COF} >> results/run_condor_eop_tile.log
    echo results/condor_all_eop_tile_COF_mc_${today}_${tag} >> results/run_condor_eop_tile.log
    echo ${files_OF1} >> results/run_condor_eop_tile.log
    echo results/condor_all_eop_tile_OF1_mc_${today}_${tag} >> results/run_condor_eop_tile.log
    echo ${files_OF2} >> results/run_condor_eop_tile.log
    echo results/condor_all_eop_tile_OF2_mc_${today}_${tag} >> results/run_condor_eop_tile.log
    echo ${files_COF} > results/run_condor_eop_tile_latest.log
    echo results/condor_all_eop_tile_COF_mc_${today}_${tag} >> results/run_condor_eop_tile_latest.log
    echo ${files_OF1} >> results/run_condor_eop_tile_latest.log
    echo results/condor_all_eop_tile_OF1_mc_${today}_${tag} >> results/run_condor_eop_tile_latest.log
    echo ${files_OF2} >> results/run_condor_eop_tile_latest.log
    echo results/condor_all_eop_tile_OF2_mc_${today}_${tag} >> results/run_condor_eop_tile_latest.log

    echo "--> Jobs submitted!"
    echo "source $ROOTCOREBIN/../EoverPAnalysis/scripts/merge_condor_eop.sh $ROOTCOREBIN/../results/run_condor_eop_tile_latest.log # when condor jobs are finished to merge output files"

fi
