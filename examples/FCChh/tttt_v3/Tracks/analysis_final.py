# Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lberiet/Histmaker/tttt_v3/Tracks"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lberiet/Histmaker/tttt_v3/Tracks/final"

processList = {
       'mgp8_pp_tttt_wlep_Q_0_1000_5f_84TeV': {},
             'mgp8_pp_tttt_wlep_Q_1000_3000_5f_84TeV': {},
             'mgp8_pp_tttt_wlep_Q_3000_10000_5f_84TeV': {},
             'mgp8_pp_tttt_wlep_Q_10000_84000_5f_84TeV': {},
    
}

# Link to the dictonary that contains all the cross section informations etc...
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v06_II.json"
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
        "Iso_all_elec_vs_D0_sig_electrons": {
       "name": ["abs_D0_sig_electrons", "iso_all_elec"],
       "title": "D0_{sig_electrons} vs iso_{all_elec};D0_{sig_electrons};iso_{all_elec}",
       "bin": [100, 100],
       "xmin": [0, 0],
       "xmax": [4, 1]  
    },
       "Prompt_Iso_all_elec_vs_D0_sig_prompt_electrons": {
       "name": ["abs_D0_sig_prompt_electrons", "prompt_electrons_iso_dr02"],
       "title": "D0_{sig_prompt_electrons} vs iso_{all_elec};D0_{sig_prompt_electrons};iso_{all_elec}",
       "bin": [100, 100],
       "xmin": [0, 0],
       "xmax": [4, 1]  
    },
    "Non_Prompt_Iso_all_elec_vs_D0_sig_non_prompt_electrons": {
       "name": ["abs_D0_sig_non_prompt_electrons", "non_prompt_electrons_iso_dr02"],
       "title": "D0_{sig_non_prompt_electrons} vs iso_{all_elec};D0_{sig_non_prompt_electrons};iso_{all_elec}",
       "bin": [100, 100],
       "xmin": [0, 0],
       "xmax": [4, 1]  
    },
}
