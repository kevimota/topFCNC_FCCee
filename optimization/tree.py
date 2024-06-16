import os
import sys
import math
from array import array
import ROOT

class tree():

    def __init__(self):
        
        self.weight = array( 'f', [ -777 ] )

        self.electron_pt, self.electron_eta, self.electron_phi, self.electron_e \
        = (ROOT.vector('float')() for _ in range(4))

        self.muon_pt, self.muon_eta, self.muon_phi, self.muon_e \
        = (ROOT.vector('float')() for _ in range(4))

        self.jet_pt, self.jet_eta, self.jet_phi, self.jet_e, self.jet_isbtag \
        = (ROOT.vector('float')() for _ in range(5))
        
        self.t = ROOT.TTree( 'ntuple', 'Analysis tree' )

        self.t.Branch( 'weight', self.weight, 'weight/F' )

        self.t.Branch( 'electron_pt', self.electron_pt)
        self.t.Branch( 'electron_eta', self.electron_eta)
        self.t.Branch( 'electron_phi', self.electron_phi)
        self.t.Branch( 'electron_e', self.electron_e)
        
        self.t.Branch( 'muon_pt', self.muon_pt)
        self.t.Branch( 'muon_eta', self.muon_eta)
        self.t.Branch( 'muon_phi', self.muon_phi)
        self.t.Branch( 'muon_e', self.muon_e)

        self.t.Branch( 'jet_pt', self.jet_pt)
        self.t.Branch( 'jet_eta', self.jet_eta)
        self.t.Branch( 'jet_phi', self.jet_phi)
        self.t.Branch( 'jet_e', self.jet_e)
        self.t.Branch( 'jet_isbtag', self.jet_isbtag)
        
    def fill(self):

        self.t.Fill()

    def clear(self):

        self.electron_pt.clear()
        self.electron_eta.clear()
        self.electron_phi.clear()
        self.electron_e.clear()
        self.muon_pt.clear()
        self.muon_eta.clear()
        self.muon_phi.clear()
        self.muon_e.clear()
        self.jet_pt.clear()
        self.jet_eta.clear()
        self.jet_phi.clear()
        self.jet_e.clear()
        self.jet_isbtag.clear()
        