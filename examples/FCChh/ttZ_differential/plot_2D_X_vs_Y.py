import ROOT
import sys

# Usage: python plot_2D_dRll_vs_HT.py <input_root_file> [hist_name]
# Example: python plot_2D_dRll_vs_HT.py /eos/user/l/lberiet/ttZ_diff_results/final/mgp8_pp_ttz_5f_84TeV_ttzlep_sel1_histo.root

def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_2D_dRll_vs_HT.py <input_root_file> [hist_name]")
        sys.exit(1)

    input_file = sys.argv[1]
    hist_name = sys.argv[2] if len(sys.argv) > 2 else "Non_Prompt_Iso_all_elec_vs_D0_sig_non_prompt_electrons"

    f = ROOT.TFile.Open(input_file)
    if not f or f.IsZombie():
        print(f"Could not open file: {input_file}")
        sys.exit(1)

    hist = f.Get(hist_name)
    if not hist:
        print(f"Histogram '{hist_name}' not found in file {input_file}")
        sys.exit(1)

    c = ROOT.TCanvas("c", "c", 800, 700)
    hist.SetStats(0)
    hist.Draw("COLZ")
    c.SetRightMargin(0.15)
    c.SetLeftMargin(0.15)  # Increased left margin to ensure y-axis label is closer to the axis
    c.SetBottomMargin(0.15)  # Increased bottom margin to ensure x-axis label is properly placed
    c.SetTopMargin(0.08)
    c.SetLogz(True)  # Enable logarithmic scale on z-axis for better visualization
    #c.SetLogy(True)
   # hist.GetYaxis().SetRangeUser(0.0001, 10)  # Set y-axis range to cover typical isolation values
    # Customize axis titles to ensure they are correctly placed and labeled
    hist.GetXaxis().SetTitle("D0 sig")  # Ensure x-axis title is set correctly
    hist.GetYaxis().SetTitle("Iso value")  # Ensure y-axis title is set correctly
    hist.GetZaxis().SetTitle("Events")  # Ensure z-axis title is set correctly
    # hist.GetXaxis().SetTitleOffset(1.2)  # Adjust offset for x-axis title to position it properly
    # hist.GetYaxis().SetTitleOffset(1.5)  # Adjust offset for y-axis title to bring it closer to the axis
    # hist.GetZaxis().SetTitleOffset(1.2)  # Adjust offset for z-axis title
    hist.GetXaxis().SetTitleSize(0.03)   # Set size of x-axis title
    hist.GetYaxis().SetTitleSize(0.03)   # Set size of y-axis title
    hist.GetZaxis().SetTitleSize(0.03)   # Set size of z-axis title
    hist.GetXaxis().SetLabelSize(0.03)   # Set size of x-axis labels
    hist.GetYaxis().SetLabelSize(0.03)   # Set size of y-axis labels
    hist.GetZaxis().SetLabelSize(0.03)   # Set size of z-axis labels
    
    c.Update()
    output_dir = "/eos/user/l/lberiet/ttZ_diff_results/tracks/plots"
    outname = f"{output_dir}/{hist_name}.png"
    c.SaveAs(outname)
    print(f"Saved plot as {outname}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()