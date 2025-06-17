import os
import json
# Set paths
output_dir = "/eos/user/l/lberiet/ttZ_diff_results/final"
json_file = os.path.join(output_dir, "results.json")

# Define signal and background process names
signal_process = "mgp8_pp_ttz_5f_84TeV_ttzlep"
background_processes = ["mgp8_pp_tttt_5f_84TeV_4tlep", "mgp8_pp_tth_5f_84TeV", "mgp8_pp_ZZjj_HF_5f_84TeV_zzlep"]

# Load results
if not os.path.isfile(json_file):
    print(f"results.json not found in {output_dir}. Please run the final analysis with saveJSON=True.")
    exit(1)

with open(json_file, "r") as f:
    results = json.load(f)

# Get the list of cuts (selection names) from the signal process
cut_names = list(results[signal_process].keys())

print("\n=== S/sqrt(B) for the whole analysis (all_events) ===")
cut = 'all_events'
S = results[signal_process][cut]["n_events"]
B = sum(results[bkg][cut]["n_events"] for bkg in background_processes)
s_over_sqrtb = S / ((B)**0.5) if B > 0 else 0
print(f"{cut}: S = {S:.2f}, B = {B:.2f}, S/sqrt(B) = {s_over_sqrtb:.2f}")

print("\n=== S/sqrt(B) for each selection ===")
for cut in cut_names:
    S = results[signal_process][cut]["n_events"]    # number of signal events passing the cut
    B = sum(results[bkg][cut]["n_events"] for bkg in background_processes) # number of background events passing the cut
    s_over_sqrtb = S / ((B+S)**0.5) if B+S > 0 else 0
    print(f"{cut}: S = {S:.2f}, B = {B:.2f}, S/sqrt(B) = {s_over_sqrtb:.2f}") 
