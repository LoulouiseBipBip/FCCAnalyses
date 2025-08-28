"""
Ntuple production for FCC-hh analysis of top-quark pair production
"""

from argparse import ArgumentParser


fraction = 0.1

# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis:
    """
    differential ttbar analysis
    """

    def __init__(self, cmdline_args):
        parser = ArgumentParser(description="Additional analysis arguments", usage="Provide additional arguments after analysis script path")
        # parser.add_argument('--bjet-pt', default='10.', type=float,
        #                     help='Minimal pT of the selected b-jets.')
        # Parse additional arguments not known to the FCCAnalyses parsers
        # All command line arguments know to fccanalysis are provided in the
        # `cmdline_arg` dictionary.
        self.ana_args, _ = parser.parse_known_args(cmdline_args["unknown"])


        # Mandatory: List of processes to run over
        self.process_list = {
        # "mgp8_pp_tta_Q_200_1000_5f_84TeV": {"fraction": fraction, 'Chunks': 50},
        # "mgp8_pp_tta_Q_1000_3000_5f_84TeV": {"fraction": fraction, 'Chunks': 50},
        # "mgp8_pp_tta_Q_3000_5000_5f_84TeV": {"fraction": fraction, 'Chunks': 50},
        # "mgp8_pp_tta_Q_5000_15000_5f_84TeV": {"fraction": fraction, 'Chunks': 50},
        # "mgp8_pp_tta_Q_15000_84000_5f_84TeV": {"fraction": fraction, 'Chunks': 50},
            "mgp8_pp_tta_5f_wlep_84TeV": {"fraction": fraction, 'Chunks': 50},
  
                }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/"

        # Optional: output directory, default is local running directory
        self.output_dir =  "/eos/user/l/lberiet/Histmaker/tta"
        #self.output_dir = "/eos/user/s/selvaggi/analysis/ttbar_differential_v2/"

        # Optional: analysisName, default is ''
        self.analysis_name = "FCC-hh tttt pair analysis 4l"

        # Optional: number of threads to run on, default is 'all available'
        #self.ncpus = 1

        # Optional: running on HTCondor, default is False
        # self.run_batch = False
        self.run_batch = False

        # Optional: Use weighted events
        self.do_weighted = False

        # Optional: read the input files with podio::DataSource
        self.use_data_source = False  # explicitly use old way in this version

        # Optional: test file that is used if you run with the --test argument
        self.test_file = "root://eospublic.cern.ch//eos/experiment/fcc/hh/" "generation/DelphesEvents/fcc_v06/II/mgp8_pp_tth01j_5f_haa/" "events_000001472.root"

    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        """
        Analysis graph.
        """
        dframe2 = dframe.Define("weight", "EventHeader.weight")
        weightsum = dframe2.Sum("weight")
        print(f"Weight sum: {weightsum}")
        
        dframe2 = (
            dframe2
            ########################################### DEFINITION OF VARIABLES ###########################################
            # generator event weight


        .Define("mc_particles", "Particle")  # All Monte Carlo particles
        .Alias("mc_parents", "_Particle_parents.index")  # Alias for particle parents
        .Alias("mc_daughters", "_Particle_daughters.index")  # Alias for particle daughters
        .Define("particle_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(mc_particles)") 

        
        .Define("photons_truth", "FCCAnalyses::MCParticle::sel_pdgID(22, true)(mc_particles)")
        .Define("photon_gen_status", "FCCAnalyses::MCParticle::get_genStatus(photons_truth)")
        .Define("hard_photons","FCCAnalyses::MCParticle::sel_genStatus(23)(photons_truth)")
        .Define("n_hard_photons", "hard_photons.size()")
        .Define("pT_photons_truth", "FCCAnalyses::MCParticle::get_pt(photons_truth)")
        .Define("sort_pt_photons", "FCCAnalyses::MCParticle::SortParticleCollection(photons_truth)")
        .Define("leading_photon", "sort_pt_photons.size() > 0 ? ROOT::VecOps::Take(sort_pt_photons, 1) : ROOT::VecOps::RVec<edm4hep::MCParticleData>{}")
        .Define("leading_photon_origin_1", "FCCAnalyses::MCParticle::get_parent_pdg_photon(hard_photons, mc_particles, mc_parents)")
        .Define("leading_photon_origin_2", "FCCAnalyses::MCParticle::get_parent_pdg(hard_photons, mc_particles, mc_parents)")
        .Define("photon_origin", "FCCAnalyses::MCParticle::get_parent_pdg(photons_truth, mc_particles, mc_parents)")
        .Define("n_leading_photon", "leading_photon.size()")
        .Define("leading_photon_pt", "leading_photon.size() > 0 ? FCCAnalyses::MCParticle::get_pt(leading_photon) : ROOT::VecOps::RVec<float>{}")

        .Define("top_truth", "FCCAnalyses::MCParticle::sel_pdgID(6, true)(mc_particles)")
        .Define("top_daughters", "FCCAnalyses::MCParticle::get_direct_daughters(top_truth, mc_particles, mc_daughters)")
        .Define("photon_from_top", "AnalysisFCChh::getTopPhotons(mc_particles,mc_daughters)")
        .Define("n_photon_from_top", "photon_from_top.size()")
        #.Define("sel_photons_truth", "FCCAnalyses::MCParticle::sel_pt(500.)(photons_truth)")
        #.Define("n_photons_truth", "sel_photons_truth.size()")
     
        .Define("electrons_truth", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(particle_final)")
        .Define("muons_truth", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(particle_final)")
        .Define("leptons_truth", "FCCAnalyses::MCParticle::mergeParticles(electrons_truth, muons_truth)")
        .Define("pT_leptons_truth", "FCCAnalyses::MCParticle::get_pt(leptons_truth)")
        .Define("n_leptons_truth", "leptons_truth.size()")
        .Define("lep_origin", "FCCAnalyses::MCParticle::get_leptons_origin(leptons_truth, mc_particles, mc_parents)")
        .Define("sel_lep_W", "FCCAnalyses::MCParticle::sel_origin_lep(leptons_truth, mc_particles, mc_parents, 24)")
        .Define("charge_sel_lep_W", "FCCAnalyses::MCParticle::get_charge(sel_lep_W)")
        .Define("n_lep_W", "sel_lep_W.size()")

        .Define("pT_lep_W", "FCCAnalyses::MCParticle::get_pt(sel_lep_W)")
        .Define("bs", "FCCAnalyses::MCParticle::sel_pdgID(5, true)(mc_particles)")
        .Define("bs_top", "FCCAnalyses::MCParticle::sel_parent_pdg(bs, mc_particles, mc_parents,6)")
        .Define("charge_bs_top", "FCCAnalyses::MCParticle::get_charge(bs_top)")
        .Define("type_bs_top", "FCCAnalyses::MCParticle::get_pdg(bs_top)")
        .Define("n_bs_top", "bs_top.size()")
        #.Define("dR_lep_b",  "FCCAnalyses::MCParticle::AngleBetweenTwoMCParticles(sel_lep_W, bs_top)")
        .Define("lep_b_pairs", "AnalysisFCChh::makeOppositeChargePairs(sel_lep_W, bs_top)")
        .Define("n_lep_b_pairs", "lep_b_pairs.size()")
        .Filter("n_lep_b_pairs == 2")
        .Define("lep_b_pairs_merged", "AnalysisFCChh::merge_pairs(lep_b_pairs)")
        .Define("first_pair", "AnalysisFCChh::get_nth_pair(lep_b_pairs, 0)")
        .Define("second_pair", "AnalysisFCChh::get_nth_pair(lep_b_pairs, 1)")
        .Define("n_first_pair", "first_pair.size()")
        .Define("n_second_pair", "second_pair.size()")
        #.Define("second_pair", "AnalysisFCChh::get_second_pair(lep_b_pairs)")
        .Define("first_pair_1", "AnalysisFCChh::get_first_from_pair(first_pair)")
        .Define("first_pair_2", "AnalysisFCChh::get_second_from_pair(first_pair)")
        .Define("second_pair_1", "AnalysisFCChh::get_first_from_pair(second_pair)")
        .Define("second_pair_2", "AnalysisFCChh::get_second_from_pair(second_pair)")
        # .Define("first_pair_2", "AnalysisFCChh::get_first_from_pair(second_pair)")
        # .Define("second_pair_2", "AnalysisFCChh::get_second_from_pair(second_pair)")
        .Define("top_recons_tlv_first_pair", "FCCAnalyses::MCParticle::get_tlv(first_pair_1)+FCCAnalyses::MCParticle::get_tlv(first_pair_2)")
        .Define("top_recons_tlv_second_pair", "FCCAnalyses::MCParticle::get_tlv(second_pair_1)+FCCAnalyses::MCParticle::get_tlv(second_pair_2)")

        .Define("mid_tlv", "top_recons_tlv_first_pair+top_recons_tlv_second_pair")
        
        #.Define("top_recons_tlv", "FCCAnalyses::MCParticle::get_tlv(lep_b_pairs_merged)[0]")
        .Define("photon_lead_tlv", "FCCAnalyses::MCParticle::get_tlv(leading_photon)")
        


        #.Define("lep_b_pairs_2", "AnalysisFCChh::get_second_pair(lep_b_pairs)")
        .Define("lep_b_pairs_1_mass", "FCCAnalyses::MCParticle::get_mass(lep_b_pairs_merged)[0]")
        #.Define("top_recons_tlv", "FCCAnalyses::MCParticle::get_tlv(lep_b_pairs_1_first)+FCCAnalyses::MCParticle::get_tlv(lep_b_pairs_1_second)")


        .Define("dR_lep_b", "AnalysisFCChh::get_angularDist_pair(lep_b_pairs, TString(\"dR\"))[0]")
        .Define("dR_phot_top_manual", """
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

         .Define("dR_phot_highest_pt_tlv_manual", """
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
    .Define("dPhi_phot_top_manual", """
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
    .Define("dEta_phot_top_manual", """
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
    .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(MuonNoIso_objIdx.index, ReconstructedParticles)") 
    .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
    .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
    .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") #sort by pT
    .Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
    .Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")

    # select electrons
    .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso_objIdx.index, ReconstructedParticles)")
    .Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
    .Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
    .Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)") #sort by pT
    .Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
    .Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")

    # combine leptons
    .Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons, sel_electrons)")
    .Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)") #sort by pT
    .Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")

    

    #select photons 
    .Define("photons",  "FCCAnalyses::ReconstructedParticle::get(Photon_objIdx.index, ReconstructedParticles)")
    .Define("selpt_photons", "FCCAnalyses::ReconstructedParticle::sel_pt(500.)(photons)")
    .Define("sel_photons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_photons)")
    .Define("sel_photons", "AnalysisFCChh::SortParticleCollection(sel_photons_unsort)") #sort by pT
    .Define("n_photons", "FCCAnalyses::ReconstructedParticle::get_n(sel_photons)")
    .Define("pT_photons", "FCCAnalyses::ReconstructedParticle::get_pt(sel_photons)")

    
   

  
    # select jets
    .Define(
        "b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)"
    )  
    .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
    .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
    .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")  # sort by pT
    .Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
    .Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
   
    .Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
    .Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
    .Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)") 
    .Define("n_jets", "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
    .Define("sumJetPt", "FCCAnalyses::ReconstructedParticle::sumJetPt(sel_jets)")

    .Define("n_leptons", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")
    .Define("lep_b_pairs_reco", "AnalysisFCChh::makeOppositeChargePairs(sel_leptons, sel_bjets)")
    .Define("n_lep_b_pairs_reco", "lep_b_pairs_reco.size()")
    .Define("dR_lep_b_reco", "AnalysisFCChh::get_angularDist_pair(lep_b_pairs_reco, TString(\"dR\"))[0]")
    .Define("leading_photon_reco", "sel_photons.size() > 0 ? ROOT::VecOps::Take(sel_photons, 1) : ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{}")
    .Define("leading_photon_pt_reco", "FCCAnalyses::ReconstructedParticle::get_pt(leading_photon_reco)")

    .Define("lep_b_from_top", "AnalysisFCChh::getLeptonBPairsfromTop(sel_muons,sel_electrons, sel_bjets)")
    .Define("lep_b_from_top_merged", "AnalysisFCChh::merge_pairs(lep_b_from_top)")
    .Define("lep_b_from_top_1_merged_mass", "FCCAnalyses::ReconstructedParticle::get_mass(lep_b_from_top_merged)[0]")
    .Define("lep_b_from_top_2_merged_mass", "FCCAnalyses::ReconstructedParticle::get_mass(lep_b_from_top_merged)[1]")
    .Define("n_lep_b_from_top", "lep_b_from_top_merged.size()")



   

   #
        )
        return dframe2

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        """
        Output variables which will be saved to output root file.
        """
        branch_list = [
          
           #"b_jets_origin",
           #"W_origin",
        
          
          #"n_lep_b_pairs",
          "dR_lep_b_reco",
          "n_lep_b_pairs_reco",
          "leading_photon_pt_reco",
          "n_leptons",
          "top_daughters",
          "n_photon_from_top",
          "dR_lep_b",
         # "dR_phot_top_manual",
        #   "dPhi_phot_top_manual",
        #   "dEta_phot_top_manual",
        #   "pT_photons_truth",
          "leading_photon_pt",
          "n_lep_b_from_top",
          "lep_b_from_top_1_merged_mass",
          "lep_b_from_top_2_merged_mass",
        #   "n_lep_b_pairs",
        #   "lep_b_pairs_1_mass",
        #   "n_first_pair",
        #  "n_second_pair",
        #  "dR_phot_top_manual",
        #  "dR_phot_highest_pt_tlv_manual",
        #  "leading_photon_origin_1",
        #  "leading_photon_origin_2",
        #  "lep_origin",
        #  "n_hard_photons",
        #  "photon_gen_status",
         #"photon_origin",
         #"dR_top_top_manual",

          #"top_recons_tlv",

                  
        ]
        return branch_list