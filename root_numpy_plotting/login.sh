export ALRB_CONT_CMDOPTS="$ALRB_CONT_CMDIOTS -B /eos/atlas/atlascerngroupdisk/perf-jets/EoverP:/mnt"
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
asetup AnalysisBase,21.2.23

export EOPPlottingDir=$PWD
mkdir -p $PWD/CondorPythonLocal/lib/python2.7/site-packages
export PYTHONPATH=$PWD/CondorPythonLocal/lib/python2.7/site-packages:$PYTHONPATH
export BLAS=None LAPACK=None ATLAS=None

echo "READY TO GO!"
