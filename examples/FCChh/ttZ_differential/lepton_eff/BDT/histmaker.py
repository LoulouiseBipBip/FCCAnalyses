import ROOT
import array
import os
import numpy as np
import subprocess
from xgboost import XGBClassifier

intLumi = 3e7
fraction = 0.1
debug = False

processList = {
    'mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
}

procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json"
inputDir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II_trackCov/"
outputDir = "/eos/user/l/lberiet/Histmaker/ttZ_diff_results/BDT/histmaker"
nCPUS = -1
run_batch = True

# Load trained BDT models (optional, for reference)
bdt_mu = XGBClassifier()
bdt_mu.load_model("/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_muons.json")
bdt_e = XGBClassifier()
bdt_e.load_model("/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_electrons.json")
print("Loaded BDT models for muons and electrons")

# Set verbose error output for ROOT
ROOT.gErrorIgnoreLevel = ROOT.kPrint

# Add XGBoost library path to ROOT's dynamic path
xgboost_lib_path = "/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/xgboost/2.1.1-xijqyj/lib"
current_dynamic_path = ROOT.gSystem.GetDynamicPath()
if xgboost_lib_path not in current_dynamic_path.split(":"):
    new_dynamic_path = f"{xgboost_lib_path}:{current_dynamic_path}"
    ROOT.gSystem.SetDynamicPath(new_dynamic_path)
    #print(f"Added XGBoost library path {xgboost_lib_path} to ROOT dynamic path")
else:
    #print("XGBoost library path already in ROOT dynamic path")
    pass

# Add XGBoost include path to ROOT's interpreter
xgboost_include_path = "/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/xgboost/2.1.1-xijqyj/include"
ROOT.gInterpreter.AddIncludePath(xgboost_include_path)
print(f"Added XGBoost include path {xgboost_include_path} to ROOT interpreter")

# Load the shared library
library_path = "/afs/cern.ch/user/l/lberiet/MatteoCode/FCCAnalyses/examples/FCChh/ttZ_differential/lepton_eff/BDT/libBDTScorer.so"
if not os.path.exists(library_path):
    #print(f"Error: Library {library_path} does not exist")
    exit(1)
load_result = ROOT.gSystem.Load(library_path)
if load_result == 0:
    #print("Successfully loaded BDT scorer shared library")
    # Declare the computeBDTScores function to ROOT
    ROOT.gInterpreter.Declare('''
    #include <xgboost/c_api.h>
    #include <ROOT/RVec.hxx>
    ROOT::VecOps::RVec<float> computeBDTScores(
        ROOT::VecOps::RVec<float> d0, ROOT::VecOps::RVec<float> z0,
        ROOT::VecOps::RVec<float> iso1, ROOT::VecOps::RVec<float> iso2,
        ROOT::VecOps::RVec<float> iso3, ROOT::VecOps::RVec<float> iso4,
        ROOT::VecOps::RVec<float> pt, ROOT::VecOps::RVec<float> eta,
        const char* modelPath);
    ''')
    #print("Declared computeBDTScores function to ROOT")
else:
    #print("Failed to load BDT scorer shared library, return code:", load_result)
    #print("Dynamic path:", ROOT.gSystem.GetDynamicPath())
    #print("Library dependencies:")
    result = subprocess.run(["ldd", library_path], capture_output=True, text=True)
    #print(result.stdout)
    exit(1)



# ========================================================
# ========================================================

bins_count = (50, -0.5, 49.5)

def build_graph(df, dataset):
    results = []
    selections = []
    df = df.Define("weight", "EventHeader.weight")
    weightsum = df.Sum("weight")

    # cut 0: all events
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("All events")

    # Truth-level processing (unchanged)
    df = df.Define("mc_particles", "Particle")
    df = df.Alias("mc_parents", "_Particle_parents.index")
    df = df.Alias("mc_daughters", "_Particle_daughters.index")
    df = df.Define("electron_truth", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(mc_particles)")
    df = df.Define("muon_truth", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(mc_particles)")
    df = df.Define("tau_truth", "FCCAnalyses::MCParticle::sel_pdgID(15, true)(mc_particles)")
    df = df.Define("n_truth_taus", "tau_truth.size()")
    df = df.Filter("n_truth_taus == 0", "no_tau")

    df = df.Define("truth_leptons", "FCCAnalyses::MCParticle::mergeParticles(electron_truth, muon_truth)")
    df = df.Define("lepton_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(truth_leptons)")
    df = df.Define("n_truth_leptons_final", "lepton_truth_final.size()")
    df = df.Define("muons_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(muon_truth)")
    df = df.Define("electrons_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(electron_truth)")

    df = df.Define("truth_prompt_leptons", "FCCAnalyses::MCParticle::getPromptLeptons(mc_particles, lepton_truth_final, mc_parents)")
    df = df.Define("truth_prompt_electrons1", "FCCAnalyses::MCParticle::getPromptLeptons(mc_particles, electrons_truth_final, mc_parents)")

    df = df.Define("truth_prompt_e_first", "truth_prompt_electrons1.first")
    df = df.Define("truth_prompt_e_second", "truth_prompt_electrons1.second")
    df = df.Define("truth_prompt_electrons", "FCCAnalyses::MCParticle::mergeParticles(truth_prompt_e_first, truth_prompt_e_second)")
    df = df.Define("truth_prompt_muons1", "FCCAnalyses::MCParticle::getPromptLeptons(mc_particles, muons_truth_final, mc_parents)")
    df = df.Define("truth_prompt_mu_first", "truth_prompt_muons1.first")
    df = df.Define("truth_prompt_mu_second", "truth_prompt_muons1.second")
    df = df.Define("truth_prompt_muons", "FCCAnalyses::MCParticle::mergeParticles(truth_prompt_mu_first, truth_prompt_mu_second)")
    df = df.Define("truth_non_prompt_electrons", "FCCAnalyses::MCParticle::getNonPromptLeptons(mc_particles, electrons_truth_final, mc_parents)")
    df = df.Define("truth_prompt_lep_merged", "FCCAnalyses::MCParticle::mergeParticles(truth_prompt_electrons, truth_prompt_muons)")
    df = df.Define("truth_prompt_lep_merged_size", "truth_prompt_lep_merged.size()")
    df = df.Define("truth_non_prompt_muons", "FCCAnalyses::MCParticle::getNonPromptLeptons(mc_particles, muons_truth_final, mc_parents)")
    df = df.Define("truth_non_prompt_leptons_pre", "FCCAnalyses::MCParticle::mergeParticles(truth_non_prompt_electrons, truth_non_prompt_muons)")
    df = df.Define("truth_non_prompt_leptons_sel_pt", "FCCAnalyses::MCParticle::sel_pt(1.)(truth_non_prompt_leptons_pre)")
    df = df.Define("truth_non_prompt_leptons", "FCCAnalyses::MCParticle::sel_eta(6)(truth_non_prompt_leptons_sel_pt)")
    df = df.Define("truth_non_prompt_lep_size", "truth_non_prompt_leptons.size()")

    # Reco-level processing
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get(MuonNoIso_objIdx.index, ReconstructedParticles)")
    df = df.Define("muon_noiso_var", "MuonNoIso_IsolationVar")
    df = df.Define("muon_iso_var", "Muon_IsolationVar")
    df = df.Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
    df = df.Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
    df = df.Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)")
    df = df.Define("pT_muons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")
    df = df.Define("eta_muons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_muons)")
    df = df.Define("phi_muons_sel", "FCCAnalyses::ReconstructedParticle::get_phi(sel_muons)")

    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso_objIdx.index, ReconstructedParticles)")
    df = df.Define("electron_noiso_var", "ElectronNoIso_IsolationVar")
    df = df.Define("electron_iso_var", "Electron_IsolationVar")
    df = df.Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
    df = df.Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
    df = df.Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)")
    df = df.Define("n_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
    df = df.Define("pT_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")
    df = df.Define("eta_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_electrons)")
    df = df.Define("phi_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_phi(sel_electrons)")

    df = df.Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons, sel_electrons)")
    df = df.Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)")
    df = df.Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")

    # Define jets (ensure this is present before BDT variables)
    df = df.Define("sel_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
    df = df.Define("n_jets", "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
    df = df.Define("pT_jets", "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)")
    df = df.Define(
        "b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)"
    )  # bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
    # select medium b-jets with pT > 30 GeV, |eta| < 4
    df = df.Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
    df = df.Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
    df = df.Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")  # sort by pT
    df = df.Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
    df = df.Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")

    # Remove leptons from the collection of all reconstructed particles
    df = df.Define("RP_no_lep", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, sel_leptons)")

    # Reco matching
    df = df.Define("matched_prompt_electrons", "AnalysisFCChh::find_reco_matches(truth_prompt_electrons, sel_electrons, 0.1)")
    df = df.Define("matched_prompt_electrons_size", "matched_prompt_electrons.size()")
    df = df.Define("matched_non_prompt_electrons", "AnalysisFCChh::find_reco_matches(truth_non_prompt_electrons, sel_electrons, 0.1)")
    df = df.Define("matched_non_prompt_electrons_size", "matched_non_prompt_electrons.size()")
    df = df.Define("matched_prompt_muons", "AnalysisFCChh::find_reco_matches(truth_prompt_muons, sel_muons, 0.1)")
    df = df.Define("matched_prompt_muons_size", "matched_prompt_muons.size()")
    df = df.Define("matched_non_prompt_muons", "AnalysisFCChh::find_reco_matches(truth_non_prompt_muons, sel_muons, 0.1)")
    df = df.Define("matched_non_prompt_muons_size", "matched_non_prompt_muons.size()")
    df = df.Define("matched_prompt_lep", "FCCAnalyses::ReconstructedParticle::merge(matched_prompt_electrons, matched_prompt_muons)")
    df = df.Define("matched_non_prompt_lep", "FCCAnalyses::ReconstructedParticle::merge(matched_non_prompt_electrons, matched_non_prompt_muons)")
    df = df.Define("n_leptons", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")

    # BDT variables
    df = df.Define("pT_prompt_electrons", "FCCAnalyses::ReconstructedParticle::get_pt(matched_prompt_electrons)")
    df = df.Define("pT_non_prompt_electrons", "FCCAnalyses::ReconstructedParticle::get_pt(matched_non_prompt_electrons)")
    df = df.Define("pT_prompt_muons", "FCCAnalyses::ReconstructedParticle::get_pt(matched_prompt_muons)")
    df = df.Define("pT_non_prompt_muons", "FCCAnalyses::ReconstructedParticle::get_pt(matched_non_prompt_muons)")
    df = df.Define("pT_prompt_leptons", "FCCAnalyses::ReconstructedParticle::get_pt(matched_prompt_lep)")
    df = df.Define("pT_non_prompt_leptons", "FCCAnalyses::ReconstructedParticle::get_pt(matched_non_prompt_lep)")

    # BDT features
    df = df.Define("D0_sig_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(sel_electrons, _EFlowTrack_trackStates)")
    df = df.Define("Z0_sig_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_Z0_sig(sel_electrons, _EFlowTrack_trackStates)")
    df = df.Define("iso_dr01_electrons", "AnalysisFCChh::get_IP_delphes(sel_electrons, RP_no_lep, 0.1, 0.5)")
    df = df.Define("iso_dr02_electrons", "AnalysisFCChh::get_IP_delphes(sel_electrons, RP_no_lep, 0.2, 0.5)")
    df = df.Define("iso_dr03_electrons", "AnalysisFCChh::get_IP_delphes(sel_electrons, RP_no_lep, 0.3, 0.5)")
    df = df.Define("iso_dr04_electrons", "AnalysisFCChh::get_IP_delphes(sel_electrons, RP_no_lep, 0.4, 0.5)")

    df = df.Define("D0_sig_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(sel_muons, _EFlowTrack_trackStates)")
    df = df.Define("Z0_sig_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_Z0_sig(sel_muons, _EFlowTrack_trackStates)")
    df = df.Define("iso_dr01_muons", "AnalysisFCChh::get_IP_delphes(sel_muons, RP_no_lep, 0.1, 0.5)")
    df = df.Define("iso_dr02_muons", "AnalysisFCChh::get_IP_delphes(sel_muons, RP_no_lep, 0.2, 0.5)")
    df = df.Define("iso_dr03_muons", "AnalysisFCChh::get_IP_delphes(sel_muons, RP_no_lep, 0.3, 0.5)")
    df = df.Define("iso_dr04_muons", "AnalysisFCChh::get_IP_delphes(sel_muons, RP_no_lep, 0.4, 0.5)")

    # Compute BDT scores
    # NOTE: Features are not scaled here as they are in BDT.py. For accurate scores, features should be scaled using the same StandardScaler mean and std as in training. This is a known issue causing discrepancies in BDT score distributions.
    df = df.Define("muon_bdt_scores", "computeBDTScores(D0_sig_muons, Z0_sig_muons, iso_dr01_muons, iso_dr02_muons, iso_dr03_muons, iso_dr04_muons, pT_muons_sel, eta_muons_sel, \"/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_muons.json\")")
    df = df.Define("electron_bdt_scores", "computeBDTScores(D0_sig_electrons, Z0_sig_electrons, iso_dr01_electrons, iso_dr02_electrons, iso_dr03_electrons, iso_dr04_electrons, pT_electrons_sel, eta_electrons_sel, \"/eos/user/l/lberiet/ttZ_diff_results/BDT/bdt_model_electrons.json\")")

    # Apply BDT selection
    # Using Youden point thresholds from BDT.py (replace with actual values from your latest BDT.py run)
    muon_threshold = 0.969  # Placeholder, update with actual Youden point for muons
    df = df.Define("sel_muons_bdt", f"sel_muons[muon_bdt_scores > {muon_threshold}]")
    electron_threshold = 0.931  # Placeholder, update with actual Youden point for electrons
    df = df.Define("sel_electrons_bdt", f"sel_electrons[electron_bdt_scores > {electron_threshold}]")
    df = df.Define("sel_leptons_bdt_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons_bdt, sel_electrons_bdt)")
    df = df.Define("sel_leptons_bdt", "AnalysisFCChh::SortParticleCollection(sel_leptons_bdt_unsort)")
    df = df.Define("n_leptons_bdt", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons_bdt)")

    # Debug histograms for BDT scores
    results.append(df.Histo1D(("muon_bdt_scores_hist", "", 50, 0, 1), "muon_bdt_scores"))
    results.append(df.Histo1D(("electron_bdt_scores_hist", "", 50, 0, 1), "electron_bdt_scores"))
    results.append(df.Histo1D(("n_leptons_bdt_hist", "", *bins_count), "n_leptons_bdt"))

    # Rest of your build_graph
    df = df.Define("Z_ll_and_second_pairs", "AnalysisFCChh::getZllAndSecondOSPair(sel_muons_bdt, sel_electrons_bdt)")
    df = df.Define("Z_ll_and_second_pairs_size", "Z_ll_and_second_pairs.size()")
    df = df.Define('Z_ll_and_second_pairs_merged', 'AnalysisFCChh::merge_pairs(Z_ll_and_second_pairs)')
    df = df.Define('Z_ll_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[0]')
    df = df.Define('Z_ll_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[0]')
    df = df.Define('Z_ll_eta', 'FCCAnalyses::ReconstructedParticle::get_eta(Z_ll_and_second_pairs_merged)[0]')
    df = df.Define('Z_ll_flavor', 'Z_ll_and_second_pairs[0].flavour_flag')
    df = df.Define('Second_Pair_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[1]')
    df = df.Define('Second_Pair_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[1]')
    df = df.Define('Second_Pair_eta', 'FCCAnalyses::ReconstructedParticle::get_eta(Z_ll_and_second_pairs_merged)[1]')
    df = df.Define('Second_Pair_flavor', 'Z_ll_and_second_pairs[1].flavour_flag')
    df = df.Define('dR_ll', 'AnalysisFCChh::get_angularDist_pair(Z_ll_and_second_pairs, TString(\"dR\"))[0]')
    df = df.Define('dR_second_pair', 'AnalysisFCChh::get_angularDist_pair(Z_ll_and_second_pairs, TString(\"dR\"))[1]')

    df = df.Define("HT", "pT_leptons_sel[0] + pT_leptons_sel[1] + pT_leptons_sel[2] + pT_leptons_sel[3] + sel_bjets_pt[0] + sel_bjets_pt[1]")
    df = df.Define("ht_tev", "HT/1000.")


    results.append(df.Histo1D(("n_bjets_pre", "", *bins_count), "n_bjets"))
    results.append(df.Histo1D(("n_leptons_pre", "", *bins_count), "n_leptons"))

    # Filter events based on BDT-selected leptons
    df = df.Filter("n_leptons_bdt == 4")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("N_{lep} = 4 ")

    df = df.Filter("n_bjets >= 1 && n_bjets <= 2")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("1 or 2 b-jets")

    df = df.Filter("Z_ll_mass > 80. && Z_ll_mass < 100.")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("|N_{ll} - m_{Z}| < 10 GeV")

    df = df.Filter("Second_Pair_flavor == 3")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("Second pair is OF")


    df = df.Define("wp_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, 1.0)")
    df = df.Define("wm_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, -1.0)")
    df = df.Define("wp_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_sel, 1.0, 1.0)")
    df = df.Define("wm_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_sel, 1.0, -1.0)")
    df = df.Define("wp_bjetId", "AnalysisFCChh::get_weight_emugamma_product(sel_bjets_pt, 3.0, 1.0)")
    df = df.Define("wm_bjetId", "AnalysisFCChh::get_weight_emugamma_product(sel_bjets_pt, 3.0, -1.0)")

   

    bins_zpt = array.array('d', [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 650.0, 800.0, 1000.0, 1300.0, 1800.0, 2500.0])
    results.append(df.Histo1D(("Z_ll_pt_sel", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt"))
    results.append(df.Histo1D(("Z_ll_pt_sel_eleId_wp", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wp_eleId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_eleId_wm", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wm_eleId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_muId_wp", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wp_muId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_muId_wm", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wm_muId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_bjetId_wp", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wp_bjetId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_bjetId_wm", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wm_bjetId"))

    from ROOT import TObjString
    selection_str = "\n".join(selections)
    selection_obj = TObjString(selection_str)
    for obj in results:
        h = obj.GetValue()
        if h.GetName() == "cutFlow":
            h.GetListOfFunctions().Add(selection_obj)
            break

    return results, weightsum

def save_results(results, output_file):
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    file = ROOT.TFile(output_file, "RECREATE")
    for hist in results:
        h = hist.GetValue()
        h.Write()
    file.Close()
    logger.info(f"Saved results to {output_file}")

if __name__ == "__main__":
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("Starting parallel analysis with histmaker.py")
    results_dict = run_parallel(processList, nCPUS)
    for ds, (results, weightsum) in results_dict.items():
        logger.info(f"Dataset: {ds}, Weightsum: {weightsum}")
        output_file = os.path.join(outputDir, f"{ds}_4l.root")
        save_results(results, output_file)
    logger.info("Parallel analysis completed")
