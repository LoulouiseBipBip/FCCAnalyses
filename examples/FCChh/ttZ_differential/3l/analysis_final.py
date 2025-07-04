# Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lberiet/ttZ_diff_results"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lberiet/ttZ_diff_results/3l/"

processList = {
    'mgp8_pp_ttz_5f_84TeV_ttzlep': {},

    'mgp8_pp_tttt_5f_84TeV_4tlep': {"fraction": 1},
    'mgp8_pp_tth_5f_84TeV': {},
    'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep': {},

    'mgp8_pp_zzz_5f_84TeV': {},
    'mgp8_pp_wzz_5f_84TeV': {},
    'mgp8_pp_wwz_5f_84TeV': {},
    'mgp8_pp_wwww_5f_84TeV': {},
    'mgp8_pp_wwwz_5f_84TeV': {},
    'mgp8_pp_wwzz_5f_84TeV': {},
    'mgp8_pp_wzzz_5f_84TeV': {},
    'mgp8_pp_zzzz_5f_84TeV': {},
    'mgp8_pp_ttzz_5f_84TeV': {},
    'mgp8_pp_ttwz_5f_84TeV': {},

    
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
    "all_events": "n_leptons >= 0", # all events (no selection)
    "sel1_lep": "n_leptons == 3", # 4 leptons
    "sel2_bjets": "n_bjets >= 1 && n_bjets <= 2 && n_leptons == 3", # 1 or 2 b-jets and 4 leptons
    "sel3_njets": "n_jets < 6 && n_leptons == 3 && n_bjets >= 1 && n_bjets <= 2", # 4 leptons and less than 6 jets and 1 or 2 b-jets
    #"sel3_bjets": "(n_leptons == 4) && Second_Pair_flavor == 3 && (n_bjets >= 1) && (n_bjets <= 2) ", # 4 leptons and second OS pair and 1 or 2 b-jets
    "sel4_mll": " (Z_ll_mass) > 80. && (Z_ll_mass  < 100.) && n_bjets >= 1 && n_bjets <= 2 && n_leptons == 3 && n_jets < 6", # 4 leptons and second OS pair and 1 or 2 b-jets and Z mass between 80 and 100 GeV
    #"sel5_second_pair": "(Z_ll_mass) > 80. && (Z_ll_mass  < 100.) && n_bjets >= 1 && n_bjets <= 2 && n_leptons == 4 && n_jets < 6 && Second_Pair_flavor == 3", # 4 leptons and second OS pair and 1 or 2 b-jets and Z mass between 80 and 100 GeV
    # add more cuts here: note you need to && them, they are not sequential!
}
histoList = {
    "n_jets": {"name": "n_jets", "title": "Number of jets", "bin": 10, "xmin": 0, "xmax": 10},
    "Second_Pair_mass": {"name": "Second_Pair_mass", "title": "Second OS pair mass [GeV]", "bin": 50, "xmin": 5, "xmax": 250},
    "Second_Pair_flavor": {"name": "Second_Pair_flavor", "title": "Second OS pair flavor", "bin": 4, "xmin": 0, "xmax": 4},
    "Z_ll_and_second_pairs_size": {"name": "Z_ll_and_second_pairs_size", "title": "Z_ll and second OS pair size", "bin": 10, "xmin": 0, "xmax": 10},
    "electron_noiso_var": {"name": "electron_noiso_var", "title": "Electron noiso var", "bin": 100, "xmin": 0, "xmax": 2.5},
    "electron_iso_var": {"name": "electron_iso_var", "title": "Electron iso var", "bin": 100, "xmin": 0, "xmax": 2.5},
    "muon_noiso_var": {"name": "muon_noiso_var", "title": "Muon noiso var", "bin": 100, "xmin": 0, "xmax": 2.5},
    "muon_iso_var": {"name": "muon_iso_var", "title": "Muon iso var", "bin": 100, "xmin": 0, "xmax": 2.5},
    #"Zll_and_second_pairs": {"name": "Zll_and_second_pairs_flavor", "title": "Zll and second OS pair is e-mu", "bin": 10, "xmin": 0, "xmax": 10},
    "n_bjets": {"name": "n_bjets", "title": "Number of b-Jets", "bin": 15, "xmin": 0, "xmax": 15},
    "n_leptons": {"name": "n_leptons", "title": "Number of Leptons", "bin": 10, "xmin": 0, "xmax": 10},
    "Z_ll_mass": {"name": "Z_ll_mass", "title": "Z_{ll} mass [GeV]", "bin": 50, "xmin": 5, "xmax": 250},
    "dR_ll": {"name": "dR_ll", "title": "dR_{ll}", "bin": 50, "xmin": 0, "xmax": 10},
    "HT": {"name": "HT", "title": "H_{T} [GeV]", "bin": 100, "xmin": 0, "xmax": 3500},
    "MET": {"name": "MET", "title": "MET [GeV]", "bin": 20, "xmin": 0, "xmax": 2000},
    "dRll_vs_HT": {
        "name": ["dR_ll", "HT"],
        "title": "dR_{ll} vs H_{T};dR_{ll};H_{T} [GeV]",
        "bin": [50, 50],
        "xmin": [0, 0],
        "xmax": [10, 2000]
    },
}
