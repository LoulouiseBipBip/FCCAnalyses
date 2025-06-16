import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttZ'
delphesVersion = '3.4.2'
energy         = 84
collider       = 'FCC-hh'
inputDir       = '/eos/user/l/lberiet/ttZ_diff_results/final/'
formats        = ['png'] #['png','pdf']
yaxis          = ['log']
stacksig       = ['stack','nostack']
# stacksig       = ['stack','nostack']
outdir         = '/eos/user/l/lberiet/ttZ_diff_results/plots/'
plotStatUnc    = True

variables = ['Z_ll_mass', 'dR_ll', 'n_jets', 'n_leptons', 'HT', 'MET']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttZ_analysis']   = ["sel1","sel2_lep","sel3_jets","sel4_mll"]

extralabel = {}
extralabel['sel1'] = "No Selection"
extralabel['sel2_lep'] = "Sel 3 or 4 leptons"
extralabel['sel3_jets'] = "Sel 1 or 2 jets"
extralabel['sel4_mll'] = "Sel Z mass"

colors = {}
colors['ttZ_signal'] = ROOT.kRed
colors['4t_bkg'] = ROOT.kBlue
colors['ttH_bkg_lep'] = ROOT.kGreen 


plots = {}
plots['ttZ_analysis'] = {
                            'signal':{'ttZ_signal':[ 'mgp8_pp_ttz_5f_84TeV_ttzlep']},
                            'backgrounds':{
                                '4t_bkg':[ 'mgp8_pp_tttt_5f_84TeV_4tlep'],
                                'ttH_bkg_lep':[ 'mgp8_pp_tth_5f_84TeV'],
                            
                            },
           }


legend = {}
legend['ttZ_signal'] = 'ttZ'
legend['4t_bkg'] = '4t'
legend['ttH_bkg_lep'] = 'ttH'