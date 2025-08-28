# Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lberiet/Histmaker/tta"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lberiet/Histmaker/tta/final/"

processList = {
   "mgp8_pp_tta_5f_wlep_84TeV": {},
    
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
saveJSON = True
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

        # add more cuts here: note you need to && them, they are not sequential!
}
histoList = {
    # "n_jets": {"name": "n_jets", "title": "n_jets", "bin": 10, "xmin": 0, "xmax": 10},
  "n_leptons": {"name": "n_leptons", "title": "n_{leptons}", "bin": 10, "xmin": 0, "xmax": 10},
    #"dR_phot_mid_manual": {"name": "dR_phot_mid_manual", "title": "dR_{phot-mid}", "bin": 100, "xmin": 0, "xmax": 5},
    # "dR_lep_b_reco": {"name": "dR_lep_b_reco", "title": "dR_{lep-b}", "bin": 100, "xmin": 0, "xmax": 5},
    # "n_lep_b_pairs_reco": {"name": "n_lep_b_pairs_reco", "title": "n_{lep-b}", "bin": 100, "xmin": 0, "xmax": 5},
    # "leading_photon_pt_reco": {"name": "leading_photon_pt_reco", "title": "pT_{leading_photon}", "bin": 100, "xmin": 0, "xmax": 2000},
    # # "lep_b_pairs_1_mass": {"name": "lep_b_pairs_1_mass", "title": "m_{lep-b}", "bin": 100, "xmin": 0, "xmax": 200},
    # # "dR_phot_top_manual": {"name": "dR_phot_top_manual", "title": "dR_{phot-top}", "bin": 100, "xmin": 0, "xmax": 5},
    # # "dPhi_phot_top_manual": {"name": "dPhi_phot_top_manual", "title": "d#phi_{phot-top}", "bin": 100, "xmin": -3.14, "xmax": 3.14},
    #   "dR_lep_b_reco_vs_leading_photon_pt_reco": {
    #     "name": ["dR_lep_b_reco", "leading_photon_pt_reco"],
    #     "title": "dR_{lep-b} vs pT_{leading_photon};dR_{lep-b};pT_{leading_photon}",
    #     "bin": [100, 100],
    #     "xmin": [0, 0],
    #     "xmax": [5, 2000],
    #  },
    #   "dR_lep_b_vs_leading_photon_pt": {
    #     "name": ["dR_lep_b", "leading_photon_pt"],
    #     "title": "dR_{lep-b} vs pT_{leading_photon};dR_{lep-b};pT_{leading_photon}",
    #     "bin": [100, 100],
    #     "xmin": [0, 0],
    #     "xmax": [5, 2000],
    #  },
    "lep_b_from_top_1_merged_mass": {"name": "lep_b_from_top_1_merged_mass", "title": "m_{lep_b_from_top_1}", "bin": 50, "xmin": 0, "xmax": 250},
    "lep_b_from_top_2_merged_mass": {"name": "lep_b_from_top_2_merged_mass", "title": "m_{lep_b_from_top_2}", "bin": 50, "xmin": 0, "xmax": 250},

}
