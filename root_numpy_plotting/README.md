# EoverPPlotting

These plotting macros use root_numpy, cython and a module called atlas-plot. To keep the same root version and environment consistent, always run these macros after setting up AnalysisBase,21.2.23

## Setup
This creates local installations of root_numpy, cython and psutils. These packages are needed for these plotting macros.
```
source setup.sh
```

## When logging back in
```
source login.sh
```

## Prepare batch plotting jobs for submission
```
python condorSubmission/PrepareSubmission.py -tn EoverP_InDetTrackParticlesLooseIsolatedVertexAssociated_tree --NPartitions 100 --jobName test1
```

## Test one of the jobs locally
```
python condorSubmission/submit.py --num 0 --picklefile test1/Submission/test1.pickle --jobName test1
```

## Submit all of the batch jobs
```
condor_submit condor_testPlotting.sub
```

## Upon job completion
```
hadd testPlotting_hadded.root testPlotting*.root
```

## Draw histograms
```
git clone git@github.com:joeycarter/atlas-plots.git
cd atlas-plots
pip install -e . --user
cd ..
python
from CreatePlots import CreatePlots
CreatePlots("Outputs/testPlotting/testPlotting_hadded.root")
```
