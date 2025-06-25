import ROOT

# plot the mumu bkg sample in the separate HT slices

# global parameters
intLumi = 30e06  # in pb-1
ana_tex = "pp #rightarrow tttt 3l"
delphesVersion = "3.4.2"
energy = 84
collider = "FCC-hh"
inputDir = "/eos/user/l/lberiet/newttttresult/3l/sf_ss=0_sel/histo/"
formats = ["png"]
# formats        = ['png','pdf']
# yaxis          = ['log']
yaxis = ["lin", "log"]
# stacksig       = ['stack']
stacksig = ["stack", "nostack"]
outdir = "/eos/user/l/lberiet/newttttresult/3l/sf_ss=0_sel/plot/"
plotStatUnc = True


variables = ['n_bjets', 'n_leptons', 'HT', 'MET', 'n_sf_ss_of_leptons', 'n_jets', 'Z_ll_mass', 'Second_Pair_mass', 'dR_ll']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['tttt_analysis_3l_sf_ss=0']   = ["all_events","sel0_sf_ss","sel1_sf_ss","sel2_bjets","sel3_jets","sel4_notZ"]

extralabel = {}
extralabel['all_events'] = "All events" 
extralabel['sel0_sf_ss'] = "Sel 3 leptons"
extralabel['sel1_sf_ss'] = "Sel 0 SFSS OS leptons"
extralabel['sel2_bjets'] = "Sel 3 or more b-Jets"
extralabel['sel3_jets'] = "Sel 6 or more jets"
extralabel['sel4_notZ'] = "Not Z"
#extralabel['sel5_sf_ss'] = "SFSS leptons and 1 OS lepton"


colors = {}
colors['tttt_signal'] = ROOT.kRed
colors['ttZ_bkg'] = ROOT.kGray
colors['ttH_bkg_lep'] = ROOT.kPink + 1
colors['ZZ_bkg_lep'] = ROOT.kViolet - 2
colors['VVV_bkg_lep'] = ROOT.kYellow - 7
colors['VVVV_bkg_lep'] = ROOT.kAzure +6
colors['ttVV_bkg_lep'] = ROOT.kTeal + 6


plots = {}
plots['tttt_analysis_3l_sf_ss=0'] = {
                            'signal':{'tttt_signal':[ 
                                    'mgp8_pp_tttt_wmlep_Q_0_1000_5f_84TeV',
                                    'mgp8_pp_tttt_wmlep_Q_1000_3000_5f_84TeV',
                                    'mgp8_pp_tttt_wmlep_Q_3000_10000_5f_84TeV',
                                    'mgp8_pp_tttt_wmlep_Q_10000_84000_5f_84TeV',
                                    'mgp8_pp_tttt_wplep_Q_0_1000_5f_84TeV',
                                    'mgp8_pp_tttt_wplep_Q_1000_3000_5f_84TeV',
                                    'mgp8_pp_tttt_wplep_Q_3000_10000_5f_84TeV',
                                    'mgp8_pp_tttt_wplep_Q_10000_84000_5f_84TeV',

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

