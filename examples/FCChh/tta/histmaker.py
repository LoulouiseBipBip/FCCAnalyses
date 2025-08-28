import ROOT
import array
from multiprocessing import Pool, Manager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intLumi = 3e7

fraction = 1
debug = False

processList = {
    "mgp8_pp_tta_5f_wlep_84TeV": {"fraction": fraction, 'Chunks': 50},
   # "mgp8_pp_tta_5f_pTa1500_wlep_84TeV": {"fraction": fraction, 'Chunks': 50},
  
}

prodTag = "FCChh/fcc_v07/II/"
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json"
outputDir = "/eos/user/l/lberiet/Histmaker/tta"
nCPUS = 16

bins_count = (50, -0.5, 49.5)
bins_leppt = array.array('d', [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500])
bins_zpt = array.array('d', [500.0,700.0,900.0,1100.0,1400.0,1750.0,2200.0])
def build_graph(df, dataset):

    results = []
    selections = []

    df = df.Define("weight", "EventHeader.weight")
    weightsum = df.Sum("weight")

    df=df.Define("mc_particles", "Particle")  # All Monte Carlo particles
    df=df.Alias("mc_parents", "_Particle_parents.index")  # Alias for particle parents
    df=df.Alias("mc_daughters", "_Particle_daughters.index")  # Alias for particle daughters
    df=df.Define("particle_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(mc_particles)") 

        
    df=df.Define("photons_truth", "FCCAnalyses::MCParticle::sel_pdgID(22, true)(mc_particles)")
    df=df.Define("photon_gen_status", "FCCAnalyses::MCParticle::get_genStatus(photons_truth)")
    df=df.Define("hard_photons","FCCAnalyses::MCParticle::sel_genStatus(23)(photons_truth)")
    df=df.Define("n_hard_photons", "hard_photons.size()")
    df=df.Define("pT_photons_truth", "FCCAnalyses::MCParticle::get_pt(photons_truth)")
    df=df.Define("sort_pt_photons", "FCCAnalyses::MCParticle::SortParticleCollection(photons_truth)")
    df=df.Define("leading_photon", "sort_pt_photons.size() > 0 ? ROOT::VecOps::Take(sort_pt_photons, 1) : ROOT::VecOps::RVec<edm4hep::MCParticleData>{}")
    df=df.Define("leading_photon_origin_1", "FCCAnalyses::MCParticle::get_parent_pdg_photon(hard_photons, mc_particles, mc_parents)")
    df=df.Define("leading_photon_origin_2", "FCCAnalyses::MCParticle::get_parent_pdg(hard_photons, mc_particles, mc_parents)")
    df=df.Define("photon_origin", "FCCAnalyses::MCParticle::get_parent_pdg(photons_truth, mc_particles, mc_parents)")
    df=df.Define("n_leading_photon", "leading_photon.size()")
    df=df.Define("leading_photon_pt", "leading_photon.size() > 0 ? FCCAnalyses::MCParticle::get_pt(leading_photon) : ROOT::VecOps::RVec<float>{}")
    df=df.Filter("leading_photon_pt[0] < 1500")

        #.Define("sel_photons_truth", "FCCAnalyses::MCParticle::sel_pt(500.)(photons_truth)")
        #.Define("n_photons_truth", "sel_photons_truth.size()")
     
    df=df.Define("electrons_truth", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(particle_final)")
    df=df.Define("muons_truth", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(particle_final)")
    df=df.Define("leptons_truth", "FCCAnalyses::MCParticle::mergeParticles(electrons_truth, muons_truth)")
    df=df.Define("pT_leptons_truth", "FCCAnalyses::MCParticle::get_pt(leptons_truth)")
    df=df.Define("n_leptons_truth", "leptons_truth.size()")
    df=df.Define("lep_origin", "FCCAnalyses::MCParticle::get_leptons_origin(leptons_truth, mc_particles, mc_parents)")
    df=df.Define("sel_lep_W", "FCCAnalyses::MCParticle::sel_origin_lep(leptons_truth, mc_particles, mc_parents, 24)")
    df=df.Define("charge_sel_lep_W", "FCCAnalyses::MCParticle::get_charge(sel_lep_W)")
    df=df.Define("n_lep_W", "sel_lep_W.size()")

    df=df.Define("pT_lep_W", "FCCAnalyses::MCParticle::get_pt(sel_lep_W)")
    df=df.Define("bs", "FCCAnalyses::MCParticle::sel_pdgID(5, true)(mc_particles)")
    df=df.Define("bs_top", "FCCAnalyses::MCParticle::sel_parent_pdg(bs, mc_particles, mc_parents,6)")
    df=df.Define("charge_bs_top", "FCCAnalyses::MCParticle::get_charge(bs_top)")
    df=df.Define("type_bs_top", "FCCAnalyses::MCParticle::get_pdg(bs_top)")
    df=df.Define("n_bs_top", "bs_top.size()")
        #.Define("dR_lep_b",  "FCCAnalyses::MCParticle::AngleBetweenTwoMCParticles(sel_lep_W, bs_top)")
    df=df.Define("lep_b_pairs", "AnalysisFCChh::makeOppositeChargePairs(sel_lep_W, bs_top)")
    df=df.Define("n_lep_b_pairs", "lep_b_pairs.size()")

    df=df.Define("lep_b_pairs_merged", "AnalysisFCChh::merge_pairs(lep_b_pairs)")
    df=df.Define("first_pair", "AnalysisFCChh::get_nth_pair(lep_b_pairs, 0)")
    df=df.Define("second_pair", "AnalysisFCChh::get_nth_pair(lep_b_pairs, 1)")
    df=df.Define("n_first_pair", "first_pair.size()")
    df=df.Define("n_second_pair", "second_pair.size()")
        #.Define("second_pair", "AnalysisFCChh::get_second_pair(lep_b_pairs)")
    df=df.Define("first_pair_1", "AnalysisFCChh::get_first_from_pair(first_pair)")
    df=df.Define("first_pair_2", "AnalysisFCChh::get_second_from_pair(first_pair)")
    df=df.Define("second_pair_1", "AnalysisFCChh::get_first_from_pair(second_pair)")
    df=df.Define("second_pair_2", "AnalysisFCChh::get_second_from_pair(second_pair)")
    # .Define("first_pair_2", "AnalysisFCChh::get_first_from_pair(second_pair)")
    # .Define("second_pair_2", "AnalysisFCChh::get_second_from_pair(second_pair)")
    df=df.Define("top_recons_tlv_first_pair", "FCCAnalyses::MCParticle::get_tlv(first_pair_1)+FCCAnalyses::MCParticle::get_tlv(first_pair_2)")
    df=df.Define("top_recons_tlv_second_pair", "FCCAnalyses::MCParticle::get_tlv(second_pair_1)+FCCAnalyses::MCParticle::get_tlv(second_pair_2)")

    df=df.Define("mid_tlv", "top_recons_tlv_first_pair+top_recons_tlv_second_pair")
        
        #.Define("top_recons_tlv", "FCCAnalyses::MCParticle::get_tlv(lep_b_pairs_merged)[0]")
    df=df.Define("photon_lead_tlv", "FCCAnalyses::MCParticle::get_tlv(leading_photon)")
        


        #.Define("lep_b_pairs_2", "AnalysisFCChh::get_second_pair(lep_b_pairs)")
    df=df.Define("lep_b_pairs_1_mass", "FCCAnalyses::MCParticle::get_mass(lep_b_pairs_merged)[0]")
        #.Define("top_recons_tlv", "FCCAnalyses::MCParticle::get_tlv(lep_b_pairs_1_first)+FCCAnalyses::MCParticle::get_tlv(lep_b_pairs_1_second)")


    df=df.Define("dR_lep_b", "AnalysisFCChh::get_angularDist_pair(lep_b_pairs, TString(\"dR\"))[0]")
    df=df.Define("dR_phot_top_manual", """
            if (n_second_pair> 0 && n_first_pair > 0) {
                auto tlv1 = top_recons_tlv_first_pair;
                auto tlv2 = photon_lead_tlv;
                if (tlv1.size() > 0 && tlv2.size() > 0) {
                    float deta = tlv1[0].Eta() - tlv2[0].Eta();
                    float dphi = ROOT::Math::VectorUtil::Phi_mpi_pi(tlv1[0].Phi() - tlv2[0].Phi());
                    return ROOT::VecOps::RVec<float>{std::sqrt(deta*deta + dphi*dphi)};
                }
            }
            return ROOT::VecOps::RVec<float>{-1.0};
        """)

    df=df.Define("dR_phot_highest_pt_tlv_manual", """
            if (n_leading_photon > 0 && n_first_pair > 0 && n_second_pair > 0) {
                auto tlv1 = top_recons_tlv_first_pair;
                auto tlv2 = top_recons_tlv_second_pair;
                auto tlv_phot = photon_lead_tlv;
                if (tlv1.size() > 0 && tlv2.size() > 0 && tlv_phot.size() > 0) {
                    
                    auto highest_pt_tlv = (tlv1[0].Pt() > tlv2[0].Pt()) ? tlv1 : tlv2;
                    float deta = highest_pt_tlv[0].Eta() - tlv_phot[0].Eta();
                    float dphi = ROOT::Math::VectorUtil::Phi_mpi_pi(highest_pt_tlv[0].Phi() - tlv_phot[0].Phi());
                    return ROOT::VecOps::RVec<float>{std::sqrt(deta*deta + dphi*dphi)};
                }
            }
            return ROOT::VecOps::RVec<float>{-1.0};
        """)
    df=df.Define("dPhi_phot_top_manual", """
        if (n_leading_photon > 0 && n_first_pair > 0) {
            auto tlv1 = top_recons_tlv_first_pair;
            auto tlv2 = top_recons_tlv_second_pair;
            if (tlv1.size() > 0 && tlv2.size() > 0) {
                float dphi = ROOT::Math::VectorUtil::Phi_mpi_pi(tlv1[0].Phi() - tlv2[0].Phi());
                return ROOT::VecOps::RVec<float>{dphi};
            }
        }
        return ROOT::VecOps::RVec<float>{-1.0};
    """)
    df=df.Define("dEta_phot_top_manual", """
        if (n_leading_photon > 0 && n_first_pair > 0) {
            auto tlv1 = top_recons_tlv_first_pair;
            auto tlv2 = photon_lead_tlv;
            if (tlv1.size() > 0 && tlv2.size() > 0) {
                float deta = tlv1[0].Eta() - tlv2[0].Eta();
                return ROOT::VecOps::RVec<float>{deta};
            }
        }
        return ROOT::VecOps::RVec<float>{-1.0};
    """)

    

    # select muons 
    df=df.Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)") 
    df=df.Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
    df=df.Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
    df=df.Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") #sort by pT
    df=df.Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
    df=df.Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")

    # select electrons
    df=df.Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
    df=df.Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
    df=df.Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
    df=df.Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)") #sort by pT
    df=df.Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
    df=df.Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")

    # combine leptons
    df=df.Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons, sel_electrons)")
    df=df.Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)") #sort by pT
    df=df.Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")
    df=df.Define("n_leptons_sel", "sel_leptons.size()")

    

    #select photons 
    df=df.Define("photons",  "FCCAnalyses::ReconstructedParticle::get(Photon_objIdx.index, ReconstructedParticles)")
    df=df.Define("selpt_photons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(photons)")
    df=df.Define("sel_photons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_photons)")
    df=df.Define("sel_photons", "AnalysisFCChh::SortParticleCollection(sel_photons_unsort)") #sort by pT
    df=df.Define("n_photons", "FCCAnalyses::ReconstructedParticle::get_n(sel_photons)")
    df=df.Define("pT_photons", "FCCAnalyses::ReconstructedParticle::get_pt(sel_photons)")
    df = df.Define("leading_photon_pt_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_photons)[0]")
 
    
   

  
    # select jets
    df=df.Define(
        "b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)"
    )  
    df=df.Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
    df=df.Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
    df=df.Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")  # sort by pT
    df=df.Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
    df=df.Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
   
    df=df.Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
    df=df.Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
    df=df.Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)") 
    df=df.Define("n_jets", "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
    df=df.Define("sumJetPt", "FCCAnalyses::ReconstructedParticle::sumJetPt(sel_jets)")

  

    results.append(df.Histo1D(("n_leptons_pre", "", *bins_count), "n_leptons_sel"))
    results.append(df.Histo1D(("n_bjets_pre", "", *bins_count), "n_bjets"))
    results.append(df.Histo1D(("phot_pt_pre", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel"))


    df=df.Filter("n_leptons_sel == 2")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("N_{lep} == 2")

    df = df.Filter("n_bjets == 2")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("N_{bjets} == 2")


    df = df.Define("lep_b_from_top", "AnalysisFCChh::getLeptonBPairsfromTop(sel_muons,sel_electrons, sel_bjets)")
    #df = df.Define("lep_b_from_top_merged", "AnalysisFCChh::merge_pairs(lep_b_from_top)")
    #df = df.Define("n_lep_b_from_top", "lep_b_from_top_merged.size()")
    df = df.Define("n_lep_b_from_top", "lep_b_from_top.size()")
    results.append(df.Histo1D(("n_lep_b_from_top_pre", "", *bins_count), "n_lep_b_from_top"))
    
    df = df.Filter("n_lep_b_from_top == 2")
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{len(selections)}"))
    selections.append("N_{lep_b_from_top} == 2")

    results.append(df.Histo1D(("pT_leptons_sel", "", len(bins_leppt) - 1, bins_leppt), "pT_leptons_sel"))


    df = df.Define("wp_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, 1.0)")
    df = df.Define("wm_eleId", "AnalysisFCChh::get_weight_emugamma_product(pT_electrons_sel, 2.0, -1.0)")
    df = df.Define("wp_photId", "AnalysisFCChh::get_weight_emugamma_product(pT_photons, 2.0, 1.0)")
    df = df.Define("wm_photId", "AnalysisFCChh::get_weight_emugamma_product(pT_photons, 2.0, -1.0)")
    df = df.Define("wp_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_sel, 1.0, 1.0)")
    df = df.Define("wm_muId", "AnalysisFCChh::get_weight_emugamma_product(pT_muons_sel, 1.0, -1.0)")
    df = df.Define("wp_bjetId", "AnalysisFCChh::get_weight_emugamma_product(sel_bjets_pt, 3.0, 1.0)")
    df = df.Define("wm_bjetId", "AnalysisFCChh::get_weight_emugamma_product(sel_bjets_pt, 3.0, -1.0)")
 
    results.append(df.Histo1D(("phot_pt_sel", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel"))
    results.append(df.Histo1D(("phot_pt_sel_eleId_wp", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wp_eleId"))
    results.append(df.Histo1D(("phot_pt_sel_eleId_wm", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wm_eleId"))
    results.append(df.Histo1D(("phot_pt_sel_muId_wp", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wp_muId"))
    results.append(df.Histo1D(("phot_pt_sel_muId_wm", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wm_muId"))
    results.append(df.Histo1D(("phot_pt_sel_bjetId_wp", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wp_bjetId"))
    results.append(df.Histo1D(("phot_pt_sel_bjetId_wm", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wm_bjetId"))
    results.append(df.Histo1D(("phot_pt_sel_photId_wp", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wp_photId"))
    results.append(df.Histo1D(("phot_pt_sel_photId_wm", "", len(bins_zpt) - 1, bins_zpt), "leading_photon_pt_sel", "wm_photId"))                           


   
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
