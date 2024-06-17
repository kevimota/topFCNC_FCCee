#!/usr/local/bin/python3

import os, sys, ROOT
import hist
import objects as obj
import xml.etree.ElementTree as ET

ROOT.gROOT.SetBatch()

samples = []
xmlTree = ET.parse("../input.xml")
for s in xmlTree.findall('sample'):
    info = {"name": "../ntuple/"+s.get('name')+".root", "type": s.get('type')}
    samples.append(info)
    
def cat(nb, nj):
    c = ''
    if nb == 2 and nj == 3: c = 'b2j3'
    elif nb == 2 and nj == 4: c = 'b2j4'
    elif nb == 3 and nj == 3: c = 'b3j3'
    elif nb == 3 and nj == 4: c = 'b3j4'
    else: c = 'b3j4'
    return c

for s in samples:

    outFile = ROOT.TFile.Open("output/"+s['name'].split('/')[2], "RECREATE")
    outHist = hist.hist()
    f = ROOT.TFile(s['name'], "READ")
    tr = f.Get("ntuple")
    
    for i in range(tr.GetEntries()):
        
        tr.GetEntry(i)
        
        ev = obj.event(tr)
        w = ev.w
        
        leptons, jets, bjets, ljets = [], [], [], []
        
        for iel in range(len(tr.electron_pt)):
            lep = obj.lepton(tr, iel, 0)
            leptons.append(lep)
        for imu in range(len(tr.muon_pt)):
            lep = obj.lepton(tr, imu, 1)
            leptons.append(lep)
        for ijet in range(len(tr.jet_pt)):
            jet = obj.jet(tr, ijet)
            jets.append(jet)
            if jet.isbtag:
                bjets.append(jet)
            else:
                ljets.append(jet)
                
        nlep = len(leptons)
        njets = len(jets)
        nbjets = len(bjets)
        
        if not bool(njets >= 3): continue
        if not bool(nbjets >= 3): continue

        c = cat(nbjets, njets)

        ms = 50
#        ms = 125
        mmin = 1E+10
        ij1, ij2 = -1, -1
        for ijet1, jet1 in enumerate(bjets):
            for ijet2 in range(ijet1+1, len(bjets)):
                jet2 = bjets[ijet2]
                mbb = (jet1.p4+jet2.p4).M()
                if abs(mbb-ms) < mmin: 
                    mmin = abs(mbb-ms)
                    ij1 = ijet1
                    ij2 = ijet2
        mbb = (bjets[ij1].p4+bjets[ij2].p4).M()
        outHist.h['mbb_all'].Fill(mbb, w)
        outHist.h['mbb_'+c].Fill(mbb, w)
        
    outFile.Write()
    outFile.Close()
