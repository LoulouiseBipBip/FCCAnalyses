import ROOT

L = 30
energy = 84
# global parameters
intLumi = 1.0
intLumiLabel = f"L = {L} ab^{{-1}}"
ana_tex = ""
delphesVersion = "3.4.2"
collider = "FCC-hh"
formats = ["png","pdf"]

# outdir         = './outputs/plots/recoil/'
outdir = "/eos/user/l/lberiet/www/Histograms_Syst/4t/4l/"
inputDir ="/eos/user/l/lberiet/Histmaker/tttt_v3/4l"

plotStatUnc = True
leg_position = [0.7, 0.7, 0.9, 0.9]
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
]

# Create custom ROOT colors and store their indices
custom_color_indices = []
for i, (r, g, b) in enumerate(custom):
    color_index = 2000 + i  # Use indices starting from 2000 to avoid conflicts with ROOT's default colors
    ROOT.gROOT.ProcessLine(f"new TColor({color_index}, {r/255.0}, {g/255.0}, {b/255.0})")
    custom_color_indices.append(color_index)

colors = {}
colors["tttt"] = ROOT.kBlack
colors["ttZ"] = custom_color_indices[0]
colors["ZZjj"] = custom_color_indices[7]
colors["VVV"] = custom_color_indices[2]
colors["VVVV"] = custom_color_indices[3]
colors["ttV"] = custom_color_indices[4]
colors["ttVV"] = custom_color_indices[5]
colors["ttH"] = custom_color_indices[6]
# colors["ttH_WW"] = custom_color_indices[6]
# colors["ttH_tauTau"] = custom_color_indices[7]
# colors["ttH_ZZ"] = custom_color_indices[8]
colors["tt"] = custom_color_indices[9]
colors["WZjj"] = custom_color_indices[10]
colors["tt"] = custom_color_indices[11]

procs = {}


procs["signal"] = {
    "tttt": ["mgp8_pp_tttt_5f_84TeV_4tlep"],
    }
procs["backgrounds"] = {
    'ttZ': ['mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep',
    'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep',
    'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep',
    'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep',],

    'ZZjj': ["mgp8_pp_ZZjj_HF_5f_84TeV_zzlep"],
    "VVV": [ 'mgp8_pp_wwz_5f_Q_0_1000_84TeV',
    'mgp8_pp_wwz_5f_Q_1000_3000_84TeV',
    'mgp8_pp_wwz_5f_Q_3000_10000_84TeV',
    'mgp8_pp_wwz_5f_Q_10000_84000_84TeV',

    'mgp8_pp_wzz_5f_Q_0_1000_84TeV',
    'mgp8_pp_wzz_5f_Q_1000_3000_84TeV',
    'mgp8_pp_wzz_5f_Q_3000_10000_84TeV',
    'mgp8_pp_wzz_5f_Q_10000_84000_84TeV',

    'mgp8_pp_zzz_5f_Q_0_1000_84TeV',
    'mgp8_pp_zzz_5f_Q_1000_3000_84TeV',
    'mgp8_pp_zzz_5f_Q_3000_10000_84TeV',
    'mgp8_pp_zzz_5f_Q_10000_84000_84TeV',],
    "VVVV": ["mgp8_pp_wwwz_5f_84TeV", "mgp8_pp_wwww_5f_84TeV", "mgp8_pp_wwzz_5f_84TeV", "mgp8_pp_wzzz_5f_84TeV", "mgp8_pp_zzzz_5f_84TeV"],
       'ttH': 
            ['mgp8_pp_tth_5f_Q_0_1000_84TeV_hww',
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
            'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hzz',],
    
    "ttVV": ["mgp8_pp_ttwz_5f_84TeV",  "mgp8_pp_ttzz_5f_84TeV"],
    "WZjj": ["mgp8_pp_WZjj_HF_5f_84TeV_wzlllv"],
   # "tt": ["mgp8_pp_tt_HT_2000_10000_5f_84TeV_blvblv", "mgp8_pp_tt_HT_200_2000_5f_84TeV_blvblv"],
    }

legend = {}
legend["tttt"] = "tttt"
legend["ttZ"] = "ttZ"
legend["ZZjj"] = "ZZjj"
legend["VVV"] = "VVV"
legend["VVVV"] = "VVVV"
legend["ttVV"] = "ttVV"
legend["ttH"] = "ttH"
# legend["ttH_WW"] = "ttH_WW"
# legend["ttH_tauTau"] = "ttH_tauTau"
# legend["ttH_ZZ"] = "ttH_ZZ"
legend["WZjj"] = "WZjj"
# legend["tt"] = "tt"
legend["WZjj"] = "WZjj"

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
    # "xmin": -0.5,
    # "xmax": 2.5,
    # "xtitle": selections,
    "ytitle": "Events",
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
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
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
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
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
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
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
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
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
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
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
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
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
    "density": True,
}

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
    "yrange_syst": (-0.5,0.5),
    "ytitle": "Events / TeV",
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
    "density": False,
    "divideByBinWidth": True,
}
hists["HT_pre"] = {
    "input": "HT_pre",
    "output": "HT_pre",
    "logy": True,
    "stack": False,
    "xtitle": "H_{T} [TeV]",
    "xmin": 0.5,
    "xmax": 2.5,
    "ymin": 1e-2,
}

hists["HT_stack"] = {
    "input": "HT",
    "output": "HT_stack",
    "logy": True,
    "stack": False,
    "xtitle": "H_{T} [TeV]",
    "xmin": 0.5,
    "xmax": 2.5,
    "ymin": 1e-2,
    "ymax": 1e7,
    "ytitle": "Events / TeV",
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
    "density": False,
    "divideByBinWidth": True,
    "rebin_last": True,
    "store_csv": True,
    "yrange_syst": (-0.7,0.7),
    "systematics": [
    {
        "signal": True,
        "process": "tttt",
        "label": "muon id",
        "type": "shape",
        "hname": "muId",
        "color": custom_color_indices[7],            
    },
    {
        "signal": True,
        "process": "tttt",
        "label": "electron id",
        "type": "shape",
        "hname": "eleId",
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
    "processes": ["tttt", "ttZ", "ZZjj", "VVV", "VVVV", "ttVV", "ttH", "WZjj"],
    "density": True,
}


