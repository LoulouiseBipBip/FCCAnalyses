import ROOT
import csv
import os

base_path1 = "/eos/user/l/lberiet/Histmaker/WZ/mgp8_pp_wz_5f_Q_{qbin}_84TeV_wzlllv"
base_path2 = "/eos/user/l/lberiet/Histmaker/ttW/mgp8_pp_ttw_5f_Q_{qbin}_84TeV_ttwlep"

# qbin
q_bins = ["0_1000", "1000_3000", "3000_10000", "10000_84000"]

# Define output directory for saving plot and CSV file (change this path as needed)
output_dir = "/afs/cern.ch/user/l/lberiet/MatteoCode/FCCAnalyses/examples/FCChh/WZ"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
plot_output_path = os.path.join(output_dir, "ratio_plot.png")
csv_output_path = os.path.join(output_dir, "n_leptons_distribution.csv")

# Lists to store the opened files for each sample and Q-bin
files1 = []
files2 = []

# Data storage for CSV
n_leptons_data = []
n_leptons_data.append(["N Leptons", "WZ Events", "ttW Events"])

# Open the ROOT files for each Q-bin and collect n_leptons histograms
for qbin in q_bins:
    file_path1 = base_path1.format(qbin=qbin) + ".root"
    file_path2 = base_path2.format(qbin=qbin) + ".root"
    
    f1 = ROOT.TFile.Open(file_path1)
    f2 = ROOT.TFile.Open(file_path2)
    
    if f1 and not f1.IsZombie():
        files1.append((qbin, f1))
    else:
        print(f"Warning: Could not open file for sample1, Q-bin {qbin}: {file_path1}")
    
    if f2 and not f2.IsZombie():
        files2.append((qbin, f2))
    else:
        print(f"Warning: Could not open file for sample2, Q-bin {qbin}: {file_path2}")

# Sum histograms over all Q-bins for total n_leptons distribution
h1_total = None
h2_total = None

for qbin, f1 in files1:
    h1_temp = f1.Get("n_leptons_pre")
    if h1_temp:
        if h1_total is None:
            h1_total = h1_temp.Clone("h1_total")
        else:
            h1_total.Add(h1_temp)

for qbin, f2 in files2:
    h2_temp = f2.Get("n_leptons_pre")
    if h2_temp:
        if h2_total is None:
            h2_total = h2_temp.Clone("h2_total")
        else:
            h2_total.Add(h2_temp)

# Extract per-bin content for the total n_leptons distribution
# Update CSV header to include ratio and uncertainty
n_leptons_data = []
n_leptons_data.append(["N Leptons", "WZ Events", "WZ Error", "ttW Events", "ttW Error", "Ratio (WZ/ttW)", "Ratio Error"])

# Extract per-bin content and errors for the total n_leptons distribution
if h1_total and h2_total:
    n_bins = h1_total.GetNbinsX()
    for bin in range(1, n_bins + 1):
        n_leptons = int(h1_total.GetBinLowEdge(bin))
        events1 = h1_total.GetBinContent(bin)
        error1 = h1_total.GetBinError(bin)  # WZ bin error
        events2 = h2_total.GetBinContent(bin)
        error2 = h2_total.GetBinError(bin)  # ttW bin error

        # Calculate ratio and its uncertainty
        ratio = events1 / events2 if events2 > 0 else 0.0
        ratio_error = 0.0
        if events1 > 0 and events2 > 0:
            rel_error1 = error1 / events1  # Relative error for WZ
            rel_error2 = error2 / events2  # Relative error for ttW
            ratio_error = ratio * (rel_error1**2 + rel_error2**2)**0.5  # Propagated error

        n_leptons_data.append([n_leptons, events1, error1, events2, error2, ratio, ratio_error])
else:
    print("Error: Could not create total histograms for n_leptons distribution.")

# Write n_leptons distribution data to CSV file
with open(csv_output_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(n_leptons_data)
print(f"N leptons distribution data saved to {csv_output_path}")

# Check if total histograms exist for ratio plot
if not h1_total or not h2_total:
    print("Error: One or both total histograms 'n_leptons_pre' not found or could not be created.")
else:
    # Normalize the histograms to their integrals before calculating the ratio
    integral1 = h1_total.Integral()
    integral2 = h2_total.Integral()
    
    if integral1 > 0:
        h1_total.Scale(1.0 / integral1)
    else:
        print("Warning: Integral of WZ histogram is zero or negative, cannot normalize.")
    
    if integral2 > 0:
        h2_total.Scale(1.0 / integral2)
    else:
        print("Warning: Integral of ttW histogram is zero or negative, cannot normalize.")
    
    # Create a new histogram for the ratio
    h_ratio = h1_total.Clone("h_ratio")
    
    # Calculate ratio and propagate errors
    for bin in range(1, h_ratio.GetNbinsX() + 1):
        content1 = h1_total.GetBinContent(bin)
        error1 = h1_total.GetBinError(bin)
        content2 = h2_total.GetBinContent(bin)
        error2 = h2_total.GetBinError(bin)
        
        # Set ratio bin content
        ratio = content1 / content2 if content2 > 0 else 0.0
        h_ratio.SetBinContent(bin, ratio)
        
        # Set ratio bin error
        ratio_error = 0.0
        if content1 > 0 and content2 > 0:
            rel_error1 = error1 / content1
            rel_error2 = error2 / content2
            ratio_error = ratio * (rel_error1**2 + rel_error2**2)**0.5
        h_ratio.SetBinError(bin, ratio_error)

   # Set up the canvas for plotting
canvas = ROOT.TCanvas("canvas", "Ratio of n_leptons Histograms", 800, 600)
canvas.SetGrid()
  # Set logarithmic scale for Y-axis

# Create histograms for error bands
h_ratio_upper = h_ratio.Clone("h_ratio_upper")
h_ratio_lower = h_ratio.Clone("h_ratio_lower")

# Set bin contents for upper and lower error bands
for bin in range(1, h_ratio.GetNbinsX() + 1):
    ratio = h_ratio.GetBinContent(bin)
    error = h_ratio.GetBinError(bin)
    h_ratio_upper.SetBinContent(bin, ratio + error)
    h_ratio_lower.SetBinContent(bin, max(0, ratio - error))  # Ensure non-negative for log scale
    # Clear errors in band histograms to avoid drawing error bars
    h_ratio_upper.SetBinError(bin, 0)
    h_ratio_lower.SetBinError(bin, 0)

# Set histogram properties for better visualization
h_ratio.SetTitle("Ratio of n_leptons Distributions (Normalized)")
h_ratio.GetXaxis().SetTitle("Number of Leptons")
h_ratio.GetYaxis().SetTitle("Ratio (WZ/ttW)")
h_ratio.SetLineColor(ROOT.kBlue)
h_ratio.SetLineWidth(2)
h_ratio.SetLineStyle(1)  # Solid line for central histogram
h_ratio.SetMarkerStyle(0)  # Remove markers
h_ratio.SetStats(0)  # Disable stats box

# Set error band histogram properties
h_ratio_upper.SetLineColor(ROOT.kBlue)
h_ratio_upper.SetLineWidth(2)
h_ratio_upper.SetLineStyle(2)  # Dashed line
h_ratio_lower.SetLineColor(ROOT.kBlue)
h_ratio_lower.SetLineWidth(2)
h_ratio_lower.SetLineStyle(2)  # Dashed line

# Set custom X-axis range
xmin = 0
xmax = 5
h_ratio.GetXaxis().SetRangeUser(xmin, xmax)

# Adjust Y-axis range to accommodate error bands
max_y = max(h_ratio_upper.GetMaximum(), h_ratio.GetMaximum()) * 1.2
min_y = min(h_ratio_lower.GetMinimum(), h_ratio.GetMinimum()) * 0.8
if min_y <= 0:  # Ensure minimum is positive for log scale
    min_y = 1e-3
h_ratio.GetYaxis().SetRangeUser(0, 1.6)

# Draw the histograms
h_ratio.Draw("HIST")  # Draw central histogram first
h_ratio_upper.Draw("HIST SAME")  # Draw upper band
h_ratio_lower.Draw("HIST SAME")  # Draw lower band

# Update the canvas
canvas.Update()

# Save the plot to the specified location
canvas.SaveAs(plot_output_path)
print(f"Ratio plot saved to {plot_output_path}")

# Keep the canvas open until user closes it
canvas.WaitPrimitive()