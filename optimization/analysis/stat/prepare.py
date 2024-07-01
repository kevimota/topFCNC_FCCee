#!/usr/local/bin/python3

import os, sys, ROOT

ROOT.gROOT.SetBatch()

#f_sig = ROOT.TFile("../output/ee2tt_cHbW_h2bb.root", "READ")
f_sig = ROOT.TFile("../output/ee2tt_cSbW_S2bb_M50.root", "READ")
h_sig = f_sig.Get("mbb_all")

f_tt = ROOT.TFile("../output/ee2tt_bWbW_W2ln.root", "READ")
h_tt = f_tt.Get("mbb_all")

outFile = ROOT.TFile.Open("input.root", "RECREATE")

h_sig.Write("data_obs")
h_sig.Write("h_sig")
h_tt.Write("h_tt")
    
outFile.Write()
outFile.Close()

#os.system("docker cp datacard.txt combine:/code/analysis/datacard.txt")
#os.system("docker cp input.root combine:/code/analysis/input.root")
#os.system("docker cp combine.sh combine:/code/analysis/combine.sh")
#os.system("docker start -i combine")
