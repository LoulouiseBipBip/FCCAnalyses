import ROOT
import os
import glob
import array

# Set ROOT to batch mode to avoid pop-up windows
ROOT.gROOT.SetBatch(True)

# Define the base directories
input_dir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/test_hist"
output_dir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/efficiency_plots"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define Q bins for ttz processes
q_bins = ['0_1000', '1000_3000', '3000_10000', '10000_84000']
process_base = "mgp8_pp_ttz_5f_Q_{}_84TeV_ttzlep"

# Define Z pT binning (consistent with histmaker.py)
bins_zpt = array.array('d', [0, 100, 200, 300, 400, 500, 600, 700, 800, 950, 1150, 1350, 1800, 2500])
n_zpt_bins = len(bins_zpt) - 1

# Initialize histograms to store summed Z_ll_pt distributions
h_zpt_all = None  # Denominator (Z_ll_pt_pre)
h_zpt_cut = [None] * 5  # Numerators for each cut (will use Z_ll_pt_sel with weights)

# Selection labels (from histmaker.py)
selection_labels = [
    "All events",
    "N_{lep} == 4",
    "1 or 2 b-jets",
    "80 < Z_{ll}_mass < 100",
    "Second pair is OF"
]

# Iterate over Q bins to sum histograms
for q_bin in q_bins:
    file_path = os.path.join(input_dir, f"{process_base.format(q_bin)}.root")
    
    # Open ROOT file
    f = ROOT.TFile.Open(file_path)
    if not f or f.IsZombie():
        print(f"Could not open file: {file_path}")
        continue
    
    # Get Z_ll_pt_pre (denominator, before cuts)
    h_pre = f.Get("Z_ll_pt_pre")
    if not h_pre:
        print(f"Could not find histogram 'Z_ll_pt_pre' in {file_path}")
        f.Close()
        continue
    h_pre = h_pre.Clone()
    h_pre.SetDirectory(0)
    
    # Get Z_ll_pt_sel (numerator, after cuts)
    h_sel = f.Get("Z_ll_pt_sel")
    if not h_sel:
        print(f"Could not find histogram 'Z_ll_pt_sel' in {file_path}")
        f.Close()
        continue
    h_sel = h_sel.Clone()
    h_sel.SetDirectory(0)
    
    # Get cutFlow histogram
    h_cutflow = f.Get("cutFlow")
    if not h_cutflow:
        print(f"Could not find histogram 'cutFlow' in {file_path}")
        f.Close()
        continue
    h_cutflow = h_cutflow.Clone()
    h_cutflow.SetDirectory(0)
    
    # Initialize or add to summed histograms
    if h_zpt_all is None:
        h_zpt_all = h_pre.Clone("h_zpt_all")
        h_zpt_all.SetDirectory(0)
    else:
        h_zpt_all.Add(h_pre)
    
    # For each cut, scale Z_ll_pt_sel by the fraction of events passing the cut
    for i in range(5):  # 5 cuts including "All events"
        cut_eff = h_cutflow.GetBinContent(i + 1) / h_cutflow.GetBinContent(1) if h_cutflow.GetBinContent(1) > 0 else 0
        h_temp = h_sel.Clone(f"h_zpt_cut_{i}_{q_bin}")
        h_temp.Scale(cut_eff)
        if h_zpt_cut[i] is None:
            h_zpt_cut[i] = h_temp.Clone(f"h_zpt_cut_{i}")
            h_zpt_cut[i].SetDirectory(0)
        else:
            h_zpt_cut[i].Add(h_temp)
    
    f.Close()

# Check if histograms were loaded
if h_zpt_all is None or any(h is None for h in h_zpt_cut):
    print("Error: Not all required histograms were loaded.")
    exit(1)

# Compute efficiency histograms
eff_hists = []
colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen + 2, ROOT.kMagenta + 3]

for i in range(5):
    h_eff = h_zpt_cut[i].Clone(f"eff_cut_{i}")
    h_eff.Divide(h_zpt_all)
    h_eff.SetTitle("")
    h_eff.SetLineWidth(2)
    h_eff.SetLineColor(colors[i])
    h_eff.SetMinimum(0)
    h_eff.SetMaximum(1.1)
    eff_hists.append(h_eff)
    print(f"Cut {selection_labels[i]} efficiency entries: {h_eff.GetEntries()}")
    print(f"Cut {selection_labels[i]} efficiency integral: {h_eff.Integral()}")

# Plot efficiencies
c = ROOT.TCanvas("c", "Selection Efficiency vs Z pT", 800, 600)
eff_hists[0].SetTitle("Selection Efficiency vs Z pT;Z pT [GeV];Efficiency")
eff_hists[0].Draw("HIST")

for h_eff in eff_hists[1:]:
    h_eff.Draw("HIST SAME")

# Add legend
legend = ROOT.TLegend(0.55, 0.70, 0.88, 0.90)
for i, h_eff in enumerate(eff_hists):
    legend.AddEntry(h_eff, selection_labels[i], "l")
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.Draw()

# Save the plot
outname = os.path.join(output_dir, "efficiency_vs_ZpT.png")
c.SaveAs(outname)
print(f"Saved efficiency plot as {outname}")

# Keep canvas open until user input (optional in batch mode)
# input("Press Enter to exit...")