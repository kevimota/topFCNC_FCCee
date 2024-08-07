#!/afs/cern.ch/work/k/kmotaama/miniforge3/envs/test/bin/python

import uproot
import awkward as ak
import os

import vector
vector.register_awkward()

from hist import Hist

import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)

from tools.utils import *

input_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/outputs/stage2"
output_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/analysis/combine"

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Prepare file for combine")
    parser.add_argument("--input", help="Path to yaml input file", required=True)

    args = parser.parse_args()
    
    config = load_yaml(args.input)
    tagname = get_tagname(args.input)
    bdt_cut = config['bdt_cut']
    
    print(f"Preparing input file {args.input[args.input.rfind('/')+1:]} for combine...")

    h_sig = Hist.new.Regular(20, bdt_cut, 1.0, name="score", label=r"BDT score").Double()
    h_tt = Hist.new.Regular(20, bdt_cut, 1.0, name="score", label=r"BDT score").Double()
    n_signal = 0
    n_bkg = 0
    for c in config['processes']:
        dataset = c['name']
        filename = f"{input_folder}/{tagname}/{dataset}.root"
        
        with uproot.open(filename) as f:
            mva = ak.zip({**get_vars_dict2(f['mva'], mva_collections)})
            bdt_score = f['bdt_score'].arrays().bdt_score
            mva = mva[bdt_score > bdt_cut]
            weight = lumi*c["xsec"]/c["events"]

            if c['type'] == "signal":
                h_sig.fill(bdt_score[bdt_score > bdt_cut], weight=weight)

            else:
                h_tt.fill(bdt_score[bdt_score > bdt_cut], weight=weight)
    
    if os.path.exists(f"{output_folder}/combine_{tagname}"): os.system(f"rm -r {output_folder}/combine_{tagname}")
    os.system(f"cp -r ../combine_template {output_folder}/combine_{tagname}")
    
    with uproot.recreate(f'{output_folder}/combine_{tagname}/input.root') as nf:
        nf['h_sig'] = h_sig
        nf['h_tt'] = h_tt
        nf['data_obs'] = h_sig
        
    print(f"Number of events - Signal: {h_sig.sum():.0f} Background: {h_tt.sum():.0f}")