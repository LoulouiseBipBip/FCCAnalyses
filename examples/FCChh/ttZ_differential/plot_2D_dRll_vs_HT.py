import ROOT
import sys

# Usage: python plot_2D_dRll_vs_HT.py <input_root_file> [hist_name]
# Example: python plot_2D_dRll_vs_HT.py /eos/user/l/lberiet/ttZ_diff_results/final/mgp8_pp_ttz_5f_84TeV_ttzlep_sel1_histo.root

def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_2D_dRll_vs_HT.py <input_root_file> [hist_name]")
        sys.exit(1)

    input_file = sys.argv[1]
    hist_name = sys.argv[2] if len(sys.argv) > 2 else "dRll_vs_HT"

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
    c.SetLeftMargin(0.12)
    c.SetBottomMargin(0.12)
    c.SetTopMargin(0.08)
    c.SetLogz(False)
    c.Update()
    output_dir = "/eos/user/l/lberiet/ttZ_diff_results/2Dhistogram"
    outname = f"{output_dir}/{hist_name}.png"
    c.SaveAs(outname)
    print(f"Saved plot as {outname}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main() 