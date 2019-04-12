'''
LessonFour_histos.py

Make histograms from the four-tops trees using TTree::Draw.
Style will be done later.

'''

import ROOT
import os
from optparse import OptionParser

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetOptTitle(False)
ROOT.gStyle.SetLegendBorderSize(0);

parser = OptionParser()
parser.add_option("--input", help="Input tree to process", default="input.root")
parser.add_option("--tag", help="Output file label", default="")
parser.add_option("--verbose", action='store_true', help="Verbose output? Default is False", default=False)
(options, args) = parser.parse_args()

f = ROOT.TFile.Open(options.input,'r')
t_lambda = f.Get('EoverP_InDetTrackParticlesLooseIsolatedLambda_tree')
t_ks = f.Get('EoverP_InDetTrackParticlesLooseIsolatedKs_tree')
t_phi = f.Get('EoverP_InDetTrackParticlesLooseIsolatedPhi_tree') 

h1_mass_lambda=ROOT.TH1F('h1_mass_lambda','h1_mass_lambda',15,-0.5,14.5)
h1_mass_ks=ROOT.TH1F('h1_mass_ks','h1_mass_ks',15,-0.5,14.5)
h1_mass_phi=ROOT.TH1F('h1_mass_phi','h1_mass_phi',15,-0.5,14.5)

h1_dr_lambda=ROOT.TH1F('h1_dr_lambda','h1_dr_lambda',100,0.,5.)
h1_dr_ks=ROOT.TH1F('h1_dr_ks','h1_dr_ks',100,0.,5.)
h1_dr_phi=ROOT.TH1F('h1_dr_phi','h1_dr_phi',100,0.,5.)

t_lambda.Print()

for entry in range(0,t_lambda.GetEntries()):
    if(entry%10000==0): print "\tentry "+str(entry)
    t_lambda.GetEntry(entry)
    
    #for track in range(0,len(t_lambda.trk_pt)):
    #print len(t_lambda.trk_pt)
        
    #t1 = ROOT.TLorentzVector()
    #t2 = ROOT.TLorentzVector()

    #t1.SetPtEtaPhiE()
    #t2.SetPtEtaPhiE()

    

f_out = ROOT.TFile.Open("output_"+options.tag+".root","recreate")

h1_mass_lambda.Write()
h1_mass_ks.Write()
h1_mass_phi.Write()

h1_dr_lambda.Write()
h1_dr_ks.Write()
h1_dr_phi.Write()
