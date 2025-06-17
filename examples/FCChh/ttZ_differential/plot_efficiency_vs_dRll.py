import ROOT
import os

# Define the variable to plot efficiency against
variable = "dR_ll"  # Change to "dR_ll" or any other variable as needed

# Define the base directory and file names
output_dir = "/eos/user/l/lberiet/ttZ_diff_results/efficiencies/"
process = "/eos/user/l/lberiet/ttZ_diff_results/finals2/mgp8_pp_ttz_5f_84TeV_ttzlep"

all_file = os.path.join(output_dir, f"{process}_all_events_histo.root")
sel1_file = os.path.join(output_dir, f"{process}_sel1_lep_histo.root")
sel2_file = os.path.join(output_dir, f"{process}_sel2_bjets_histo.root")
sel3_file = os.path.join(output_dir, f"{process}_sel3_mll_histo.root")
sel4_file = os.path.join(output_dir, f"{process}_sel4_second_pair_histo.root")

# Open files
f_all = ROOT.TFile.Open(all_file)
f_sel1 = ROOT.TFile.Open(sel1_file)
f_sel2 = ROOT.TFile.Open(sel2_file)
f_sel3 = ROOT.TFile.Open(sel3_file)
f_sel4 = ROOT.TFile.Open(sel4_file)
if not f_all or f_all.IsZombie():
    print(f"Could not open file: {all_file}")
    exit(1)
if not f_sel1 or f_sel1.IsZombie():
    print(f"Could not open file: {sel1_file}")
    exit(1)
if not f_sel2 or f_sel2.IsZombie():
    print(f"Could not open file: {sel2_file}")
    exit(1)
if not f_sel3 or f_sel3.IsZombie():
    print(f"Could not open file: {sel3_file}")
    exit(1)
if not f_sel4 or f_sel4.IsZombie():
    print(f"Could not open file: {sel4_file}")
    exit(1)

# Get histograms
h_all = f_all.Get(variable)
h_sel1 = f_sel1.Get(variable)
h_sel2 = f_sel2.Get(variable)
h_sel3 = f_sel3.Get(variable)
h_sel4 = f_sel4.Get(variable)
if not h_all or not h_sel1 or not h_sel2 or not h_sel3 or not h_sel4:
    print("Could not find required histograms in the files.")
    exit(1)

# Debug: Check histogram entries
print(f"h_all entries: {h_all.GetEntries()}")
print(f"h_sel1 entries: {h_sel1.GetEntries()}")
print(f"h_sel2 entries: {h_sel2.GetEntries()}")
print(f"h_sel3 entries: {h_sel3.GetEntries()}")
print(f"h_sel4 entries: {h_sel4.GetEntries()}")

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
eff1 = get_efficiency_hist(h_all, h_sel1, "eff_sel1_lep", ROOT.kBlue)
eff2 = get_efficiency_hist(h_all, h_sel2, "eff_sel2_bjets", ROOT.kRed)
eff3 = get_efficiency_hist(h_all, h_sel3, "eff_sel3_mll", ROOT.kGreen + 2)
eff4 = get_efficiency_hist(h_all, h_sel4, "eff_sel4_second_pair", ROOT.kOrange + 2)

# Plot
c = ROOT.TCanvas("c", f"Efficiency vs {variable}", 800, 600)
eff1.SetTitle(f"Selection Efficiency vs {variable};{variable};Efficiency")
eff1.GetYaxis().SetRangeUser(0, 0.2)
eff1.Draw("HIST")
eff2.Draw("HIST SAME")
eff3.Draw("HIST SAME")
eff4.Draw("HIST SAME")

legend = ROOT.TLegend(0.55, 0.70, 0.88, 0.90)
legend.AddEntry(eff1, "sel1_lep", "l")
legend.AddEntry(eff2, "sel2_bjets", "l")
legend.AddEntry(eff3, "sel3_mll", "l")
legend.AddEntry(eff4, "sel4_second_pair", "l")
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.Draw()

outname = os.path.join(output_dir, f"efficiency_vs_{variable}_superposed.png")
c.SaveAs(outname)
print(f"Saved efficiency plot as {outname}")

# Keep canvas open until user input
input("Press Enter to exit...")