import array
# Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/result"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/final"

processList = {
    'mgp8_pp_ttz_5f_84TeV_ttzlep': {},


    
}

prodTag = "FCChh/fcc_v07/II/"
# Link to the dictonary that contains all the cross section informations etc...
#procDict = "/eos/experiment/fcc/hh/tutorials/edm4hep_tutorial_data/FCChh_procDict_tutorial.json"
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json"
# Note the numbeOfEvents and sumOfWeights are placeholders that get overwritten with the correct values in the samples

# How to add a process that is not in the official dictionary:
# procDictAdd={"pwp8_pp_hh_5f_hhbbyy": {"numberOfEvents": 4980000, "sumOfWeights": 4980000.0, "crossSection": 0.0029844128399999998, "kfactor": 1.075363, "matchingEfficiency": 1.0}}

# Expected integrated luminosity
intLumi = 30e06  # pb-1

# Whether to scale to expected integrated luminosity
doScale = True

# Number of CPUs to use
nCPUS = 48

# produces ROOT TTrees, default is False
doTree = True
saveJSON = True
saveTabular = True

# Explicitly save histograms in separate files with _histo suffix
saveHistos = True
histoSuffix = '_histo'

# Optional: Use weighted events
do_weighted = False

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
#cutList = {
   # "sel1_bjets": "n_bjets > -1",
#}

# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.

# add these variables
# "tt_m",
# "tt_pt",
# "tt_eta",
# "tt_phi",
# "t1_pt",
# "t1_eta",
# "t1_phi",
# "t1_m",
# "t2_pt",
# "t2_eta",
# "t2_phi",
# "t2_m",

cutList = {
    "all_events": "truth_prompt_lep_size >=0 ", # all events (no selection)
   # "lep_pt_cut": "truth_lep_pt > 1000",
    #"lep_pT_eta_cut": "All(abs(truth_lep_eta) < 6) && All(truth_lep_pt > 30)",
    #"cluster_test": "pt_tot_Z.size() > 0 && pt_tot_Z[0] < 200 && dR_Zll_truth < 0.2",
    # "Iso_0": "Iso_Prompt.size() > 0 && All(Iso_Prompt == 0)", # all elements are 0
    # "Iso_not_0": "Iso_Prompt.size() > 0 && Any(Iso_Prompt != 0)", # at least one element is not 0
   # "all_cuts": "n_leptons_sel==4 && (n_bjets==1|n_bjets==2) && Second_Pair_flavor==3 && Z_ll_mass>80 && Z_ll_mass<100",
   # "Zee": "Z_ll_flavor == 2",
   # # "lep_eta": "abs(truth_prompt_lep_eta[0]) < 4 && abs(truth_prompt_lep_eta[1]) < 4 && abs(truth_prompt_lep_eta[2]) < 4 && abs(truth_prompt_lep_eta[3]) < 4",
    # "lep_pt": "truth_prompt_lep_pt[0] > 10 && truth_prompt_lep_pt[1] > 10 && truth_prompt_lep_pt[2] > 10 && truth_prompt_lep_pt[3] > 10",
    #"lep_eta_pt": "n_leptons_sel >=0 && pT_leptons_sel[0]>30 && pT_leptons_sel[1]>30 && pT_leptons_sel[2]>30 && pT_leptons_sel[3]>30 && abs(eta_muons_sel[0])<4 && abs(eta_electrons_sel[0])<4 && abs(eta_muons_sel[1])<4 && abs(eta_electrons_sel[1])<4 && abs(eta_muons_sel[2])<4 && abs(eta_electrons_sel[2])<4 && abs(eta_muons_sel[3])<4 && abs(eta_electrons_sel[3])<4", 
   # "lep_pt": "truth_prompt_lep_pt[0] > 30 && truth_prompt_lep_pt[1] > 30 && truth_prompt_lep_pt[2] > 30 && truth_prompt_lep_pt[3] > 30",
    #"lep_eta_pt": "abs(truth_prompt_lep_eta[0]) < 4 && truth_prompt_lep_pt[0] > 30 && abs(truth_prompt_lep_eta[1]) < 4 && truth_prompt_lep_pt[1] > 30 && abs(truth_prompt_lep_eta[2]) < 4 && truth_prompt_lep_pt[2] > 30 && abs(truth_prompt_lep_eta[3]) < 4 && truth_prompt_lep_pt[3] > 30",
}
histoList = {
    "truth_prompt_lep_size": {"name": "truth_prompt_lep_size", "title": "truth_prompt_lep_size", "bin": 10, "xmin": 0, "xmax": 10},
    "matched_prompt_lep_size": {"name": "matched_prompt_lep_size", "title": "matched_prompt_lep_size", "bin": 10, "xmin": 0, "xmax": 10},
    # "Z_ll_pt": {"name": "Z_ll_pt", "title": "Z_ll_pt", "bin": 50, "xmin": 0, "xmax": 2000},
    # "eff_lep_pt_eta": {"name": "eff_lep_pt_eta", "title": "eff_lep_pt_eta", "bin": 100, "xmin": 0, "xmax": 1},
   # "diff_iso_electrons": {"name": "diff_iso_electrons", "title": "diff_iso_electrons", "bin": 100, "xmin": -1, "xmax": 1},
    
    # "prompt_lep_pt": {"name": "prompt_lep_pt", "title": "prompt_lep_pt", "bin": 100, "xmin": 30, "xmax": 1000},
    # "prompt_lep_eta": {"name": "prompt_lep_eta", "title": "prompt_lep_eta", "bin": 9, "xmin": -4, "xmax": 4},
    # "non_prompt_lep_pt": {"name": "non_prompt_lep_pt", "title": "non_prompt_lep_pt", "bin": 100, "xmin": 30, "xmax": 1000},
    # "non_prompt_lep_eta": {"name": "non_prompt_lep_eta", "title": "non_prompt_lep_eta", "bin": 9, "xmin": -4, "xmax": 4},
    # "prompt_lep_mass": {"name": "prompt_lep_mass", "title": "prompt_lep_mass", "bin": 100, "xmin": 0, "xmax": 1},
    # "non_prompt_lep_mass": {"name": "non_prompt_lep_mass", "title": "non_prompt_lep_mass", "bin": 100, "xmin": 0, "xmax": 1000},
    # "Iso_Prompt": {"name": "Iso_Prompt", "title": "Iso_Prompt", "bin": 100, "xmin": 0, "xmax": 1},
    # "Iso_Non_Prompt": {"name": "Iso_Non_Prompt", "title": "Iso_Non_Prompt", "bin": 100, "xmin": 0, "xmax": 1},
    #  "dR_Zll_truth": {"name": "dR_Zll_truth", "title": "dR_Zll_truth", "bin": 50, "xmin": 0, "xmax": 0.4},
    # "truth_ll_pt": {"name": "truth_ll_pt", "title": "truth_ll_pt", "bin": 50, "xmin": 0, "xmax": 1000},
    # "Iso_Prompt_Zll": {"name": "Iso_Prompt_Zll", "title": "Iso_Prompt_Zll", "bin": 100, "xmin": 0, "xmax": 1},
    # "truth_ll_mass": {"name": "truth_ll_mass", "title": "truth_ll_mass", "bin": 50, "xmin": 0, "xmax": 50},
    # "electron_mass": {"name": "electron_mass", "title": "electron_mass", "bin": 50, "xmin": 0, "xmax": 50},
    # "pt_tot_Z": {"name": "pt_tot_Z", "title": "pt_tot_Z", "bin": 50, "xmin": 0, "xmax": 2000},
    # "Z_mass": {"name": "Z_mass", "title": "Z_mass", "bin": 50, "xmin": 0, "xmax": 500},
    # "Z_mass_truth": {"name": "Z_mass_truth", "title": "Z_mass_truth", "bin": 50, "xmin": 0, "xmax": 500},
    # "Z_pt_truth": {"name": "Z_pt_truth", "title": "Z_pt_truth", "bin": 50, "xmin": 0, "xmax": 2000},
    # "p_Z_ll": {"name": "p_Z_ll", "title": "p_Z_ll", "bin": 50, "xmin": 0, "xmax": 2000},
    # "pz_Z_ll": {"name": "pz_Z_ll", "title": "pz_Z_ll", "bin": 50, "xmin": 0, "xmax": 2000},
    # "eta_Z_ll": {"name": "eta_Z_ll", "title": "eta_Z_ll", "bin": 10, "xmin": -4, "xmax": 4},
    # "matched_leptons_Zll_mass": {"name": "matched_leptons_Zll_mass", "title": "matched_leptons_Zll_mass", "bin": 50, "xmin": 0, "xmax": 500},
    # "eta_vs_pt_lep": {
    #    "name": ["prompt_lep_pt", "prompt_lep_eta"],
    #    "title": "pT_{lep} vs eta_{lep};pT_{lep} [GeV];eta_{lep}",
    #    "bin": [100, 50],
    #    "xmin": [0, 0],
    #    "xmax": [1000, 6]  
    # },
    # "prompt_muons_iso_dr01": {"name": "prompt_muons_iso_dr01", "title": "prompt_muons_iso_dr01", "bin": 100, "xmin": 0, "xmax": 1},
    # "prompt_electrons_iso_dr01": {"name": "prompt_electrons_iso_dr01", "title": "prompt_electrons_iso_dr01", "bin": 100, "xmin": 0, "xmax": 1},
    # "non_prompt_muons_iso_dr01": {"name": "non_prompt_muons_iso_dr01", "title": "non_prompt_muons_iso_dr01", "bin": 100, "xmin": 0, "xmax": 1},
    # "non_prompt_electrons_iso_dr01": {"name": "non_prompt_electrons_iso_dr01", "title": "non_prompt_electrons_iso_dr01", "bin": 100, "xmin": 0, "xmax": 1},
    # "prompt_muons_iso_dr03": {"name": "prompt_muons_iso_dr03", "title": "prompt_muons_iso_dr03", "bin": 100, "xmin": 0, "xmax": 1},
    # "prompt_electrons_iso_dr03": {"name": "prompt_electrons_iso_dr03", "title": "prompt_electrons_iso_dr03", "bin": 100, "xmin": 0, "xmax": 1},
    # "non_prompt_muons_iso_dr03": {"name": "non_prompt_muons_iso_dr03", "title": "non_prompt_muons_iso_dr03", "bin": 100, "xmin": 0, "xmax": 1},
    # "non_prompt_electrons_iso_dr03": {"name": "non_prompt_electrons_iso_dr03", "title": "non_prompt_electrons_iso_dr03", "bin": 100, "xmin": 0, "xmax": 1},
    # "Iso_Prompt_fine": {"name": "Iso_Prompt", "title": "Iso_Prompt Fine Binning", "bin": 1000000, "xmin": 0, "xmax": 10},  # for detailed counting near 0
    # "Iso_Non_Prompt_fine": {"name": "Iso_Non_Prompt", "title": "Iso_Non_Prompt Fine Binning", "bin": 1000000, "xmin": 0, "xmax": 10},  # for detailed counting near 0
}