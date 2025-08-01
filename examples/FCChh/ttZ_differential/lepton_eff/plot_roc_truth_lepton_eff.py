import ROOT
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import os

def plot_roc_curves(input_file, output_dir="plots"):
    # Open the ROOT file
    root_file = ROOT.TFile.Open(input_file)
    if not root_file or root_file.IsZombie():
        raise RuntimeError(f"Cannot open ROOT file: {input_file}")
    tree = root_file.Get("events")  # Assuming the tree name is "events"
    if not tree:
        raise RuntimeError("Cannot find tree 'events' in ROOT file")

    # Dictionaries to store isolation values and labels for each cone size
    muon_iso = {"dr01": [], "dr02": [], "dr03": []}
    electron_iso = {"dr01": [], "dr02": [], "dr03": []}
    muon_labels = {"dr01": [], "dr02": [], "dr03": []}
    electron_labels = {"dr01": [], "dr02": [], "dr03": []}

    # Loop over the tree entries
    for event in tree:
        # Muons
        for dr in ["dr01", "dr02", "dr03"]:
            prompt_key = f"prompt_muons_iso_{dr}"
            non_prompt_key = f"non_prompt_muons_iso_{dr}"
            for iso_val in getattr(event, prompt_key):
                muon_iso[dr].append(iso_val)
                muon_labels[dr].append(1)  # Prompt muons
            for iso_val in getattr(event, non_prompt_key):
                muon_iso[dr].append(iso_val)
                muon_labels[dr].append(0)  # Non-prompt muons

        # Electrons
        for dr in ["dr01", "dr02", "dr03"]:
            prompt_key = f"prompt_electrons_iso_{dr}"
            non_prompt_key = f"non_prompt_electrons_iso_{dr}"
            for iso_val in getattr(event, prompt_key):
                electron_iso[dr].append(iso_val)
                electron_labels[dr].append(1)  # Prompt electrons
            for iso_val in getattr(event, non_prompt_key):
                electron_iso[dr].append(iso_val)
                electron_labels[dr].append(0)  # Non-prompt electrons

    # Convert lists to numpy arrays and check consistency
    for dr in ["dr01", "dr02", "dr03"]:
        muon_iso[dr] = np.array(muon_iso[dr])
        muon_labels[dr] = np.array(muon_labels[dr])
        electron_iso[dr] = np.array(electron_iso[dr])
        electron_labels[dr] = np.array(electron_labels[dr])

        # Check lengths
        if len(muon_iso[dr]) != len(muon_labels[dr]):
            print(f"Warning: Inconsistent lengths for muons {dr}: iso={len(muon_iso[dr])}, labels={len(muon_labels[dr])}")
        if len(electron_iso[dr]) != len(electron_labels[dr]):
            print(f"Warning: Inconsistent lengths for electrons {dr}: iso={len(electron_iso[dr])}, labels={len(electron_labels[dr])}")

    # Plot ROC curves for muons
    plt.figure(figsize=(8, 6))
    for dr in ["dr01", "dr02", "dr03"]:
        if len(muon_iso[dr]) == 0 or len(muon_labels[dr]) == 0:
            print(f"Skipping muon ROC for {dr}: empty data")
            continue
        if len(muon_iso[dr]) != len(muon_labels[dr]):
            print(f"Skipping muon ROC for {dr}: inconsistent lengths")
            continue
        fpr, tpr, _ = roc_curve(muon_labels[dr], muon_iso[dr])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'Muons {dr} (AUC = {roc_auc:.2f})')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    #plt.yscale('log')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves for Muon Isolation')
    plt.legend(loc="lower right")
    plt.grid(False)
    plt.savefig(f"{output_dir}/roc_muons.png")
    plt.close()

    # Plot ROC curves for electrons
    plt.figure(figsize=(8, 6))
    for dr in ["dr01", "dr02", "dr03"]:
        if len(electron_iso[dr]) == 0 or len(electron_labels[dr]) == 0:
            print(f"Skipping electron ROC for {dr}: empty data")
            continue
        if len(electron_iso[dr]) != len(electron_labels[dr]):
            print(f"Skipping electron ROC for {dr}: inconsistent lengths")
            continue
        fpr, tpr, _ = roc_curve(electron_labels[dr], electron_iso[dr])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'Electrons {dr} (AUC = {roc_auc:.2f})')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    #plt.yscale('log')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves for Electron Isolation')
    plt.legend(loc="lower right")
   
    plt.savefig(f"{output_dir}/roc_electrons.png")
    plt.close()

    # Close the ROOT file
    root_file.Close()

if __name__ == "__main__":
    input_file = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/result/mgp8_pp_ttz_5f_84TeV_ttzlep.root"  # Update with your ROOT file path
    output_dir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plot_roc_curves(input_file, output_dir)