#!/afs/cern.ch/work/k/kmotaama/miniforge3/envs/test/bin/python

import uproot
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)

from tools.utils import *

input_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/analysis/combine"

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Plot the nll")
    parser.add_argument("--input", help="Path to yaml input file", required=True)

    args = parser.parse_args()
    
    config = load_yaml(args.input)
    tagname = get_tagname(args.input)
    
    input_folder = f"{input_folder}/combine_{tagname}"
    
    with uproot.open(f"{input_folder}/higgsCombineTest.MultiDimFit.mH120.root") as f_combine:
        deltaNLL = f_combine['limit']['deltaNLL'].arrays().deltaNLL
        r = f_combine['limit']['r'].arrays().r
    
    #weight = get_br_lim(xs)
    
    f, ax = plt.subplots()
    #ax.plot(r*0.001971830985915493*100, 2*deltaNLL)
    ax.plot(r, 2*deltaNLL)
    ax.set_ylabel(r"2 $\Delta$NLL")
    ax.set_xlabel("r")
    ax.axhline(1.00, c='0.8', ls='--')
    ax.axhline(3.84, c='0.8', ls='--')
    
    if not os.path.exists(f"{input_folder}/pics"): os.makedirs(f"{input_folder}//pics")
    
    f.savefig(f"{input_folder}/pics/nll.pdf")
    f.savefig(f"{input_folder}/pics/nll.png")