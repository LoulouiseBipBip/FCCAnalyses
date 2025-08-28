import ROOT
import os 
from collections import namedtuple
from array import array
import copy
import glob
import argparse
import uproot
import numpy as np

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

# Removed import from plot_HT_split_check import get_rdf

PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])

ProcessSpecs = namedtuple('ProcessSpecs', ['name', 'label', 'filepath', 'colour'])

# Command line argument parsing
parser = argparse.ArgumentParser(description='Plot histograms and ratios for prompt and non-prompt leptons from ROOT files.')
parser.add_argument('--variable', type=str, default='pTjet', help='Variable to plot (default: pTjet)')
parser.add_argument('--xlabel', type=str, default='pT_{jet} [GeV]', help='X-axis label for the plots (default: pT_{jet} [GeV])')
parser.add_argument('--logy', action='store_true', default=False, help='Use logarithmic scale for y-axis of top plot (default: linear)')
args = parser.parse_args()

#compare two histograms
def plot_hist_compare(hist_name, plot_specs, hist1_values, hist2_values, process1, process2, out_dir, norm_info="", yaxis_label="Events", 
                      do_ratio=True, file_format="png", do_logy=False, do_norm_unit=False):
    do_logy = args.logy  # Use command-line argument for logarithmic scale

    # Create ROOT histograms
    has_variable_binning = False
    if not isinstance(plot_specs.nbins, int):
        has_variable_binning = True
        hist_binEdges = array("d", plot_specs.nbins)
        hist_nBins = len(plot_specs.nbins)-1
        hist1 = ROOT.TH1D(hist_name + "_1", hist_name + "_1", hist_nBins, hist_binEdges)
        hist2 = ROOT.TH1D(hist_name + "_2", hist_name + "_2", hist_nBins, hist_binEdges)
    else:
        hist1 = ROOT.TH1D(hist_name + "_1", hist_name + "_1", plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)
        hist2 = ROOT.TH1D(hist_name + "_2", hist_name + "_2", plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)

    # Fill histograms with data
    for i in range(len(hist1_values)):
        hist1.SetBinContent(i+1, hist1_values[i])
        hist2.SetBinContent(i+1, hist2_values[i])

    hist1.SetTitle(process1.label)
    hist1.SetLineWidth(2)
    hist1.SetLineColor(process1.colour)
    hist1.GetYaxis().SetTitle(yaxis_label)
    hist1.GetXaxis().SetTitle(plot_specs.label)
    hist1.Sumw2()

    hist2.SetTitle(process2.label)
    hist2.SetLineWidth(2)
    hist2.SetLineColor(process2.colour)
    hist2.GetYaxis().SetTitle(yaxis_label)
    hist2.GetXaxis().SetTitle(plot_specs.label)
    hist2.Sumw2()

    if norm_info:
        sow1 = sum(hist1_values) if hist1_values else 1.0
        sow2 = sum(hist2_values) if hist2_values else 1.0
        hist_name+="_normed"
        hist1.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/sow1 if sow1 > 0 else 1.0)
        hist2.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/sow2 if sow2 > 0 else 1.0)

    elif do_norm_unit:
        hist1.Scale(1./hist1.Integral() if hist1.Integral() > 0 else 1.0)
        hist2.Scale(1./hist2.Integral() if hist2.Integral() > 0 else 1.0)
        hist_name+="_unitNormed"

    #set output file name
    if do_ratio:
        hist_ratio = hist1.Clone()
        hist_ratio.Divide(hist2)
        hist1.GetXaxis().SetLabelSize(0)
        hist1.GetXaxis().SetTitle("")
        hist2.GetXaxis().SetLabelSize(0)
        hist2.GetXaxis().SetTitle("")
        hist_name+="_ratio"
        
    if do_logy:
        hist_name+="_logY"

    histfile_name = "{}.{}".format(hist_name, file_format)
    histfile_path = os.path.join(out_dir, histfile_name)

    #setup canvas
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
    canvas.SetLogy(do_logy)
    canvas.cd()

    canvas.SetLeftMargin(0.16)

    if do_ratio:
        pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
        pad_up.SetFillStyle(0)
        pad_up.SetBottomMargin(0.32)
        pad_up.SetTopMargin(0.03)
        pad_up.SetLeftMargin(0.13)
        pad_up.SetRightMargin(0.05)
        pad_up.SetLogy(do_logy)
        pad_up.Draw()

        pad_low = ROOT.TPad("pad_low", "pad_low", 0., 0., 1., 1.)
        pad_low.SetFillStyle(0)
        pad_low.SetBottomMargin(0.12)
        pad_low.SetTopMargin(0.72)
        pad_low.SetLeftMargin(0.13)
        pad_low.SetRightMargin(0.05)
        pad_low.SetGrid()
        pad_low.Draw()

        pad_up.cd()

    #draw histograms and legend
    hist1.Draw("HIST SAME")
    hist2.Draw("HIST SAME")

    leg = ROOT.TLegend(0.7, 0.77, 0.85, 0.95)  # Moved legend more to the left
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetMargin(0.1)
    leg.SetTextFont(43)
    leg.SetTextSize(20)
    leg.SetColumnSeparation(-0.05)
    if norm_info:
        leg.SetHeader("{} fb^{{-1}}".format(norm_info.lumi))
    leg.AddEntry(hist1, hist1.GetTitle(), "l")
    leg.AddEntry(hist2, hist2.GetTitle(), "l")
    leg.Draw()

    if do_ratio:
        pad_low.cd()
        hist_ratio.GetYaxis().SetTitle("Ratio")
        hist_ratio.GetYaxis().SetTitleOffset(1.95)
        hist_ratio.GetYaxis().SetNdivisions(1)  # Reduce number of divisions to show only min and max
        pad_low.SetLogy(True)  # Set logarithmic scale for ratio plot
        hist_ratio.SetMinimum(1e-8)  # Set reasonable range for log scale
        hist_ratio.SetMaximum(1e8)

        # Custom y-axis tick values for ratio plot (log scale)
        # You can modify this list to choose specific values to display on y-axis
        custom_ticks = [1e-8, 1e-4, 1e0, 1e4, 1e8]  # Example: show 10^-8, 10^-4, 1, 10^4, 10^8
        hist_ratio.GetYaxis().SetMoreLogLabels(False)  # Optional: cleaner log labels if needed
        hist_ratio.GetYaxis().SetLabelSize(0.04)
        # Workaround for ROOT log scale ticks: ROOT doesn't support direct custom ticks on log scale
        # Instead, we can try to influence the tick positions by setting the range and using SetNdivisions
        # For more control, consider switching to matplotlib if ROOT doesn't meet requirements
        # As a basic workaround, adjust Ndivisions based on number of custom ticks (not perfect)
        ## Note: For precise control, ROOT may not be ideal; this is a best-effort approach

        pad_low.cd()
        pad_low.Update()
        hist_ratio.Draw("E0P")
        line = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1, hist_ratio.GetXaxis().GetXmax(), 1)
        line.SetLineColor(ROOT.kBlack)  # Darker line
        line.SetLineWidth(1)  # Thicker line for visibility
        line.Draw()
        pad_low.RedrawAxis()

        canvas.RedrawAxis()
        canvas.Modified()
        canvas.Update()    

    canvas.SaveAs(histfile_path)

def plot_lepton_variables(input_dir_pattern, output_dir):
    print("Plotting variables for prompt and non-prompt leptons")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

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

    # Input ROOT files for different Q-binned datasets
    file_list = glob.glob(input_dir_pattern)
    print(f'Found {len(file_list)} ROOT files')

    # Store histogram data for each variable
    hist_data = {var_name: {'hist': None, 'bins': None} for var_name in variables}

    # Loop through each file to extract histogram data for all variables
    for file_path in file_list:
        print(f'Processing {file_path}')
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

        # Define plot specs based on the variable (adjusting ranges as needed)
        bins = hist_data[prompt_var]['bins']
        if len(bins) > 2:
            xmin = bins[0]
            xmax = bins[-1]
            nbins = len(bins) - 1
        else:
            xmin = 0.
            xmax = 100.
            nbins = 50

        plot_specs = PlotSpecs(name=args.variable, xmin=xmin, xmax=xmax, label=args.xlabel, nbins=nbins)
        processes = {
            "Prompt": ProcessSpecs(name=prompt_var, label=f"Prompt {lepton_type}", filepath="", colour=ROOT.kBlue),
            "NonPrompt": ProcessSpecs(name=non_prompt_var, label=f"Non-Prompt {lepton_type}", filepath="", colour=ROOT.kRed),
        }

        plot_hist_compare(f"lepton_{args.variable}_{lepton_type}", plot_specs, hist_data[prompt_var]['hist'], hist_data[non_prompt_var]['hist'], 
                          processes["Prompt"], processes["NonPrompt"], output_dir, norm_info="", yaxis_label="Normalized Frequency",
                          do_ratio=True, file_format="png", do_logy=False, do_norm_unit=True)
        print(f'Plot generated for {lepton_type}')

if __name__ == "__main__":
    plot_lepton_variables("/eos/user/l/lberiet/ttZ_diff_results/BDT/final/mgp8_pp_ttz_5f_Q_*_84TeV_ttzlep_all_events_histo.root", "/eos/user/l/lberiet/ttZ_diff_results/BDT/variable_distrib/")



	