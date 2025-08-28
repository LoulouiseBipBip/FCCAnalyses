import ROOT

# plot the mumu bkg sample in the separate HT slices

# global parameters
intLumi = 30e06  # in pb-1
ana_tex = "pp #rightarrow tta"
delphesVersion = "3.4.2"
energy = 84
collider = "FCC-hh"
inputDir = "/eos/user/l/lberiet/Histmaker/tta/final/"
formats = ["png"]
# formats        = ['png','pdf']
# yaxis          = ['log']
yaxis = ["lin", "log"]
# stacksig       = ['stack']
stacksig = ["nostack"]
outdir = "/eos/user/l/lberiet/Histmaker/tta/histos"
plotStatUnc = True


variables = [ 'lep_b_from_top_1_merged_mass','lep_b_from_top_2_merged_mass']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['tta_analysis']   = ["all_events"]#, "lep_b_pair=1"]

extralabel = {}
extralabel['all_events'] = "All events" 

#extralabel['lep_b_pair=1'] = "1 lep-b pair"



colors = {}
colors['tta_signal'] = ROOT.kRed



plots = {}
plots['tta_analysis'] = {
                            'signal':{'tta_signal':[ 
                                    'mgp8_pp_tta_5f_wlep_84TeV',

                            ]},
                            'backgrounds':{
           }
}

legend = {}
legend['tta_signal'] = 'tta'


