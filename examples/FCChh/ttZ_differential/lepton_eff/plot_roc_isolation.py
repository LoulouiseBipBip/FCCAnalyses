import uproot
import numpy as np
import matplotlib.pyplot as plt
import glob
# Open the ROOT file
file_list = glob.glob("/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/result/mgp8_pp_ttz_5f_Q_*_84TeV_ttzlep.root")
print(f"Found {len(file_list)} ROOT files")

# Get the tree
for file_path in file_list:
    file = uproot.open(file_path)
    if not file:
        print("Error opening file!")
        exit(1)
    tree = file["events"]
    if not tree:
        print("Error getting tree!")
        file.close()
        exit(1)

# Print available branches to debug
print("Available branches in the tree:")
for branch in tree.keys():
    print(branch)

# Define ΔR values and corresponding branch names
dr_values = ["01", "02", "03", "04", "05"]
muon_prompt_branches = [f"prompt_muons_iso_dr{dr}" for dr in dr_values]
muon_non_prompt_branches = [f"non_prompt_muons_iso_dr{dr}" for dr in dr_values]
electron_prompt_branches = [f"prompt_electrons_iso_dr{dr}" for dr in dr_values]
electron_non_prompt_branches = [f"non_prompt_electrons_iso_dr{dr}" for dr in dr_values]

# Step size for isolation threshold
step = 0.0001
max_iso = 50
n_steps = int(max_iso / step) + 1
iso_thresholds = np.linspace(0, max_iso, n_steps)

# Function to calculate efficiency and inefficiency
def calculate_roc(data_prompt, data_non_prompt, thresholds):
    # Flatten the data (since it's a jagged array)
    flat_prompt = np.concatenate(data_prompt)
    flat_non_prompt = np.concatenate(data_non_prompt)
    
    # Filter out invalid values (e.g., < -999)
    valid_prompt = flat_prompt[flat_prompt > -999]
    valid_non_prompt = flat_non_prompt[flat_non_prompt > -999]
    
    total_prompt = len(valid_prompt)
    total_non_prompt = len(valid_non_prompt)
    
    if total_prompt == 0 or total_non_prompt == 0:
        return np.array([]), np.array([]), np.array([])
    
    # Calculate efficiency and inefficiency for each threshold
    efficiency = np.array([np.sum(valid_prompt < t) / total_prompt for t in thresholds])
    inefficiency = np.array([np.sum(valid_non_prompt < t) / total_non_prompt for t in thresholds])
    
    # Calculate Youden's J Statistic (TPR - FPR)
    youden_j = efficiency - inefficiency
    optimal_idx = np.argmax(youden_j)
    optimal_threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else thresholds[-1]
    optimal_eff = efficiency[optimal_idx] if optimal_idx < len(efficiency) else efficiency[-1]
    optimal_ineff = inefficiency[optimal_idx] if optimal_idx < len(inefficiency) else inefficiency[-1]
    
    return efficiency, inefficiency, (optimal_eff, optimal_ineff, optimal_threshold)

# Load data for all branches at once to minimize I/O
all_branches = muon_prompt_branches + muon_non_prompt_branches + electron_prompt_branches + electron_non_prompt_branches
try:
    data = tree.arrays(all_branches, library="np")
except Exception as e:
    print(f"Error loading branches: {e}")
    print("Please check the branch names based on the printed list above.")
    file.close()
    exit(1)

# Process Muons
muon_roc_data = []
muon_markers = []
muon_youden_markers = []
for i, dr in enumerate(dr_values):
    branch_p = muon_prompt_branches[i]
    branch_np = muon_non_prompt_branches[i]
    
    efficiency, inefficiency, youden_point = calculate_roc(data[branch_p], data[branch_np], iso_thresholds)
    
    if len(efficiency) > 0 and len(inefficiency) > 0:
        muon_roc_data.append((efficiency, inefficiency, dr))
        # Find the index closest to iso=0.2 for muons
        idx = np.argmin(np.abs(iso_thresholds - 0.2))
        if idx < len(efficiency):
            muon_markers.append((efficiency[idx], inefficiency[idx], dr))
            print(f"Muons ΔR=0.{dr}: Iso=0.2, Efficiency={efficiency[idx]:.3f}, Inefficiency={inefficiency[idx]:.3f}")
        # Add Youden's optimal point
        muon_youden_markers.append(youden_point + (dr,))
        print(f"Muons ΔR={dr}: Data processed, Optimal Iso (Youden) = {youden_point[2]:.3f}, Efficiency={youden_point[0]:.3f}, Inefficiency={youden_point[1]:.3f}")
    else:
        print(f"Muons ΔR={dr}: No valid data")

# Process Electrons
electron_roc_data = []
electron_markers = []
electron_youden_markers = []
for i, dr in enumerate(dr_values):
    branch_p = electron_prompt_branches[i]
    branch_np = electron_non_prompt_branches[i]
    
    efficiency, inefficiency, youden_point = calculate_roc(data[branch_p], data[branch_np], iso_thresholds)
    
    if len(efficiency) > 0 and len(inefficiency) > 0:
        electron_roc_data.append((efficiency, inefficiency, dr))
        # Find the index closest to iso=0.1 for electrons
        idx = np.argmin(np.abs(iso_thresholds - 0.1))
        if idx < len(efficiency):
            electron_markers.append((efficiency[idx], inefficiency[idx], dr))
            print(f"Electrons ΔR={dr}: Iso=0.1, Efficiency={efficiency[idx]:.3f}, Inefficiency={inefficiency[idx]:.3f}")
        # Add Youden's optimal point
        electron_youden_markers.append(youden_point + (dr,))
        print(f"Electrons ΔR={dr}: Data processed, Optimal Iso (Youden) = {youden_point[2]:.3f}, Efficiency={youden_point[0]:.3f}, Inefficiency={youden_point[1]:.3f}")
    else:
        print(f"Electrons ΔR={dr}: No valid data")

# Plot ROC curves
plt.figure(figsize=(12, 5))

# Muon ROC curves
plt.subplot(1, 2, 1)
colors = ['r', 'b', 'g', 'm', 'y']
youden_colors = ['darkred', 'darkblue', 'darkgreen', 'darkmagenta', 'goldenrod']
for i, (efficiency, inefficiency, dr) in enumerate(muon_roc_data):
    plt.plot(inefficiency, efficiency, label=f'ΔR = 0.{dr}', color=colors[i % len(colors)])

# Add markers for iso=0.2 for muons, only for ΔR=0.3
for eff, ineff, dr in muon_markers:
    if dr == "03":
        plt.plot(ineff, eff, '.', markersize=10, color=colors[dr_values.index(dr) % len(colors)], label=f'Iso=0.2 (ΔR={dr})')

# Add markers for Youden's optimal iso for muons
for eff, ineff, threshold, dr in muon_youden_markers:
    plt.plot(ineff, eff, '*', markersize=12, color=youden_colors[dr_values.index(dr) % len(youden_colors)], label=f'Youden Iso={threshold:.3f} (ΔR={dr})')

plt.xlabel('Inefficiency (Non-Prompt)')
plt.ylabel('Efficiency (Prompt)')
plt.title('Muon ROC Curves')

plt.xscale('log')
plt.xlim(1e-4, 1)  # Adjusted to avoid issues with log scale at 0
plt.ylim(0.1, 1)
plt.legend()

# Electron ROC curves
plt.subplot(1, 2, 2)
for i, (efficiency, inefficiency, dr) in enumerate(electron_roc_data):
    plt.plot(inefficiency, efficiency, label=f'ΔR = {dr}', color=colors[i % len(colors)])

# Add markers for iso=0.1 for electrons, only for ΔR=0.3
for eff, ineff, dr in electron_markers:
    if dr == "03":
        plt.plot(ineff, eff, '.', markersize=10, color=colors[dr_values.index(dr) % len(colors)], label=f'Old Iso=0.1 (ΔR={dr})')

# Add markers for Youden's optimal iso for electrons
for eff, ineff, threshold, dr in electron_youden_markers:
    plt.plot(ineff, eff, '*', markersize=12, color=youden_colors[dr_values.index(dr) % len(youden_colors)], label=f'Optimal Iso={threshold:.3f}')

plt.xlabel('Inefficiency (Non-Prompt)')
plt.ylabel('Efficiency (Prompt)')
plt.title('Electron ROC Curves')

plt.xscale('log')
plt.xlim(1e-3, 1)  # Adjusted to avoid issues with log scale at 0
plt.ylim(0.1, 1)
plt.legend()

plt.tight_layout()
plt.savefig("/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/plots/ROC_iso/roc_curves_isolation_nolep.png")
plt.close()

print("Plots saved to /eos/user/l/lberiet/ttZ_diff_results/lepton_eff/plots/ROC_iso/roc_curves_isolation_nolep.png")

# Close the file
file.close()