import ROOT
import os
def save_histograms_to_images(root_filename, output_dir="hist_images"):
# Open ROOT file
    root_file = ROOT.TFile.Open(root_filename)
    if not root_file or root_file.IsZombie():
        print(f"Error opening file {root_filename}")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop over all keys in the ROOT file
    for key in root_file.GetListOfKeys():
        obj = key.ReadObj()
        # Check if the object is a histogram (TH1 or TH2)
        if isinstance(obj, ROOT.TH1):
            # Draw histogram on canvas
            canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
            obj.Draw()
            # Save canvas as PNG
            img_filename = os.path.join(output_dir, f"{obj.GetName()}.png")
            canvas.SaveAs(img_filename)
            print(f"Saved {img_filename}")
            canvas.Close()

    root_file.Close()
if __name__ == "__main__":
    save_histograms_to_images("/eos/user/l/lberiet/ttttResult/mgp8_pp_tttt_wmlep_Q_0_1000_5f_84TeV.root")