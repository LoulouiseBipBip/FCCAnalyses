import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttZ'
delphesVersion = '3.4.2'
energy         = 84
collider       = 'FCC-hh'
inputDir       = '/eos/user/l/lberiet/ttZ_diff_results/finals2/'
formats        = ['png'] #['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
# stacksig       = ['stack','nostack']
outdir         = '/eos/user/l/lberiet/ttZ_diff_results/plot/'
plotStatUnc    = True

variables = ['Z_ll_mass', 'dR_ll', 'n_bjets', 'n_leptons', 'HT', 'MET', 'Second_Pair_flavor', 'Z_ll_and_second_pairs_size', 'Second_Pair_mass']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttZ_analysis']   = ["all_events","sel1_lep","sel2_bjets","sel3_njets","sel4_mll","sel5_second_pair"]

extralabel = {}
extralabel['all_events'] = "All events" 
extralabel['sel1_lep'] = "Sel 4 leptons"
extralabel['sel2_bjets'] = "Sel 1 or 2 b-Jets"
extralabel['sel3_njets'] = "Sel less than 6 jets"
extralabel['sel4_mll'] = "Sel Z mass between 80 and 100 GeV"
extralabel['sel5_second_pair'] = "Sel second OS pair"


colors = {}
colors['ttZ_signal'] = ROOT.kRed
colors['4t_bkg'] = ROOT.kYellow + 2
colors['ttH_bkg_lep'] = ROOT.kPink + 1
colors['ZZ_bkg_lep'] = ROOT.kViolet - 2
colors['VVV_bkg_lep'] = ROOT.kYellow - 7
colors['VVVV_bkg_lep'] = ROOT.kAzure +6
colors['ttVV_bkg_lep'] = ROOT.kTeal + 6


plots = {}
plots['ttZ_analysis'] = {
                            'signal':{'ttZ_signal':[ 'mgp8_pp_ttz_5f_84TeV_ttzlep']},
                            'backgrounds':{
                                '4t_bkg':[ 'mgp8_pp_tttt_5f_84TeV_4tlep'],
                                'ttH_bkg_lep':[ 'mgp8_pp_tth_5f_84TeV'],
                                'ZZ_bkg_lep':[ 'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep'],
                                'VVV_bkg_lep':[ 'mgp8_pp_zzz_5f_84TeV', 'mgp8_pp_wzz_5f_84TeV', 'mgp8_pp_wwz_5f_84TeV'],
                                'VVVV_bkg_lep':[ 'mgp8_pp_wwww_5f_84TeV', 'mgp8_pp_wwwz_5f_84TeV', 'mgp8_pp_wwzz_5f_84TeV', 'mgp8_pp_wzzz_5f_84TeV', 'mgp8_pp_zzzz_5f_84TeV'],
                                'ttVV_bkg_lep':[ 'mgp8_pp_ttzz_5f_84TeV', 'mgp8_pp_ttwz_5f_84TeV'],
                            },
           }


legend = {}
legend['ttZ_signal'] = 'ttZ'
legend['4t_bkg'] = '4t'
legend['ttH_bkg_lep'] = 'ttH'
legend['ZZ_bkg_lep'] = 'ZZ'
legend['VVV_bkg_lep'] = 'VVV'
legend['VVVV_bkg_lep'] = 'VVVV'
legend['ttVV_bkg_lep'] = 'ttVV'








