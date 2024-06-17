#!/usr/local/bin/python3

import os, sys, ROOT
import tree
import objects as obj
import xml.etree.ElementTree as ET

lumi = 1500000 # pb

ROOT.gROOT.SetBatch()

samples = []
xmlTree = ET.parse("input.xml")
for s in xmlTree.findall('sample'):
    info = {"name": "samples/"+s.get('name')+".root", "type": s.get('type'), "events": float(s.get('events')), "xsec": float(s.get('xsec'))}
    samples.append(info)

for s in samples:
    
    outFile = ROOT.TFile.Open("ntuple/"+s['name'].split('/')[1], "RECREATE")
    outTree = tree.tree()
    f = ROOT.TFile(s['name'], "READ")
    tr = f.Get("events")
    
    outTree.weight[0] = float(lumi/(s['events']/s['xsec']))
    
    for i in range(tr.GetEntries()):
        
        tr.GetEntry(i)
        outTree.clear()
        
        leptons, jets, bjets = [], [], []
        
        for iel in range(len(tr.electrons_pt)):
            lep = obj.lepton(tr, iel, 0)
            if lep.quality == 1:
                leptons.append(lep)
        for imu in range(len(tr.muons_pt)):
            lep = obj.lepton(tr, imu, 1)
            if lep.quality == 1:
                leptons.append(lep)
        for ijet in range(len(tr.jet_antikt_pt)):
            jet = obj.jet(tr, ijet)
            if jet.quality == 1:
                jets.append(jet)
                if jet.isbtag == 1:
                    bjets.append(jet)

        nlep = len(leptons)
        njet = len(jets)
        nbjet = len(bjets)
        
        if not bool(nlep >= 1 and njet >= 2 and nbjet >= 2): continue
            
        for lep in leptons:
            if lep.typ == 0:
                outTree.electron_pt.push_back(lep.pt)
                outTree.electron_eta.push_back(lep.eta)
                outTree.electron_phi.push_back(lep.phi)
                outTree.electron_e.push_back(lep.e)
            else:                
                outTree.muon_pt.push_back(lep.pt)
                outTree.muon_eta.push_back(lep.eta)
                outTree.muon_phi.push_back(lep.phi)
                outTree.muon_e.push_back(lep.e)

        for ijet, jet in enumerate(jets):
            outTree.jet_pt.push_back(jet.pt)
            outTree.jet_eta.push_back(jet.eta)
            outTree.jet_phi.push_back(jet.phi)
            outTree.jet_e.push_back(jet.p4.E())
            outTree.jet_isbtag.push_back(jet.isbtag)

        outTree.fill()
        
    outFile.Write()
    outFile.Close()
            
