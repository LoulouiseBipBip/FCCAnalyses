import ROOT
import array
import pandas as pd
import numpy as np

# Read the CSV files for 3l and 4l channels
df_3l = pd.read_csv("/eos/user/l/lberiet/Histmaker/ttZ_differential/new3l/plots/Z_ll_pt_stack_uncertainties.csv")
df_4l = pd.read_csv("/eos/user/l/lberiet/ttZ_diff_results/new_iso_noORL/plot_iso_hadrons/Z_ll_pt_stack_uncertainties.csv")

# Extract the relevant columns for electron, muon, and b-jet systematic uncertainties
# Assuming the columns are named 'rel_syst_electron id', 'rel_syst_muon id', and 'rel_syst_bjet id'
electron_3l = df_3l['rel_syst_electron id']
muon_3l = df_3l['rel_syst_muon id']
bjet_3l = df_3l['rel_syst_bjet id']
electron_4l = df_4l['rel_syst_electron id']
muon_4l = df_4l['rel_syst_muon id']
bjet_4l = df_4l['rel_syst_bjet id']
lumi_3l = df_3l['rel_syst_luminosity']
lumi_4l = df_4l['rel_syst_luminosity']
syst_tot_3l = df_3l['rel_syst_tot']
syst_tot_4l = df_4l['rel_syst_tot']
stat_3l = df_3l['rel_stat']
stat_4l = df_4l['rel_stat']

# Extract the number of signal events for each bin
nsig_3l= df_3l['nsig'].astype(float)
nsig_4l = df_4l['nsig'].astype(float)

# Multiply uncertainties by the number of events for each bin
electron_3l_weighted = electron_3l * nsig_3l
muon_3l_weighted = muon_3l * nsig_3l
bjet_3l_weighted = bjet_3l * nsig_3l
electron_4l_weighted = electron_4l * nsig_4l
muon_4l_weighted = muon_4l * nsig_4l
bjet_4l_weighted = bjet_4l * nsig_4l

# Compute the total number of signal events for normalization
total_nsig_3l = nsig_3l.sum()
total_nsig_4l = nsig_4l.sum()
total_nsig = total_nsig_3l + total_nsig_4l

# Iterate over all lines to compute per-bin combined uncertainties
combined_data = []
min_length = min(len(df_3l), len(df_4l))
print(f"Number of bins in 3l: {len(df_3l)}, in 4l: {len(df_4l)}, using minimum: {min_length}")
for i in range(min_length):
    bin_min = df_3l['bin_min'][i]
    bin_max = df_3l['bin_max'][i]
    nsig_3l_bin = nsig_3l[i] if i < len(nsig_3l) else 0.0
    nsig_4l_bin = nsig_4l[i] if i < len(nsig_4l) else 0.0
    total_nsig_bin = nsig_3l_bin + nsig_4l_bin

    lumi_unc_3l_bin = lumi_3l[i] if i < len(lumi_3l) else 0.0
    lumi_unc_4l_bin = lumi_4l[i] if i < len(lumi_4l) else 0.0
    stat_unc_3l_bin = stat_3l[i] if i < len(stat_3l) else 0.0
    stat_unc_4l_bin = stat_4l[i] if i < len(stat_4l) else 0.0

    syst_tot_3l_bin = syst_tot_3l[i] if i < len(syst_tot_3l) else 0.0
    syst_tot_4l_bin = syst_tot_4l[i] if i < len(syst_tot_4l) else 0.0

    electron_unc_3l_bin = electron_3l_weighted[i] if i < len(electron_3l_weighted) else 0.0
    electron_unc_4l_bin = electron_4l_weighted[i] if i < len(electron_4l_weighted) else 0.0
    muon_unc_3l_bin = muon_3l_weighted[i] if i < len(muon_3l_weighted) else 0.0
    muon_unc_4l_bin = muon_4l_weighted[i] if i < len(muon_4l_weighted) else 0.0
    bjet_unc_3l_bin = bjet_3l_weighted[i] if i < len(bjet_3l_weighted) else 0.0
    bjet_unc_4l_bin = bjet_4l_weighted[i] if i < len(bjet_4l_weighted) else 0.0
    
    electron_combined_unc_bin = np.sqrt((electron_unc_3l_bin**2 + electron_unc_4l_bin**2 + 2*electron_unc_3l_bin*electron_unc_4l_bin)) / total_nsig_bin if total_nsig_bin > 0 else 0.0
    muon_combined_unc_bin = np.sqrt((muon_unc_3l_bin**2 + muon_unc_4l_bin**2 + 2*muon_unc_3l_bin*muon_unc_4l_bin)) / total_nsig_bin if total_nsig_bin > 0 else 0.0
    bjet_combined_unc_bin = np.sqrt((bjet_unc_3l_bin**2 + bjet_unc_4l_bin**2 + 2*bjet_unc_3l_bin*bjet_unc_4l_bin)) / total_nsig_bin if total_nsig_bin > 0 else 0.0

    lumi_combined_unc_bin = np.sqrt((lumi_unc_3l_bin**2 + lumi_unc_4l_bin**2 + 2*lumi_unc_3l_bin*lumi_unc_4l_bin)) if total_nsig_bin > 0 else 0.0
    stat_combined_unc_bin = np.sqrt((stat_unc_3l_bin**2 + stat_unc_4l_bin**2)) if total_nsig_bin > 0 else 0.0
    syst_tot_combined_unc_bin = np.sqrt((syst_tot_3l_bin**2 + syst_tot_4l_bin**2)) if total_nsig_bin > 0 else 0.0
    rel_unc_total_bin = np.sqrt((electron_combined_unc_bin**2 + muon_combined_unc_bin**2 + bjet_combined_unc_bin**2 + lumi_combined_unc_bin**2 + stat_combined_unc_bin**2)) if total_nsig_bin > 0 else 0.0
    # Calculate total background events for the bin by summing all background category columns
    nbkg_3l_bin = sum(df_3l[col][i] for col in df_3l.columns if col not in ['bin_min', 'bin_max', 'nsig', 'rel_syst_electron id', 'rel_syst_muon id', 'rel_syst_bjet id', 'rel_syst_luminosity', 'rel_syst_tot', 'rel_stat'] and i < len(df_3l)) if i < len(df_3l) else 0.0
    nbkg_4l_bin = sum(df_4l[col][i] for col in df_4l.columns if col not in ['bin_min', 'bin_max', 'nsig', 'rel_syst_electron id', 'rel_syst_muon id', 'rel_syst_bjet id', 'rel_syst_luminosity', 'rel_syst_tot', 'rel_stat'] and i < len(df_4l)) if i < len(df_4l) else 0.0
    total_nbkg_bin = nbkg_3l_bin + nbkg_4l_bin
    
    combined_data.append({
        'bin_min': bin_min,
        'bin_max': bin_max,
        'nsig_combined': total_nsig_bin,
        'nbkg_combined': total_nbkg_bin,
        'electron_combined_unc': electron_combined_unc_bin,
        'muon_combined_unc': muon_combined_unc_bin,
        'bjet_combined_unc': bjet_combined_unc_bin,
        'lumi_combined_unc': lumi_combined_unc_bin,
        'stat_combined_unc': stat_combined_unc_bin,
        'syst_tot_combined_unc': syst_tot_combined_unc_bin,
        'rel_unc_total': rel_unc_total_bin
    })

# Create DataFrame for per-bin results
results_per_bin = pd.DataFrame(combined_data)

# Compute overall combined uncertainties
electron_combined_weighted = electron_3l_weighted.sum() + electron_4l_weighted.sum()
muon_combined_weighted = muon_3l_weighted.sum() + muon_4l_weighted.sum()
bjet_combined_weighted = bjet_3l_weighted.sum() + bjet_4l_weighted.sum()
electron_combined_unc = electron_combined_weighted / total_nsig
muon_combined_unc = muon_combined_weighted / total_nsig
bjet_combined_unc = bjet_combined_weighted / total_nsig

# Print overall results
print(f"Overall Combined Electron Systematic Uncertainty (correlated, normalized): {electron_combined_unc:.3f}")
print(f"Overall Combined Muon Systematic Uncertainty (correlated, normalized): {muon_combined_unc:.3f}")
print(f"Overall Combined B-jet Systematic Uncertainty (correlated, normalized): {bjet_combined_unc:.3f}")

# Print per-bin results
print("\nPer-bin Combined Uncertainties:")
print(results_per_bin.to_string(index=False))

# Save per-bin results
results_per_bin.to_csv('/eos/user/l/lberiet/www/Histograms_Syst/ttZ/combined/combined_uncertainties_per_bin.csv', index=False)
# Save overall results
overall_results = pd.DataFrame({
    'Uncertainty_Type': ['Electron_ID', 'Muon_ID', 'Bjet_ID'],
    'Combined_Uncertainty': [electron_combined_unc, muon_combined_unc, bjet_combined_unc]
})
overall_results.to_csv('/eos/user/l/lberiet/www/Histograms_Syst/ttZ/combined/combined_uncertainties_overall.csv', index=False)

print("Per-bin results saved to '/eos/user/l/lberiet/www/Histograms_Syst/ttZ/combined/combined_uncertainties_per_bin.csv'")
print("Overall results saved to '/eos/user/l/lberiet/www/Histograms_Syst/ttZ/combined/combined_uncertainties_overall.csv'")
