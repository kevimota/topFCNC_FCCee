import os
import sys
import math
import ROOT

class event():
    def __init__(self, ev):
        self.w = ev.__getattr__("weight")

class lepton():
    idx = -1
    def __init__(self, ev, idx, typ):
        self.idx = idx
        self.typ = typ

        if typ == 0:
            self.pt = ev.__getattr__("electron_pt")[idx]
            self.eta = ev.__getattr__("electron_eta")[idx]
            self.phi = ev.__getattr__("electron_phi")[idx]
            self.e = ev.__getattr__("electron_e")[idx]
            self.p4 = ROOT.TLorentzVector()
            self.p4.SetPtEtaPhiE(self.pt, self.eta, self.phi, self.e)
        else:
            self.pt = ev.__getattr__("muon_pt")[idx]
            self.eta = ev.__getattr__("muon_eta")[idx]
            self.phi = ev.__getattr__("muon_phi")[idx]
            self.e = ev.__getattr__("muon_e")[idx]
            self.p4 = ROOT.TLorentzVector()
            self.p4.SetPtEtaPhiE(self.pt, self.eta, self.phi, self.e)
        
class jet():
    idx = -1
    def __init__(self, ev, idx):
        self.idx = idx

        self.pt = ev.__getattr__("jet_pt")[idx]
        self.eta = ev.__getattr__("jet_eta")[idx]
        self.phi = ev.__getattr__("jet_phi")[idx]
        self.e = ev.__getattr__("jet_e")[idx]
        self.isbtag = ev.__getattr__("jet_isbtag")[idx]
        self.p4 = ROOT.TLorentzVector()
        self.p4.SetPtEtaPhiE(self.pt, self.eta, self.phi, self.e)        