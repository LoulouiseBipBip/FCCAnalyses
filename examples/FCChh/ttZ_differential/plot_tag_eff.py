
from collections import namedtuple
import ROOT
import argparse
import os 
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptTitle(0)

def getHfromRDF(hist):
    h = None
    t = hist.GetValue()
    h = t.Clone()
    return h

def makeEffPlots(dict_of_vars, ref_var, sel_cutstring, input_filepath, out_dir_base, out_format=".pdf", do_log_y=False):
    if not os.path.exists(out_dir_base):
        os.makedirs(out_dir_base)

    rdf = ROOT.RDataFrame("events", input_filepath)

    if sel_cutstring:
        rdf = rdf.Filter(sel_cutstring)  # apply the selection

    if not rdf:
        print(f"Error: Empty or invalid RDF for { {input_filepath} }. Exiting.")
        return

    # Denominator histogram for reference variable
    print(f"Plotting denominator: {ref_var.name}")
    has_variable_binning = False
    
    if not isinstance(ref_var.nbins, int):
        has_variable_binning = True
        hist_binEdges = np.array(ref_var.nbins, dtype=float)
        hist_nBins = len(ref_var.nbins) - 1
        model = ROOT.RDF.TH1DModel(f"{ref_var.name}_model_hist", ref_var.name, hist_nBins, hist_binEdges)
    else:
        model = ROOT.RDF.TH1DModel(f"{ref_var.name}_model_hist", ref_var.name, ref_var.nbins, ref_var.xmin, ref_var.xmax)
    
    tmp_hist_den = rdf.Histo1D(model, ref_var.name)
    
    if not tmp_hist_den.GetEntries():
        print(f"Error: Empty denominator histogram for { {input_filepath} }. Exiting.")
        return
    else:
        print(f"Number of entries in denominator: { {tmp_hist_den.GetEntries()}}")
    
    tmp_den = getHfromRDF(tmp_hist_den)

    for plot_name, plot in dict_of_vars.items():
        print(f"Plotting numerator: { {plot_name}}")

        has_variable_binning = False
        if not isinstance(plot.nbins, int):
            has_variable_binning = True
            hist_binEdges = np.array(plot.nbins, dtype=float)
            hist_nBins = len(plot.nbins) - 1
            model = ROOT.RDF.TH1DModel(f"{plot_name}_model_hist", plot_name, hist_nBins, hist_binEdges)
        else:
            model = ROOT.RDF.TH1DModel(f"{plot_name}_model_hist", plot_name, plot.nbins, plot.xmin, plot.xmax)

        tmp_hist_num = rdf.Histo1D(model, plot.name)
        
        if not tmp_hist_num.GetEntries():
            print(f"Error: Empty numerator histogram for { {plot_name} } in { {input_filepath} }. Exiting.")
            return
        else:
            print(f"Number of entries in numerator: { {tmp_hist_num.GetEntries()}}")

        tmp_num = getHfromRDF(tmp_hist_num)
        
        if ROOT.TEfficiency.CheckConsistency(tmp_num, tmp_den):
            Eff = ROOT.TEfficiency(tmp_num, tmp_den)
            Eff.SetTitle(f";{plot.label};Efficiency")
            Eff.SetName(plot_name)
            
            # Add text label for lepton type
            ptext = ROOT.TPaveText(0.7, 0.85, 0.85, 0.9, "NDC")
            if "muons" in plot_name:
                ptext.AddText("Muon Efficiency")
            elif "electrons" in plot_name:
                ptext.AddText("Electron Efficiency")
            elif "leptons" in plot_name:
                ptext.AddText("Lepton Efficiency")
            else:
                ptext.AddText(plot_name)
            
            # Output filename
            if sel_cutstring == "":
                filename = f"ttZ_noSel_Eff_{plot_name}{out_format}"
            else:
                filename = f"ttZ_withSel_Eff_{plot_name}{out_format}"
            fileout = os.path.join(out_dir_base, filename)

            canvas = ROOT.TCanvas("canvas", "canvas", 900, 700)
            canvas.SetGrid()
            Eff.Draw("AP")
            canvas.Update()
            graph = Eff.GetPaintedGraph()
            graph.SetMinimum(0.0)
            graph.SetMaximum(1.1)
            canvas.Update()
            if "pT" in plot_name:
                canvas.SetLogx()  # Log scale for pT plots
            ptext.Draw()
            canvas.SaveAs(fileout)
        else:
            print(f"Error: Histograms for { {plot_name} } are not consistent with denominator!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot lepton selection efficiencies from FCCAnalyses output")
    parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inFile", required=True, help="Path to the input ROOT file.")
    parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory for plots.")
    args = parser.parse_args()

    # Use a custom namedtuple to transfer plotting info
    PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])

    # pT binning for efficiency plots (same as b-tagging script)
    pT_binedges = [10, 20, 30, 50, 100, 200, 500, 1000]  # Adjusted for lepton pT range

    # Efficiency plots for pT
    ttZ_plot_pTeff = {
        "pT_muons_genmatched_l": PlotSpecs(
            name="pT_muons_genmatched_l",
            xmin=0.,
            xmax=1000.,
            label="p_{T} #mu [GeV]",
            nbins=pT_binedges
        ),
        "pT_electrons_genmatched_l": PlotSpecs(
            name="pT_electrons_genmatched_l",
            xmin=0.,
            xmax=1000.,
            label="p_{T} e [GeV]",
            nbins=pT_binedges
        ),
        "pT_leptons_genmatched_l": PlotSpecs(
            name="pT_leptons_genmatched_l",
            xmin=0.,
            xmax=1000.,
            label="p_{T} #ell [GeV]",
            nbins=pT_binedges
        ),
    }

    # Efficiency plots for eta
    ttZ_plot_etaeff = {
        "eta_muons_genmatched_l": PlotSpecs(
            name="eta_muons_genmatched_l",
            xmin=-5.,
            xmax=5.,
            label="#eta #mu",
            nbins=20
        ),
        "eta_electrons_genmatched_l": PlotSpecs(
            name="eta_electrons_genmatched_l",
            xmin=-5.,
            xmax=5.,
            label="#eta e",
            nbins=20
        ),
        "eta_leptons_genmatched_l": PlotSpecs(
            name="eta_leptons_genmatched_l",
            xmin=-5.,
            xmax=5.,
            label="#eta #ell",
            nbins=20
        ),
    }

    # Reference variables for denominator
    pT_ref = PlotSpecs(
        name="pT_leptons_genmatched_l",
        xmin=0.,
        xmax=1000.,
        label="p_{T} #ell [GeV]",
        nbins=pT_binedges
    )
    eta_ref = PlotSpecs(
        name="eta_leptons_genmatched_l",
        xmin=-5.,
        xmax=5.,
        label="#eta #ell",
        nbins=20
    )

    # Selection cuts (require at least one gen-matched lepton)
    sel_cuts_leptons = "n_leptons_genmatched_l >= 0"

    # Make efficiency plots for pT and eta
    makeEffPlots(ttZ_plot_pTeff, pT_ref, sel_cuts_leptons, args.inFile, args.outDir, out_format=".pdf")
    makeEffPlots(ttZ_plot_etaeff, eta_ref, sel_cuts_leptons, args.inFile, args.outDir, out_format=".pdf")

# Run it with:
# python plot_lepton_eff.py -i /path/to/input.root -o /path/to/output/dir
