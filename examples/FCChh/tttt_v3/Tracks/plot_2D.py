import ROOT
import os

def main():
    # Base input directory for Q-binned files
    input_dir = "/eos/user/l/lberiet/Histmaker/tttt_v3/Tracks/final"
    hist_name =  "Prompt_Iso_all_elec_vs_D0_sig_prompt_electrons"  # Ensure this matches the 2D histogram name in analysis_final.py
    
    # List of Q-binned processes to handle
    processes = [
         'mgp8_pp_tttt_wlep_Q_0_1000_5f_84TeV',
             'mgp8_pp_tttt_wlep_Q_1000_3000_5f_84TeV',
             'mgp8_pp_tttt_wlep_Q_3000_10000_5f_84TeV',
             'mgp8_pp_tttt_wlep_Q_10000_84000_5f_84TeV'
    ]
    
    output_dir = "/eos/user/l/lberiet/Histmaker/tttt_v3/Tracks/plots"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a combined histogram to store the sum of all Q-binned histograms
    combined_hist = None

    # Keep track of open files to close them later
    open_files = []

    for proc in processes:
        # Construct the full file path for each process
        input_file = os.path.join(input_dir, f"{proc}_all_events_histo.root")
        
        print(f"Processing file: {input_file}")
        f = ROOT.TFile.Open(input_file)
        if not f or f.IsZombie():
            print(f"Could not open file: {input_file}")
            continue
        
        hist = f.Get(hist_name)
        if not hist:
            print(f"Histogram '{hist_name}' not found in file {input_file}. Listing available histograms:")
            f.ls()  # List contents of the file to debug
            f.Close()
            continue
            
        if combined_hist is None:
            # Initialize the combined histogram with the first histogram's structure
            combined_hist = hist.Clone("combined_hist")
            combined_hist.SetTitle("Combined Q-binned Iso_prompt_elec_vs_D0_sig_prompt_electrons")
            combined_hist.GetXaxis().SetTitle("D0_{sig_electrons}")  # Ensure x-axis title is set correctly
            combined_hist.GetYaxis().SetTitle("iso_{all_elec}")  # Ensure y-axis title is set correctly
            combined_hist.GetZaxis().SetTitle("Events")  # Ensure z-axis title is set correctly
            # hist.GetXaxis().SetTitleOffset(1.2)  # Adjust offset for x-axis title to position it properly
            # hist.GetYaxis().SetTitleOffset(1.5)  # Adjust offset for y-axis title to bring it closer to the axis
            # hist.GetZaxis().SetTitleOffset(1.2)  # Adjust offset for z-axis title
            combined_hist.GetXaxis().SetTitleSize(0.03)   # Set size of x-axis title
            combined_hist.GetYaxis().SetTitleSize(0.03)   # Set size of y-axis title
            combined_hist.GetZaxis().SetTitleSize(0.03)   # Set size of z-axis title
            combined_hist.GetXaxis().SetLabelSize(0.03)   # Set size of x-axis labels
            combined_hist.GetYaxis().SetLabelSize(0.03)   # Set size of y-axis labels
            combined_hist.GetZaxis().SetLabelSize(0.03)   # Set size of z-axis labels
            print(f"Initialized combined histogram with data from {input_file}")
        else:
            # Add subsequent histograms to the combined one
            print(f"Adding histogram from {input_file} to combined histogram")
            combined_hist.Add(hist)
        
        open_files.append(f)  # Keep file open until the end to prevent memory issues
        print(f"Processed histogram from {input_file}")

    if combined_hist:
        # Create a single canvas for the combined histogram
        c = ROOT.TCanvas("c_combined", "Combined Q-binned Histogram", 800, 700)
        combined_hist.SetStats(0)
        combined_hist.Draw("COLZ")
        c.SetRightMargin(0.15)
        c.SetLeftMargin(0.12)
        c.SetBottomMargin(0.12)
        c.SetTopMargin(0.08)
        c.SetLogz(True) 
        c.Update()
        
        outname = f"{output_dir}/{hist_name}_combined.png"
        c.SaveAs(outname)
        print(f"Saved combined plot as {outname}")
    else:
        print("No histograms were found to combine. Please check if the histogram name '{hist_name}' is correct.")

    # Close all open files
    for f in open_files:
        f.Close()
        print(f"Closed file: {f.GetName()}")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
