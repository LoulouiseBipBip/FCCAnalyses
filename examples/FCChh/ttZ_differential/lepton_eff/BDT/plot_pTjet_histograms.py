import glob
import uproot
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Command line argument parsing
parser = argparse.ArgumentParser(description='Plot histograms and ratios for prompt and non-prompt leptons from ROOT files.')
parser.add_argument('--variable', type=str, default='pTjet', help='Variable to plot (default: pTjet)')
parser.add_argument('--xlabel', type=str, default='pT_{jet} (GeV)', help='X-axis label for the plots (default: pT_{jet} (GeV))')
args = parser.parse_args()

# Input ROOT files for different Q-binned datasets
file_pattern = '/eos/user/l/lberiet/ttZ_diff_results/BDT/final/mgp8_pp_ttz_5f_Q_*_84TeV_ttzlep_all_events_histo.root'
file_list = glob.glob(file_pattern)
print(f'Found {len(file_list)} ROOT files')

# Variables to plot based on user input
variables = {
    f'{args.variable}_prompt_muons': f'{args.variable} (Prompt Muons)',
    f'{args.variable}_prompt_electrons': f'{args.variable} (Prompt Electrons)',
    f'{args.variable}_non_prompt_muons': f'{args.variable} (Non-Prompt Muons)',
    f'{args.variable}_non_prompt_electrons': f'{args.variable} (Non-Prompt Electrons)'
}

# Pairs for combined distribution and ratio plots (prompt vs non-prompt for muons and electrons)
plot_pairs = [
    (f'{args.variable}_prompt_muons', f'{args.variable}_non_prompt_muons', 'Muons'),
    (f'{args.variable}_prompt_electrons', f'{args.variable}_non_prompt_electrons', 'Electrons')
]

# Check contents of each file to debug histogram keys
for file_path in file_list:
    print(f'\nChecking contents of {file_path}:')
    with uproot.open(file_path) as f:
        keys = f.keys()
        print('Available keys:', keys)
        # Look for anything that might resemble the histograms we're interested in
        for key in keys:
            if args.variable in key:
                print(f'Found potential match: {key}')

# Store histogram data for each variable
hist_data = {var_name: {'hist': None, 'bins': None} for var_name in variables}

# Loop through each file to extract histogram data for all variables
for file_path in file_list:
    with uproot.open(file_path) as f:
        for var_name in variables:
            hist_key = f'{var_name};1'
            if hist_key in f:
                hist = f[hist_key].to_numpy()
                hist_values = hist[0]  # Histogram values
                bins = hist[1]  # Bin edges

                if hist_data[var_name]['hist'] is None:
                    hist_data[var_name]['hist'] = hist_values
                    hist_data[var_name]['bins'] = bins
                else:
                    # Ensure bins match across files (they should)
                    if not np.array_equal(hist_data[var_name]['bins'], bins):
                        print(f'Warning: Bin mismatch for {var_name} in {file_path}, skipping...')
                        continue
                    hist_data[var_name]['hist'] += hist_values
            else:
                print(f'Histogram {var_name} not found in {file_path}, skipping...')

# Plot combined normalized histograms and ratio for each lepton type
for prompt_var, non_prompt_var, lepton_type in plot_pairs:
    if hist_data[prompt_var]['hist'] is None or hist_data[non_prompt_var]['hist'] is None:
        print(f'No data found for {prompt_var} or {non_prompt_var}, skipping plot for {lepton_type}...')
        continue

    # Normalize histograms to integral (total area under the curve = 1)
    prompt_integral = np.sum(hist_data[prompt_var]['hist'])
    non_prompt_integral = np.sum(hist_data[non_prompt_var]['hist'])

    prompt_normalized = hist_data[prompt_var]['hist']
    non_prompt_normalized = hist_data[non_prompt_var]['hist']

    if prompt_integral > 0:
        prompt_normalized = prompt_normalized / prompt_integral
    else:
        print(f'Warning: Integral for {prompt_var} is zero, cannot normalize.')

    if non_prompt_integral > 0:
        non_prompt_normalized = non_prompt_normalized / non_prompt_integral
    else:
        print(f'Warning: Integral for {non_prompt_var} is zero, cannot normalize.')

    # Calculate ratio, avoiding division by zero
    ratio = np.divide(prompt_normalized, non_prompt_normalized, out=np.zeros_like(prompt_normalized), where=non_prompt_normalized != 0)

    # Create figure with two subplots (main distribution plot and smaller ratio panel)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [3, 1]})

    # Plot combined histograms for prompt and non-prompt on the same graph
    bin_centers = (hist_data[prompt_var]['bins'][:-1] + hist_data[prompt_var]['bins'][1:]) / 2
    ax1.step(bin_centers, prompt_normalized, where='mid', label=f'Prompt {lepton_type}', color='blue')
    ax1.step(bin_centers, non_prompt_normalized, where='mid', label=f'Non-Prompt {lepton_type}', color='red')
    ax1.set_xlabel(args.xlabel)
    ax1.set_ylabel('Normalized Frequency')
    #ax1.set_yscale('log')
    ax1.set_title(f'Distribution of {args.variable} for {lepton_type} (All Q-bins Combined)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot ratio in the smaller panel below
    ax2.step(bin_centers, ratio, where='mid', color='black', label='Prompt/Non-Prompt Ratio')
    ax2.set_xlabel(args.xlabel)
    ax2.set_ylabel('Ratio')
    ax2.set_yscale('log')
    ax2.set_ylim(1e-8, 1e8)
    ax2.axhline(y=1, color='red', linestyle='--',)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Save the plot
    output_path = f'/eos/user/l/lberiet/ttZ_diff_results/BDT/variable_distrib/{args.variable}_{lepton_type}_distribution_and_ratio.png'
    plt.savefig(output_path)
    plt.close()
    print(f'Plot saved as {output_path}')

print('All plots generated.')
