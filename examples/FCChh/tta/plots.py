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
outdir = "/eos/user/l/lberiet/Histmaker/tta/histos"
inputDir ="/eos/user/l/lberiet/Histmaker/tta"

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
colors["tta"] = custom_color_indices[0]

procs = {}


procs["signal"] = {
    "tta": [ "mgp8_pp_tta_5f_wlep_84TeV","mgp8_pp_tta_5f_pTa1500_wlep_84TeV"],
    }
procs["backgrounds"] = {
   
    }

legend = {}
legend["tta"] = "tta"

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
    "processes": ["tta"],
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
  "processes": ["tta"],
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
  "processes": ["tta"],
    "density": False,
}

hists["n_lep_b_from_top_pre_stack"] = {
    "input": "n_lep_b_from_top_pre",
    "output": "n_lep_b_from_top_pre_stack",
    "logy": True,
    "stack": False,
    "xtitle": "N_{lep_b_from_top}",
    "xmin": -0.5,
    "xmax": 10.5,
    "ytitle": "Events",
  "processes": ["tta"],
    "density": False,
}
hists['phot_pt_pre_stack'] = {
    'input': 'phot_pt_pre',
    'output': 'phot_pt_pre_stack',
    'logy': True,
    'stack': False,
    'xtitle': 'p_{T} [GeV]',
    'xmin': 500,
    'xmax': 2200,
    'ytitle': 'Events / GeV',
    "processes": ["tta"],
    'density': False,
    'divideByBinWidth': True,
    'rebin_last': True,
  
}

hists["pT_leptons_stack"] = {
    "input": "pT_leptons_sel",
    "output": "pT_leptons_stack",
    "logy": True,
    "stack": False,
    "xtitle": "pT [GeV]",
    "xmin": 0,
    "xmax": 2200,
    "ytitle": "Events",
    "processes": ["tta"],
    "density": False,
    "divideByBinWidth": True,
    "rebin_last": True,  
}

hists["phot_pt_stack"] = {
    "input": "phot_pt_sel",
    "output": "phot_pt_stack",
    "logy": True,
    "stack": False,
    "xtitle": "pT [GeV]",
    "xmin": 500,
    "xmax": 2200,
    "ymin": 0.01,
    "ymax": 1e5,
    "ytitle": "Events / GeV",
    "processes": ["tta"],
    'density': False,
    'divideByBinWidth': True,
    'rebin_last': True,
    'store_csv': True,
    'yrange_syst': (-0.5,0.5),
    "systematics": [
    {
        "signal": True,
        "process": "tta",
        "label": "muon id",
        "type": "shape",
        "hname": "muId",
        "color": custom_color_indices[8],            
    },
    {
        "signal": True,
        "process": "tta",
        "label": "electron id",
        "type": "shape",
        "hname": "eleId",
        "color": custom_color_indices[9],            
    },
    {
        "signal": True,
        "process": "tta",
        "label": "photon id",
        "type": "shape",
        "hname": "photId",
        "color": custom_color_indices[3],            
    },
    {
        "signal": True,
        "process": "tta",
        "label": "bjet id",
        "type": "shape",
        "hname": "bjetId",
        "color": custom_color_indices[10],            
    },    
    {
        "signal": True,
        "process": "tta",
        "label": "luminosity",
        "type": "const",
        "value": 0.01,
        "color": custom_color_indices[1],            
    },
    ]
}