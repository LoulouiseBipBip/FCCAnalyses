import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttZ'
delphesVersion = '3.4.2'
energy         = 84
collider       = 'FCC-hh'
inputDir       =  "/eos/user/l/lberiet/ttZ_diff_results/tracks/final/"
formats        = ['png'] #['png','pdf']
yaxis          = ['log','lin']
stacksig       = ['nostack']
# stacksig       = ['stack','nostack']
outdir         = '/eos/user/l/lberiet/ttZ_diff_results/tracks/plots'
plotStatUnc    = True

variables = ["Z0_sig_prompt_electrons","Z0_sig_non_prompt_electrons","Z0_sig_prompt_muons","Z0_sig_non_prompt_muons","Z0_sig_prompt_leptons","Z0_sig_non_prompt_leptons"]#,"n_electron_iso_delphes","n_electrons_iso","n_muon_iso_delphes","n_prompt_muons_iso_dr03"] #, "prompt_muons_iso_dr03","prompt_electrons_iso_dr03","non_prompt_muons_iso_dr03","non_prompt_electrons_iso_dr03"]#,"non_prompt_muons_iso_dr03","prompt_electrons_iso_dr03","non_prompt_electrons_iso_dr03"]

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttZ_analysis']   = [ "all_events"]



extralabel = {}
extralabel[ "all_events"] = "All events" 


colors = {}
colors['ttZ_signal'] = ROOT.kRed


plots = {}
plots['ttZ_analysis'] = {
                            'signal':{'ttZ_signal':[ 'mgp8_pp_ttz_5f_84TeV_ttzlep']},
                            'backgrounds':{
                                
                            },
           }


legend = {}
legend['ttZ_signal'] = 'ttZ'









