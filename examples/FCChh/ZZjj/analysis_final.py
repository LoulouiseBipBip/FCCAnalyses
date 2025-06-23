# Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lberiet/ZZjj_results/results/"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lberiet/ZZjj_results/final/"

processList = {
    'mgp8_pp_tttt_5f_84TeV_4tlep': {},


    'mgp8_pp_ttz_5f_84TeV_ttzlep': {},
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

# Link to the dictonary that contains all the cross section informations etc...
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
            #"sel1_lep":"n_leptons == 4", # 3 leptons
            #"sel2_bjets":"(n_leptons == 4) && (n_bjets <= 2) ", # at most 2 b-jets
            #"sel3_jets":"(n_leptons == 4) && (n_bjets <= 2) && (n_jets <= 3) ", # at most 3 jets
            #"sel4_Z_1": "(n_leptons == 4) && (n_bjets <= 2) && (n_jets <= 3) && (Z_ll_1_mass > 80 && Z_ll_1_mass < 100)", # first pair is Z
            #"sel5_Z_2": "(n_leptons == 4) && (n_bjets <= 2) && (n_jets <= 3) && (Z_ll_2_mass > 80 && Z_ll_2_mass < 100) && (Z_ll_1_mass > 80 && Z_ll_1_mass < 100)" # second pair is Z
            # add more cuts here: note you need to && them, they are not sequential!
            }
histoList = {
    # "n_jets": {"name": "n_jets", "title": "n_jets", "bin": 10, "xmin": 0, "xmax": 10},
    #"n_of_ss_sf_leptons": {"name": "n_of_ss_sf_leptons", "title": "n_of_ss_sf_leptons", "bin": 10, "xmin": 0, "xmax": 10},  
    #"Z_ll_1_pt": {"name": "Z_ll_1_pt", "title": "Z_ll_1_pt", "bin": 25, "xmin": 0, "xmax": 100},
    #"Z_ll_2_pt": {"name": "Z_ll_2_pt", "title": "Z_ll_2_pt", "bin": 25, "xmin": 0, "xmax": 100},
    "Z_ll_2_flavor": {"name": "Z_ll_2_flavor", "title": "Z_ll_2_flavor", "bin": 4, "xmin": 0, "xmax": 4},
    "pT_jets": {"name": "pT_jets", "title": "pT_jets", "bin": 50, "xmin": 0, "xmax": 200},
    "pT_bjets": {"name": "pT_bjets", "title": "pT_bjets", "bin": 50, "xmin": 0, "xmax": 200},
    "Z_ll_and_second_pairs_size": {"name": "Z_ll_and_second_pairs_size", "title": "Z_ll_and_second_pairs_size", "bin": 10, "xmin": 0, "xmax": 10},
    "Z_ll_1_mass": {"name": "Z_ll_1_mass", "title": "Z_ll_1_mass", "bin": 50, "xmin": 0, "xmax": 250},
    "Z_ll_2_mass": {"name": "Z_ll_2_mass", "title": "Z_ll_2_mass", "bin": 50, "xmin": 0, "xmax": 250},
    "Z_ll_1_pt": {"name": "Z_ll_1_pt", "title": "Z_ll_1_pt", "bin": 50, "xmin": 0, "xmax": 250},
    "Z_ll_2_pt": {"name": "Z_ll_2_pt", "title": "Z_ll_2_pt", "bin": 50, "xmin": 0, "xmax": 250},
    "n_jets": {"name": "n_jets", "title": "n_jets", "bin": 10, "xmin": 0, "xmax": 10},
    "n_bjets": {"name": "n_bjets", "title": "n_bjets", "bin": 10, "xmin": 0, "xmax": 10},
    "n_leptons": {"name": "n_leptons", "title": "n_leptons", "bin": 10, "xmin": 0, "xmax": 10},
    #"Z_ll_mass": {"name": "Z_ll_mass", "title": "Z_ll_mass", "bin": 50, "xmin": 0, "xmax": 250},
    #"Second_Pair_mass": {"name": "Second_Pair_mass", "title": "Second_Pair_mass", "bin": 10, "xmin": 0, "xmax": 10},
    "dR_ll": {"name": "dR_ll", "title": "dR_ll", "bin": 10, "xmin": 0, "xmax": 10},
    "HT": {"name": "HT", "title": "H_{T} [TeV]", "bin": 100, "xmin": 0, "xmax": 8000},
    "MET": {"name": "MET", "title": "MET", "bin": 20, "xmin": 0, "xmax": 2000},
    #"HT_sel": {"name": "HT_sel", "title": "H_{T} [TeV]", "bin": 50, "xmin": 0, "xmax": 2000},
    #"MET_sel": {"name": "MET_sel", "title": "MET", "bin": 20, "xmin": 0, "xmax": 2000},
}
