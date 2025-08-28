import ROOT

L = 30
energy = 84
# global parameters
intLumi = 1.0
intLumiLabel = f"L = {L} ab^{{-1}}"
ana_tex = ""
delphesVersion = "3.4.2"
collider = "FCC-hh"
formats = ["pdf"]

# outdir         = './outputs/plots/recoil/'
outdir = "/eos/user/l/lberiet/www/Histograms_Syst/4t/3l/"
inputDir = "/eos/user/l/lberiet/Histmaker/tttt_v3/3l"

plotStatUnc = True

# Define custom colors using RGB values
custom = [
    (213, 62, 79),  # red 0
    (253, 174, 97),  # orange 1
    (254, 224, 144),  # yellow 2
    (230, 245, 152),  # yg 3
    (26, 152, 80),  # green 4
    (50, 136, 189),  # blue 5
    (208, 28, 139),  # pink 6
    (241, 182, 218),  # light pink 7
    (128, 205, 193),  # light blue 8
    (1, 133, 113),  # blue green 9
]

# Create custom ROOT colors and store their indices
custom_color_indices = []
for i, (r, g, b) in enumerate(custom):
    color_index = 2000 + i  # Use indices starting from 2000 to avoid conflicts with ROOT's default colors
    ROOT.gROOT.ProcessLine(f"new TColor({color_index}, {r/255.0}, {g/255.0}, {b/255.0})")
    custom_color_indices.append(color_index)

colors = {}
colors["tttt"] = ROOT.kBlack
colors["VVV"] = custom_color_indices[1]
colors["VVVV"] = custom_color_indices[2]
colors["ttVV"] = custom_color_indices[4]
colors["ttH"] = custom_color_indices[5]
colors["ttZ"] = custom_color_indices[3]
colors["ZZjj"] = custom_color_indices[6]

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
    "tttt": ["mgp8_pp_tttt_5f_84TeV_4tlep"],
    }
procs["backgrounds"] = {
    'ttZ': ['mgp8_pp_ttz_5f_84TeV_ttzlep'],
    'ZZjj': ["mgp8_pp_ZZjj_HF_5f_84TeV_zzlep"],
    "VVV": ["mgp8_pp_wwz_5f_84TeV", "mgp8_pp_wzz_5f_84TeV", "mgp8_pp_zzz_5f_84TeV"],
    "VVVV": ["mgp8_pp_wwwz_5f_84TeV", "mgp8_pp_wwww_5f_84TeV", "mgp8_pp_wwzz_5f_84TeV", "mgp8_pp_wzzz_5f_84TeV", "mgp8_pp_zzzz_5f_84TeV"],
    'ttH': ["mgp8_pp_tth_5f_Q_0_1000_84TeV", "mgp8_pp_tth_5f_Q_1000_3000_84TeV", "mgp8_pp_tth_5f_Q_3000_10000_84TeV", "mgp8_pp_tth_5f_Q_10000_84000_84TeV"],
    "ttVV": ["mgp8_pp_ttwz_5f_84TeV",  "mgp8_pp_ttzz_5f_84TeV"],
    }

legend = {}
legend["tttt"] = "tttt"
legend["ttZ"] = "ttZ"
legend["ZZjj"] = "ZZjj"
legend["VVV"] = "VVV"
legend["VVVV"] = "VVVV"
legend["ttVV"] = "ttVV"
legend["ttH"] = "ttH"

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
     "ymin": 1,
     "ymax": 1e10,
    # "xtitle": selections,
    "ytitle": "Events",
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
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
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
    "density": False,
}

hists["n_leptons_pre_stack"] = {
    "input": "n_leptons_pre",
    "output": "n_leptons_pre_stack",
    "logy": True,
    "stack": False,
    "xtitle": "N_{leptons}",
    "xmin": -0.5,
    "xmax": 10.5,
    "ytitle": "Events",
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
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
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
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
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
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
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
    "density": False,
}

hists["MET_norm"] = {
    "input": "MET_sel",
    "output": "MET_norm",
    "logy": False,
    "stack": False,
    "xtitle": "E_{T}^{miss} [GeV]",
    "xmin": 0,
    "xmax": 1000,
    "ytitle": "Events",
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
    "density": True,
}

hists["HT_sel_stack"] = {
    "input": "HT_sel",
    "output": "HT_sel_stack",
    "logy": True,
    "stack": False,
    "xtitle": "H_{T} [TeV]",
    "xmin": 0.5,
    "xmax": 6.0,
    "ymin": 1,
    "ymax": 1e6,
    "rebin_last": True,
    "store_csv": True,
    "yrange_syst": (-0.5,0.5),
    "ytitle": "Events / TeV",
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
    "density": False,
    "divideByBinWidth": True,
}

hists["HT_stack"] = {
    "input": "HT",
    "output": "HT_stack",
    "logy": True,
    "stack": False,
    "xtitle": "H_{T} [TeV]",
    "xmin": 0.5,
    "xmax": 6.0,
    "ymin": 1,
    "ymax": 1e4,
    "ytitle": "Events / TeV",
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
    "density": False,
    "divideByBinWidth": True,
    "rebin_last": True,
    "store_csv": True,
    "yrange_syst": (-0.5,0.5),
    "systematics": [
    {
        "signal": True,
        "process": "tttt",
        "label": "electron id",
        "type": "shape",
        "hname": "eleId",
        "color": custom_color_indices[7],            
    },
    {
        "signal": True,
        "process": "tttt",
        "label": "muon id",
        "type": "shape",
        "hname": "muId",
        "color": custom_color_indices[8],            
    },
    
    {
        "signal": True,
        "process": "tttt",
        "label": "bjet id",
        "type": "shape",
        "hname": "bjetId",
        "color": custom_color_indices[9],            
    },    
    {
        "signal": True,
        "process": "tttt",
        "label": "luminosity",
        "type": "const",
        "value": 0.01,
        "color": custom_color_indices[1],            
    },

    ]       
}


hists["HT_norm"] = {
    "input": "HT_sel",
    "output": "HT_norm",
    "logy": False,
    "stack": False,
    "xtitle": "H_{T} [TeV]",
    "xmin": 0,
    "xmax": 5,
    "ytitle": "Events",
    "processes": ["tttt", "VVV", "VVVV", "ttZ", "ttVV", "ttH", "ZZjj"],
    "density": True,
}


