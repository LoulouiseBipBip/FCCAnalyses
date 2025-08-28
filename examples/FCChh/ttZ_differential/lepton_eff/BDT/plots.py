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
outdir = "/eos/user/l/lberiet/Histmaker/ttZ_diff_results/BDT/histmaker/plots"
inputDir = "/eos/user/l/lberiet/Histmaker/ttZ_diff_results/BDT/histmaker"

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
    (208, 28, 139),  # pink 7
    (241, 182, 218),  # light pink 8
    (128, 205, 193),  # light blue 9
    (1, 133, 113),  # blue green 10
    (102, 102, 102),  # dark grey 11
    (255, 127, 0),  # orange 12
    (128, 128, 128),  # grey 13
]

# Create custom ROOT colors and store their indices
custom_color_indices = []
for i, (r, g, b) in enumerate(custom):
    color_index = 2000 + i  # Use indices starting from 2000 to avoid conflicts with ROOT's default colors
    ROOT.gROOT.ProcessLine(f"new TColor({color_index}, {r/255.0}, {g/255.0}, {b/255.0})")
    custom_color_indices.append(color_index)

colors = {}
colors["ttZ"] = ROOT.kBlack

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
    "mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep",],
    }
procs["backgrounds"] = {
    
    }

legend = {}
legend["ttZ"] = "ttZ"

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
    "processes": ["ttZ"],
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
    "processes": ["WZ", "ttZ", "tttt", "ZZ", "VVV", "VVVV", "ttV", "ttVV", "ttW", "ttH", "tt", "Z+j"],
    "density": False,
}

hists["n_leptons_pre_stack"] = {
    "input": "n_leptons_pre",
    "output": "n_leptons_pre_stack",
    "logy": True,
    "stack": False,
    "xtitle": "N_{leptons}",
    "xmin": -0.5,
    "xmax": 8.0,
    "ytitle": "Events",
    "processes": ["WZ", "ttZ", "tttt", "ZZ", "VVV", "VVVV", "ttV", "ttVV", "ttW", "ttH", "tt", "Z+j"],
    "density": False,
}

hists["muon_bdt_scores_hist"] = {
    "input": "muon_bdt_scores_hist",
    "output": "muon_bdt_scores_hist",
    "logy": True,
    "stack": False,
    "xtitle": "BDT score",
    "xmin": 0,
    "xmax": 1,
    "ytitle": "Events",
    "processes": ["ttZ"],
}
hists["electron_bdt_scores_hist"] = {
    "input": "electron_bdt_scores_hist",
    "output": "electron_bdt_scores_hist",
    "logy": True,
    "stack": False,
    "xtitle": "BDT score",
    "xmin": 0,
    "xmax": 1,
    "ytitle": "Events",
    "processes": ["ttZ"],
}

hists['n_leptons_bdt_stack'] = {
    'input': 'n_leptons_bdt_hist',
    'output': 'n_leptons_bdt_stack',
    'logy': True,
    'stack': False,
    'xtitle': 'N_{leptons}',
    'xmin': -0.5,
    'xmax': 8.5,
    'ytitle': 'Events',
    'processes': ["ttZ"],
    'density': False,
}


hists['Z_ll_pt_stack'] = {
    'input': 'Z_ll_pt_sel',
    'output': 'Z_ll_pt_stack',
    'logy': False,
    'stack': False,
    'xtitle': 'p_{T}(Z_{ll}) [GeV]',
    'xmin': 0,
    'xmax': 2500,
    "ymin": 0.01,
    "ymax": 1e6,
    'ytitle': 'Events / GeV',
    'processes':  ["ttZ"],
    'density': False,
    'divideByBinWidth': True,
    'rebin_last': True,
    'store_csv': True,
    'yrange_syst': (-0.15,0.15),
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
