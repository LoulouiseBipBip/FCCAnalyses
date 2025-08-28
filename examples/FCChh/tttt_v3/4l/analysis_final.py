# Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lberiet/Histmaker/tttt_v3/4l/"
#inputDir = "/eos/user/s/selvaggi/analysis/ttbar_diff"

# Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lberiet/ttttfinal/"

processList = {
    'mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep',
    'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep',
    'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep',
    'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep',
    'mgp8_pp_ttw_5f_84TeV',
    'mgp8_pp_tttt_5f_84TeV_4tlep',
    'mgp8_pp_tth_5f_84TeV',

    'mgp8_pp_tth_5f_Q_0_1000_84TeV_hww',
    'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hww',
    'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hww',
    'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hww',
            
    'mgp8_pp_tth_5f_Q_0_1000_84TeV_htautau',
    'mgp8_pp_tth_5f_Q_1000_3000_84TeV_htautau',
    'mgp8_pp_tth_5f_Q_3000_10000_84TeV_htautau',
    'mgp8_pp_tth_5f_Q_10000_84000_84TeV_htautau',

    'mgp8_pp_tth_5f_Q_0_1000_84TeV_hzz',
    'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hzz',
    'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hzz',
    'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hzz',
    'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep',

    'mgp8_pp_WZjj_HF_5f_84TeV_wzlllv',

    'mgp8_pp_wzz_5f_Q_0_1000_84TeV',
    'mgp8_pp_wzz_5f_Q_1000_3000_84TeV',
    'mgp8_pp_wzz_5f_Q_3000_10000_84TeV',
    'mgp8_pp_wzz_5f_Q_10000_84000_84TeV',

    'mgp8_pp_zzz_5f_Q_0_1000_84TeV',
    'mgp8_pp_zzz_5f_Q_1000_3000_84TeV',
    'mgp8_pp_zzz_5f_Q_3000_10000_84TeV',
    'mgp8_pp_zzz_5f_Q_10000_84000_84TeV',
            

            
    'mgp8_pp_ttzz_5f_84TeV',
    'mgp8_pp_ttwz_5f_84TeV',

    #'mgp8_pp_tt_HT_2000_100000_5f_84TeV_blvblv',
    #'mgp8_pp_tt_HT_200_2000_5f_84TeV_blvblv',

    
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
    # "n_jets": {"name": "n_jets", "title": "n_jets", "bin": 10, "xmin": 0, "xmax": 10},
    "n_bjets": {"name": "n_bjets", "title": "n_bjets", "bin": 10, "xmin": 0, "xmax": 10},
    "n_leptons": {"name": "n_leptons", "title": "n_leptons", "bin": 10, "xmin": 0, "xmax": 10},
    
    "HT": {"name": "HT", "title": "H_{T} [TeV]", "bin": 100, "xmin": 0, "xmax": 8000},
    
    #"HT_sel": {"name": "HT_sel", "title": "H_{T} [TeV]", "bin": 50, "xmin": 0, "xmax": 2000},
    #"MET_sel": {"name": "MET_sel", "title": "MET", "bin": 20, "xmin": 0, "xmax": 2000},
}
