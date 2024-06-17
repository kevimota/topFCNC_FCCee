import os
import sys
import math
from array import array
import ROOT

class hist():

    def __init__(self):
        
        var = ['mbb']
        cat = ['all', 'b2j3', 'b2j4', 'b3j3', 'b3j4']
        self.h = {}
        
        for v in var:
            for c in cat:
                hname = v+'_'+c
                self.h[hname] = ROOT.TH1F( hname, hname, 50, 0., 500. )
