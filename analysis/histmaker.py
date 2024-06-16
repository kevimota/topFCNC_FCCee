import os

processList = {
    'mg_ee_tt_cHbW_H2bb': {
        "fraction": 1, 
        "crossSection":  0.0004838,
    },
#    'mg_ee_tt_cSbW_S2bb_M20': {
#        "fraction": 1,
#        "crossSection":  0.0002362,
#    },
    'mg_ee_tt_bWbW': {
        "fraction": 1,
        "crossSection":  0.02148,
    },
    
}

mass = 125

outputDir   = f"./outputs/hists_{mass}/"

inputDir    = "./outputs/stage1"

includePaths = ["functions.h"]

nCPUS = 4

procDict = "FCCee_procDict_winter2023_IDEA.json"

includePaths = ["functions.h"]

bins_p = (200, 0, 200)
bins_e = (200, 0, 200)
bins_m = (195, 5, 200)
bins_y = (100, -3, 3)
bins_yt = (100, -1, 1)
bins_phi = (100, -4, 4)

bins_nbtag = (10, -0.5, 9.5)

doScale = True

def build_graph(df, dataset):

    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Define("jet_btag", "recojet_isB > 0.9")
    df = df.Define("jet_nbtag", "Sum(jet_btag)")
    df = df.Filter("FCCANA > 30.")
    df = df.Filter("(jet_eta < 2.5) && (jet_eta > -2.5)")

    df = df.Filter("jet_nbtag > 1")
    df = df.Filter("sqrt(jet_dmerge3) > 10")
    
    df = df.Define("best_hjj", f"TOPFCNCfunctions::ressonance_builder({mass})(jet_p4, jet_btag)")
    df = df.Define("all_jj_mass", f"JetConstituentsUtils::all_invariant_masses(jet_p4)")
    df = df.Filter("best_hjj.size() > 0")

    df = df.Define("best_hjj_mass", "best_hjj[0].M()")
    df = df.Define("best_hjj_pt", "best_hjj[0].Pt()")
    df = df.Define("best_hjj_p", "best_hjj[0].P()")
    df = df.Define("best_hjj_e", "best_hjj[0].E()")
    df = df.Define("best_hjj_y", "best_hjj[0].Rapidity()")
    df = df.Define("best_hjj_phi", "best_hjj[0].Phi()")

    df = df.Define("best_hjj_leading_mass", "best_hjj[1].M()")
    df = df.Define("best_hjj_leading_pt", "best_hjj[1].Pt()")
    df = df.Define("best_hjj_leading_p", "best_hjj[1].P()")
    df = df.Define("best_hjj_leading_e", "best_hjj[1].E()")
    df = df.Define("best_hjj_leading_y", "best_hjj[1].Rapidity()")
    df = df.Define("best_hjj_leading_phi", "best_hjj[1].Phi()")

    df = df.Define("best_hjj_trailing_mass", "best_hjj[2].M()")
    df = df.Define("best_hjj_trailing_pt", "best_hjj[2].Pt()")
    df = df.Define("best_hjj_trailing_p", "best_hjj[2].P()")
    df = df.Define("best_hjj_trailing_e", "best_hjj[2].E()")
    df = df.Define("best_hjj_trailing_y", "best_hjj[2].Rapidity()")
    df = df.Define("best_hjj_trailing_phi", "best_hjj[2].Phi()")

    results.append(df.Histo1D((f"jet_nbtag", "", *bins_nbtag), "jet_nbtag"))
    results.append(df.Histo1D((f"all_jj_mass", "", *bins_m), "all_jj_mass"))
    results.append(df.Histo1D((f"best_hjj_mass", "", *bins_m), "best_hjj_mass"))
    results.append(df.Histo1D((f"best_hjj_pt", "", *bins_p), "best_hjj_pt"))
    results.append(df.Histo1D((f"best_hjj_p", "", *bins_p), "best_hjj_p"))
    results.append(df.Histo1D((f"best_hjj_e", "", *bins_e), "best_hjj_e"))
    results.append(df.Histo1D((f"best_hjj_y", "", *bins_y), "best_hjj_y"))
    results.append(df.Histo1D((f"best_hjj_phi", "", *bins_phi), "best_hjj_phi"))

    results.append(df.Histo1D((f"best_hjj_leading_mass", "", *bins_m), "best_hjj_leading_mass"))
    results.append(df.Histo1D((f"best_hjj_leading_pt", "", *bins_p), "best_hjj_leading_pt"))
    results.append(df.Histo1D((f"best_hjj_leading_p", "", *bins_p), "best_hjj_leading_p"))
    results.append(df.Histo1D((f"best_hjj_leading_e", "", *bins_e), "best_hjj_leading_e"))
    results.append(df.Histo1D((f"best_hjj_leading_y", "", *bins_y), "best_hjj_leading_y"))
    results.append(df.Histo1D((f"best_hjj_leading_phi", "", *bins_phi), "best_hjj_leading_phi"))

    results.append(df.Histo1D((f"best_hjj_trailing_mass", "", *bins_m), "best_hjj_trailing_mass"))
    results.append(df.Histo1D((f"best_hjj_trailing_pt", "", *bins_p), "best_hjj_trailing_pt"))
    results.append(df.Histo1D((f"best_hjj_trailing_p", "", *bins_p), "best_hjj_trailing_p"))
    results.append(df.Histo1D((f"best_hjj_trailing_e", "", *bins_e), "best_hjj_trailing_e"))
    results.append(df.Histo1D((f"best_hjj_trailing_y", "", *bins_y), "best_hjj_trailing_y"))
    results.append(df.Histo1D((f"best_hjj_trailing_phi", "", *bins_phi), "best_hjj_trailing_phi"))

    results.append(df.Histo1D((f"recojet_isB", "", 100, 0, 9), "recojet_isB"))

    return results, weightsum