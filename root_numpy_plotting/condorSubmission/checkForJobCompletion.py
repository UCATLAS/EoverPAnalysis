##This is a script that checks for job completion
import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='check that all of the plotting jobs have finished running')
parser.add_argument('--jobDir', '-jd', dest="jobDir", type=str, required=True, help='where to look for the jobs that ran')

args = parser.parse_args()
jobDir = args.jobDir

outputFiles = []
for root, dirs, files in os.walk(jobDir+"/Log/", topdown=False):
   for name in files:
      outputFiles.append(os.path.join(root, name))
print "There are this many log files " + str(len(outputFiles))

#First check for the existence of LSF folders in the directory
not_finished_count = 0
#Root File Exists Count
root_file_count = 0
allJobsDone = True
for outputFile in outputFiles:
    #get the STDOUT file

    found_finished = False
    with open(outputFile) as f:
        lines = f.readlines()
        for line in lines:
            if "Normal termination (return value 0)" in line:
                found_finished = True
            if "killed" in line:
                print outputFile + " killed prematurely"

    if not found_finished:
        allJobsDone = False
        not_finished_count += 1
        print "the job with ID " + outputFile.split(".")[-1] + " didn't finish"

    job_number = outputFile.split(".")[-1]
    has_file = os.path.isfile(jobDir + "_" + job_number + ".root")
    if not has_file:
        root_file_count += 1

if allJobsDone:
    print "all plotting jobs have finished"
else:
    print "This many jobs didn't finish " + str(not_finished_count)
    print "This many root files don't exist " + str(root_file_count)

