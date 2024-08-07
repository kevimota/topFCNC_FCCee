import uproot
import awkward as ak
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from tqdm.auto import tqdm

import vector
ak.behavior.update(vector.backends.awkward.behavior)

from tools.utils import *

import os

n_cores = 6

input_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/outputs/stage1"
output_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/outputs/stage2"

btag_wp = 0.4
ctag_wp = 0.4
mass = 125
tagname = ""

def run_analysis(config):
    dataset = config['name']
    filename = f"{input_folder}/{dataset}.root"
    with uproot.open(filename) as f:
        events = f["events"]
        jet = ak.zip(
            {**get_vars_dict(events, jet_ee_kt_collections)},
            with_name="Momentum4D"
        )

        electron = ak.zip(
            {**get_vars_dict(events, electron_collections), "lepton":0},
            with_name="Momentum4D"
        )

        muon = ak.zip(
            {**get_vars_dict(events, muon_collections), "lepton":1},
            with_name="Momentum4D"
        )

        ME = ak.zip(
            {**get_vars_dict(events, ME_collections)},
            with_name="Momentum4D"
        )

        lepton = ak.concatenate([electron, muon], axis=1)

        #jet = jet[np.abs(jet.eta) < 3.0]
        nb_cut = ak.num(jet[jet.isB > btag_wp], axis=1) > 2
        jet = jet[nb_cut]
        lepton = lepton[nb_cut]
        ME = ME[nb_cut]

        nc_cut = ak.num(jet[jet.isC > ctag_wp], axis=1) > 0
        jet = jet[nc_cut]
        lepton = lepton[nc_cut]
        ME = ME[nc_cut]
        #jet = jet[np.sqrt(jet.dmerge3) > 10]

        lepton = lepton[lepton.iso < 0.5]
        lepton = lepton[lepton.p > 5]
        lepton = lepton[np.abs(lepton.eta) < 2.9]

        nlepton = ak.num(lepton)
        jet = jet[nlepton > 0]
        lepton = lepton[nlepton > 0]
        ME = ME[nlepton > 0]

        dijet = ak.combinations(jet, 2)
        dijet_arg = ak.argcombinations(jet, 2)
        dijet_bjet = (dijet["0"].isB > btag_wp) & (dijet["1"].isB > btag_wp)
        #dijet = dijet[dijet_bjet]
        #dijet_arg = dijet_arg[dijet_bjet]

        dijet_p4 = dijet["0"] + dijet["1"]

        dijet_sort = ak.argsort(np.abs(dijet_p4.m - mass), ascending=True)
        dijet_sorted = dijet[dijet_sort]
        dijet_arg_sorted = dijet_arg[dijet_sort]
        dijet_p4_sorted = dijet_p4[dijet_sort]
        dijet_best = dijet_sorted[:,0]
        dijet_arg_best = dijet_arg_sorted[:,0]
        dijet_p4_best = dijet_p4_sorted[:,0]

        deltaR_best = dijet_best["0"].deltaR(dijet_best["1"])

        jet_indexes = ak.local_index(jet)
        jets_indexes_removed = jet_indexes[(jet_indexes != dijet_arg_best["0"]) & (jet_indexes != dijet_arg_best["1"])]
        jet_jj_removed = jet[jets_indexes_removed]

        trijet = ak.cartesian([dijet_p4_best, jet_jj_removed])
        trijet_p4 = trijet["0"] + trijet["1"]

        trijet_sort = ak.argsort(np.abs(trijet_p4.m - t_mass), ascending=True)
        trijet_p4_sorted = trijet_p4[trijet_sort]
        trijet_p4_best = trijet_p4_sorted[:,0]

        jet_btag = {}
        for i in range(4):
            jet_btag[f"j{i}_isB"] = jet.isB[:,i]

        jet_ctag = {}
        for i in range(4):
            jet_ctag[f"j{i}_isC"] = jet.isC[:,i]

        leading_jet = (dijet_best["0"].p > dijet_best["1"].p)
        jet_lead = ak.where(leading_jet, dijet_best["0"], dijet_best["1"])
        #jet_trail = ak.where(~leading_jet, dijet_best["0"], dijet_best["1"])

        lepton = lepton[ak.argsort(lepton.p, ascending=False)]
        lepton_lead = lepton[:,0]

        deltaR_lj = jet_lead.deltaR(lepton_lead)

        p_ME_l = lepton_lead + ME

        if not os.path.exists(f"{output_folder}/{tagname}"): os.makedirs(f"{output_folder}/{tagname}")
        
        with uproot.recreate(f"{output_folder}/{tagname}/{dataset}.root") as outf:
            outf["jet"] = jet
            outf["lepton"] = lepton
            outf["dijet"] = dijet_p4
            outf["dijet_best"] = dijet_p4_best
            outf["ME"] = ME
            outf["mva"] = ak.zip({
                "m_jj_best": dijet_p4_best.m,
                "deltaR_jj_best": deltaR_best,
                'm_jjj_best': trijet_p4_best.m,
                **jet_btag,
                **jet_ctag,
                "deltaR_lj": deltaR_lj,
                "m_l_ME": p_ME_l.m,
                "ME_e": ME.e,
            })
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Analysis stage 2")
    parser.add_argument("--input", required=True, help="Input files path", type=str)
    parser.add_argument("--njobs", default=6, help="Number of parallel jobs [default: %default]", type=int)
    
    args = parser.parse_args()
    
    config = load_yaml(args.input)
    mass = config['mass']
    tagname = get_tagname(args.input)
    
    if not os.path.exists(output_folder): os.mkdir(output_folder)
    with ProcessPoolExecutor(max_workers=len(config['processes']) if (len(config['processes']) < n_cores) else n_cores) as executor:
        list(tqdm(executor.map(run_analysis, config['processes']), total=len(config['processes']), unit=" files", desc="Processing"))
