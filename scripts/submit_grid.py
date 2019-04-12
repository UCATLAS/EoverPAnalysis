#!/usr/bin/env python 
import os

import subprocess
#try:
#  __version__ = subprocess.check_output(['git','log', '--pretty=format:%h', '-n 1'], cwd=os.path.dirname(os.path.realpath(__file__))).strip()
#except:
#  print('git not available to extract current tag')
#  __version__ = 'private'

import argparse
parser = argparse.ArgumentParser(description='Submit gridjobs for EoverPAnalysis')

parser.add_argument('--user', '-u', dest="user", type=str, required=True, help='Your (CERN id) grid username')
parser.add_argument('--tag', dest='analysisTag', type=str, default="", help='Tag for the analysis')
parser.add_argument('--submitDir', dest="submitDir", type=str, default='submitDir', help='dir to store the output')
parser.add_argument('--overwrite', dest="overwrite", type=bool, default=False, help='overwrite previous submitDir')
parser.add_argument('--FileList', dest="FileList", required=True, type=str, help='the .txt file containing all dataset names')
parser.add_argument('--config', dest="config", required=True, type=str, help="the file containing the configuration")
parser.add_argument('--descriptor', dest="descriptor", required=True, type=str, help="a string that will be appended to the output dataset")

args = parser.parse_args()

FileList=args.FileList

samples = []
try:
  samples.extend([sample.rstrip('\n') for sample in open(os.path.expandvars(FileList))])
except IOError, e:
  print e
  exit()

for sample in samples:

  split = sample.split('.')
  sampleTag = split[2] + '.' + split[3] + '.' + split[4]
  optGridOutputSampleName = 'user.{0:s}.{1:s}.{2:s}'.format(args.user, sampleTag, args.analysisTag)

  config = os.path.expandvars(args.config)

  command = 'xAH_run.py --files={0:s}  --inputRucio --config={1:s} --submitDir={2:s}'.format(sample, config, args.submitDir)
  if args.overwrite:
     command += ' --force '
  command += " prun "
  command += ' --optSubmitFlags="--excludeFile=src/EoverPAnalysis/root_numpy_plotting/"'
  if "data17" in sample:
      command += ' --optGridNFilesPerJob=30 '
  else:
      command += ' --optGridNFilesPerJob=3 '
  command += ' --optGridNGBPerJob=2 '
  command += "--optGridOutputSampleName={}".format(optGridOutputSampleName) + "_"+ args.descriptor

  #if ("data" in sample or "Data" in sample):
  #    command += ' --optGridNFilesPerJob 40 '

  print('submitting {0:s}'.format(sample))
  print('running: {0:s}'.format(command))
  subprocess.call(command, shell=True)
