import os
user = os.environ['USER']

#TOP_DIRECTORY = "/tmp/" + user + "/HmumuTuplesVer_2_4/"
TOP_DIRECTORY = "/mnt/"

INPUT = \
{ "PythiaJetJet": ("Pythia8 MinBias and Dijet", [\
TOP_DIRECTORY + "user.luadamek.mc16_13TeV.361020.jetjet._Jan13_hist",\
TOP_DIRECTORY + "user.luadamek.mc16_13TeV.361021.jetjet._Jan13_hist",\
TOP_DIRECTORY + "user.luadamek.mc16_13TeV.361022.jetjet._Jan13_hist",\
]),\
"LowMuData": ("2017 Low-<#mu> Data",[\
TOP_DIRECTORY + "user.luadamek.data17_13TeV.00341294.physics_MinBias._Jan14_hist",\
TOP_DIRECTORY + "user.luadamek.data17_13TeV.00341615.physics_MinBias._Jan14_hist",\
TOP_DIRECTORY + "user.luadamek.data17_13TeV.00341649.physics_MinBias._Jan14_hist",\
TOP_DIRECTORY + "user.luadamek.data17_13TeV.00341312.physics_MinBias._Jan14_hist",\
TOP_DIRECTORY + "user.luadamek.data17_13TeV.00341419.physics_MinBias._Jan14_hist",\
])}
