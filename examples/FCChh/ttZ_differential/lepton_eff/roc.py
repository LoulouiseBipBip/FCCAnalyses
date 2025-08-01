import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_roc_curves(input_file, output_dir="plots"):
    # Open the ROOT file
    root_file = ROOT.TFile.Open(input_file)
    if not root_file or root_file.IsZombie():
        raise RuntimeError(f"Cannot open ROOT file: {input_file}")
    tree = root_file.Get("events")  # Assuming the tree name is "events"
    if not tree:
        raise RuntimeError("Cannot find tree 'events' in ROOT file")

    # Dictionaries to store isolation values for each cone size
    muon_iso = {"dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": []}
    electron_iso = {"dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": []}
    muon_labels = {"dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": []}
    electron_labels = {"dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": []}

    # Loop over the tree entries
    for event in tree:
        # Muons
        for dr in ["dr01", "dr02", "dr03", "dr04", "dr05"]:
            prompt_key = f"prompt_muons_iso_{dr}"
            non_prompt_key = f"non_prompt_muons_iso_{dr}"
            for iso_val in getattr(event, prompt_key):
                muon_iso[dr].append(iso_val)
                muon_labels[dr].append(1)  # Prompt muons
            for iso_val in getattr(event, non_prompt_key):
                muon_iso[dr].append(iso_val)
                muon_labels[dr].append(0)  # Non-prompt muons

        # Electrons
        for dr in ["dr01", "dr02", "dr03", "dr04", "dr05"]:
            prompt_key = f"prompt_electrons_iso_{dr}"
            non_prompt_key = f"non_prompt_electrons_iso_{dr}"
            for iso_val in getattr(event, prompt_key):
                electron_iso[dr].append(iso_val)
                electron_labels[dr].append(1)  # Prompt electrons
            for iso_val in getattr(event, non_prompt_key):
                electron_iso[dr].append(iso_val)
                electron_labels[dr].append(0)  # Non-prompt electrons

    # Convert lists to numpy arrays
    for dr in ["dr01", "dr02", "dr03", "dr04", "dr05"]:
        muon_iso[dr] = np.array(muon_iso[dr])
        muon_labels[dr] = np.array(muon_labels[dr])
        electron_iso[dr] = np.array(electron_iso[dr])
        electron_labels[dr] = np.array(electron_labels[dr])

    # Calculate efficiencies and inefficiencies for ROC curves
    d_values_check = 100
    efficiencies_prompt_muons = { "dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": [] }
    inefficiencies_non_prompt_muons = { "dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": [] }
    efficiencies_prompt_electrons = { "dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": [] }
    inefficiencies_non_prompt_electrons = { "dr01": [], "dr02": [], "dr03": [], "dr04": [], "dr05": [] }

    for i in range(0, d_values_check):
        d_val = i / d_values_check  # D_Iso value from 0 to 1
        for dr in ["dr01", "dr02", "dr03", "dr04", "dr05"]:
            # Muons
            mask_prompt_muons = muon_iso[dr][muon_labels[dr] == 1] < d_val
            mask_non_prompt_muons = muon_iso[dr][muon_labels[dr] == 0] < d_val
            prompt_muons = muon_iso[dr][muon_labels[dr] == 1][mask_prompt_muons]
            non_prompt_muons = muon_iso[dr][muon_labels[dr] == 0][mask_non_prompt_muons]
            total_prompt_muons = len(muon_iso[dr][muon_labels[dr] == 1])
            total_non_prompt_muons = len(muon_iso[dr][muon_labels[dr] == 0])
            efficiencies_prompt_muons[dr].append(len(prompt_muons) / total_prompt_muons if total_prompt_muons > 0 else 0)
            inefficiencies_non_prompt_muons[dr].append(len(non_prompt_muons) / total_non_prompt_muons if total_non_prompt_muons > 0 else 0)

            # Electrons
            mask_prompt_electrons = electron_iso[dr][electron_labels[dr] == 1] < d_val
            mask_non_prompt_electrons = electron_iso[dr][electron_labels[dr] == 0] < d_val
            prompt_electrons = electron_iso[dr][electron_labels[dr] == 1][mask_prompt_electrons]
            non_prompt_electrons = electron_iso[dr][electron_labels[dr] == 0][mask_non_prompt_electrons]
            total_prompt_electrons = len(electron_iso[dr][electron_labels[dr] == 1])
            total_non_prompt_electrons = len(electron_iso[dr][electron_labels[dr] == 0])
            efficiencies_prompt_electrons[dr].append(len(prompt_electrons) / total_prompt_electrons if total_prompt_electrons > 0 else 0)
            inefficiencies_non_prompt_electrons[dr].append(len(non_prompt_electrons) / total_non_prompt_electrons if total_non_prompt_electrons > 0 else 0)

    # Plot ROC curves for muons
    plt.figure(figsize=(8, 6))
    for dr in ['dr01', 'dr02', 'dr03', 'dr04', 'dr05']:
        fpr = inefficiencies_non_prompt_muons[dr]
        tpr = efficiencies_prompt_muons[dr]
        plt.plot(fpr, tpr, label=f'Muons {dr}')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    #plt.yscale('symlog')
    plt.xlabel('False Positive Rate (Non-Prompt Muon Inefficiency)')
    plt.ylabel('True Positive Rate (Prompt Muon Efficiency)')
    plt.title('ROC Curves for Muon Isolation')
    plt.legend(loc="lower right")
    plt.grid(False)
    plt.savefig(f"{output_dir}/roc_muons.png")
    plt.close()

    # Plot ROC curves for electrons
    plt.figure(figsize=(8, 6))
    for dr in ['dr01', 'dr02', 'dr03', 'dr04', 'dr05']:
        fpr = inefficiencies_non_prompt_electrons[dr]
        tpr = efficiencies_prompt_electrons[dr]
        plt.plot(fpr, tpr, label=f'Electrons {dr}')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
   # plt.yscale('log')
    plt.xlabel('False Positive Rate (Non-Prompt Electron Inefficiency)')
    plt.ylabel('True Positive Rate (Prompt Electron Efficiency)')
    plt.title('ROC Curves for Electron Isolation')
    plt.legend(loc="lower right")
    plt.grid(False)
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
