import ROOT

# plot the mumu bkg sample in the separate HT slices

# global parameters
intLumi = 30e06  # in pb-1
ana_tex = "pp #rightarrow tttt 4l"
delphesVersion = "3.4.2"
energy = 84
collider = "FCC-hh"
inputDir = "/eos/user/l/lberiet/ttttfinal/"
formats = ["png"]
# formats        = ['png','pdf']
# yaxis          = ['log']
yaxis = ["lin", "log"]
# stacksig       = ['stack']
stacksig = ["stack", "nostack"]
outdir = "/eos/user/l/lberiet/www/4t_analysis/4l/SS_OF=0"
plotStatUnc = True


variables = ['n_bjets', 'n_leptons', 'HT', 'MET', 'n_of_ss_of_leptons', 'n_jets', 'Z_ll_mass', 'Second_Pair_mass', 'dR_ll']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['tttt_analysis']   = ["all_events","sel1_lep","sel_SS_OF=0","sel2_bjets","sel3_jets","sel4_notZ"]

extralabel = {}
extralabel['all_events'] = "All events" 
extralabel['sel1_lep'] = "Sel up to 4 leptons"
extralabel['sel_SS_OF=0'] = "Sel SS OF=0"

extralabel['sel2_bjets'] = "Sel 3 or more b-Jets"
extralabel['sel3_jets'] = "Sel 3 or more jets"
extralabel['sel4_notZ'] = "Sel 4 leptons not Z"


colors = {}
colors['tttt_signal'] = ROOT.kRed
colors['ttZ_bkg'] = ROOT.kGray
colors['ttH_bkg_lep'] = ROOT.kPink + 1
colors['ZZ_bkg_lep'] = ROOT.kViolet - 2
colors['VVV_bkg_lep'] = ROOT.kYellow - 7
colors['VVVV_bkg_lep'] = ROOT.kAzure +6
colors['ttVV_bkg_lep'] = ROOT.kTeal + 6


plots = {}
plots['tttt_analysis'] = {
                            'signal':{'tttt_signal':[ 
                                    'mgp8_pp_tttt_5f_84TeV_4tlep',

                            ]},
                            'backgrounds':{
                                'ttZ_bkg':[ 'mgp8_pp_ttz_5f_84TeV_ttzlep'],
                                'ttH_bkg_lep':[ 'mgp8_pp_tth_5f_84TeV'],
                                'ZZ_bkg_lep':[ 'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep'],
                                'VVV_bkg_lep':[ 'mgp8_pp_zzz_5f_84TeV', 'mgp8_pp_wzz_5f_84TeV', 'mgp8_pp_wwz_5f_84TeV'],
                                'VVVV_bkg_lep':[ 'mgp8_pp_wwww_5f_84TeV', 'mgp8_pp_wwwz_5f_84TeV', 'mgp8_pp_wwzz_5f_84TeV', 'mgp8_pp_wzzz_5f_84TeV', 'mgp8_pp_zzzz_5f_84TeV'],
                                'ttVV_bkg_lep':[ 'mgp8_pp_ttzz_5f_84TeV', 'mgp8_pp_ttwz_5f_84TeV'],
                            },
           }


legend = {}
legend['tttt_signal'] = 'tttt'
legend['ttZ_bkg'] = 'ttZ'
legend['ttH_bkg_lep'] = 'ttH'
legend['ZZ_bkg_lep'] = 'ZZ'
legend['VVV_bkg_lep'] = 'VVV'
legend['VVVV_bkg_lep'] = 'VVVV'
legend['ttVV_bkg_lep'] = 'ttVV'

