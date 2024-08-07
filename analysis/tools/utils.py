import awkward as ak
import yaml

jet_ee_kt_collections = [
    "jet_ee_kt_px", "jet_ee_kt_py", "jet_ee_kt_pz", "jet_ee_kt_e", "jet_ee_kt_isB", "jet_ee_kt_isC", "jet_ee_kt_dmerge3",
]

jet_genkt_collections = [
    "jet_genkt_px", "jet_genkt_py", "jet_genkt_pz", "jet_genkt_e", "jet_genkt_isB",
]

muon_collections = [
    "muons_px", "muons_py", "muons_pz", "muons_e", "muons_iso",
]

electron_collections = [
    "electrons_px", "electrons_py", "electrons_pz", "electrons_e", "electrons_iso",
]

dijet_collections = [
    "x", "y", "z", 't',
]

ME_collections = [
    "MET_e", "MET_px", "MET_py", "MET_pz",
]

mva_collections = [
    'm_jj_best', 'deltaR_jj_best', 'm_jjj_best', 'j0_isB', 'j1_isB', 'j2_isB', 'j3_isB', 'j0_isC', 'j1_isC', 'j2_isC', 'j3_isC', 'deltaR_lj', 'm_l_ME', 'ME_e',
]

t_mass = 172.76

lumi = 1500000

def load_yaml(path):
    with open(path, 'r') as f:
        r = yaml.load(f, Loader=yaml.FullLoader)
    return r

def get_tagname(path):
    return path[path.rfind("input_")+6:path.rfind(".")]

def get_vars_dict(events, col_list):
    result = {}
    col = ''
    for c in col_list:
        col = c[c.rfind("_")+1:]
        
        array = events[c].array()
        if len(array) == 0:
            result[col] = ak.Array([])
        else:
            result[col] = array
    return result

def get_vars_dict2(events, col_list):
    result = {}
    for c in col_list:
        array = events[c].array()
        if len(array) == 0:
            result[c] = ak.Array([])
        else:
            result[c] = array
    return result

def get_br_lim(xs_exc, r):
    return xs_exc*r/0.16/0.3
    