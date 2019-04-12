from sys import path as sys_path
from os import path as os_path
Curr_DIR = os_path.expandvars('$EOPPlottingDir')
sys_path.insert(1, Curr_DIR)

from PlottingTools.Plotter import Plotter
from FillingScript import FillingScript
import pickle
import ROOT

import os
import subprocess

#file.write("python submit.py --num " + str(i) + "--picklefile " + submission_pickle_file + "--jobname sub" + str(i))

import argparse
parser = argparse.ArgumentParser(description='Submit plotting batch jobs for the EoverPAnalysis plotting')
parser.add_argument('--num', '-n', dest="num", type=int, required=True, help='Which submission number was this?')
parser.add_argument('--picklefile' '-p', dest='picklefile', type=str, default="", help='Where to get the plotter')
parser.add_argument('--jobName', '-j', dest="jobname", type=str, default='""', help='the names of the batch jobs')

args = parser.parse_args()

i = args.num
file = args.picklefile
name = args.jobname

plots = pickle.load(open(file, "rb"))[i]
FillingScript(plots, name + "_" + str(i) + ".root")
