import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttZ'
delphesVersion = '3.4.2'
energy         = 84
collider       = 'FCC-hh'
inputDir       = '/eos/user/l/lberiet/ttZ_diff_results/BDT/final/'
formats        = ['png'] #['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['nostack']
# stacksig       = ['stack','nostack']
outdir         = '/eos/user/l/lberiet/ttZ_diff_results/BDT/plots'
plotStatUnc    = True

variables = ['pTjet_prompt_muons', 'pTjet_prompt_electrons', 'pTjet_non_prompt_muons', 'pTjet_non_prompt_electrons']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttZ_analysis']   = ["all_events"]

extralabel = {}
extralabel['all_events'] = "All events" 

#extralabel['sel5_second_pair'] = "Sel second OS pair"

colors = {}
colors['ttZ_signal'] = ROOT.kRed


plots = {}
plots['ttZ_analysis'] = {
                            'signal':{'ttZ_signal':[ 'mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep', 'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep', 'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep', 'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep']},
                            'backgrounds':{
                                
                            },
           }


legend = {}
legend['ttZ_signal'] = 'ttZ'








