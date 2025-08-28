import ROOT

# plot the mumu bkg sample in the separate HT slices

# global parameters
intLumi = 30e06  # in pb-1
ana_tex = "pp #rightarrow tttt 4l"
delphesVersion = "3.4.2"
energy = 84
collider = "FCC-hh"
inputDir = "/eos/user/l/lberiet/Histmaker/tttt_v3/Tracks/final"
formats = ["png"]
# formats        = ['png','pdf']
# yaxis          = ['log']
yaxis = ["lin", "log"]
# stacksig       = ['stack']
stacksig = ["stack", "nostack"]
outdir = "/eos/user/l/lberiet/Histmaker/tttt_v3/Tracks/plots"
plotStatUnc = True


variables = []

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['tttt_analysis']   = ["all_events"]

extralabel = {}
extralabel['all_events'] = "All events" 



colors = {}
colors['tttt_signal'] = ROOT.kRed



plots = {}
plots['tttt_analysis'] = {
                            'signal':{'tttt_signal':[ 
                                    'mgp8_pp_tttt_5f_84TeV_4tlep',

                            ]},
                            'backgrounds':{
                            }
           }


legend = {}
legend['tttt_signal'] = 'tttt'


