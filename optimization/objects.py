import os
import sys
import math
import ROOT

class lepton():
    idx = -1
    def __init__(self, ev, idx, typ):
        self.idx = idx
        self.typ = typ
        self.quality = 0

        if typ == 0:
            self.pt = ev.__getattr__("electrons_pt")[idx]
            self.eta = ev.__getattr__("electrons_eta")[idx]
            self.phi = ev.__getattr__("electrons_phi")[idx]
            self.e = ev.__getattr__("electrons_e")[idx]
            self.iso = ev.__getattr__("electrons_iso")[idx]/self.pt
        else:
            self.pt = ev.__getattr__("muons_pt")[idx]
            self.eta = ev.__getattr__("muons_eta")[idx]
            self.phi = ev.__getattr__("muons_phi")[idx]
            self.e = ev.__getattr__("muons_e")[idx]
            self.iso = ev.__getattr__("muons_iso")[idx]/self.pt
        self.p4 = ROOT.TLorentzVector()
        self.p4.SetPtEtaPhiE(self.pt, self.eta, self.phi, self.e)
            
        if self.pt > 20 and abs(self.eta) < 2.5 and self.iso < 0.5: self.quality = 1
        
class jet():
    idx = -1
    def __init__(self, ev, idx):
        self.idx = idx
        self.quality = 0

        self.px = ev.__getattr__("jet_antikt_px")[idx]
        self.py = ev.__getattr__("jet_antikt_py")[idx]
        self.pz = ev.__getattr__("jet_antikt_pz")[idx]
        self.e = ev.__getattr__("jet_antikt_e")[idx]
        self.btag = ev.__getattr__("jet_antikt_isB")[idx]
        self.isbtag = bool(self.btag > 0.95)
        self.p4 = ROOT.TLorentzVector()
        self.p4.SetPxPyPzE(self.px, self.py, self.pz, self.e)
        self.pt = self.p4.Pt()
        self.eta = self.p4.Eta()
        self.phi = self.p4.Phi()

        if self.pt > 30 and abs(self.eta) < 2.5: self.quality = 1