#!/bin/bash

if [ $# -eq 0 ]

then
  echo "Usage: merge_condor_eop.sh run_condor_eop_xyz.log"

else

#  cd $WorkDir_DIR/..

  logfile=$1
  echo
  echo "Reading from logfile: "${logfile}
  echo

  count=0
  while read line; do
    if [ $((count%2)) -eq 0 ]
    then
      file_tag=$(echo ${line} | sed -e 's/^.*\///g' | sed -e 's/\.txt$//g')
      echo "---> Processing output of: "${file_tag}
    else
      condor_output=${line}
      echo "condor output files: "${condor_output}
      echo "merging files:"
      echo hadd -f ${condor_output}.root ${condor_output}/fetch/hist-${file_tag}-*.root
      hadd -f ${condor_output}.root ${condor_output}/fetch/hist-${file_tag}-*.root > /dev/null 2>&1
      echo "merging cutflows"
      echo hadd -f ${condor_output}-cutflows.root ${condor_output}/fetch/data-cutflow/${file_tag}-*.root
      hadd -f ${condor_output}-cutflows.root ${condor_output}/fetch/data-cutflow/${file_tag}-*.root > /dev/null 2>&1
      echo "writing to logfile:"
      echo "# ---> "$(date +"%Y-%m-%d:%H:%M:%S") -- merge >> results/run_condor_eop.log
      echo ${condor_output}.root | sed -e 's/^results\///g' >> results/merge_condor_eop.log
      echo ${condor_output}-cutflows.root | sed -e 's/^results\///g' >> results/merge_condor_eop.log
    fi
    ((count++));
  done <${logfile};

  echo "--> All done!"

fi
