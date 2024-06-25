#!/usr/local/bin/python3

import os
import sys
import math, ctypes
import subprocess
from subprocess import call
import numpy as np
import style
import json
import ROOT

ROOT.gROOT.SetBatch(1)

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

pstyle = style.SetPlotStyle()

#f_sig = ROOT.TFile('output/ee2tt_cHbW_h2bb.root', 'READ')
f_sig = ROOT.TFile('output/ee2tt_cSbW_S2bb_M50.root', 'READ')
f_tt = ROOT.TFile('output/ee2tt_bWbW_W2ln.root', 'READ')

h_sig = f_sig.Get('mbb_all')
h_tt = f_tt.Get('mbb_all')

c1 = ROOT.TCanvas()

h_sig.SetMarkerSize(0)
h_sig.SetLineColor(ROOT.kRed-7)
h_sig.SetFillColor(0)

h_tt.SetMarkerSize(0)
h_tt.SetLineColor(ROOT.kBlue-3)
h_tt.SetFillColor(ROOT.kBlue-3)

leg = ROOT.TLegend(0.6, 0.5, 0.85, 0.7)
leg.SetBorderSize(0)
leg.SetLineWidth(0)
leg.SetLineColor(0)
leg.SetFillStyle(0)
leg.SetFillColor(0)

ev_tt = h_tt.Integral()
ev_sig = h_sig.Integral()
sf = int(ev_tt/ev_sig)
h_sig.Scale(sf)

#leg.AddEntry(h_sig, 'B(t #rightarrow hc) = 0.0028 x '+str(sf), 'f')
leg.AddEntry(h_sig, 'B(t #rightarrow hc) = 0.01054 x '+str(sf), 'f')
leg.AddEntry(h_tt, 'Background', 'f')

h_tt.Draw('hist')
h_sig.Draw('hist same')

h_tt.GetYaxis().SetTitle('Events')
h_tt.GetYaxis().SetTitleSize(0.06)
h_tt.GetXaxis().SetTitle('m_{b#bar{b}} [GeV]')
h_tt.GetXaxis().SetTitleSize(0.06)

leg.Draw()

hmax = max(h_sig.GetMaximum(), h_tt.GetMaximum())
h_tt.SetMaximum(hmax*1.2)
        
t1, t2, t3 = style.fcclabel()
t1.Draw()
t2.Draw()
t3.Draw()

c1.Update()
c1.Print('pics/mbb.pdf')
