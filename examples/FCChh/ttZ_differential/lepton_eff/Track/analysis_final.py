import array
# Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lberiet/ttZ_diff_results/tracks"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lberiet/ttZ_diff_results/tracks/final"

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
    "all_events": "n_leptons >=0", # all events (no selection)
 
}
histoList = {
   "Z0_sig_prompt_electrons": {"name": "Z0_sig_prompt_electrons", "title": "Z0_sig_prompt_electrons", "bin": 100, "xmin": 0, "xmax": 1},
   "Z0_sig_non_prompt_electrons": {"name": "Z0_sig_non_prompt_electrons", "title": "Z0_sig_non_prompt_electrons", "bin": 100, "xmin": 0, "xmax": 1},
   "Z0_sig_prompt_muons": {"name": "Z0_sig_prompt_muons", "title": "Z0_sig_prompt_muons", "bin": 100, "xmin": 0, "xmax": 1},
   "Z0_sig_non_prompt_muons": {"name": "Z0_sig_non_prompt_muons", "title": "Z0_sig_non_prompt_muons", "bin": 100, "xmin": 0, "xmax": 1},
   "Z0_sig_prompt_leptons": {"name": "Z0_sig_prompt_leptons", "title": "Z0_sig_prompt_leptons", "bin": 100, "xmin": 0, "xmax": 1},
   "Z0_sig_non_prompt_leptons": {"name": "Z0_sig_non_prompt_leptons", "title": "Z0_sig_non_prompt_leptons", "bin": 100, "xmin": 0, "xmax": 1},
   #  "pTjet_prompt_lep": {"name": "pTjet_prompt_lep", "title": "pT_{lep}/pT_{jet}", "bin": 100, "xmin": 0, "xmax": 10},
   #  "pTjet_non_prompt_lep": {"name": "pTjet_non_prompt_lep", "title": "pT_{lep}/pT_{jet}", "bin": 100, "xmin": 0, "xmax": 10},
   #  "pTjet_all_lep": {"name": "pTjet_all_lep", "title": "pT_{lep}/pT_{jet}", "bin": 100, "xmin": 0, "xmax": 10},
   #  "pTjet_prompt_muons": {"name": "pTjet_prompt_muons", "title": "pT_{lep}/pT_{jet}", "bin": 100, "xmin": 0, "xmax": 10},
   #  "pTjet_prompt_electrons": {"name": "pTjet_prompt_electrons", "title": "pT_{lep}/pT_{jet}", "bin": 100, "xmin": 0, "xmax": 10},
   #  "pTjet_non_prompt_muons": {"name": "pTjet_non_prompt_muons", "title": "pT_{lep}/pT_{jet}", "bin": 100, "xmin": 0, "xmax": 10},
   #  "pTjet_non_prompt_electrons": {"name": "pTjet_non_prompt_electrons", "title": "pT_{lep}/pT_{jet}", "bin": 100, "xmin": 0, "xmax": 10},
   #  "pTjet_prompt_elec_vs_iso_elec": {
   #      "name": ["pTjet_prompt_electrons", "prompt_electrons_iso_dr02"],
   #      "title": "pT_{lep}/pT_{jet} vs Iso_{lep};pT_{lep}/pT_{jet};Iso_{lep}",
   #      "bin": [100, 100],
   #      "xmin": [0, 0],
   #      "xmax": [10, 1],
   #   },
   #   "pTjet_non_prompt_elec_vs_iso_elec": {
   #      "name": ["pTjet_non_prompt_electrons", "non_prompt_electrons_iso_dr02"],
   #      "title": "pT_{lep}/pT_{jet} vs Iso_{lep};pT_{lep}/pT_{jet};Iso_{lep}",
   #      "bin": [100, 100],
   #      "xmin": [0, 0],
   #      "xmax": [10, 1],
   #   },
   #   "pTjet_prompt_elec_vs_D0_sig_prompt_elec": {
   #      "name": ["pTjet_prompt_electrons", "abs_D0_sig_prompt_electrons"],
   #      "title": "pT_{lep}/pT_{jet} vs D0_{lep};pT_{lep}/pT_{jet};D0_{lep}",
   #      "bin": [100, 100],
   #      "xmin": [0, 0],
   #      "xmax": [10, 5],
   #   },
   #   "pTjet_non_prompt_elec_vs_D0_sig_non_prompt_elec": {
   #      "name": ["pTjet_non_prompt_electrons", "abs_D0_sig_non_prompt_electrons"],
   #      "title": "pT_{lep}/pT_{jet} vs D0_{lep};pT_{lep}/pT_{jet};D0_{lep}",
   #      "bin": [100, 100],
   #      "xmin": [0, 0],
   #      "xmax": [10, 5],
   #   },
}