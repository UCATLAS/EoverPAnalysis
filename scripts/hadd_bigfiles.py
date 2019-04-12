import ROOT
import os, sys

print 'Merging %s' % sys.argv[1]

print "Max tree size",ROOT.TTree.GetMaxTreeSize()
ROOT.TTree.SetMaxTreeSize(300000000000) # 300 Gb
print "Updated tree size",ROOT.TTree.GetMaxTreeSize()

rm = ROOT.TFileMerger(True)
rm.SetFastMethod(True)
rm.SetPrintLevel(1)


path = '%s' % sys.argv[2]
file_output = '%s.root' % sys.argv[1]
file_list = []
for path, dirs, files in os.walk(path):
  for filename in files:
    file_list.append(path+filename)

print "Input file list:",file_list
print "Output file:",file_output
rm.SetMaxOpenedFiles(21)

for F in file_list:
    print "Adding ->",F
    rm.AddFile(F)

if not rm.OutputFile(file_output, "RECREATE"):
    raise ValueError("COULDN'T CREATE ROOT FILE")

if not rm.Merge():
    print "WARNING!!! THE FILES DIDN'T MERGE TOGETHER"
