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
outdir = "/eos/user/l/lberiet/www/Histograms_Syst/4t/4l/"
plotStatUnc = True


variables = ['n_bjets', 'n_leptons', 'HT']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['tttt_analysis']   = ["all_events","sel1_lep","sel_SS_OF=0","sel2_bjets","sel3_jets","sel4_notZ"]

extralabel = {}
extralabel['all_events'] = "All events" 



colors = {}
colors['tttt_signal'] = ROOT.kRed
colors['ttZ'] = ROOT.kGray
colors['ttH_WW'] = ROOT.kBlue
colors['ttH_tauTau'] = ROOT.kBlue
colors['ttH_ZZ'] = ROOT.kBlue
colors['ttVV'] = ROOT.kBlue
colors['WZjj'] = ROOT.kBlue
colors['ZZjj'] = ROOT.kGreen
colors['VVV'] = ROOT.kOrange
colors['VVVV'] = ROOT.kPurple
colors['ttVV'] = ROOT.kPink
colors['WZjj'] = ROOT.kBrown


plots = {}
plots['tttt_analysis'] = {
                            'signal':{'tttt_signal':[ 
                                    'mgp8_pp_tttt_5f_84TeV_4tlep',

                            ]},
                            'backgrounds':{
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
                                'ttH_WW': 
                                        ['mgp8_pp_tth_5f_Q_0_1000_84TeV_hww',
                                        'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hww',
                                        'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hww',
                                        'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hww'],
                                'ttH_tauTau':       
                                        ['mgp8_pp_tth_5f_Q_0_1000_84TeV_htautau',
                                        'mgp8_pp_tth_5f_Q_1000_3000_84TeV_htautau',
                                        'mgp8_pp_tth_5f_Q_3000_10000_84TeV_htautau',
                                        'mgp8_pp_tth_5f_Q_10000_84000_84TeV_htautau'],

                                'ttH_ZZ':       
                                        ['mgp8_pp_tth_5f_Q_0_1000_84TeV_hzz',
                                        'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hzz',
                                        'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hzz',
                                        'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hzz'],
                                "ttH": ["mgp8_pp_tth_5f_Q_0_1000_84TeV_hww",
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
                                        'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hzz'],
                                "ttVV": ["mgp8_pp_ttwz_5f_84TeV",  "mgp8_pp_ttzz_5f_84TeV"],
                                "WZjj": ["mgp8_pp_WZjj_HF_5f_84TeV_wzlllv"],
           }


legend = {}
legend['tttt_signal'] = 'tttt'
legend['ttZ'] = 'ttZ'
legend['ZZjj'] = 'ZZjj'
legend['VVV'] = 'VVV'
legend['VVVV'] = 'VVVV'
legend['ttH_WW'] = 'ttH WW'
legend['ttH_tauTau'] = 'ttH tauTau'
legend['ttH_ZZ'] = 'ttH ZZ'
legend['ttH'] = 'ttH'
legend['ttVV'] = 'ttVV'
legend['WZjj'] = 'WZjj'

