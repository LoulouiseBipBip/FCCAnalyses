import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttZ'
delphesVersion = '3.4.2'
energy         = 84
collider       = 'FCC-hh'
inputDir       =  "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/final/"
formats        = ['png'] #['png','pdf']
yaxis          = ['log','lin']
stacksig       = ['nostack']
# stacksig       = ['stack','nostack']
outdir         = '/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/iso'
plotStatUnc    = True

variables = ["diff_iso_muons"]#,"n_electron_iso_delphes","n_electrons_iso","n_muon_iso_delphes","n_prompt_muons_iso_dr03"] #, "prompt_muons_iso_dr03","prompt_electrons_iso_dr03","non_prompt_muons_iso_dr03","non_prompt_electrons_iso_dr03"]#,"non_prompt_muons_iso_dr03","prompt_electrons_iso_dr03","non_prompt_electrons_iso_dr03"]

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttZ_analysis']   = ["all_events"]#,"cluster_test"]#,"Iso_0","Iso_not_0"]#,"Zee","Zmm"]#,"lep_eta","lep_pt","lep_eta_pt"]#,"sel5_second_pair"]



extralabel = {}
extralabel['all_events'] = "All events" 
#extralabel['Iso_0'] = "Iso_0" 
#extralabel['Iso_not_0'] = "Iso_not_0" 
#extralabel['cluster_test'] = "Cluster test"

#extralabel['lep_eta_pt'] = "|#eta| < 4, p_{T} > 10 GeV"
#extralabel['Zmm'] = "Zmm"
#extralabel['Zee'] = "Zee"
#extralabel['lep_eta'] = "|#eta| < 4"
#extralabel['lep_pt'] = "p_{T} > 30 GeV"
#extralabel['lep_eta_pt'] = "|#eta| < 4, p_{T} > 30 GeV"


#extralabel['n_truth_taus_cut'] = "No tau"
#extralabel['sel5_second_pair'] = "Sel second OS pair"

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









