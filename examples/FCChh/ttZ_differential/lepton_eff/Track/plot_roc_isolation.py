import uproot
import numpy as np
import matplotlib.pyplot as plt
import os

# Open the ROOT file
file_path = "/eos/user/l/lberiet/ttZ_diff_results/tracks/mgp8_pp_ttz_5f_84TeV_ttzlep.root"
file = uproot.open(file_path)
if not file:
    print("Error opening file!")
    exit(1)

# Get the tree
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


# Custom branch input functionality
custom_prompt_branch = input("Enter the prompt branch name: ")
custom_non_prompt_branch = input("Enter the non-prompt branch name: ")
plot_multiple = input("Do you want to plot for different values? (y/n): ").lower() == 'y'
if plot_multiple:
    custom_dr_values = input("Enter the value identifiers separated by commas (e.g., 02,03): ").split(',')
    custom_prompt_branches = [f"{custom_prompt_branch}_dr{dr}" for dr in custom_dr_values]
    custom_non_prompt_branches = [f"{custom_non_prompt_branch}_dr{dr}" for dr in custom_dr_values]
else:
    custom_dr_values = ["custom"]
    custom_prompt_branches = [custom_prompt_branch]
    custom_non_prompt_branches = [custom_non_prompt_branch]

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
all_branches = custom_prompt_branches + custom_non_prompt_branches
try:
    data = tree.arrays(all_branches, library="np")
except Exception as e:
    print(f"Error loading branches: {e}")
    print("Please check the branch names based on the printed list above.")
    file.close()
    exit(1)

# Process Custom branches
custom_roc_data = []
custom_markers = []
custom_youden_markers = []
for i, dr in enumerate(custom_dr_values):
    branch_p = custom_prompt_branches[i]
    branch_np = custom_non_prompt_branches[i]
    
    efficiency, inefficiency, youden_point = calculate_roc(data[branch_p], data[branch_np], iso_thresholds)
    
    if len(efficiency) > 0 and len(inefficiency) > 0:
        custom_roc_data.append((efficiency, inefficiency, dr, 'custom'))
        # Find the index closest to iso=0.2 for custom
        idx = np.argmin(np.abs(iso_thresholds - 0.2))
        if idx < len(efficiency):
            custom_markers.append((efficiency[idx], inefficiency[idx], dr, 'custom'))
            print(f"Custom Value={dr}: Threshold=0.2, Efficiency={efficiency[idx]:.3f}, Inefficiency={inefficiency[idx]:.3f}")
        # Add Youden's optimal point
        custom_youden_markers.append(youden_point + (dr, 'custom'))
        print(f"Custom Value={dr}: Data processed, Optimal Threshold (Youden) = {youden_point[2]:.3f}, Efficiency={youden_point[0]:.3f}, Inefficiency={youden_point[1]:.3f}")
    else:
        print(f"Custom Value={dr}: No valid data")

# Plot ROC curves
plt.figure(figsize=(8, 6))

# Custom ROC curves
colors = ['r', 'b', 'g', 'm', 'y']
youden_colors_custom = ['darkred', 'darkblue', 'darkgreen', 'darkmagenta', 'goldenrod']
linestyles = {'custom': '-'}
for i, (efficiency, inefficiency, dr, cut_type) in enumerate(custom_roc_data):
    plt.plot(inefficiency, efficiency, label=f'Value = {dr} ({cut_type})', 
             color=colors[i % len(colors)], linestyle=linestyles[cut_type])

# Add markers for threshold=0.2 for custom, only for the first value if multiple
for eff, ineff, dr, cut_type in custom_markers:
    if len(custom_dr_values) == 1 or custom_dr_values.index(dr) == 0:
        plt.plot(ineff, eff, '.', markersize=10, color=colors[custom_dr_values.index(dr) % len(colors)], 
                 label=f'Threshold=0.2 (Value={dr}, {cut_type})')

# Add markers for Youden's optimal threshold for custom
for eff, ineff, threshold, dr, cut_type in custom_youden_markers:
    plt.plot(ineff, eff, '*', markersize=12, color=youden_colors_custom[custom_dr_values.index(dr) % len(youden_colors_custom)], 
             label=f'Youden Threshold={threshold:.3f} (Value={dr}, {cut_type})')

plt.xlabel('Inefficiency (Non-Prompt)')
plt.ylabel('Efficiency (Prompt)')
plt.title('ROC Curves')

plt.xscale('log')
plt.xlim(1e-2, 1)  # Adjusted to avoid issues with log scale at 0
plt.ylim(0.1, 1)
plt.legend()

plt.tight_layout()
# Ensure the directory exists
plot_dir = os.path.dirname("/eos/user/l/lberiet/ttZ_diff_results/tracks/plots/roc_curves_custom.png")
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir, exist_ok=True)
    print(f"Created directory {plot_dir}")
plt.savefig("/eos/user/l/lberiet/ttZ_diff_results/tracks/plots/roc_curves_custom.png")
plt.close()

print("Plots saved to /eos/user/l/lberiet/ttZ_diff_results/tracks/plots/roc_curves_custom.png")

# Close the file
file.close()