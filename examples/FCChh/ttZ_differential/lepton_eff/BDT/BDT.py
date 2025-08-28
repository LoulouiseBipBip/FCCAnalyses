#!/usr/bin/env python3
import glob
import uproot
import awkward as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend("Agg")  # non-interactive backend

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc
from xgboost import XGBClassifier

# ------------------------------------------------------
# Input ROOT files (all Q-binned files)
# ------------------------------------------------------
import argparse

parser = argparse.ArgumentParser(description='Process ROOT files for BDT training.')
parser.add_argument('--process-individual', action='store_true', help='Process each ROOT file individually instead of globbing them into one')
args = parser.parse_args()

file_list = glob.glob("/eos/user/l/lberiet/ttZ_diff_results/BDT/mgp8_pp_ttz_5f_Q_*_84TeV_ttzlep.root")
print(f"Found {len(file_list)} ROOT files")

branches = [
    "D0_sig_prompt_muons", "Z0_sig_prompt_muons", #"pTjet_prompt_muons",
    "D0_sig_non_prompt_muons", "Z0_sig_non_prompt_muons", #"pTjet_non_prompt_muons",
    "D0_sig_prompt_electrons", "Z0_sig_prompt_electrons", #"pTjet_prompt_electrons",
    "D0_sig_non_prompt_electrons", "Z0_sig_non_prompt_electrons", #"pTjet_non_prompt_electrons",
    "iso_dr01_prompt_muons", "iso_dr01_non_prompt_muons", "iso_dr01_prompt_electrons", "iso_dr01_non_prompt_electrons",
    "iso_dr02_prompt_muons", "iso_dr02_non_prompt_muons", "iso_dr02_prompt_electrons", "iso_dr02_non_prompt_electrons",
    "iso_dr03_prompt_muons", "iso_dr03_non_prompt_muons", "iso_dr03_prompt_electrons", "iso_dr03_non_prompt_electrons",
    "iso_dr04_prompt_muons", "iso_dr04_non_prompt_muons", "iso_dr04_prompt_electrons", "iso_dr04_non_prompt_electrons",
    "pT_prompt_electrons", "pT_non_prompt_electrons", "pT_prompt_muons", "pT_non_prompt_muons", "pT_prompt_leptons", "pT_non_prompt_leptons",
    "eta_prompt_electrons", #"phi_prompt_electrons",
    "eta_non_prompt_electrons", #"phi_non_prompt_electrons",
    "eta_prompt_muons", #"phi_prompt_muons", 
    "eta_non_prompt_muons", #"phi_non_prompt_muons",
    "eta_prompt_leptons", #"phi_prompt_leptons",
    "eta_non_prompt_leptons", #"phi_non_prompt_leptons",
    "weight_prompt_electrons", "weight_non_prompt_electrons", "weight_prompt_muons", "weight_non_prompt_muons", "weight_prompt_leptons", "weight_non_prompt_leptons",
]

# Read and merge all files or process individually
if args.process_individual:
    events_list = [uproot.open(f)["events"].arrays(branches, library="ak") for f in file_list]
    print("Processing files individually")
else:
    events = [uproot.open(f)["events"].arrays(branches, library="ak") for f in file_list]
    events = ak.concatenate(events, axis=0)
    events_list = [events]
    print("Total events loaded (combined):", len(events))


# ------------------------------------------------------
# Helper to build DataFrame per category
# ------------------------------------------------------
def build_df(events, d0, z0, iso01, iso02, iso03, iso04, pT, eta, label, flavor, debug=False):
    # Flatten the nested arrays to ensure consistent lengths
    d0_arr = ak.flatten(events[d0], axis=None)
    z0_arr = ak.flatten(events[z0], axis=None)
    iso01_arr = ak.flatten(events[iso01], axis=None)
    iso02_arr = ak.flatten(events[iso02], axis=None)
    iso03_arr = ak.flatten(events[iso03], axis=None)
    iso04_arr = ak.flatten(events[iso04], axis=None)
    pT_arr = ak.flatten(events[pT], axis=None)
    eta_arr = ak.flatten(events[eta], axis=None)
   # phi_arr = ak.flatten(events[phi], axis=None)
  
    # Use per-lepton weight collections
    category = d0.split('_')[2]  # e.g., 'prompt' or 'non_prompt'
    if category == 'non':
        category = 'non_prompt'
    weight_key = f"weight_{category}_{flavor}s"
    w_arr = ak.flatten(events[weight_key], axis=None)
    print(f"Using per-lepton weight branch: {weight_key}")
    
    print(f"Lengths: D0={len(d0_arr)}, Z0={len(z0_arr)}, iso01={len(iso01_arr)}, iso02={len(iso02_arr)}, iso03={len(iso03_arr)}, iso04={len(iso04_arr)}, Weight={len(w_arr)}")
    
    # Ensure all arrays have the same length after flattening
    min_len = min(len(d0_arr), len(z0_arr), len(pT_arr), len(w_arr))
    d0_arr = d0_arr[:min_len]
    z0_arr = z0_arr[:min_len]
    iso01_arr = iso01_arr[:min_len]
    iso02_arr = iso02_arr[:min_len]
    iso03_arr = iso03_arr[:min_len]
    iso04_arr = iso04_arr[:min_len]
    w_arr = w_arr[:min_len]
    pT_arr = pT_arr[:min_len]
    eta_arr = eta_arr[:min_len]
   # phi_arr = phi_arr[:min_len]
    df = pd.DataFrame({
        "D0sig": ak.to_numpy(d0_arr),
        "Z0sig": ak.to_numpy(z0_arr),
        "iso01": ak.to_numpy(iso01_arr),
        "iso02": ak.to_numpy(iso02_arr),
        "iso03": ak.to_numpy(iso03_arr),
        "iso04": ak.to_numpy(iso04_arr),
        "weight": ak.to_numpy(w_arr),
        "pT": ak.to_numpy(pT_arr),
        "eta": ak.to_numpy(eta_arr),
        #"phi": ak.to_numpy(phi_arr)
    })
    df["label"] = label
    df["flavor"] = flavor
    
    # Debug sanity check: print a few rows
    if debug:
        print(f"==== Debug {flavor} (label={label}) ====")
        print(df.head(10))  # first 10 leptons
        print("Unique weights in these rows:", df["weight"].unique()[:5])  # should repeat
        print("======================================")
    
    return df
# ------------------------------------------------------
# Build DataFrames for all categories
# ------------------------------------------------------
# Function to extract Q-bin from filename
def extract_q_bin(filename):
    parts = filename.split('_Q_')
    if len(parts) > 1:
        q_bin = parts[1].split('_')[0]
        return q_bin
    return 'Unknown'

# Process each set of events (either individual files or combined)
roc_data_mu = []
roc_data_e = []
for idx, events in enumerate(events_list):
    if args.process_individual:
        q_bin = extract_q_bin(file_list[idx])
        print(f"Processing file {idx+1}/{len(file_list)} - Q-bin: {q_bin}")
    else:
        q_bin = 'Combined'
    
    # Build DataFrames as before
    df_p_mu  = build_df(events, "D0_sig_prompt_muons", "Z0_sig_prompt_muons", "iso_dr01_prompt_muons", "iso_dr02_prompt_muons", "iso_dr03_prompt_muons", "iso_dr04_prompt_muons", "pT_prompt_muons", "eta_prompt_muons", 1, "muon", debug=True)
    df_np_mu = build_df(events, "D0_sig_non_prompt_muons", "Z0_sig_non_prompt_muons", "iso_dr01_non_prompt_muons", "iso_dr02_non_prompt_muons", "iso_dr03_non_prompt_muons", "iso_dr04_non_prompt_muons", "pT_non_prompt_muons", "eta_non_prompt_muons", 0, "muon", debug=True)
    df_p_e   = build_df(events, "D0_sig_prompt_electrons", "Z0_sig_prompt_electrons", "iso_dr01_prompt_electrons", "iso_dr02_prompt_electrons", "iso_dr03_prompt_electrons", "iso_dr04_prompt_electrons", "pT_prompt_electrons", "eta_prompt_electrons", 1, "electron", debug=True)
    df_np_e  = build_df(events, "D0_sig_non_prompt_electrons", "Z0_sig_non_prompt_electrons", "iso_dr01_non_prompt_electrons", "iso_dr02_non_prompt_electrons", "iso_dr03_non_prompt_electrons", "iso_dr04_non_prompt_electrons", "pT_non_prompt_electrons", "eta_non_prompt_electrons", 0, "electron", debug=True)

    df = pd.concat([df_p_mu, df_np_mu, df_p_e, df_np_e], ignore_index=True)
    df = df.dropna()
    print(f"Total leptons in DataFrame (Q-bin {q_bin}):", len(df))
    print(f"Prompt vs Non-prompt counts (Q-bin {q_bin}):\n", df["label"].value_counts())

    # ------------------------------------------------------
    # Preprocessing: clip & scale features
    # ------------------------------------------------------
    # df["D0sig"] = np.clip(df["D0sig"], -150, 150)
    # df["Z0sig"] = np.clip(df["Z0sig"], -150, 150)
    # #df["pTjet"] = np.clip(df["pTjet"], 0, 10)
    # df["iso01"] = np.clip(df["iso01"], 0,20)
    # df["iso02"] = np.clip(df["iso02"], 0,20)
    # df["iso03"] = np.clip(df["iso03"], 0,20)
    # df["iso04"] = np.clip(df["iso04"], 0,20)
    # df["pT"] = np.clip(df["pT"], 0, 2500)
    # df["eta"] = np.clip(df["eta"], -10, 10)
    # #df["phi"] = np.clip(df["phi"], -10, 10)

    # Separate data for muons and electrons
    df_mu = df[df["flavor"] == "muon"]
    df_e = df[df["flavor"] == "electron"]

    # Features and labels for muons
    X_mu = df_mu[["D0sig", "Z0sig", "iso01", "iso02", "iso03", "iso04", "pT", "eta"]]
    y_mu = df_mu["label"]
    w_mu = df_mu["weight"]

    # Features and labels for electrons
    X_e = df_e[["D0sig", "Z0sig", "iso01", "iso02", "iso03", "iso04", "pT", "eta"]]
    y_e = df_e["label"]
    w_e = df_e["weight"]

    #scaler_mu = StandardScaler()
    #X_mu_scaled = scaler_mu.fit_transform(X_mu)

    # Save mean and std for use in histmaker.py
    #import numpy as np
    #np.savetxt('/eos/user/l/lberiet/ttZ_diff_results/BDT/scaler_mu_mean.txt', scaler_mu.mean_)
    #np.savetxt('/eos/user/l/lberiet/ttZ_diff_results/BDT/scaler_mu_std.txt', scaler_mu.scale_)
    #print('Saved mean and std for muons scaler')

    X_mu_scaled = X_mu  # Use unscaled features for training

    #scaler_e = StandardScaler()
    #X_e_scaled = scaler_e.fit_transform(X_e)

    # Save mean and std for use in histmaker.py
    #np.savetxt('/eos/user/l/lberiet/ttZ_diff_results/BDT/scaler_e_mean.txt', scaler_e.mean_)
    #np.savetxt('/eos/user/l/lberiet/ttZ_diff_results/BDT/scaler_e_std.txt', scaler_e.scale_)
    #print('Saved mean and std for electrons scaler')

    X_e_scaled = X_e  # Use unscaled features for training

    # Split data for muons
    X_mu_train, X_mu_test, y_mu_train, y_mu_test, w_mu_train, w_mu_test = train_test_split(
        X_mu_scaled, y_mu, w_mu, test_size=0.5, random_state=42, stratify=y_mu
    )

    # Split data for electrons
    X_e_train, X_e_test, y_e_train, y_e_test, w_e_train, w_e_test = train_test_split(
        X_e_scaled, y_e, w_e, test_size=0.5, random_state=42, stratify=y_e
    )

    # Train XGBoost BDT for muons
    # ------------------------------------------------------
    bdt_mu = XGBClassifier(
        tree_method="hist",          # critical for speed on millions of rows
        n_estimators=2000,           # large cap; early_stopping will stop earlier
        max_depth=4,                 
        learning_rate=0.05,          # smaller lr + more trees is safer
        min_child_weight=2.0,        # 1–5; raise to reduce overfitting
        subsample=0.8,               # row sampling
        colsample_bytree=0.8,        # feature sampling
        gamma=0.0,                   # 0–1; add if you see overfitting
        reg_lambda=2.0,              # L2; 1–5 stabilizes
        reg_alpha=0.0,               # try 0–0.5 if still overfitting
        n_jobs=8,
        random_state=42,
        eval_metric="auc"
    )
    bdt_mu.fit(X_mu_train, y_mu_train, sample_weight=w_mu_train)

    # Train XGBoost BDT for electrons
    # ------------------------------------------------------
    bdt_e = XGBClassifier(  
        tree_method="hist",          # critical for speed on millions of rows
        n_estimators=2000,           # large cap; early_stopping will stop earlier
        max_depth=4,                 # 3–5 is usually best for this task
        learning_rate=0.05,          # smaller lr + more trees is safer
        min_child_weight=2.0,        # 1–5; raise to reduce overfitting
        subsample=0.8,               # row sampling
        colsample_bytree=0.8,        # feature sampling
        gamma=0.0,                   # 0–1; add if you see overfitting
        reg_lambda=2.0,              # L2; 1–5 stabilizes
        reg_alpha=0.0,               # try 0–0.5 if still overfitting
        n_jobs=8,
        random_state=42,
        eval_metric="auc"
    )
    bdt_e.fit(X_e_train, y_e_train, sample_weight=w_e_train)

    # Evaluate for muons
    y_mu_score = bdt_mu.predict_proba(X_mu_test)[:,1]  # probability for "prompt" class
    fpr_mu, tpr_mu, thresholds_mu = roc_curve(y_mu_test, y_mu_score, sample_weight=w_mu_test)
    roc_auc_mu = auc(fpr_mu, tpr_mu)
    
    # Calculate Youden's J statistic for muons
    j_statistic_mu = tpr_mu - fpr_mu
    optimal_idx_mu = np.argmax(j_statistic_mu)
    optimal_threshold_mu = thresholds_mu[optimal_idx_mu]
    optimal_fpr_mu = fpr_mu[optimal_idx_mu]
    optimal_tpr_mu = tpr_mu[optimal_idx_mu]
    roc_data_mu.append((fpr_mu, tpr_mu, roc_auc_mu, q_bin, optimal_fpr_mu, optimal_tpr_mu, optimal_threshold_mu))

    # Evaluate for electrons
    y_e_score = bdt_e.predict_proba(X_e_test)[:,1]  # probability for "prompt" class
    fpr_e, tpr_e, thresholds_e = roc_curve(y_e_test, y_e_score, sample_weight=w_e_test)
    roc_auc_e = auc(fpr_e, tpr_e)
    
    # Calculate Youden's J statistic for electrons
    j_statistic_e = tpr_e - fpr_e
    optimal_idx_e = np.argmax(j_statistic_e)
    optimal_threshold_e = thresholds_e[optimal_idx_e]
    optimal_fpr_e = fpr_e[optimal_idx_e]
    optimal_tpr_e = tpr_e[optimal_idx_e]
    roc_data_e.append((fpr_e, tpr_e, roc_auc_e, q_bin, optimal_fpr_e, optimal_tpr_e, optimal_threshold_e))

    # Save models for individual Q-bins if processing individually, or for combined data if not
    if args.process_individual:
        bdt_mu.save_model(f"/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_muons_Q_{q_bin}.json")
        bdt_e.save_model(f"/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_electrons_Q_{q_bin}.json")
        print(f"Trained models saved for Q-bin {q_bin}")
    else:
        bdt_mu.save_model("/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_muons.json")
        bdt_e.save_model("/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_electrons.json")
        print("Trained models saved to bdt_model_muons.json and bdt_model_electrons.json")

    # Save BDT score distribution plots only for combined data (not individual processing)
    if not args.process_individual:
        # Score distributions for muons
        plt.hist(y_mu_score[y_mu_test==1], weights=w_mu_test[y_mu_test==1],
                 bins=70, histtype="step", density=True, label="Prompt Muons")
        plt.hist(y_mu_score[y_mu_test==0], weights=w_mu_test[y_mu_test==0],
                 bins=70, histtype="step", density=True, label="Non-prompt Muons")
        plt.xlabel("BDT score (Muons)")
        plt.ylabel("a.u.")
        plt.yscale("log")
        plt.legend()
        plt.savefig("/eos/user/l/lberiet/ttZ_diff_results/BDT/BDT_score_muons.png")
        plt.close()

        # Score distributions for electrons
        plt.hist(y_e_score[y_e_test==1], weights=w_e_test[y_e_test==1],
                 bins=70, histtype="step", density=True, label="Prompt Electrons")
        plt.hist(y_e_score[y_e_test==0], weights=w_e_test[y_e_test==0],
                 bins=70, histtype="step", density=True, label="Non-prompt Electrons")
        plt.xlabel("BDT score (Electrons)")
        plt.ylabel("a.u.")
        plt.yscale("log")
        plt.legend()
        plt.savefig("/eos/user/l/lberiet/ttZ_diff_results/BDT/BDT_score_electrons.png")
        plt.close()

# Plot ROC curves for muons and electrons
if args.process_individual:
    # Plot ROC curves for muons across all Q-bins
    plt.figure(figsize=(10, 8))
    for idx, (fpr, tpr, roc_auc, q_bin, optimal_fpr, optimal_tpr, optimal_threshold) in enumerate(roc_data_mu):
        plt.plot(fpr, tpr, label=f'Muons Q-bin {q_bin} (AUC = {roc_auc:.3f}, Eff = {optimal_tpr:.3f}, Mistag = {optimal_fpr:.3f}, Thresh = {optimal_threshold:.3f})', color=f'C{idx}')
        plt.plot(optimal_fpr, optimal_tpr, 'o', markersize=8, color=f'C{idx}')
    plt.xlabel("Mis-identification rate")
    plt.ylabel("Signal efficiency")
    plt.xscale("log")
    plt.legend(fontsize='small', loc='lower right')
    plt.title("ROC Curves for Muons across Q-bins")
    plt.savefig("/eos/user/l/lberiet/ttZ_diff_results/BDT/BDT_ROC_muons_Q_bins.png")
    plt.close()

    # Plot ROC curves for electrons across all Q-bins
    plt.figure(figsize=(10, 8))
    for idx, (fpr, tpr, roc_auc, q_bin, optimal_fpr, optimal_tpr, optimal_threshold) in enumerate(roc_data_e):
        plt.plot(fpr, tpr, label=f'Electrons Q-bin {q_bin} (AUC = {roc_auc:.3f}, Eff = {optimal_tpr:.3f}, Mistag = {optimal_fpr:.3f}, Thresh = {optimal_threshold:.3f})', color=f'C{idx}')
        plt.plot(optimal_fpr, optimal_tpr, 'o', markersize=8, color=f'C{idx}')
    plt.xlabel("Mis-identification rate")
    plt.ylabel("Signal efficiency")
    plt.xscale("log")
    plt.legend(fontsize='small', loc='lower right')
    plt.title("ROC Curves for Electrons across Q-bins")
    plt.savefig("/eos/user/l/lberiet/ttZ_diff_results/BDT/BDT_ROC_electrons_Q_bins.png")
    plt.close()
else:
    # Plot combined ROC curves for muons and electrons on the same plot
    plt.figure(figsize=(10, 8))
    if len(roc_data_mu) == 1:
        fpr, tpr, roc_auc, q_bin, optimal_fpr, optimal_tpr, optimal_threshold = roc_data_mu[0]
        plt.plot(fpr, tpr, label=f'Muons Combined (AUC = {roc_auc:.3f}, Eff = {optimal_tpr:.3f}, Mistag = {optimal_fpr:.3f}, Thresh = {optimal_threshold:.3f})', color='blue')
        plt.plot(optimal_fpr, optimal_tpr, 'o', color='darkblue', markersize=8, label='Muon YP Combined')
    if len(roc_data_e) == 1:
        fpr, tpr, roc_auc, q_bin, optimal_fpr, optimal_tpr, optimal_threshold = roc_data_e[0]
        plt.plot(fpr, tpr, label=f'Electrons Combined (AUC = {roc_auc:.3f}, Eff = {optimal_tpr:.3f}, Mistag = {optimal_fpr:.3f}, Thresh = {optimal_threshold:.3f})', color='red')
        plt.plot(optimal_fpr, optimal_tpr, 'o', color='darkred', markersize=8, label='Electron YP Combined')
    plt.xlabel("Mis-identification rate")
    plt.ylabel("Signal efficiency")
    plt.xscale("log")
    plt.legend(fontsize='small', loc='lower right')
    plt.title("ROC Curves for Muons and Electrons (Combined)")
    plt.savefig("/eos/user/l/lberiet/ttZ_diff_results/BDT/BDT_ROC_combined.png")
    plt.close()

# ------------------------------------------------------
# Feature importance for both models
# ------------------------------------------------------
print("Feature importance for Muons:")
for var, imp in zip(X_mu.columns, bdt_mu.feature_importances_):
    print(f"{var}: {imp:.3f}")

print("\nFeature importance for Electrons:")
for var, imp in zip(X_e.columns, bdt_e.feature_importances_):
    print(f"{var}: {imp:.3f}")

# Save the trained models
# The models are now saved individually for each Q-bin, so we don't save a combined model here.
# If you want to save a combined model, you would need to modify the loop to fit a single model
# on all data or aggregate the feature importances.
