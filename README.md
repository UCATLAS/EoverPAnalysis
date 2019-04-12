# EoverPAnalysis

This package is based on the [xAODAnaHelpers (xAH)](https://github.com/UCATLAS/xAODAnaHelpers) RootCore package, thus I strongly recommend you check out the [xAH documentation first](https://xaodanahelpers.readthedocs.io/en/latest/).

For questions please contact: lukas.adamek[at]cern.ch, or joakim.olsson[at]cern.ch

Package created by Joakim Olsson
Ported to release 21 and modified by: Lukas Adamek (lukas.adamek[at]cern.ch)

## Setup in Release 21

First setup the folders for running, building and the soruce files
```
mkdir myAnalysis; cd myAnalysis
mkdir source && mkdir run && mkdir build && mkdir run/results
cd source
```

Clone the packages that this analysis depends on. 
```
git clone http://github.com/UCATLAS/xAODAnaHelpers xAODAnaHelpers
git clone http://github.com/luadamek/EoverPAnalysis
git clone https://github.com/mattleblanc/IDTrackSel.git
asetup AnalysisBase,21.2.64,here
cd ../build
cmake ../source && make
```

## Running locally in Release 21
Inside the scripts folder are two different config files. These are config_eop_tree_dump.py for running over MC, and config_eop_dump_data.py for running over data. These files create ttrees for four different track selections, and store information about calorimeter energy deposits at the cell, EM, and LCW scale. To run a test job locally, try the following lines:
```
cd ../build
source */setup.sh
cd ../run
mkdir results
rucio download user.luadamek.14704913.EXT1._000001.pool.root
xAH_run.py --files user.luadamek/user.luadamek.14704913.EXT1._000001.pool.root --config ../source/EoverPAnalysis/scripts/config_eop_tree_dump.py --submitDir testing --force direct
```

## Submitting Grid Jobs in Release 21
Grid jobs are handled by a submission script located in $TestArea/EoverPAnalysis/scripts/. The grid job script takes four arguments as input: the submission directory, a txt file with all samples listed, a descriptor to label the output, and a configuration file. As an example, the following command will submit grid jobs to run over the 361022 jet jet MC sample.
```
cd ../run
python $TestArea/EoverPAnalysis/scripts/submit_grid.py --user luadamek --tag 21.2.64 --submitDir results --FileList $TestArea/EoverPAnalysis/filelists/test_list.txt --config $TestArea/EoverPAnalysis/scripts/config_eop_tree_dump.py --descriptor test
```

## Plotting
Plotting macros can be found the root_numpy_plotting folder. See the README contained in that folder.

## Hadding together large root files.
A macro exists for hadding together root files that are too large (> ~ 100 Gb). To use the macro, do:
```
python hadd_bigfiles.py __outputfilename__ __directorywithfiles__
```
Do this on the /tmp/user/ directory of LxPlus nodes, and then move the large file to the final destination.
