import ROOT

L = 30
energy = 84
# global parameters
intLumi = 1.0
intLumiLabel = f"L = {L} ab^{{-1}}"
ana_tex = ""
delphesVersion = "3.4.2"
collider = "FCC-hh"
formats = ["png", "pdf"]

# outdir         = './outputs/plots/recoil/'
outdir = "/eos/user/l/lberiet/ttZ_diff_results/new_iso/plot"
inputDir = "/eos/user/l/lberiet/ttZ_diff_results/new_iso"

plotStatUnc = True

# Define custom colors using RGB values
custom = [
    (213, 62, 79),  # red 0
    (150, 150, 150),  # grey 1
    (253, 174, 97),  # orange 2
    (254, 224, 144),  # yellow 3
    (230, 245, 152),  # yg 4
    (26, 152, 80),  # green 5
    (50, 136, 189),  # blue 6
    (208, 28, 139),  # pink 7fccan
    (241, 182, 218),  # light pink 8
    (128, 205, 193),  # light blue 9
    (1, 133, 113),  # blue green 10
    (102, 102, 102),  # dark grey 11
]

# Create custom ROOT colors and store their indices
custom_color_indices = []
for i, (r, g, b) in enumerate(custom):
    color_index = 2000 + i  # Use indices starting from 2000 to avoid conflicts with ROOT's default colors
    ROOT.gROOT.ProcessLine(f"new TColor({color_index}, {r/255.0}, {g/255.0}, {b/255.0})")
    custom_color_indices.append(color_index)

colors = {}
colors["ttZ"] = ROOT.kBlack
# colors["tttt"] = custom_color_indices[0]
# colors["ZZjj"] = custom_color_indices[1]
# colors["VVV"] = custom_color_indices[2]
# colors["VVVV"] = custom_color_indices[3]
# colors["ttV"] = custom_color_indices[4]
# colors["ttVV"] = custom_color_indices[5]
# colors["ttH"] = custom_color_indices[6]
# colors["ttH_WW"] = custom_color_indices[6]
# colors["ttH_tauTau"] = custom_color_indices[7]
# colors["ttH_ZZ"] = custom_color_indices[8]
# colors["tt"] = custom_color_indices[9]
# colors["WZjj"] = custom_color_indices[10]
# colors["tt"] = custom_color_indices[11]

procs = {}

# 'mgp8_pp_tth_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_wwz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_wzz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_zzz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_wwwz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_wwww_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_wwzz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_wzzz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_zzzz_5f_84TeV': {"fraction": fraction},    
# 'mgp8_pp_ttw_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_ttz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_ttwz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_ttww_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_ttzz_5f_84TeV': {"fraction": fraction},
# 'mgp8_pp_tttt_5f_84TeV': {"fraction": fraction},

procs["signal"] = {
     "ttZ": ["mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep",
    "mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep",
    "mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep",
    "mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep"],
    
    }

procs["backgrounds"] = {
    # "tttt": ["mgp8_pp_tttt_5f_84TeV_4tlep"],
    # 'ZZjj': ["mgp8_pp_ZZjj_HF_5f_84TeV_zzlep"],
    # "VVV": ["mgp8_pp_wwz_5f_Q_0_1000_84TeV", "mgp8_pp_wzz_5f_Q_0_1000_84TeV", "mgp8_pp_zzz_5f_Q_0_1000_84TeV",
    #         "mgp8_pp_wwz_5f_Q_1000_3000_84TeV", "mgp8_pp_wwz_5f_Q_3000_10000_84TeV", "mgp8_pp_wwz_5f_Q_10000_84000_84TeV",
    #         "mgp8_pp_wzz_5f_Q_1000_3000_84TeV", "mgp8_pp_wzz_5f_Q_3000_10000_84TeV", "mgp8_pp_wzz_5f_Q_10000_84000_84TeV",
    #         "mgp8_pp_zzz_5f_Q_1000_3000_84TeV", "mgp8_pp_zzz_5f_Q_3000_10000_84TeV", "mgp8_pp_zzz_5f_Q_10000_84000_84TeV"],
    # "VVVV": ["mgp8_pp_wwwz_5f_84TeV", "mgp8_pp_wwww_5f_84TeV", "mgp8_pp_wwzz_5f_84TeV", "mgp8_pp_wzzz_5f_84TeV", "mgp8_pp_zzzz_5f_84TeV"],
    # 'ttH_WW': 
    #         ['mgp8_pp_tth_5f_Q_0_1000_84TeV_hww',
    #         'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hww',
    #         'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hww',
    #         'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hww'],
    # 'ttH_tauTau':       
    #         ['mgp8_pp_tth_5f_Q_0_1000_84TeV_htautau',
    #         'mgp8_pp_tth_5f_Q_1000_3000_84TeV_htautau',
    #         'mgp8_pp_tth_5f_Q_3000_10000_84TeV_htautau',
    #         'mgp8_pp_tth_5f_Q_10000_84000_84TeV_htautau'],

    # 'ttH_ZZ':       
    #         ['mgp8_pp_tth_5f_Q_0_1000_84TeV_hzz',
    #         'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hzz',
    #         'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hzz',
    #         'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hzz'],
    # "ttVV": ["mgp8_pp_ttwz_5f_84TeV",  "mgp8_pp_ttzz_5f_84TeV"],
    # "tt": ["mgp8_pp_tt_HT_2000_100000_5f_84TeV_blvblv", "mgp8_pp_tt_HT_200_2000_5f_84TeV_blvblv"],
    # "WZjj": ["mgp8_pp_WZjj_HF_5f_84TeV_wzlllv"],
    
    }

legend = {}
legend["ttZ"] = "ttZ"
# legend["ZZjj"] = "ZZjj"
# legend["tttt"] = "tttt"
# legend["VVV"] = "VVV"
# legend["VVVV"] = "VVVV"
# legend["ttV"] = "ttV"
# legend["ttVV"] = "ttVV"
# legend["ttH"] = "ttH"
# legend["ttH_WW"] = "ttH_WW"
# legend["ttH_tauTau"] = "ttH_tauTau"
# legend["ttH_ZZ"] = "ttH_ZZ"
# legend["WZjj"] = "WZjj"
# legend["tt"] = "tt"

hists = {}
hists2D = {}

# Diagnostic print to check which files and histograms are being accessed
print(f"Signal processes defined: {procs['signal']}")
print(f"Background processes defined: {procs['backgrounds']}")
print(f"Input directory: {inputDir}")

hists["cutFlow"] = {
    "input": "cutFlow",
    "output": "cutFlow",
    "logy": True,
    "stack": False,
    "ymax": 1e11,
    # "xmin": -0.5,
    # "xmax": 2.5,
    # "xtitle": selections,
    "ytitle": "Events",
    "processes": ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
}


hists["n_bjets_pre_stack"] = {
    "input": "n_bjets_pre",
    "output": "n_bjets_pre_stack",
    "logy": True,
    "stack": False,
    "xtitle": "N_{bjets}",
    "xmin": -0.5,
    "xmax": 10.5,
    "ytitle": "Events",
    "processes": ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    "density": False,
}

hists["n_leptons_pre_stack"] = {
    "input": "n_leptons_pre",
    "output": "n_leptons_pre_stack",
    "logy": True,
    "stack": False,
    "xtitle": "N_{leptons}",
    "xmin": -0.5,
    "xmax": 8,
    "ymin": 1e-1,
    "ymax": 1e13,
    "ytitle": "Events",
    "processes": ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    "density": False,
}

hists["n_bjets_pre_norm"] = {
    "input": "n_bjets_pre",
    "output": "n_bjets_pre_norm",
    "logy": False,
    "stack": False,
    "xtitle": "N_{bjets}",
    "xmin": -0.5,
    "xmax": 10.5,
    "ytitle": "Events",
    "processes": ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    "density": True,
}

hists["n_leptons_pre_norm"] = {
    "input": "n_leptons_pre",
    "output": "n_leptons_pre_norm",
    "logy": False,
    "stack": False,
    "xtitle": "N_{leptons}",
    "xmin": -0.5,
    "xmax": 10.5,
    "ytitle": "Events",
    "processes": ["ttZ"],#   ,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    "density": True,
}


hists["MET_stack"] = {
    "input": "MET_sel",
    "output": "MET_stack",
    "logy": True,
    "stack": False,
    "xtitle": "E_{T}^{miss} [GeV]",
    "xmin": 0,
    "xmax": 1000,
    "ytitle": "Events",
    "processes": ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    "density": False,
}

# hists["MET_norm"] = {
#     "input": "MET_sel",
#     "output": "MET_norm",
#     "logy": False,
#     "stack": False,
#     "xtitle": "E_{T}^{miss} [GeV]",
#     "xmin": 0,
#     "xmax": 1000,
#     "ytitle": "Events",
#     "processes": ["ttZ","ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
#     "density": True,
# }

hists["HT_sel_stack"] = {
    "input": "HT_sel",
    "output": "HT_sel_stack",
    "logy": True,
    "stack": False,
    "xtitle": "H_{T} [TeV]",
    "xmin": 0.5,
    "xmax": 2.5,
    "ymin": 1,
    "ymax": 1e6,
    "rebin_last": True,
    "store_csv": True,
    "yrange_syst": (-0.1,0.1),
    "ytitle": "Events / TeV",
    "processes": ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    "density": False,
    "divideByBinWidth": True,
}

hists["HT_stack"] = {
    "input": "HT",
    "output": "HT_stack",
    "logy": False,
    "stack": False,
    "xtitle": "H_{T} [TeV]",
    "xmin": 0.5,
    "xmax": 4.5,
    "ymin": 1,
    "ymax": 1e7,
    "ytitle": "Events / TeV",
    "processes": ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    "density": False,
    "divideByBinWidth": True,
    "rebin_last": True,
    "store_csv": True,
    "yrange_syst": (-0.1,0.1),
    "systematics": [
    {
        "signal": True,
        "process": "ttZ",
        "label": "muon id",
        "type": "shape",
        "hname": "muId",
        "color": custom_color_indices[8],            
    },
    {
        "signal": True,
        "process": "ttZ",
        "label": "electron id",
        "type": "shape",
        "hname": "eleId",
        "color": custom_color_indices[9],            
    },
    {
        "signal": True,
        "process": "ttZ",
        "label": "bjet id",
        "type": "shape",
        "hname": "bjetId",
        "color": custom_color_indices[10],            
    },    
    {
        "signal": True,
        "process": "ttZ",
        "label": "luminosity",
        "type": "const",
        "value": 0.01,
        "color": custom_color_indices[1],            
    },

    ]       
}


# hists["HT_norm"] = {
#     "input": "HT_sel",
#     "output": "HT_norm",
#     "logy": False,
#     "stack": False,
#     "xtitle": "H_{T} [TeV]",
#     "xmin": 0,
#     "xmax": 5,
#     "ytitle": "Events",
#     "processes": ["ttZ","ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
#     "density": True,
# }
# hists["Z_ll_pt_pre"] = {
#     "input": "Z_ll_pt_pre",
#     "output": "Z_ll_pt_pre",
#     "logy": True,
#     "stack": False,
#     "xtitle": "p_{T}(Z_{ll}) [GeV]",
#     "xmin": 0,
#     "xmax": 2500,
#     "ytitle": "Events",
#     "processes": ["ttZ","ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
#     "density": False,
# }
hists['Z_ll_pt_stack'] = {
    'input': 'Z_ll_pt_sel',
    'output': 'Z_ll_pt_stack',
    'logy': True,
    'stack': False,
    'xtitle': 'p_{T}(Z_{ll}) [GeV]',
    'xmin': 0,
    'xmax': 2500,
    "ymin": 0.01,
    "ymax": 1e3,
    'ytitle': 'Events / GeV',
    'processes': ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    'density': False,
    'divideByBinWidth': True,
    'rebin_last': True,
    'store_csv': True,
    'yrange_syst': (-0.5,0.5),
    "systematics": [
    {
        "signal": True,
        "process": "ttZ",
        "label": "muon id",
        "type": "shape",
        "hname": "muId",
        "color": custom_color_indices[8],            
    },
    {
        "signal": True,
        "process": "ttZ",
        "label": "electron id",
        "type": "shape",
        "hname": "eleId",
        "color": custom_color_indices[9],            
    },
    {
        "signal": True,
        "process": "ttZ",
        "label": "bjet id",
        "type": "shape",
        "hname": "bjetId",
        "color": custom_color_indices[10],            
    },    
    {
        "signal": True,
        "process": "ttZ",
        "label": "luminosity",
        "type": "const",
        "value": 0.01,
        "color": custom_color_indices[1],            
    },

    ]       

}

hists['Z_ll_pt_norm'] = {
    'input': 'Z_ll_pt_sel',
    'output': 'Z_ll_pt_norm',
    'logy': False,
    'stack': False,
    'xtitle': 'Z_{ll} p_{T} [GeV]',
    'xmin': 0,
    'xmax': 1000,
    'ytitle': 'Events',
    'processes': ["ttZ"],#,"ZZjj", "tttt", "VVV", "VVVV", "ttV", "ttVV", "ttH_WW", "ttH_tauTau", "ttH_ZZ", "WZjj", "tt"],
    'density': True,
}
