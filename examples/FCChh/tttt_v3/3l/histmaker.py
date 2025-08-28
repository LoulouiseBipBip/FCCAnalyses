import ROOT
import array
from multiprocessing import Pool, Manager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intLumi = 3e7

fraction = 0.1
debug = False

processList = {
    'mgp8_pp_tttt_5f_84TeV_4tlep':{},

    'mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep': {},
    'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep': {},
    'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep': {},
    'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep': {},
    
    'mgp8_pp_tth_5f_Q_0_1000_84TeV': {},
    'mgp8_pp_tth_5f_Q_1000_3000_84TeV': {},
    'mgp8_pp_tth_5f_Q_3000_10000_84TeV': {},
    'mgp8_pp_tth_5f_Q_10000_84000_84TeV': {},

    'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep': {},

    'mgp8_pp_wwz_5f_Q_0_1000_84TeV': {},
    'mgp8_pp_wwz_5f_Q_1000_3000_84TeV': {},
    'mgp8_pp_wwz_5f_Q_3000_10000_84TeV': {},
    'mgp8_pp_wwz_5f_Q_10000_84000_84TeV': {},

    'mgp8_pp_wzz_5f_Q_0_1000_84TeV': {},
    'mgp8_pp_wzz_5f_Q_1000_3000_84TeV': {},
    'mgp8_pp_wzz_5f_Q_3000_10000_84TeV': {},
    'mgp8_pp_wzz_5f_Q_10000_84000_84TeV': {},

    'mgp8_pp_zzz_5f_Q_0_1000_84TeV': {},
    'mgp8_pp_zzz_5f_Q_1000_3000_84TeV': {},
    'mgp8_pp_zzz_5f_Q_3000_10000_84TeV': {},
    'mgp8_pp_zzz_5f_Q_10000_84000_84TeV': {},
            
    'mgp8_pp_wwww_5f_84TeV': {},
    'mgp8_pp_wwwz_5f_84TeV': {},
    'mgp8_pp_wwzz_5f_84TeV': {},
    'mgp8_pp_wzzz_5f_84TeV': {},
    'mgp8_pp_zzzz_5f_84TeV': {},
            
    'mgp8_pp_ttzz_5f_84TeV': {},
    'mgp8_pp_ttwz_5f_84TeV': {},
    #"mgp8_pp_tt012j_5f_84TeV": {"fraction": fraction},
    
}

prodTag = "FCChh/fcc_v07/II/"
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json"
outputDir = "/eos/user/l/lberiet/Histmaker/tttt_v3/3l"
nCPUS = 16

bins_count = (50, -0.5, 49.5)
bins_ht = array.array('d', [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3.5])

def build_graph(df, dataset):
    results = []
    selections = []

    df = df.Define("weight", "EventHeader.weight")
    weightsum = df.Sum("weight")

    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("All events")

    df = df.Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)")
    df = df.Define("muon_noiso_var", "MuonNoIso_IsolationVar")
    df = df.Define("muon_iso_var", "Muon_IsolationVar")
    df = df.Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
    df = df.Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
    df = df.Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)")
    df = df.Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
    df = df.Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")
    df = df.Define("type_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_type(sel_muons)")

    df = df.Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
    df = df.Define("electron_noiso_var", "ElectronNoIso_IsolationVar")
    df = df.Define("electron_iso_var", "Electron_IsolationVar")
    df = df.Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
    df = df.Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
    df = df.Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)")
    df = df.Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
    df = df.Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")

    df = df.Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons, sel_electrons)")
    df = df.Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)")
    df = df.Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")
    df = df.Define("n_leptons", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")
    df = df.Define("Z_ll_and_second_pairs", "AnalysisFCChh::getZllAndSecondOSPair(sel_muons, sel_electrons)")
    df = df.Define("Z_ll_and_second_pairs_size", "Z_ll_and_second_pairs.size()")

    df = df.Define("sf_ss_of_leptons",  "AnalysisFCChh::findSameFlavorSameSignWithOppositeFlavor(sel_electrons, sel_muons)")
    df = df.Define("n_sf_ss_of_leptons",  "FCCAnalyses::ReconstructedParticle::get_n(sf_ss_of_leptons)")

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

    df = df.Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
    df = df.Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
    df = df.Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)")
    df = df.Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
    df = df.Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)")
    df = df.Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)")
    df = df.Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)")
    df = df.Define("phi_jets",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)")
    df = df.Define(
        "b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)"
    )
    df = df.Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
    df = df.Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
    df = df.Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")
    df = df.Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
    df = df.Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")

    df = df.Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")

    results.append(df.Histo1D(("n_bjets_pre", "", *bins_count), "n_bjets"))
    results.append(df.Histo1D(("n_leptons_pre", "", *bins_count), "n_leptons"))

    df = df.Filter("n_leptons == 3")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("N_{lep} == 3")

    df = df.Filter("n_bjets >= 4")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("N_{bjets} >= 4")

    df = df.Filter("n_sf_ss_of_leptons == 3")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("1 SF-SS pair + 1 OF single")


    
    #df = df.Filter("n_jets >= 3")
    #df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    #results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    #selections.append("N_{jets} >= 3")

    #df = df.Filter("Z_ll_mass < 80 || Z_ll_mass > 100")
   # df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
   # results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    #selections.append("Z_ll_mass < 80 || Z_ll_mass > 100")

    df = df.Define("HT", "ScalarHT")
    df = df.Define("ht_tev", "HT/1000.")

    results.append(df.Histo1D(("HT_sel", "", len(bins_ht) - 1, bins_ht), "ht_tev"))
    results.append(df.Histo1D(("MET_sel", "", 20, 0, 2000), "MET"))

    df = df.Define("wp_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, 1.0)")
    df = df.Define("wm_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, -1.0)")
    df = df.Define("wp_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_sel, 1.0, 1.0)")
    df = df.Define("wm_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_sel, 1.0, -1.0)")
    df = df.Define("wp_bjetId", "AnalysisFCChh::get_weight_emugamma_product(sel_bjets_pt, 3.0, 1.0)")
    df = df.Define("wm_bjetId", "AnalysisFCChh::get_weight_emugamma_product(sel_bjets_pt, 3.0, -1.0)")

    results.append(df.Histo1D(("HT", "", len(bins_ht) - 1, bins_ht), "ht_tev"))
    results.append(df.Histo1D(("HT_muId_wp", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wp_muId"))
    results.append(df.Histo1D(("HT_muId_wm", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wm_muId"))
    results.append(df.Histo1D(("HT_eleId_wp", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wp_eleId"))
    results.append(df.Histo1D(("HT_eleId_wm", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wm_eleId"))
    results.append(df.Histo1D(("HT_bjetId_wp", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wp_bjetId"))
    results.append(df.Histo1D(("HT_bjetId_wm", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wm_bjetId"))
    results.append(df.Histo1D(("MET", "", 20, 0, 2000), "MET"))

    from ROOT import TObjString
    selection_str = "\n".join(selections)
    selection_obj = TObjString(selection_str)
    for obj in results:
        h = obj.GetValue()
        if h.GetName() == "cutFlow":
            h.GetListOfFunctions().Add(selection_obj)
            break

    return results, weightsum

# --- Parallelization logic ---

def process_dataset(args):
    """
    Worker function for processing a single dataset in parallel.
    """
    dataset_name, dataset_info, shared_results = args
    try:
        logger.info(f"Processing dataset: {dataset_name}")
        # Load the DataFrame for the dataset using ROOT.RDataFrame
        # Assuming dataset_info might contain file paths or other metadata in the future
        # For now, we'll use a placeholder file path or tree name; adjust as needed
        file_path = f"/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/{dataset_name}/*.root"
        df = ROOT.RDataFrame("events", file_path)
        
        if df is None:
            logger.warning(f"Failed to load DataFrame for {dataset_name}, skipping.")
            return

        results, weightsum = build_graph(df, dataset_name)
        shared_results[dataset_name] = (results, float(weightsum.GetValue()))
        logger.info(f"Finished processing {dataset_name}")
    except Exception as e:
        logger.error(f"Error processing {dataset_name}: {e}")

def run_parallel(processList, ncpus=None):
    """
    Run the analysis in parallel over the processList using multiprocessing.
    """
    if ncpus is None or ncpus < 1:
        import os
        ncpus = os.cpu_count()
    logger.info(f"Running with {ncpus} CPUs")

    with Manager() as manager:
        shared_results = manager.dict()
        # Prepare arguments for each process
        args_list = []
        for dataset_name, dataset_info in processList.items():
            args_list.append((dataset_name, dataset_info, shared_results))
        with Pool(processes=ncpus) as pool:
            pool.map(process_dataset, args_list)
        # Convert shared_results to a normal dict for further processing
        results_dict = dict(shared_results)
    return results_dict

# Main entry point for running the analysis
if __name__ == "__main__":
    logger.info("Starting parallel analysis with histmaker.py")
    results_dict = run_parallel(processList, nCPUS)
    for ds, (results, weightsum) in results_dict.items():
        logger.info(f"Dataset: {ds}, Weightsum: {weightsum}")
    logger.info("Parallel analysis completed")
