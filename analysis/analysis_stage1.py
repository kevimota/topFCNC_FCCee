import os

processList = {
    'ee2tt_bWbW': {
        "fraction": 1, 
    },
    'ee2tt_cHbW_h2bb': {
        "fraction": 1,
    },
    'ee2tt_cSbW_S2bb_M50': {
        "fraction": 1,
    },
    'ee2tt_uHbW_h2bb': {
        "fraction": 1,
    },
    'ee2tt_uSbW_S2bb_M50': {
        "fraction": 1,
    },
}

outputDir   = "./outputs/stage1/"

inputDir    = "./gen/"

includePaths = ["functions.h"]

nCPUS = 4

## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc_v1"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = (
    "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
)
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)

weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
)

output_branches = []

# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    def analysers(df):
        df = df.Alias("Muon0", "Muon_objIdx.index")
        df = df.Alias("Photon0", "Photon_objIdx.index")
        df = df.Alias("Electron0", "Electron_objIdx.index")

        df = df.Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
        df = df.Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
        df = df.Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
        df = df.Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
        df = df.Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
        df = df.Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")

        df = df.Define("muons_all", "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
        df = df.Define("muons", "ReconstructedParticle::sel_p(5)(muons_all)")

        df = df.Define("muons_iso", "FCCAnalyses::TOPFCNCfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        df = df.Define("muons_e", "FCCAnalyses::ReconstructedParticle::get_e(muons)")
        df = df.Define("muons_px", "FCCAnalyses::ReconstructedParticle::get_px(muons)")
        df = df.Define("muons_py", "FCCAnalyses::ReconstructedParticle::get_py(muons)")
        df = df.Define("muons_pz", "FCCAnalyses::ReconstructedParticle::get_pz(muons)")
        df = df.Define("muons_pt", "FCCAnalyses::ReconstructedParticle::get_pt(muons)")
        df = df.Define("muons_eta", "FCCAnalyses::ReconstructedParticle::get_eta(muons)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_n", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

        df = df.Define("electrons_all", "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
        df = df.Define("electrons", "ReconstructedParticle::sel_p(5)(electrons_all)")

        df = df.Define("electrons_iso", "FCCAnalyses::TOPFCNCfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
        df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
        df = df.Define("electrons_e", "FCCAnalyses::ReconstructedParticle::get_e(electrons)")
        df = df.Define("electrons_px", "FCCAnalyses::ReconstructedParticle::get_px(electrons)")
        df = df.Define("electrons_py", "FCCAnalyses::ReconstructedParticle::get_py(electrons)")
        df = df.Define("electrons_pz", "FCCAnalyses::ReconstructedParticle::get_pz(electrons)")
        df = df.Define("electrons_pt", "FCCAnalyses::ReconstructedParticle::get_pt(electrons)")
        df = df.Define("electrons_eta", "FCCAnalyses::ReconstructedParticle::get_eta(electrons)")
        df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
        df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        df = df.Define("electrons_n", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

        df = df.Define("photons_all", "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
        df = df.Define("photons", "ReconstructedParticle::sel_p(5)(photons_all)")

        df = df.Define("photons_iso", "FCCAnalyses::TOPFCNCfunctions::coneIsolation(0.01, 0.5)(photons, ReconstructedParticles)")
        df = df.Define("photons_p", "FCCAnalyses::ReconstructedParticle::get_p(photons)")
        df = df.Define("photons_e", "FCCAnalyses::ReconstructedParticle::get_e(photons)")
        df = df.Define("photons_px", "FCCAnalyses::ReconstructedParticle::get_px(photons)")
        df = df.Define("photons_py", "FCCAnalyses::ReconstructedParticle::get_py(photons)")
        df = df.Define("photons_pz", "FCCAnalyses::ReconstructedParticle::get_pz(photons)")
        df = df.Define("photons_pt", "FCCAnalyses::ReconstructedParticle::get_pt(photons)")
        df = df.Define("photons_eta", "FCCAnalyses::ReconstructedParticle::get_eta(photons)")
        df = df.Define("photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons)")
        df = df.Define("photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(photons)")
        df = df.Define("photons_n", "FCCAnalyses::ReconstructedParticle::get_n(photons)")

        df = df.Define("MissingET", "TOPFCNCfunctions::missingEnergy(365, ReconstructedParticles)")

        df = df.Define("MET_e", "ReconstructedParticle::get_e(MissingET)")
        df = df.Define("MET_p", "ReconstructedParticle::get_p(MissingET)")
        df = df.Define("MET_pt", "ReconstructedParticle::get_pt(MissingET)")
        df = df.Define("MET_px", "ReconstructedParticle::get_px(MissingET)") #x-component of MET
        df = df.Define("MET_py", "ReconstructedParticle::get_py(MissingET)") #y-component of MET
        df = df.Define("MET_pz", "ReconstructedParticle::get_pz(MissingET)") #z-component of MET
        df = df.Define("MET_eta", "ReconstructedParticle::get_eta(MissingET)")
        df = df.Define("MET_theta", "ReconstructedParticle::get_theta(MissingET)")
        df = df.Define("MET_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of RecoMissingEnergy

        df = df.Define(
            "muons_sel_iso",
            "FCCAnalyses::TOPFCNCfunctions::sel_iso(0.25)(muons, muons_iso)",
        )
        
        df = df.Define(
            "electrons_sel_iso",
            "FCCAnalyses::TOPFCNCfunctions::sel_iso(0.25)(electrons, electrons_iso)",
        )

        df = df.Define(
            "ReconstructedParticlesNoIsoMuons",
            "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,muons_sel_iso)",
        )

        df = df.Define(
            "ReconstructedParticlesNoIsoLeptons",
            "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoIsoMuons,electrons_sel_iso)",
        )

        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticlesNoIsoLeptons",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "_EFlowTrack_trackStates",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "_EFlowTrack_dxQuantities",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }

        jetClusteringHelper = ExclusiveJetClusteringHelper(
            collections["PFParticles"], 4, "ee_kt"
        )
        df = jetClusteringHelper.define(df)

        global output_branches
        output_branches = set()

        jetFlavourHelper = JetFlavourHelper(
            collections,
            jetClusteringHelper.jets,
            jetClusteringHelper.constituents,
            "ee_kt"
        )
        df = jetFlavourHelper.define(df)
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        df = df.Define('event_thrust',     'Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
        df = df.Define('RP_thrustangle',   'Algorithms::getAxisCosTheta(event_thrust, RP_px, RP_py, RP_pz)')
        df = df.Define('event_thrust_x',   "event_thrust.at(0)")
        df = df.Define('event_thrust_y',   "event_thrust.at(1)")
        df = df.Define('event_thrust_z',   "event_thrust.at(2)")
        df = df.Define('event_thrust_val', "event_thrust.at(3)")

        df = df.Define('event_sphericity',     'Algorithms::minimize_sphericity("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
        df = df.Define('event_sphericity_x',   "event_sphericity.at(0)")
        df = df.Define('event_sphericity_y',   "event_sphericity.at(1)")
        df = df.Define('event_sphericity_z',   "event_sphericity.at(2)")
        df = df.Define('event_sphericity_val', "event_sphericity.at(3)")
        df = df.Define('RP_sphericityangle', 'Algorithms::getAxisCosTheta(event_sphericity, RP_px, RP_py, RP_pz)')

        df = df.Define('RP_hemis0_mass',   "Algorithms::getAxisMass(0)(RP_thrustangle, RP_e, RP_px, RP_py, RP_pz)")
        df = df.Define('RP_hemis1_mass',   "Algorithms::getAxisMass(1)(RP_thrustangle, RP_e, RP_px, RP_py, RP_pz)")

        df = df.Define("RP_total_mass",    "Algorithms::getMass(ReconstructedParticles)")

        df = df.Define("jet_ee_kt_dmerge1", "JetClusteringUtils::get_exclusive_dmerge(_jet_ee_kt, 1)")
        df = df.Define("jet_ee_kt_dmerge2", "JetClusteringUtils::get_exclusive_dmerge(_jet_ee_kt, 2)")
        df = df.Define("jet_ee_kt_dmerge3", "JetClusteringUtils::get_exclusive_dmerge(_jet_ee_kt, 3)")

        df = df.Define("jet_ee_kt_px",        "JetClusteringUtils::get_px(jet_ee_kt)")
        df = df.Define("jet_ee_kt_py",        "JetClusteringUtils::get_py(jet_ee_kt)")
        df = df.Define("jet_ee_kt_pz",        "JetClusteringUtils::get_pz(jet_ee_kt)")
        df = df.Define("jet_ee_kt_pt",        "JetClusteringUtils::get_pt(jet_ee_kt)")
        df = df.Define("jet_ee_kt_eta",       "JetClusteringUtils::get_eta(jet_ee_kt)")
        df = df.Define("jet_ee_kt_phi_std",   "JetClusteringUtils::get_phi_std(jet_ee_kt)")
        df = df.Alias("jet_ee_kt_n",          "event_njet_ee_kt")
        for i in set([*jetClusteringHelper.outputBranches(), *jetFlavourHelper.outputBranches()]):
            if i.startswith("jet_"): b = i[4:i.find("_ee_kt")]
            elif i.startswith("recojet_"): b = i[8:i.find("_ee_kt")]
            else: continue
            df = df.Alias(f"jet_ee_kt_{b}", i)
            output_branches.add(f"jet_ee_kt_{b}")

        df = df.Define("RPnl_px",          "ReconstructedParticle::get_px(ReconstructedParticlesNoIsoLeptons)")
        df = df.Define("RPnl_py",          "ReconstructedParticle::get_py(ReconstructedParticlesNoIsoLeptons)")
        df = df.Define("RPnl_pz",          "ReconstructedParticle::get_pz(ReconstructedParticlesNoIsoLeptons)")
        df = df.Define("RPnl_e",           "ReconstructedParticle::get_e(ReconstructedParticlesNoIsoLeptons)")
        df = df.Define("RPnl_m",           "ReconstructedParticle::get_mass(ReconstructedParticlesNoIsoLeptons)")
        df = df.Define("RPnl_q",           "ReconstructedParticle::get_charge(ReconstructedParticlesNoIsoLeptons)")

        df = df.Define("pseudo_jets",            "JetClusteringUtils::set_pseudoJets_xyzm(RPnl_px, RPnl_py, RPnl_pz, RPnl_m)")
        df = df.Define("FCCAnalysesJets_antikt", "JetClustering::clustering_antikt(0.5, 0, 20, 0, 0)(pseudo_jets)")
        df = df.Define("jet_antikt",             "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_antikt)")
        df = df.Define("jetconstituents_antikt", "JetClusteringUtils::get_constituents(FCCAnalysesJets_antikt)")
        df = df.Define("jetc_antikt",            "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticlesNoIsoLeptons,jetconstituents_antikt)")
        df = df.Define("jet_antikt_nconst",      "JetConstituentsUtils::count_consts(jetc_antikt)")
        df = df.Define("jet_antikt_e",           "JetClusteringUtils::get_e(jet_antikt)")
        df = df.Define("jet_antikt_px",          "JetClusteringUtils::get_px(jet_antikt)")
        df = df.Define("jet_antikt_py",          "JetClusteringUtils::get_py(jet_antikt)")
        df = df.Define("jet_antikt_pz",          "JetClusteringUtils::get_pz(jet_antikt)")
        df = df.Define("jet_antikt_pt",          "JetClusteringUtils::get_pt(jet_antikt)")
        df = df.Define("jet_antikt_p",           "JetClusteringUtils::get_p(jet_antikt)")
        df = df.Define("jet_antikt_phi",         "JetClusteringUtils::get_phi(jet_antikt)")
        df = df.Define("jet_antikt_eta",         "JetClusteringUtils::get_eta(jet_antikt)")
        df = df.Define("jet_antikt_mass",        "JetClusteringUtils::get_m(jet_antikt)")
        df = df.Define("jet_antikt_n",           "JetConstituentsUtils::count_jets(jetc_antikt)")

        jetFlavourHelper = JetFlavourHelper(
            collections,
            "jet_antikt",
            "jetc_antikt",
            "antikt"
        )
        df = jetFlavourHelper.define(df)
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        for i in set(jetFlavourHelper.outputBranches()):
            if i.startswith("jet_"): b = i[4:i.find("_antikt")]
            elif i.startswith("recojet_"): b = i[8:i.find("_antikt")]
            else: continue
            df = df.Alias(f"jet_antikt_{b}", i)
            output_branches.add(f"jet_antikt_{b}")

        df = df.Define("FCCAnalysesJets_genkt", "JetClustering::clustering_genkt(1.5, 0, 1, 0, 0)(pseudo_jets)")
        df = df.Define("jet_genkt",             "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_genkt)")
        df = df.Define("jetconstituents_genkt", "JetClusteringUtils::get_constituents(FCCAnalysesJets_genkt)")
        df = df.Define("jetc_genkt",            "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticlesNoIsoLeptons,jetconstituents_genkt)")
        df = df.Define("jet_genkt_nconst",      "JetConstituentsUtils::count_consts(jetc_genkt)")
        df = df.Define("jet_genkt_e",           "JetClusteringUtils::get_e(jet_genkt)")
        df = df.Define("jet_genkt_px",          "JetClusteringUtils::get_px(jet_genkt)")
        df = df.Define("jet_genkt_py",          "JetClusteringUtils::get_py(jet_genkt)")
        df = df.Define("jet_genkt_pz",          "JetClusteringUtils::get_pz(jet_genkt)")
        df = df.Define("jet_genkt_pt",          "JetClusteringUtils::get_pt(jet_genkt)")
        df = df.Define("jet_genkt_p",           "JetClusteringUtils::get_p(jet_genkt)")
        df = df.Define("jet_genkt_phi",         "JetClusteringUtils::get_phi(jet_genkt)")
        df = df.Define("jet_genkt_eta",         "JetClusteringUtils::get_eta(jet_genkt)")
        df = df.Define("jet_genkt_mass",        "JetClusteringUtils::get_m(jet_genkt)")
        df = df.Define("jet_genkt_n",           "JetConstituentsUtils::count_jets(jetc_genkt)")

        jetFlavourHelper = JetFlavourHelper(
            collections,
            "jet_genkt",
            "jetc_genkt",
            "genkt"
        )
        df = jetFlavourHelper.define(df)
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        for i in set(jetFlavourHelper.outputBranches()):
            if i.startswith("jet_"): b = i[4:i.find("_genkt")]
            elif i.startswith("recojet_"): b = i[8:i.find("_genkt")]
            else: continue
            df = df.Alias(f"jet_genkt_{b}", i)
            output_branches.add(f"jet_genkt_{b}")

        return df

    def output():
        branchList = [
            "RP_px", "RP_py", "RP_pz", "RP_e", "RP_m", "RP_q",

            "event_thrust_x", "event_thrust_y", "event_thrust_z", "event_thrust_val",

            "event_sphericity_x", "event_sphericity_y", "event_sphericity_z", "event_sphericity_val",

            "RP_thrustangle",
            "RP_sphericityangle",

            "RP_hemis0_mass",
            "RP_hemis1_mass",
            "RP_total_mass",

            "muons_p",
            "muons_e",
            "muons_pt",
            "muons_px",
            "muons_py",
            "muons_pz",
            "muons_eta",
            "muons_theta",
            "muons_phi",
            "muons_q",
            "muons_iso",
            "muons_n",

            "electrons_p",
            "electrons_e",
            "electrons_pt",
            "electrons_px",
            "electrons_py",
            "electrons_pz",
            "electrons_eta",
            "electrons_theta",
            "electrons_phi",
            "electrons_q",
            "electrons_iso",
            "electrons_n",

            "MET_e",
            "MET_p",
            "MET_pt",
            "MET_px",
            "MET_py",
            "MET_pz",
            "MET_eta",
            "MET_theta",
            "MET_phi",

            #"jet_ee_kt_e",    
            "jet_ee_kt_px",    
            "jet_ee_kt_py",    
            "jet_ee_kt_pz",    
            #"jet_ee_kt_p",    
            "jet_ee_kt_pt",    
            #"jet_ee_kt_phi",    
            "jet_ee_kt_eta",    
            #"jet_ee_kt_mass",
            #"jet_ee_kt_nconst",
            "jet_ee_kt_n",

            "jet_antikt_e",    
            "jet_antikt_px",    
            "jet_antikt_py",    
            "jet_antikt_pz",    
            "jet_antikt_p",    
            "jet_antikt_pt",    
            "jet_antikt_phi",    
            "jet_antikt_eta",    
            "jet_antikt_mass",
            "jet_antikt_nconst",
            "jet_antikt_n",

            "jet_genkt_e",    
            "jet_genkt_px",    
            "jet_genkt_py",    
            "jet_genkt_pz",    
            "jet_genkt_p",    
            "jet_genkt_pt",
            "jet_genkt_phi",
            "jet_genkt_eta",
            "jet_genkt_mass",
            "jet_genkt_nconst",
            "jet_genkt_n",
        ]

        branchList += output_branches
        
        return branchList