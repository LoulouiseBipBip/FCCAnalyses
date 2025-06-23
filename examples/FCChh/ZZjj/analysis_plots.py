import ROOT

# plot the mumu bkg sample in the separate HT slices

# global parameters
intLumi = 30e06  # in pb-1
ana_tex = "pp #rightarrow ZZjj "
delphesVersion = "3.4.2"
energy = 84
collider = "FCC-hh"
inputDir = "/eos/user/l/lberiet/ZZjj_results/final/"
formats = ["png"]
# formats        = ['png','pdf']
# yaxis          = ['log']
yaxis = ["lin", "log"]
# stacksig       = ['stack']
stacksig = ["stack", "nostack"]
outdir = "/eos/user/l/lberiet/ZZjj_results/plot/"
plotStatUnc = True


variables = ['n_bjets', 'n_leptons', 'HT', 'MET', 'n_jets', 'pT_jets', 'Z_ll_and_second_pairs_size', 'Z_ll_1_mass', 'Z_ll_2_mass', 'dR_ll', 'pT_bjets', 'Z_ll_1_pt', 'Z_ll_2_pt', 'Z_ll_2_flavor']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZZjj_analysis']   = ["all_events", "sel1_lep","sel2_bjets","sel3_jets","sel4_Z_1","sel5_Z_2"] #,"sel1_lep","sel2_bjets","sel3_jets","sel4_notZ"]

extralabel = {}
extralabel['all_events'] = "All events" 
#extralabel['sel1_lep'] = "Sel up to 4 leptons"
#extralabel['sel2_bjets'] = "Sel 3 or more b-Jets"
#extralabel['sel3_jets'] = "Sel 3 or more jets"
#extralabel['sel4_Z_1'] = "Sel 4 leptons, first pair is Z"
#extralabel['sel5_Z_2'] = "Sel 4 leptons, second pair is Z"


colors = {}
colors['ZZjj_signal'] = ROOT.kRed
colors['ttZ_bkg'] = ROOT.kGray
colors['ttH_bkg_lep'] = ROOT.kPink + 1
colors['tttt_bkg_lep'] = ROOT.kOrange - 9
colors['VVV_bkg_lep'] = ROOT.kYellow - 7
colors['VVVV_bkg_lep'] = ROOT.kAzure +6
colors['ttVV_bkg_lep'] = ROOT.kTeal + 6


plots = {}
plots['ZZjj_analysis'] = {
                            'signal':{'ZZjj_signal':[ 
                                    'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep',

                            ]},
                            'backgrounds':{
                                'ttZ_bkg':[ 'mgp8_pp_ttz_5f_84TeV_ttzlep'],
                                'ttH_bkg_lep':[ 'mgp8_pp_tth_5f_84TeV'],
                                'tttt_bkg_lep':[ 'mgp8_pp_tttt_5f_84TeV_4tlep'],
                                'VVV_bkg_lep':[ 'mgp8_pp_zzz_5f_84TeV', 'mgp8_pp_wzz_5f_84TeV', 'mgp8_pp_wwz_5f_84TeV'],
                                'VVVV_bkg_lep':[ 'mgp8_pp_wwww_5f_84TeV', 'mgp8_pp_wwwz_5f_84TeV', 'mgp8_pp_wwzz_5f_84TeV', 'mgp8_pp_wzzz_5f_84TeV', 'mgp8_pp_zzzz_5f_84TeV'],
                                'ttVV_bkg_lep':[ 'mgp8_pp_ttzz_5f_84TeV', 'mgp8_pp_ttwz_5f_84TeV'],
                            },
           }


legend = {}
legend['ZZjj_signal'] = 'ZZjj'
legend['ttZ_bkg'] = 'ttZ'
legend['ttH_bkg_lep'] = 'ttH'
legend['tttt_bkg_lep'] = 'tttt'
legend['VVV_bkg_lep'] = 'VVV'
legend['VVVV_bkg_lep'] = 'VVVV'
legend['ttVV_bkg_lep'] = 'ttVV'

