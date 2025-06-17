import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttZ'
delphesVersion = '3.4.2'
energy         = 84
collider       = 'FCC-hh'
inputDir       = '/eos/user/l/lberiet/ttZ_diff_results/finals2/'
formats        = ['png'] #['png','pdf']
yaxis          = ['log']
stacksig       = ['stack','nostack']
# stacksig       = ['stack','nostack']
outdir         = '/eos/user/l/lberiet/ttZ_diff_results/plotsiso/'
plotStatUnc    = True

variables = ['electron_noiso_var', 'electron_iso_var', 'muon_noiso_var', 'muon_iso_var']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttZ_analysis']   = ["all_events"]

extralabel = {}
extralabel['all_events'] = "All events" 



colors = {}
colors['ttZ_signal'] = ROOT.kRed
colors['4t_bkg'] = ROOT.kBlue
colors['ttH_bkg_lep'] = ROOT.kGreen 
colors['ZZ_bkg_lep'] = ROOT.kOrange

plots = {}
plots['ttZ_analysis'] = {
                            'signal':{'ttZ_signal':[ 'mgp8_pp_ttz_5f_84TeV_ttzlep']},
                            'backgrounds':{
                                '4t_bkg':[ 'mgp8_pp_tttt_5f_84TeV_4tlep'],
                                'ttH_bkg_lep':[ 'mgp8_pp_tth_5f_84TeV'],
                                'ZZ_bkg_lep':[ 'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep'],
                            
                            },
           }


legend = {}
legend['ttZ_signal'] = 'ttZ'
legend['4t_bkg'] = '4t'
legend['ttH_bkg_lep'] = 'ttH'
legend['ZZ_bkg_lep'] = 'ZZ'









