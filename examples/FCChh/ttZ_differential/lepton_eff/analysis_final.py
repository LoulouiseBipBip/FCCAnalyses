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
    "all_events": "n_truth_Zll >=0 ", # all events (no selection)
   # "Zee": "Z_ll_flavor == 2",
   # # "lep_eta": "abs(truth_prompt_lep_eta[0]) < 4 && abs(truth_prompt_lep_eta[1]) < 4 && abs(truth_prompt_lep_eta[2]) < 4 && abs(truth_prompt_lep_eta[3]) < 4",
    # "lep_pt": "truth_prompt_lep_pt[0] > 10 && truth_prompt_lep_pt[1] > 10 && truth_prompt_lep_pt[2] > 10 && truth_prompt_lep_pt[3] > 10",
    #"lep_eta_pt": "n_leptons_sel >=0 && pT_leptons_sel[0]>30 && pT_leptons_sel[1]>30 && pT_leptons_sel[2]>30 && pT_leptons_sel[3]>30 && abs(eta_muons_sel[0])<4 && abs(eta_electrons_sel[0])<4 && abs(eta_muons_sel[1])<4 && abs(eta_electrons_sel[1])<4 && abs(eta_muons_sel[2])<4 && abs(eta_electrons_sel[2])<4 && abs(eta_muons_sel[3])<4 && abs(eta_electrons_sel[3])<4", 
   # "lep_pt": "truth_prompt_lep_pt[0] > 30 && truth_prompt_lep_pt[1] > 30 && truth_prompt_lep_pt[2] > 30 && truth_prompt_lep_pt[3] > 30",
    #"lep_eta_pt": "abs(truth_prompt_lep_eta[0]) < 4 && truth_prompt_lep_pt[0] > 30 && abs(truth_prompt_lep_eta[1]) < 4 && truth_prompt_lep_pt[1] > 30 && abs(truth_prompt_lep_eta[2]) < 4 && truth_prompt_lep_pt[2] > 30 && abs(truth_prompt_lep_eta[3]) < 4 && truth_prompt_lep_pt[3] > 30",
}
histoList = {
    #"Z_ll_flavor": {"name": "Z_ll_flavor", "title": "flavour of Zll", "bin": 3, "xmin": 1, "xmax": 3},
    # "Z_ll_pt": {"name": "Z_ll_pt", "title": "p_{T} of Zll [GeV]", "bin": len(bins_zpt)-1, "xmin": bins_zpt[0], "xmax": bins_zpt[-1]},
   # "n_leptons_sel": {"name": "n_leptons_sel", "title": "number of leptons", "bin": 8, "xmin": 0, "xmax": 8},
   #"truth_prompt_lep_pt": {"name": "truth_prompt_lep_pt", "title": "p_{T} of truth prompt leptons [GeV]", "bin": 200, "xmin": 0, "xmax": 1000},
  # "truth_prompt_lep_eta": {"name": "truth_prompt_lep_eta", "title": "#eta of truth prompt leptons", "bin": 20, "xmin": -5, "xmax": 5},
  # "lepton_1_pt": {"name": "lepton_1_pt", "title": "p_{T} of lepton 1 [GeV]", "bin": 200, "xmin": 0, "xmax": 1000},
  # "lepton_2_pt": {"name": "lepton_2_pt", "title": "p_{T} of lepton 2 [GeV]", "bin": 200, "xmin": 0, "xmax": 1000},
   #"lepton_1_eta": {"name": "lepton_1_eta", "title": "#eta of lepton 1", "bin": 20, "xmin": -5, "xmax": 5},
   #"lepton_2_eta": {"name": "lepton_2_eta", "title": "#eta of lepton 2", "bin": 20, "xmin": -5, "xmax": 5},
#   "dR_ll": {"name": "dR_ll", "title": "dR_{ll}", "bin": 50, "xmin": 0, "xmax": 10},
#   lepton_iso": {"name": "lepton_iso", "title": "lepton isolation", "bin": 100, "xmin": 0, "xmax": 2},
#   "flavour_Z_decay": {"name": "flavour_Z_decay", "title": "flavour of Z decay", "bin": 3, "xmin": 1, "xmax": 4},
#   "n_truth_leptons": {"name": "n_truth_leptons", "title": "number of truth leptons", "bin": 50, "xmin": 0, "xmax": 50},
#   "n_truth_leptons_final": {"name": "n_truth_leptons_final", "title": "number of truth leptons (final)", "bin": 50, "xmin": 0, "xmax": 50},
#   "n_truth_leptons_temp_final": {"name": "n_truth_leptons_temp_final", "title": "number of truth leptons (temp final)", "bin": 50, "xmin": 0, "xmax": 50},
#   "truth_lep_pt": {"name": "truth_lep_pt", "title": "p_{T} of truth leptons [GeV]", "bin": 200, "xmin": 0, "xmax": 1000},
#   "truth_lep_eta": {"name": "truth_lep_eta", "title": "#eta of truth leptons", "bin": 20, "xmin": -5, "xmax": 5},
#   #"n_tau_final": {"name": "n_tau_final", "title": "number of truth taus (final)", "bin": 50, "xmin": 0, "xmax": 50},
#   # "n_lep_cut_pt": {"name": "n_lep_cut_pt", "title": "number of truth leptons (pT > 20 GeV)", "bin": 50, "xmin": 0, "xmax": 50},
#  #"n_lep_cut_pt_eta": {"name": "n_lep_cut_pt_eta", "title": "number of truth leptons (pT > 20 GeV, |#eta| < 3)", "bin": 50, "xmin": 0, "xmax": 50},
#   "lep_origin": {"name": "lep_origin", "title": "origin of truth leptons", "bin": 1000, "xmin": 0, "xmax": 1000},
#   "matched_leptons_Zll_size": {"name": "matched_leptons_Zll_size", "title": "number of matched truth leptons to Zll", "bin": 3, "xmin": 0, "xmax": 3},
    #"matched_electrons_Zll_size": {"name": "matched_electrons_Zll_size", "title": "number of matched truth electrons to Zll", "bin": 3, "xmin": 0, "xmax": 3},
   # "matched_muons_Zll_size": {"name": "matched_muons_Zll_size", "title": "number of matched truth muons to Zll", "bin": 3, "xmin": 0, "xmax": 3},
  # "lepton_1_pt": {"name": "lepton_1_pt", "title": "p_{T} of lepton 1 [GeV]", "bin": 200, "xmin": 0, "xmax": 1000},
  # "lepton_2_pt": {"name": "lepton_2_pt", "title": "p_{T} of lepton 2 [GeV]", "bin": 200, "xmin": 0, "xmax": 1000},
  # "lepton_1_eta": {"name": "lepton_1_eta", "title": "#eta of lepton 1", "bin": 20, "xmin": -5, "xmax": 5},
  # "lepton_2_eta": {"name": "lepton_2_eta", "title": "#eta of lepton 2", "bin": 20, "xmin": -5, "xmax": 5},
   #"truth_ll_pt": {"name": "truth_ll_pt", "title": "p_{T} of truth Zll [GeV]", "bin": 200, "xmin": 0, "xmax": 1000},
   #"truth_ll_eta": {"name": "truth_ll_eta", "title": "#eta of truth Zll", "bin": 20, "xmin": -5, "xmax": 5},
   #"n_truth_prompt_lep": {"name": "n_truth_prompt_lep", "title": "number of truth prompt leptons", "bin": 1000, "xmin": 0, "xmax": 1000},
   #"n_truth_non_prompt_lep": {"name": "n_truth_non_prompt_lep", "title": "number of truth non-prompt leptons", "bin": 1000, "xmin": 0, "xmax": 1000},
#    "pt_Z_truth_prompt_lep": {"name": "pt_Z_truth_prompt_lep", "title": "p_{T} of Z truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 200},
#    "eta_Z_truth_prompt_lep": {"name": "eta_Z_truth_prompt_lep", "title": "#eta of Z truth prompt lepton", "bin": 20, "xmin": -5, "xmax": 5},
#    "pt_t_truth_prompt_lep": {"name": "pt_t_truth_prompt_lep", "title": "p_{T} of t truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 200},
#    "eta_t_truth_prompt_lep": {"name": "eta_t_truth_prompt_lep", "title": "#eta of t truth prompt lepton", "bin": 20, "xmin": -5, "xmax": 5},
#    "HT": {"name": "HT", "title": "HT", "bin": 300, "xmin": 0, "xmax": 3000}
#     "min_DR_prompt_lep_1": {"name": "min_DR_prompt_lep_1", "title": "min DR of Z truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 0.5},
#     "min_DR_prompt_lep_2": {"name": "min_DR_prompt_lep_2", "title": "min DR of Z truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 0.1},
#     "min_DR_prompt_lep_3": {"name": "min_DR_prompt_lep_3", "title": "min DR of t truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 0.5},
#     "min_DR_prompt_lep_4": {"name": "min_DR_prompt_lep_4", "title": "min DR of t truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 0.1},
#     #"closest_part_prompt_lep": {"name": "closest_part_prompt_lep", "title": "closest part of truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 1000},
#     "closest_DR_test": {"name": "closest_DR_test", "title": "closest DR of truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 1000},
#     "pt_closest_part_prompt_lep": {"name": "pt_closest_part_prompt_lep", "title": "p_{T} of closest part of truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 1000},
    # "min_DR_lep_reco": {"name": "min_DR_lep_reco", "title": "min DR of truth lepton", "bin": 100, "xmin": 0, "xmax": 0.15},
    # "min_DR_lep_reco_prompt": {"name": "min_DR_lep_reco_prompt", "title": "min DR of truth prompt lepton", "bin": 100, "xmin": 0, "xmax": 0.15},
    # "min_dR_reco_prompt": {"name": "min_dR_reco_prompt", "title": "min DR of reco prompt lepton", "bin": 100, "xmin": 0, "xmax":1},
    # "min_dR_reco_prompt_test": {"name": "min_dR_reco_prompt_test", "title": "min DR of reco prompt lepton test", "bin": 100, "xmin": 0, "xmax":1},
    "reco_truth_lep_dR": {"name": "reco_truth_lep_dR", "title": "min DR of reco truth lepton", "bin": 100, "xmin": 0, "xmax":0.2},
    "Iso_Prompt": {"name": "Iso_Prompt", "title": "prompt muons iso dr01", "bin": 100, "xmin": 0, "xmax":1},
    "Iso_Non_Prompt": {"name": "Iso_Non_Prompt", "title": "non prompt muons iso dr01", "bin": 100, "xmin": 0, "xmax":1},
    # "prompt_muons_iso_dr01": {"name": "prompt_muons_iso_dr01", "title": "prompt muons iso dr01", "bin": 100, "xmin": 0, "xmax":0.1},
    # "non_prompt_muons_iso_dr01": {"name": "non_prompt_muons_iso_dr01", "title": "non prompt muons iso dr01", "bin": 100, "xmin": 0, "xmax":0.1},
    # "prompt_electrons_iso_dr01": {"name": "prompt_electrons_iso_dr01", "title": "prompt electrons iso dr01", "bin": 100, "xmin": 0, "xmax":0.1},
    # "non_prompt_electrons_iso_dr01": {"name": "non_prompt_electrons_iso_dr01", "title": "non prompt electrons iso dr01", "bin": 100, "xmin": 0, "xmax":0.1},
    # "prompt_muons_iso_dr02": {"name": "prompt_muons_iso_dr02", "title": "prompt muons iso dr02", "bin": 100, "xmin": 0, "xmax":0.1},
    # "non_prompt_muons_iso_dr02": {"name": "non_prompt_muons_iso_dr02", "title": "non prompt muons iso dr02", "bin": 100, "xmin": 0, "xmax":0.1},
    # "prompt_electrons_iso_dr02": {"name": "prompt_electrons_iso_dr02", "title": "prompt electrons iso dr02", "bin": 100, "xmin": 0, "xmax":0.1},
    # "non_prompt_electrons_iso_dr02": {"name": "non_prompt_electrons_iso_dr02", "title": "non prompt electrons iso dr02", "bin": 100, "xmin": 0, "xmax":0.1},
    # "prompt_muons_iso_dr03": {"name": "prompt_muons_iso_dr03", "title": "prompt muons iso dr03", "bin": 100, "xmin": 0, "xmax":0.1},
  }