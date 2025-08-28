import array
# Input directory where the files produced at the pre-selection level are
inputDir =  "/eos/user/l/lberiet/ttZ_diff_results/BDT"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir =  "/eos/user/l/lberiet/ttZ_diff_results/BDT/final"

processList = {
    'mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep': {},
    'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep': {},
    'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep': {},
    'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep': {},   


    
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
    "all_events": "n_leptons >=0 ", # all events (no selection)
}
histoList = {
    "D0_sig_prompt_muons": {"name": "D0_sig_prompt_muons", "title": "D0 (prompt muons)", "bin": 50, "xmin": -10, "xmax": 10}, 
    "D0_sig_non_prompt_muons": {"name": "D0_sig_non_prompt_muons", "title": "D0 (non prompt muons)", "bin": 50, "xmin": -10, "xmax": 10}, 
    "D0_sig_prompt_electrons": {"name": "D0_sig_prompt_electrons", "title": "D0 (prompt electrons)", "bin": 50, "xmin": -10, "xmax": 10}, 
    "D0_sig_non_prompt_electrons": {"name": "D0_sig_non_prompt_electrons", "title": "D0 (non prompt electrons)", "bin": 50, "xmin": -10, "xmax": 10}, 

    "Z0_sig_prompt_muons": {"name": "Z0_sig_prompt_muons", "title": "Z0 (prompt muons)", "bin": 50, "xmin": -10, "xmax": 10}, 
    "Z0_sig_non_prompt_muons": {"name": "Z0_sig_non_prompt_muons", "title": "Z0 (non prompt muons)", "bin": 50, "xmin": -10, "xmax": 10}, 
    "Z0_sig_prompt_electrons": {"name": "Z0_sig_prompt_electrons", "title": "Z0 (prompt electrons)", "bin": 50, "xmin": -10, "xmax": 10}, 
    "Z0_sig_non_prompt_electrons": {"name": "Z0_sig_non_prompt_electrons", "title": "Z0 (non prompt electrons)", "bin": 50, "xmin": -10, "xmax": 10}, 

    # "pTjet_prompt_muons": {"name": "pTjet_prompt_muons", "title": "pT_{jet} (prompt muons)", "bin": 20, "xmin": 0, "xmax": 4}, 
    # "pTjet_prompt_electrons": {"name": "pTjet_prompt_electrons", "title": "pT_{jet} (prompt electrons)", "bin": 20, "xmin": 0, "xmax": 4}, 
    # "pTjet_non_prompt_muons": {"name": "pTjet_non_prompt_muons", "title": "pT_{jet} (non prompt muons)", "bin": 20, "xmin": 0, "xmax": 4}, 
    # "pTjet_non_prompt_electrons": {"name": "pTjet_non_prompt_electrons", "title": "pT_{jet} (non prompt electrons)", "bin": 20, "xmin": 0, "xmax": 4},

    "iso_dr01_prompt_muons": {"name": "iso_dr01_prompt_muons", "title": "iso_dr01 (prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr01_prompt_electrons": {"name": "iso_dr01_prompt_electrons", "title": "iso_dr01 (prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr01_non_prompt_muons": {"name": "iso_dr01_non_prompt_muons", "title": "iso_dr01 (non prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr01_non_prompt_electrons": {"name": "iso_dr01_non_prompt_electrons", "title": "iso_dr01 (non prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 

    "iso_dr02_prompt_muons": {"name": "iso_dr02_prompt_muons", "title": "iso_dr02 (prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr02_prompt_electrons": {"name": "iso_dr02_prompt_electrons", "title": "iso_dr02 (prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr02_non_prompt_muons": {"name": "iso_dr02_non_prompt_muons", "title": "iso_dr02 (non prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr02_non_prompt_electrons": {"name": "iso_dr02_non_prompt_electrons", "title": "iso_dr02 (non prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 

    "iso_dr03_prompt_muons": {"name": "iso_dr03_prompt_muons", "title": "iso_dr03 (prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr03_prompt_electrons": {"name": "iso_dr03_prompt_electrons", "title": "iso_dr03 (prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr03_non_prompt_muons": {"name": "iso_dr03_non_prompt_muons", "title": "iso_dr03 (non prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr03_non_prompt_electrons": {"name": "iso_dr03_non_prompt_electrons", "title": "iso_dr03 (non prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 

    "iso_dr04_prompt_muons": {"name": "iso_dr04_prompt_muons", "title": "iso_dr04 (prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr04_prompt_electrons": {"name": "iso_dr04_prompt_electrons", "title": "iso_dr04 (prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr04_non_prompt_muons": {"name": "iso_dr04_non_prompt_muons", "title": "iso_dr04 (non prompt muons)", "bin": 100, "xmin": 0, "xmax": 1}, 
    "iso_dr04_non_prompt_electrons": {"name": "iso_dr04_non_prompt_electrons", "title": "iso_dr04 (non prompt electrons)", "bin": 100, "xmin": 0, "xmax": 1}, 

}