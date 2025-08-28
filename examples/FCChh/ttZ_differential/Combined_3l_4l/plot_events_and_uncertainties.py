import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV files for 3l and 4l channels
df_3l = pd.read_csv('/eos/user/l/lberiet/Histmaker/ttZ_differential/new3l/plots/Z_ll_pt_stack_uncertainties.csv')
df_4l = pd.read_csv('/eos/user/l/lberiet/ttZ_diff_results/new_iso_noORL/plot_iso_hadrons/Z_ll_pt_stack_uncertainties.csv')

# Read the combined uncertainties per bin
df_combined_unc = pd.read_csv('/eos/user/l/lberiet/www/Histograms_Syst/ttZ/combined/combined_uncertainties_per_bin.csv')

# Compute total events per bin for ttZ (combined 3l + 4l)
total_events_combined = (df_combined_unc['nsig_combined'].astype(float) / 100).tolist()
print(total_events_combined)
# Ensure the signal data covers all bins defined in the combined uncertainties file
min_length = len(df_combined_unc)
if len(total_events_combined) <= min_length:
    total_events_combined.extend([0.0] * (min_length - len(total_events_combined)))

# Dictionary to customize background names for the legend
bkg_names = {
    'n_tttt': 'tttt',
    'n_ZZjj': 'ZZjj',
    'n_VVV': 'VVV',
    'n_VVVV': 'VVVV',
    'n_ttVV': 'ttVV',
    'n_ttH': 'ttH',
    'n_WZjj': 'WZjj',
    'n_tt': 'tt',
    'n_ttW': 'ttW',
}

# Compute combined total events per bin and separate background contributions
bin_centers = []
bin_widths = []
bkg_contributions_3l = {}
bkg_contributions_4l = {}
bin_edges = [float(df_combined_unc['bin_min'][0])]
for i in range(min_length):
    bin_min = float(df_combined_unc['bin_min'][i])
    bin_max = float(df_combined_unc['bin_max'][i])
    bin_centers.append((bin_min + bin_max) / 2)
    bin_widths.append(bin_max - bin_min)
    bin_edges.append(bin_max)
    for bkg_col in df_3l.columns:
        if bkg_col.startswith('n_'):
            bkg_name = bkg_names.get(bkg_col, bkg_col.replace('n_', ''))
            if bkg_name not in bkg_contributions_3l:
                bkg_contributions_3l[bkg_name] = []
                bkg_contributions_4l[bkg_name] = []
            bkg_contributions_3l[bkg_name].append((float(df_3l[bkg_col][i]) / 100) if i < len(df_3l) else 0.0)
            bkg_contributions_4l[bkg_name].append((float(df_4l[bkg_col][i]) / 100) if i < len(df_4l) else 0.0)

# Extract uncertainties from combined uncertainties file
electron_unc = df_combined_unc['electron_combined_unc']
muon_unc = df_combined_unc['muon_combined_unc']
bjet_unc = df_combined_unc['bjet_combined_unc']
lumi_unc = df_combined_unc['lumi_combined_unc']
stat_unc = df_combined_unc['stat_combined_unc']
syst_tot_unc = df_combined_unc['syst_tot_combined_unc']
rel_unc_total = df_combined_unc['rel_unc_total']

# Create subplots: one for total events and one for uncertainties
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

# Plot total events per bin on the top subplot using plt.hist
ax1.hist(bin_edges[:-1], bins=bin_edges, weights=total_events_combined, histtype='step', color='red', linestyle='-', log=True, linewidth=1.5, label='ttZ')

# Plot individual background contributions as stacked bars
colors = ['#d53e4f', '#969696', '#fde090', '#e6f598', '#1a9850', '#3288b3', '#d01c8b', '#d3b6da', '#80cdc1', '#018571', '#666666']
bottom = np.zeros(min_length)
bar_handles = []
bar_labels = []
for idx, (bkg_name, bkg_values_3l) in enumerate(bkg_contributions_3l.items()):
    bkg_values_combined = [bkg_values_3l[i] + bkg_contributions_4l[bkg_name][i] for i in range(min_length)]
    bar = ax1.bar(bin_centers, bkg_values_combined, width=bin_widths, align='center', alpha=0.9, color=colors[idx % len(colors)], log=True, label=f'{bkg_name}', bottom=bottom)
    bar_handles.append(bar[0])
    bar_labels.append(f'{bkg_name}')
    bottom += np.array(bkg_values_combined)

# Add the signal (ttZ) as a step histogram
signal_hist = ax1.hist(bin_edges[:-1], bins=bin_edges, weights=total_events_combined, histtype='step', density=True, color='red', linestyle='-', linewidth=1.5, label='ttZ')
signal_handle = signal_hist[2][0]  # The Line2D object

# Set labels and styling for the top subplot
ax1.set_xlabel('$p_{T}(Z_{ll})$ [GeV]')
ax1.set_ylabel('Events / GeV')
ax1.set_title('Z_ll pT (3l + 4l)')

# Custom 2-column legend: half signal/bkg in each column
# First column: signal + first half of backgrounds, Second column: rest of backgrounds
n_bkg = len(bar_handles)
half_bkg = (n_bkg + 1) // 2  # split backgrounds as evenly as possible

legend_handles = [signal_handle] + bar_handles[:half_bkg] + bar_handles[half_bkg:]
legend_labels = ['ttZ'] + bar_labels[:half_bkg] + bar_labels[half_bkg:]

# Split into two columns: left = signal + first half bkg, right = rest of bkg
col1_handles = [signal_handle] + bar_handles[:half_bkg]
col1_labels = ['ttZ'] + bar_labels[:half_bkg]
col2_handles = bar_handles[half_bkg:]
col2_labels = bar_labels[half_bkg:]

# Interleave for 2-column legend
handles_2col = []
labels_2col = []
max_len = max(len(col1_handles), len(col2_handles))
for i in range(max_len):
    if i < len(col1_handles):
        handles_2col.append(col1_handles[i])
        labels_2col.append(col1_labels[i])
    if i < len(col2_handles):
        handles_2col.append(col2_handles[i])
        labels_2col.append(col2_labels[i])

ax1.legend(handles_2col, labels_2col, ncol=2, loc='upper right', fontsize='medium', columnspacing=1.2, handletextpad=1.2, frameon=True)

#ax1.set_yscale('log')  # Set logarithmic scale for y-axis
ax1.set_ylim(1e-1, 1e6)
ax1.set_xlim(0, max(bin_centers) + bin_widths[-1]/2 if len(bin_widths) > 0 else 2500)
ax1.set_xticks(bin_edges[1:])  # Use upper edges of bins
ax1.set_xticklabels([f'{df_combined_unc["bin_max"][i]:.1f}' for i in range(min_length)], rotation=45, ha='right')

# Plot uncertainties using plt.hist for upper and lower bounds
uncertainties = [
    ('electron id', electron_unc, 'green', '-'),
    ('muon id', muon_unc, 'blue', '-'),
    ('b-jet id', bjet_unc, 'teal', '-'),
    ('lumi', lumi_unc, 'orange', '-'),
    ('stat', stat_unc, 'grey', '-'),
    ('syst', syst_tot_unc, 'brown', '-'),
    ('total', rel_unc_total, 'black', '-'),
]

for label, unc, color, linestyle in uncertainties:
    unc_array = np.abs(unc)  # Ensure positive uncertainties for symmetric bounds
    ax2.hist(bin_edges[:-1], bins=bin_edges, weights=unc_array, histtype='step', color=color, linestyle=linestyle, linewidth=0.8, label=f'{label}')
    ax2.hist(bin_edges[:-1], bins=bin_edges, weights=-unc_array, histtype='step', color=color, linestyle=linestyle, linewidth=0.8)

# Set labels and styling for uncertainties plot
ax2.set_xlabel('$p_{T}(Z_{ll})$ [GeV]', fontsize=12)
ax2.set_ylabel('Uncertainty', fontsize=12)
ax2.grid(True, alpha=0.4)
ax2.set_ylim(-0.4, 0.4)  
ax2.set_xticks(bin_edges[1:])  # Use upper edges of bins
ax2.set_xlim(0, max(bin_centers) + bin_widths[-1]/2 if len(bin_widths) > 0 else 2500)
ax2.set_xticklabels([f'{df_combined_unc["bin_max"][i]:.1f}' for i in range(min_length)], rotation=45, ha='right', fontsize=12)
ax2.tick_params(axis='y', labelsize=12)

# Custom legend: two columns, 3 labels on left, 4 on right
handles, labels = ax2.get_legend_handles_labels()
if len(handles) >= 7:
    ax2.legend(
        handles[:3] + handles[3:7],
        labels[:3] + labels[3:7],
        loc='upper left',
        bbox_to_anchor=(0.05, 1),
        ncol=2,
        columnspacing=1.0,
        handletextpad=0.8,
        frameon=True,
        title=None,
        borderaxespad=0.2,
        labelspacing=0.4,
        handlelength=1.2,
        fontsize='x-small'
    )
else:
    ax2.legend(ncol=2, fontsize='small')

# Adjust layout to prevent overlap and give more space to the uncertainty plot
plt.tight_layout(pad=1.0, rect=[0, 0, 1, 1.3])

# Save the plot
output_path = '/eos/user/l/lberiet/www/Histograms_Syst/ttZ/combined/events_and_uncertainties_plot.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to '{output_path}'")

# Close the plot
plt.close()