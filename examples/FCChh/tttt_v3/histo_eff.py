
import ROOT
import os
import glob
import argparse

# Set ROOT to batch mode
ROOT.gROOT.SetBatch(True)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Plot 2D efficiency histogram for a given process and selection")
    parser.add_argument("--process", default="3l", help="Process name (e.g., 3l, ttZ)")
    parser.add_argument("--selection", default="sel0_sf_ss", 
                       choices=["sel0_sf_ss", "sel1_sf_ss", "sel2_bjets", "sel3_jets", "sel4_notZ"],
                       help="Selection to plot efficiency for")
    args = parser.parse_args()

    # Define directories
    input_dir = f"/eos/user/l/lberiet/newttttresult/{args.process}/sf_ss=3_sel/histo/"
    output_dir = f"/eos/user/l/lberiet/www/4t_analysis/{args.process}/SF_SS_pair_OF_single=3"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define histogram settings
    variable = "HT"
    ht_bins = 100
    ht_min = 0
    ht_max = 5000  # Adjust based on your HT range
    eff_bins = 50
    eff_min = 0
    eff_max = 1.1

    # Find all Q bin files
    process_base = "mgp8_pp_tttt_wmlep_Q_*_5f_84TeV" if args.process == "3l" else f"mgp8_pp_{args.process}_5f_84TeV_{args.process}"
    all_files = glob.glob(os.path.join(input_dir, f"{process_base}_all_events_histo.root"))
    if not all_files:
        print(f"No files found for process {args.process} in {input_dir}")
        exit(1)
    
    q_bins = [os.path.basename(f).split("Q_")[1].split("_5f_84TeV")[0] for f in all_files if "Q_" in f] or [""]

    # Initialize histograms
    h_all = None
    h_sel = None

    # Iterate over Q bins
    for q_bin in q_bins:
        # Construct file paths
        all_file = os.path.join(input_dir, f"{process_base}_all_events_histo.root".replace("Q_*", f"Q_{q_bin}" if q_bin else ""))
        sel_file = os.path.join(input_dir, f"{process_base}_{args.selection}_histo.root".replace("Q_*", f"Q_{q_bin}" if q_bin else ""))

        # Open files
        f_all = ROOT.TFile.Open(all_file)
        if not f_all or f_all.IsZombie():
            print(f"Could not open file: {all_file}")
            continue

        f_sel = ROOT.TFile.Open(sel_file)
        if not f_sel or f_sel.IsZombie():
            print(f"Could not open file: {sel_file}")
            f_all.Close()
            continue

        # Get histograms
        h_all_tmp = f_all.Get(variable)
        h_sel_tmp = f_sel.Get(variable)
        if not h_all_tmp or not h_sel_tmp:
            print(f"Could not find histogram '{variable}' in {all_file} or {sel_file}")
            f_all.Close()
            f_sel.Close()
            continue

        # Clone and detach histograms
        h_all_tmp = h_all_tmp.Clone()
        h_all_tmp.SetDirectory(0)
        h_sel_tmp = h_sel_tmp.Clone()
        h_sel_tmp.SetDirectory(0)

        # Initialize or add to summed histograms
        if h_all is None:
            h_all = h_all_tmp.Clone("h_all")
            h_all.SetDirectory(0)
        else:
            h_all.Add(h_all_tmp)
        
        if h_sel is None:
            h_sel = h_sel_tmp.Clone(f"h_{args.selection}")
            h_sel.SetDirectory(0)
        else:
            h_sel.Add(h_sel_tmp)

        f_all.Close()
        f_sel.Close()

    # Check if histograms were loaded
    if not h_all or not h_sel:
        print("Error: Could not load required histograms.")
        exit(1)

    # Debug: Check histogram entries
    print(f"h_all entries: {h_all.GetEntries()}")
    print(f"h_{args.selection} entries: {h_sel.GetEntries()}")

    # Create 2D histogram
    h_2d = ROOT.TH2F(f"eff_{args.selection}_vs_{variable}", 
                     f"Efficiency vs {variable} ({args.selection});{variable} [GeV];Efficiency;Events",
                     ht_bins, ht_min, ht_max, eff_bins, eff_min, eff_max)

    # Fill 2D histogram
    for i in range(1, h_all.GetNbinsX() + 1):
        n_all = h_all.GetBinContent(i)
        n_sel = h_sel.GetBinContent(i)
        if n_all > 0:  # Avoid division by zero
            efficiency = n_sel / n_all
            h_2d.Fill(h_all.GetBinCenter(i), efficiency, n_sel)

    # Set up canvas and style
    c = ROOT.TCanvas("c", f"Efficiency vs {variable}", 800, 600)
    
    # Set color palette
    ROOT.gStyle.SetPalette(ROOT.kRainBow)
    ROOT.gStyle.SetNumberContours(50)

    # Draw 2D histogram
    h_2d.SetStats(0)
    h_2d.Draw("COLZ")

    # Add color bar
    ROOT.gPad.Update()
    palette = h_2d.GetListOfFunctions().FindObject("palette")
    if palette:
        palette.SetX1NDC(0.92)
        palette.SetX2NDC(0.94)
        palette.SetY1NDC(0.1)
        palette.SetY2NDC(0.9)

    # Save the plot
    outname = os.path.join(output_dir, f"efficiency_2d_{args.selection}_vs_{variable}_{args.process}.png")
    c.SaveAs(outname)
    print(f"Saved 2D efficiency plot as {outname}")

    # Keep canvas open (optional in batch mode)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
