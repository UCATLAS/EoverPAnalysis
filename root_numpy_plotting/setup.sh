
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
asetup AnalysisBase,21.2.23

#pip uninstall cython
#pip uninstall root_numpy
#pip uninstall psutil

export EOPPlottingDir=$PWD
mkdir -p $PWD/CondorPythonLocal/lib/python2.7/site-packages
export PYTHONPATH=$PWD/CondorPythonLocal/lib/python2.7/site-packages:$PYTHONPATH
export BLAS=None LAPACK=None ATLAS=None

pip install --install-option="--prefix=$PWD/CondorPythonLocal" --ignore-installed cython
pip install --install-option="--prefix=$PWD/CondorPythonLocal" --ignore-installed root_numpy
pip install --install-option="--prefix=$PWD/CondorPythonLocal" --ignore-installed psutil 

echo "READY TO GO!"
