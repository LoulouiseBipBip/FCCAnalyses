import uproot
import numpy as np
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

# Custom branch input functionality
custom_prompt_branch = input("Enter the prompt branch name: ")
custom_non_prompt_branch = input("Enter the non-prompt branch name: ")
plot_multiple = input("Do you want to compute for different values? (y/n): ").lower() == 'y'
if plot_multiple:
    custom_dr_values = input("Enter the value identifiers separated by commas (e.g., 02,03): ").split(',')
    custom_prompt_branches = [f"{custom_prompt_branch}_dr{dr}" for dr in custom_dr_values]
    custom_non_prompt_branches = [f"{custom_non_prompt_branch}_dr{dr}" for dr in custom_dr_values]
else:
    custom_dr_values = ["custom"]
    custom_prompt_branches = [custom_prompt_branch]
    custom_non_prompt_branches = [custom_non_prompt_branch]

# User input for threshold
threshold = float(input("Enter the isolation threshold value: "))
threshold_type = input("Is the threshold a minimum (min) or maximum (max) value? (min/max): ").lower()
while threshold_type not in ['min', 'max']:
    threshold_type = input("Invalid input. Please enter 'min' or 'max': ").lower()

# Function to calculate efficiency and inefficiency
def calculate_efficiency(data_prompt, data_non_prompt, threshold, threshold_type):
    # Flatten the data (since it's a jagged array)
    flat_prompt = np.concatenate(data_prompt)
    flat_non_prompt = np.concatenate(data_non_prompt)
    
    # Filter out invalid values (e.g., < -999)
    valid_prompt = flat_prompt[flat_prompt > -999]
    valid_non_prompt = flat_non_prompt[flat_non_prompt > -999]
    
    total_prompt = len(valid_prompt)
    total_non_prompt = len(valid_non_prompt)
    
    if total_prompt == 0 or total_non_prompt == 0:
        return 0.0, 0.0
    
    # Calculate efficiency and inefficiency for the threshold based on type
    if threshold_type == 'min':
        efficiency = np.sum(valid_prompt > threshold) / total_prompt
        inefficiency = np.sum(valid_non_prompt > threshold) / total_non_prompt
    else:  # max
        efficiency = np.sum(valid_prompt < threshold) / total_prompt
        inefficiency = np.sum(valid_non_prompt < threshold) / total_non_prompt
    
    return efficiency, inefficiency

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
print(f"\nResults for Isolation Threshold = {threshold} ({threshold_type} value):")
efficiency, inefficiency = calculate_efficiency(
    data[custom_prompt_branch], 
    data[custom_non_prompt_branch], 
    threshold, 
    threshold_type
)

if efficiency > 0 or inefficiency > 0:
    print(f"Efficiency={efficiency:.3f}, Inefficiency={inefficiency:.3f}")
else:
    print("No valid data")

# Ask user if they want to recalculate with a different threshold
while True:
    redo = input("\nDo you want to recalculate with a different threshold value? (y/n): ").lower()
    if redo == 'y':
        threshold = float(input("Enter the new threshold value: "))
        threshold_type = input("Is the threshold a minimum (min) or maximum (max) value? (min/max): ").lower()
        while threshold_type not in ['min', 'max']:
            threshold_type = input("Invalid input. Please enter 'min' or 'max': ").lower()
        
        print(f"\nResults for Isolation Threshold = {threshold} ({threshold_type} value):")
        efficiency, inefficiency = calculate_efficiency(
            data[custom_prompt_branch], 
            data[custom_non_prompt_branch], 
            threshold, 
            threshold_type
        )
        
        if efficiency > 0 or inefficiency > 0:
            print(f"Efficiency={efficiency:.3f}, Inefficiency={inefficiency:.3f}")
        else:
            print("No valid data")
    elif redo == 'n':
        print("Exiting script.")
        break
    else:
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

# Close the file
file.close()
