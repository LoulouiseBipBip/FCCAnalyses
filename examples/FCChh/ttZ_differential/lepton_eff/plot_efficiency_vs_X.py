import ROOT
import os
import glob

# Set ROOT to batch mode to avoid pop-up windows
ROOT.gROOT.SetBatch(True)

# Define the variable to plot efficiency against
variable = "Z_ll_pt"

# Define the base directories
input_dir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/final"
output_dir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/kine_plots"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Find all Q bin files
process_base = "mgp8_pp_ttz_5f_84TeV_ttzlep"
all_files = glob.glob(os.path.join(input_dir, f"{process_base}_all_events_histo.root"))
q_bins = ['']

# Initialize histograms to store sums
h_all = None
#h_sel0_sf_ss = None
h_sel1 = None
h_sel2 = None
h_sel3 = None
h_sel4 = None

# Iterate over Q bins
for q_bin in q_bins:
    # Construct file paths for this Q bin
    all_file = os.path.join(input_dir, f"mgp8_pp_ttz_5f_84TeV_ttzlep_all_events_histo.root")
    #sel0_sf_ss_file = os.path.join(input_dir, f"mgp8_pp_tttt_wmlep_Q_{q_bin}_5f_84TeV_sel0_sf_ss_histo.root")
    sel1_file = os.path.join(input_dir, f"mgp8_pp_ttz_5f_84TeV_ttzlep_lep_pT_eta_cut_histo.root")
    
   

    # Open files
    files = [
        (all_file, "all"),
        #(sel0_sf_ss_file, "sel0_sf_ss"),
        (sel1_file, "sel1_lep_pT_eta_cut"),
        #(sel2_file, "sel2_bjets"),
        #(sel3_file, "sel3_jets"),
        #(sel4_file, "sel4_notZ"),
    ]
    
    for file_path, label in files:
        f = ROOT.TFile.Open(file_path)
        if not f or f.IsZombie():
            print(f"Could not open file: {file_path}")
            continue
        
        h = f.Get(variable)
        if not h:
            print(f"Could not find histogram '{variable}' in {file_path}")
            f.Close()
            continue
        
        # Clone histogram to avoid memory issues
        h = h.Clone()
        h.SetDirectory(0)  # Detach from file
        
        # Initialize or add to summed histograms
        if label == "all":
            if h_all is None:
                h_all = h.Clone("h_all")
                h_all.SetDirectory(0)
            else:
                h_all.Add(h)
        #elif label == "sel0_sf_ss":
        #    if h_sel0_sf_ss is None:
        #        h_sel0_sf_ss = h.Clone("h_sel0_sf_ss")
        #        h_sel0_sf_ss.SetDirectory(0)
        #    else:
        #        h_sel0_sf_ss.Add(h)
        elif label == "sel1_lep_pT_eta_cut":
            if h_sel1 is None:
                h_sel1 = h.Clone("h_sel1")
                h_sel1.SetDirectory(0)
            else:
                h_sel1.Add(h)
        # elif label == "sel2_bjets":
        #     if h_sel2 is None:
        #         h_sel2 = h.Clone("h_sel2")
        #         h_sel2.SetDirectory(0)
        #     else:
        #         h_sel2.Add(h)
        # elif label == "sel3_jets":
        #     if h_sel3 is None:
        #         h_sel3 = h.Clone("h_sel3")
        #         h_sel3.SetDirectory(0)
        #     else:
        #         h_sel3.Add(h)
        # elif label == "sel4_notZ":
        #     if h_sel4 is None:
        #         h_sel4 = h.Clone("h_sel4")
        #         h_sel4.SetDirectory(0)
        #     else:
        #         h_sel4.Add(h)
        
        f.Close()

# Check if all histograms were loaded
if not all([h_all, h_sel1]):
    print("Error: Not all required histograms were loaded.")
    exit(1)

# Debug: Check histogram entries
print(f"h_all entries: {h_all.GetEntries()}")
#print(f"h_sel0_sf_ss entries: {h_sel0_sf_ss.GetEntries()}")
print(f"h_sel1 entries: {h_sel1.GetEntries()}")
#print(f"h_sel2 entries: {h_sel2.GetEntries()}")
#print(f"h_sel3 entries: {h_sel3.GetEntries()}")
#print(f"h_sel4 entries: {h_sel4.GetEntries()}")

def get_efficiency_hist(h_all, h_sel, name, color):
    h_eff = h_sel.Clone(name)
    h_eff.SetTitle("")
    h_eff.Divide(h_all)
    h_eff.SetMinimum(0)
    h_eff.SetMaximum(1.1)
    h_eff.SetLineWidth(2)
    h_eff.SetLineColor(color)
    print(f"{name} entries after division: {h_eff.GetEntries()}")
    print(f"{name} integral: {h_eff.Integral()}")
    return h_eff

# Compute efficiency histograms
#eff0 = get_efficiency_hist(h_all, h_sel0_sf_ss, "eff_sel0_sf_ss", ROOT.kBlue)
eff1 = get_efficiency_hist(h_all, h_sel1, "eff_sel1_lep_eta_pt", ROOT.kMagenta + 3)
#eff2 = get_efficiency_hist(h_all, h_sel2, "eff_sel2_bjets", ROOT.kRed)
#eff3 = get_efficiency_hist(h_all, h_sel3, "eff_sel3_jets", ROOT.kGreen + 2)
#eff4 = get_efficiency_hist(h_all, h_sel4, "eff_sel4_notZ", ROOT.kOrange + 2)

# Plot
c = ROOT.TCanvas("c", f"Efficiency vs {variable}", 800, 600)
#eff0.SetTitle(f"Selection Efficiency vs {variable};{variable} [GeV];Efficiency")
# eff0.GetYaxis().SetRangeUser(0, 0.05)
#eff0.Draw("HIST")
eff1.SetTitle(f"Selection Efficiency vs {variable};{variable} [GeV];Efficiency")
eff1.GetXaxis().SetRangeUser(0, 2300)
eff1.GetYaxis().SetRangeUser(0, 1.4)

eff1.Draw("HIST")
#eff2.Draw("HIST SAME")
#eff3.Draw("HIST SAME")
#eff4.Draw("HIST SAME")

# Add legend
legend = ROOT.TLegend(0.55, 0.70, 0.88, 0.90)
#legend.AddEntry(eff0, "sel0_leptons", "l")
legend.AddEntry(eff1, "pT>30 GeV, |#eta|<4", "l")
# legend.AddEntry(eff2, "sel2_bjets", "l")
# legend.AddEntry(eff3, "sel3_jets", "l")
# legend.AddEntry(eff4, "sel4_notZ", "l")
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.Draw()

# Save the plot
outname = os.path.join(output_dir, f"efficiency_vs_{variable}_superposed.png")
c.SaveAs(outname)
print(f"Saved efficiency plot as {outname}")

# Keep canvas open until user input (optional in batch mode)
input("Press Enter to exit...")