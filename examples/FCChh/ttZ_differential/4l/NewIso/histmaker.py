import ROOT
import array

intLumi = 3e7

fraction = 0.1
debug = False

# check Nl in inclusive 4t 
# eemumu same sign 
# check normalizations 
# DR bparton vs lepton reco 
# check analysis without isolation 




processList = {
   #'mgp8_pp_ttz_5f_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    'mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_ttw_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
    #        'mgp8_pp_tttt_5f_84TeV_4tlep': {"fraction": fraction, 'Chunks': 50},
    #    #      'mgp8_pp_tth_5f_84TeV': {"fraction": fraction, 'Chunks': 50},

    #         'mgp8_pp_tth_5f_Q_0_1000_84TeV_hww': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hww': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hww': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hww': {"fraction": fraction, 'Chunks': 50},
            
    #         'mgp8_pp_tth_5f_Q_0_1000_84TeV_htautau': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_1000_3000_84TeV_htautau': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_3000_10000_84TeV_htautau': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_10000_84000_84TeV_htautau': {"fraction": fraction, 'Chunks': 50},

    #         'mgp8_pp_tth_5f_Q_0_1000_84TeV_hzz': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_1000_3000_84TeV_hzz': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_3000_10000_84TeV_hzz': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_tth_5f_Q_10000_84000_84TeV_hzz': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep': {"fraction": fraction, 'Chunks': 50},

    #         'mgp8_pp_WZjj_HF_5f_84TeV_wzlllv': {"fraction": fraction, 'Chunks': 50},

    #         'mgp8_pp_wwz_5f_Q_0_1000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wwz_5f_Q_1000_3000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wwz_5f_Q_3000_10000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wwz_5f_Q_10000_84000_84TeV': {"fraction": fraction, 'Chunks': 50},

    #         'mgp8_pp_wzz_5f_Q_0_1000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wzz_5f_Q_1000_3000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wzz_5f_Q_3000_10000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wzz_5f_Q_10000_84000_84TeV': {"fraction": fraction, 'Chunks': 50},

    #         'mgp8_pp_zzz_5f_Q_0_1000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_zzz_5f_Q_1000_3000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_zzz_5f_Q_3000_10000_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_zzz_5f_Q_10000_84000_84TeV': {"fraction": fraction, 'Chunks': 50},
            
    #         'mgp8_pp_wwww_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wwwz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wwzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
    #         'mgp8_pp_wzzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
    #          'mgp8_pp_zzzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            
    #          'mgp8_pp_ttzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
    #          'mgp8_pp_ttwz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},

    #          'mgp8_pp_tt_HT_2000_100000_5f_84TeV_blvblv': {"fraction": fraction, 'Chunks': 50},
    #          'mgp8_pp_tt_HT_200_2000_5f_84TeV_blvblv': {"fraction": fraction, 'Chunks': 50},
    
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag = "FCChh/fcc_v07/II/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json"

# Define the input dir (optional)
# inputDir    = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/"
# inputDir    = "./localSamples/"

# Optional: output directory, default is local running directory
outputDir = "/eos/user/l/lberiet/ttZ_diff_results/new_iso"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS = -1

# scale the histograms with the cross-section and integrated luminosity
# doScale = True

# define some binning for various histograms
bins_count = (50, -0.5, 49.5)
bins_ht = array.array('d', [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.75, 3.5, 4.5])


run_batch = True

# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    selections = []

    df = df.Define("weight", "EventHeader.weight")
    weightsum = df.Sum("weight")

    # cut 0 : all events
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("All events")

    # select muons 
    df = df.Define("muons",  "FCCAnalyses::ReconstructedParticle::get(MuonNoIso_objIdx.index, ReconstructedParticles)")
    df = df.Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
    df = df.Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
    df = df.Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") 
    df = df.Define("muons_iso", "AnalysisFCChh::get_IP_delphes(sel_muons, ReconstructedParticles, 0.3, 0.5)")
    df = df.Define("muons_isolated","FCCAnalyses::ReconstructedParticle::sel_iso(0.2)(sel_muons,muons_iso)")
 
    df = df.Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(muons_isolated)") 
    df = df.Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(muons_isolated)")
    
   
   
    
  
    # select electrons
    df = df.Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso_objIdx.index, ReconstructedParticles)")
    df = df.Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
    df = df.Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
    df = df.Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)") 
    df = df.Define("electrons_iso", "AnalysisFCChh::get_IP_delphes(sel_electrons, ReconstructedParticles, 0.3, 0.5)")
    df = df.Define("electrons_isolated","FCCAnalyses::ReconstructedParticle::sel_iso(0.1)(sel_electrons,electrons_iso)")
    df = df.Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(electrons_isolated)") 
    df = df.Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons_isolated)")
    #Overlap removal

    # Step 1: Remove muons overlapping with electrons (dR < 0.3)
    df = df.Define("muons_no_electron_overlap", """
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
        float dR_threshold = 0.3;
        for (size_t i = 0; i < muons_isolated.size(); ++i) {
            bool overlap = false;
            TLorentzVector m_tlv;
            m_tlv.SetXYZM(muons_isolated[i].momentum.x, muons_isolated[i].momentum.y, muons_isolated[i].momentum.z, muons_isolated[i].mass);
            for (size_t j = 0; j < electrons_isolated.size(); ++j) {
                TLorentzVector e_tlv;
                e_tlv.SetXYZM(electrons_isolated[j].momentum.x, electrons_isolated[j].momentum.y, electrons_isolated[j].momentum.z, electrons_isolated[j].mass);
                if (m_tlv.DeltaR(e_tlv) < dR_threshold) {
                    overlap = true;
                    break;
                }
            }
            if (!overlap) {
                result.push_back(muons_isolated[i]);
            }
        }
        return result;
    """)
    df = df.Define("n_muons_no_electron_overlap", "FCCAnalyses::ReconstructedParticle::get_n(muons_no_electron_overlap)")
    df = df.Define("pT_muons_no_electron_overlap", "FCCAnalyses::ReconstructedParticle::get_pt(muons_no_electron_overlap)")

    # Step 2: Merge electrons with remaining muons -> clean leptons
    df=df.Define("clean_leptons_temp", "FCCAnalyses::ReconstructedParticle::merge(electrons_isolated, muons_no_electron_overlap)")
    df=df.Define("clean_leptons", "AnalysisFCChh::SortParticleCollection(clean_leptons_temp)")  # Sort by pT
    df=df.Define("n_clean_leptons", "FCCAnalyses::ReconstructedParticle::get_n(clean_leptons)")
    df=df.Define("pT_clean_leptons", "FCCAnalyses::ReconstructedParticle::get_pt(clean_leptons)")
    df=df.Define("eta_clean_leptons", "FCCAnalyses::ReconstructedParticle::get_eta(clean_leptons)")


   #df =df.Define("Jet", "FCCAnalyses::ReconstructedParticle::get(Jet_objIdx.index, ReconstructedParticles)")
    # Step 3: Remove jets overlapping with clean leptons (dR < 0.2)
    df = df.Define("clean_jets", """
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
        float dR_threshold = 0.3;
        for (size_t i = 0; i < Jet.size(); ++i) {
            bool overlap = false;
            TLorentzVector j_tlv;
            j_tlv.SetXYZM(Jet[i].momentum.x, Jet[i].momentum.y, Jet[i].momentum.z, Jet[i].mass);
            for (size_t j = 0; j < clean_leptons.size(); ++j) {
                TLorentzVector l_tlv;
                l_tlv.SetXYZM(clean_leptons[j].momentum.x, clean_leptons[j].momentum.y, clean_leptons[j].momentum.z, clean_leptons[j].mass);
                if (j_tlv.DeltaR(l_tlv) < dR_threshold) {
                    overlap = true;
                    break;
                }
            }
            if (!overlap) {
                result.push_back(Jet[i]);
            }
        }
        return result;
    """)
    df = df.Define("clean_jets_pt", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(clean_jets)")  # Apply pT cut
    df = df.Define("clean_jets_eta", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(clean_jets_pt)")  # Apply eta cut
    df = df.Define("clean_jets_sorted", "AnalysisFCChh::SortParticleCollection(clean_jets_eta)")
    df = df.Define("n_clean_jets", "FCCAnalyses::ReconstructedParticle::get_n(clean_jets_sorted)")
    df = df.Define("pT_clean_jets", "FCCAnalyses::ReconstructedParticle::get_pt(clean_jets_sorted)")

    # For b-jets, apply OLR to b-tagged jets as well
    df = df.Define("clean_b_tagged_jets", "AnalysisFCChh::get_tagged_jets(clean_jets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)")  # bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
    df = df.Define("clean_selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(clean_b_tagged_jets)")
    df = df.Define("clean_sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(clean_selpt_bjets)")
    df = df.Define("clean_sel_bjets", "AnalysisFCChh::SortParticleCollection(clean_sel_bjets_unsort)")
    df = df.Define("clean_sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(clean_sel_bjets)")
    df = df.Define("n_clean_bjets", "FCCAnalyses::ReconstructedParticle::get_n(clean_sel_bjets)")
    
    # combine leptons (no overlap removal)
    # df = df.Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(muons_isolated, electrons_isolated)")
    # df = df.Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)") #sort by pT
    # df = df.Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")

    # df = df.Define("n_leptons", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")

    # select Z_ll and second pair
    df = df.Define("Z_ll_and_second_pairs", "AnalysisFCChh::getZllAndSecondOSPair(electrons_isolated, muons_no_electron_overlap)")
    df = df.Define("Z_ll_and_second_pairs_size", "Z_ll_and_second_pairs.size()")
    
    #.Filter("AnalysisFCChh::isSecondPairOSOF(sel_leptons, Z_ll_candidate_unmerged[0])")
    df = df.Define('Z_ll_and_second_pairs_merged', 'AnalysisFCChh::merge_pairs(Z_ll_and_second_pairs)')
    df = df.Define('Z_ll_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[0]')
    df = df.Define('Z_ll_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[0]')
    df = df.Define('Z_ll_eta', 'FCCAnalyses::ReconstructedParticle::get_eta(Z_ll_and_second_pairs_merged)[0]')
    df = df.Define('Z_ll_flavor', 'Z_ll_and_second_pairs[0].flavour_flag')

    df = df.Define('Second_Pair_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[1]')
    df = df.Define('Second_Pair_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[1]')
    df = df.Define('Second_Pair_eta', 'FCCAnalyses::ReconstructedParticle::get_eta(Z_ll_and_second_pairs_merged)[1]')
    df = df.Define('Second_Pair_flavor', 'Z_ll_and_second_pairs[1].flavour_flag')

    #df = df.Define("n_leptons", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")
    # df = df.Define('dR_ll', 'AnalysisFCChh::get_angularDist_pair(Z_ll_and_second_pairs, TString("dR"))[0]')
    # df = df.Define('dR_second_pair', 'AnalysisFCChh::get_angularDist_pair(Z_ll_and_second_pairs, TString("dR"))[1]')

    # # select jets
    # df = df.Define("b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)")
    # # select medium b-jets with pT > 30 GeV, |eta| < 4
    # df = df.Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
    # df = df.Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
    # df = df.Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")  # sort by pT
    # df = df.Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
    # df = df.Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")

    # # select jets
    # df = df.Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
    # df = df.Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
    # df = df.Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)") 
    # df = df.Define("n_jets", "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
    # missing ET
    df = df.Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
    df = df.Define("HT", "pT_clean_leptons[0] + pT_clean_leptons[1] + pT_clean_leptons[2] + pT_clean_leptons[3] + clean_sel_bjets_pt[0] + clean_sel_bjets_pt[1]")
    df = df.Define("ht_tev", "HT/1000.")
    results.append(df.Histo1D(("HT_pre", "", len(bins_ht) - 1, bins_ht), "ht_tev"))
    results.append(df.Histo1D(("n_bjets_pre", "", *bins_count), "n_clean_bjets"))
    results.append(df.Histo1D(("n_leptons_pre", "", *bins_count), "n_clean_leptons"))
    #results.append(df.Histo1D(("n_jets_pre", "", *bins_count), "n_jets"))
    
    #results.append(df.Histo1D(("Z_ll_pt_pre", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt"))
#    results.append(df.Histo1D(("Z_ll_mass_pre", "", *bins_count), "Z_ll_mass"))
#    results.append(df.Histo1D(("Z_ll_flavor_pre", "", *bins_count), "Z_ll_flavor"))
#    results.append(df.Histo1D(("Second_Pair_mass_pre", "", *bins_count), "Second_Pair_mass"))
#    results.append(df.Histo1D(("Second_Pair_flavor_pre", "", *bins_count), "Second_Pair_flavor"))
#    results.append(df.Histo1D(("dR_ll_pre", "", *bins_count), "dR_ll"))
#    results.append(df.Histo1D(("dR_second_pair_pre", "", *bins_count), "dR_second_pair"))

    df = df.Filter("n_clean_leptons == 4")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("N_{lep} == 4")

    
  # ######### cut on number of bjets and leptons
  
    
    df = df.Filter("n_clean_bjets >= 1 && n_clean_bjets <= 2")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("1 or 2 b-jets")
    
    # cut on number of jets
   # df = df.Filter("n_jets <6")
   # df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
   # results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
   # selections.append("N_{jets} < 6")

    # cut on Z_ll mass
    df = df.Filter("Z_ll_mass > 80. && Z_ll_mass < 100.")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("80. < Z_ll_mass < 100.")

    df = df.Filter("Second_Pair_flavor == 3")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("Second pair is OF")

    # df = df.Filter("pT_leptons_sel[0] > 30. && pT_leptons_sel[1] > 30. && pT_leptons_sel[2] > 30. && pT_leptons_sel[3] > 30.")
    # df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    # results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    # selections.append("pT_{lep} > 30.")
#     # Temporarily comment out the Z_ll_flavor == 3 cut to diagnose empty histograms
#     # df = df.Filter("Z_ll_flavor == 3")
#     df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
#     results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
#     #selections.append("Z_ll_flavor == 3 (commented out)")

    results.append(df.Histo1D(("HT_sel", "", len(bins_ht) - 1, bins_ht), "ht_tev"))
    results.append(df.Histo1D(("MET_sel", "", 20, 0, 2000), "MET"))


    

    # Apply weights based on flavor flags as a workaround since getElectrons and getMuons are not working
    df = df.Define("wp_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, 1.0)")
    df = df.Define("wm_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, -1.0)")
    df = df.Define("wp_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_no_electron_overlap, 1.0, 1.0)")
    df = df.Define("wm_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_no_electron_overlap, 1.0, -1.0)")
    df = df.Define("wp_bjetId", "AnalysisFCChh::get_weight_emugamma_product(clean_sel_bjets_pt, 3.0, 1.0)")
    df = df.Define("wm_bjetId", "AnalysisFCChh::get_weight_emugamma_product(clean_sel_bjets_pt, 3.0, -1.0)")

    results.append(df.Histo1D(("HT", "", len(bins_ht) - 1, bins_ht), "ht_tev"))
    results.append(df.Histo1D(("HT_eleId_wp", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wp_eleId"))
    results.append(df.Histo1D(("HT_eleId_wm", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wm_eleId"))
    results.append(df.Histo1D(("HT_muId_wp", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wp_muId"))
    results.append(df.Histo1D(("HT_muId_wm", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wm_muId"))
    results.append(df.Histo1D(("HT_bjetId_wp", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wp_bjetId"))
    results.append(df.Histo1D(("HT_bjetId_wm", "", len(bins_ht) - 1, bins_ht), "ht_tev", "wm_bjetId"))

    #, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000 ])  # GeV
    bins_zpt = array.array('d', [0.0,100.0,200.0,300.0,400.0,500.0,650.0,800.0,1000.0,1300.0,1800.0,2500.0])
    results.append(df.Histo1D(("Z_ll_pt_sel", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt"))
    results.append(df.Histo1D(("Z_ll_pt_sel_eleId_wp", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wp_eleId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_eleId_wm", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wm_eleId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_muId_wp", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wp_muId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_muId_wm", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wm_muId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_bjetId_wp", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wp_bjetId"))
    results.append(df.Histo1D(("Z_ll_pt_sel_bjetId_wm", "", len(bins_zpt) - 1, bins_zpt), "Z_ll_pt", "wm_bjetId"))                            

    results.append(df.Histo1D(("MET", "", 20, 0, 2000), "MET"))    

    # store selection labels dynamically in the ROOT file
    from ROOT import TObjString

    selection_str = "\n".join(selections)
    selection_obj = TObjString(selection_str)

    # Identify the cutFlow histogram and attach the object
    for obj in results:
        h = obj.GetValue()  # returns the TH1
        if h.GetName() == "cutFlow":
            h.GetListOfFunctions().Add(selection_obj)
            break

    return results, weightsum

# Function to save results to ROOT file
def save_results(results, output_file):
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    file = ROOT.TFile(output_file, "RECREATE")
    for hist in results:
        h = hist.GetValue()
        h.Write()
    file.Close()
    logger.info(f"Saved results to {output_file}")

