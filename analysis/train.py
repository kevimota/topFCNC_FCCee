#!/afs/cern.ch/work/k/kmotaama/miniforge3/envs/test/bin/python

import os, uproot
import awkward as ak
import numpy as np
import pandas as pd
from tools.utils import *

import matplotlib.pyplot as plt
plt.switch_backend('agg')

import xgboost as xgb
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.covariance import EllipticEnvelope

import mplhep as hep
plt.style.use(hep.style.ROOT)
from hist import Hist

input_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/outputs/stage2"
output_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/analysis/bdt_model"

def set_xgbc(conf, n_jobs, stop):
    xgbc = xgb.XGBClassifier(
        use_label_encoder = False,
        **conf,
        missing = np.nan,
        early_stopping_rounds = stop,
        n_jobs = n_jobs
    )

    return xgbc

def prepare_input_data(input_files):
    features = []
    y = np.array([])
    for d in input_files:
        filename = f"{input_folder}/{tagname}/{d['name']}.root"
        with uproot.open(filename) as uf:
            mva = ak.zip({**get_vars_dict2(uf["mva"], mva_collections)})
            features.append(mva)
            y = np.append(y, np.ones(len(mva)) if d['type'] == "signal" else np.zeros(len(mva)))
    features = ak.concatenate(features)
    X = ak.concatenate([features[f] for f in features.fields], axis=1)
    X = X.to_numpy()
    X = pd.DataFrame(X, columns=mva.fields)
    return X, y

def infer(input_file, xgbc):
    filename = f"{input_folder}/{tagname}/{input_file['name']}.root"
    X, y = prepare_input_data([input_file])
    x = xgb.DMatrix(X, feature_names=mva_collections)
    y_pred = xgbc.predict(x)

    with uproot.update(filename) as f:
        f["bdt_score"] = ak.zip({"bdt_score": y_pred})

    return X, y, y_pred

def plot_roc(y, y_pred):
    fpr, tpr, thresholds = roc_curve(y, y_pred) 
    roc_auc = auc(fpr, tpr)

    fig = plt.figure()  
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--', label='No Skill')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for BDT Classification')
    plt.legend()
    fig.savefig(f"{output_folder}/{tagname}/pics/roc.pdf")
    fig.savefig(f"{output_folder}/{tagname}/pics/roc.png")

def plot_learning_curve(results, epochs, tagname):
    x_axis = range(0, epochs)
    fig, ax = plt.subplots()
    plt.title(tagname)
    ax.plot(x_axis, results['validation_0']['logloss'], label='Logloss (Train)')
    ax.plot(x_axis, results['validation_1']['logloss'], label='Logloss (Test)')
    ax.plot(x_axis, results['validation_0']['auc'], label='AUC (Train)')
    ax.plot(x_axis, results['validation_1']['auc'], label='AUC (Test)')
    ax.legend(loc='best')
    plt.xlabel('Number of boosting rounds')
    plt.ylabel('Log Loss/AUC')
    fig.savefig(f"{output_folder}/{tagname}/pics/learn.pdf")
    fig.savefig(f"{output_folder}/{tagname}/pics/learn.png")
    plt.close()

def plot_classification_error(results, epochs, tagname):
    x_axis = range(0, epochs)
    fig, ax = plt.subplots()
    plt.title(tagname)
    ax.plot(x_axis, results['validation_0']['error'], label='Train')
    ax.plot(x_axis, results['validation_1']['error'], label='Test')
    ax.legend(loc='best')
    plt.xlabel('Number of boosting rounds')
    plt.ylabel('Classification error')
    fig.savefig(f"{output_folder}/{tagname}/pics/error.pdf")
    fig.savefig(f"{output_folder}/{tagname}/pics/error.png")
    plt.close()

def plot_importance(xgbc, tagname):
    plt.figure(figsize = (16, 12))
    xgb.plot_importance(xgbc)
    plt.savefig(f"{output_folder}/{tagname}/pics/importance.pdf")
    plt.savefig(f"{output_folder}/{tagname}/pics/importance.png")
    plt.close()

if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser(description="Train BDT")
    parser.add_argument("--njobs", default=6, help="Number of parallel jobs [default: %default]", type=int)
    parser.add_argument("--stop", default=10, help="Early stopping rounds in final fit [default: %default]", type=int)
    parser.add_argument("--xc", help="Path to configuration file for xgboost", required=True)
    parser.add_argument("--input", help="Path to yaml input file", required=True)
    parser.add_argument("--seed", default=12345, type=int, help="Seed for rng")
    parser.add_argument("--test_size", default=0.2, type=float, help="Seed for rng")
    parser.add_argument("--infer", action="store_true", help="Use trained model for inference")
    args = parser.parse_args()

    input_files = load_yaml(args.input)
    xgb_conf = load_yaml(args.xc)
    tagname = args.input[args.input.rfind("input_")+6:args.input.rfind(".")]

    if not args.infer:
        X, y = prepare_input_data(input_files['processes'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=args.seed)

        xgbc = set_xgbc(xgb_conf, args.njobs, args.stop)
        eval_set = [(X_train, y_train), (X_test, y_test)]

        xgbc.fit(
            X_train, y_train,
            eval_set=eval_set,
            verbose=True,
        )

        results = xgbc.evals_result()
        epochs = len(results['validation_0']['error'])
        print()

        if not os.path.exists(f"{output_folder}/{tagname}"): 
            os.makedirs(f"{output_folder}/{tagname}/pics")
        bst = xgbc.get_booster()
        bst.save_model(f"{output_folder}/{tagname}/xgb.bin")
        bst.dump_model(f"{output_folder}/{tagname}/xgb.txt")

        plot_learning_curve(results, epochs, tagname)
        plot_classification_error(results, epochs, tagname)
        plot_importance(xgbc, tagname)

    else:
        xgbc = xgb.Booster()
        xgbc.load_model(f"{output_folder}/{tagname}/xgb.bin")

        y_pred_all = np.array([])
        y_all = np.array([])

        h_bdt_signal = Hist.new.Regular(20, 0.0, 1.0, name="score", label=r"BDT score").Double()
        h_bdt_background = Hist.new.Regular(20, 0.0, 1.0, name="score", label=r"BDT score").Double()
        
        h_bdt_signal_zoomed_50 = Hist.new.Regular(20, 0.50, 1.0, name="score", label=r"BDT score").Double()
        h_bdt_background_zoomed_50 = Hist.new.Regular(20, 0.50, 1.0, name="score", label=r"BDT score").Double()
        
        h_bdt_signal_zoomed_90 = Hist.new.Regular(20, 0.90, 1.0, name="score", label=r"BDT score").Double()
        h_bdt_background_zoomed_90 = Hist.new.Regular(20, 0.90, 1.0, name="score", label=r"BDT score").Double()
        
        h_bdt_signal_zoomed_97 = Hist.new.Regular(20, 0.97, 1.0, name="score", label=r"BDT score").Double()
        h_bdt_background_zoomed_97 = Hist.new.Regular(20, 0.97, 1.0, name="score", label=r"BDT score").Double()

        h_bdt = {}

        for input_file in input_files['processes']:
            print(f"Running inference for {input_file['name']}")
            X, y, y_pred = infer(input_file, xgbc)
            y_all = np.append(y_all, y)
            y_pred_all = np.append(y_pred_all, y_pred)
            h_bdt[input_file["process"]] = Hist.new.Regular(50, 0, 1, name="score", label=r"BDT score").Double()
            weight = lumi*input_file["xsec"]/input_file["events"]
            h_bdt[input_file["process"]].fill(score=y_pred, weight=weight)
            if input_file['type'] == "signal":
                h_bdt_signal.fill(score=y_pred, weight=weight)
                h_bdt_signal_zoomed_50.fill(score=y_pred, weight=weight)
                h_bdt_signal_zoomed_90.fill(score=y_pred, weight=weight)
                h_bdt_signal_zoomed_97.fill(score=y_pred, weight=weight)
            else:
                h_bdt_background.fill(score=y_pred, weight=weight)
                h_bdt_background_zoomed_50.fill(score=y_pred, weight=weight)
                h_bdt_background_zoomed_90.fill(score=y_pred, weight=weight)
                h_bdt_background_zoomed_97.fill(score=y_pred, weight=weight)


        f, ax = plt.subplots()
        hep.histplot([h_bdt[h] for h in h_bdt], label=[h for h in h_bdt], ax=ax)
        ax.set_yscale('log')
        ax.legend(fontsize=16)
        ax.set_title(r"BDT output m$_S$ = %d GeV" % input_files['mass'])
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdt.pdf")
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdt.png")

        f, ax = plt.subplots()
        hep.histplot([h_bdt_signal, h_bdt_background], label=["Signal", "Background"], ax=ax)
        ax.set_yscale('log')
        ax.legend(fontsize=16)
        ax.set_title(r"BDT output m$_S$ = %d GeV" % input_files['mass'])
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm.pdf")
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm.png")
        
        f, ax = plt.subplots()
        hep.histplot([h_bdt_signal_zoomed_50, h_bdt_background_zoomed_50], label=["Signal", "Background"], ax=ax)
        ax.set_yscale('log')
        ax.legend(fontsize=16)
        ax.set_title(r"BDT output m$_S$ = %d GeV" % input_files['mass'])
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm_zoomed_50.pdf")
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm_zoomed_50.png")
        
        f, ax = plt.subplots()
        hep.histplot([h_bdt_signal_zoomed_90, h_bdt_background_zoomed_90], label=["Signal", "Background"], ax=ax)
        ax.set_yscale('log')
        ax.legend(fontsize=16)
        ax.set_title(r"BDT output m$_S$ = %d GeV" % input_files['mass'])
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm_zoomed_90.pdf")
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm_zoomed_90.png")
        
        f, ax = plt.subplots()
        hep.histplot([h_bdt_signal_zoomed_97, h_bdt_background_zoomed_97], label=["Signal", "Background"], ax=ax)
        ax.set_yscale('log')
        ax.legend(fontsize=16)
        ax.set_title(r"BDT output m$_S$ = %d GeV" % input_files['mass'])
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm_zoomed_97.pdf")
        f.savefig(f"{output_folder}/{tagname}/pics/h_bdtm_zoomed_97.png")

        plot_roc(y_all, y_pred_all)