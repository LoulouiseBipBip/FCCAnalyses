'''
Analysis example for FCC-hh, using ttZ events to check lepton identification efficiencies
'''
from argparse import ArgumentParser

class Analysis():
    '''
    Validation of lepton identification efficiencies in ttZ events.
    '''
    def __init__(self, cmdline_args):
        parser = ArgumentParser(
            description='Additional analysis arguments',
            usage='Provide additional arguments after analysis script path')
        self.ana_args, _ = parser.parse_known_args(cmdline_args['unknown'])

        self.process_list = {
            'mgp8_pp_tttt_wlep_Q_0_1000_5f_84TeV': {'fraction': 0.1},
            'mgp8_pp_tttt_wlep_Q_1000_3000_5f_84TeV': {'fraction': 0.1},
            'mgp8_pp_tttt_wlep_Q_3000_10000_5f_84TeV': {'fraction': 0.1},
            'mgp8_pp_tttt_wlep_Q_10000_84000_5f_84TeV': {'fraction': 0.1},
             #'mgp8_pp_tttt_5f_84TeV_4tlep': {'fraction': 0.1},
        }
        self.input_dir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II_trackCov/"
        #self.input_dir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II_trackCov"
        self.output_dir = "/eos/user/l/lberiet/Histmaker/tttt_v3/Tracks"
        self.analysis_name = 'tttt 4l'
        self.nCPUS = 32
        self.n_chunks = 50
        self.run_batch = False
        self.do_weighted = False
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/hh/' \
                         'tutorials/edm4hep_tutorial_data/' \
                         'pwp8_pp_hh_5f_hhbbyy.root'

    def analyzers(self, dframe):
        """
        Analysis graph for processing ttZ events to evaluate lepton identification efficiencies.
        """
        dframe2 = (
            dframe
            #--------------------------------truth level--------------------------------
            # Event weight and basic particle collections
            .Define("weight", "EventHeader.weight")  # Event weight from header (not used in output)
            .Define("mc_particles", "Particle")  # All Monte Carlo particles
            .Alias("mc_parents", "_Particle_parents.index")  # Alias for particle parents
            .Alias("mc_daughters", "_Particle_daughters.index")  # Alias for particle daughters
            
            # Truth-level Z->ll selection and particle categorization
            .Define("truth_Zll", "AnalysisFCChh::getTruthll_from_Z(mc_particles, mc_daughters)")  # Truth Z decaying to leptons
            .Define("Z_mass", "FCCAnalyses::MCParticle::get_invariant_mass(truth_Zll)")
            .Define("pt_tot_Z", "FCCAnalyses::MCParticle::get_total_pt(truth_Zll)")
            .Define("pT_Comp_Z", "FCCAnalyses::MCParticle::get_pt(truth_Zll)")
            .Define("particle_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(mc_particles)")  # Final state particles
            .Define("electron_truth", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(mc_particles)")  # Truth electrons
            .Define("Z_truth", "FCCAnalyses::MCParticle::sel_pdgID(23, false)(mc_particles)")
            .Define("Z_mass_truth", "FCCAnalyses::MCParticle::get_mass(Z_truth)")
            .Define("Z_pt_truth", "FCCAnalyses::MCParticle::get_pt(Z_truth)")
            .Define("muon_truth", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(mc_particles)")  # Truth muons
            .Define("tau_truth", "FCCAnalyses::MCParticle::sel_pdgID(15, true)(mc_particles)")  # Truth taus
            .Define("n_truth_taus", "tau_truth.size()")  # Number of truth taus (used in filter)
            .Filter("n_truth_taus == 0", "no_tau")  # Filter out events with taus
       
            # Merging leptons and kinematic properties
            .Define("truth_leptons", "FCCAnalyses::MCParticle::mergeParticles(electron_truth, muon_truth)")  # Merge electrons and muons
            .Define("truth_leptons_size", "truth_leptons.size()")
            #.Define("truth_leptons", "FCCAnalyses::MCParticle::mergeParticles(truth_leptons_temp, tau_truth)")  # Commented out: unused tau merging
            .Define("truth_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_leptons)")  # Truth lepton pT 
            .Define("truth_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_leptons)")  # Truth lepton eta 
            .Define("electron_truth_tlv", "FCCAnalyses::MCParticle::get_tlv(electron_truth)")  # Electron truth four-vector 
            .Define("muon_truth_tlv", "FCCAnalyses::MCParticle::get_tlv(muon_truth)")  # Muon truth four-vector 
            

            .Define("lepton_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(truth_leptons)")  # Final state truth leptons
            .Define("n_truth_leptons_final", "lepton_truth_final.size()")  # Number of final state leptons 
            .Define("muons_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(muon_truth)")  # Final state truth muons
            .Define("electrons_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(electron_truth)")  # Final state truth electrons

            .Define("lep_cut_pt", "FCCAnalyses::MCParticle::sel_pt(0.)(lepton_truth_final)")  # Leptons with pT > 30 GeV
            .Define("lep_cut_pt_eta", "FCCAnalyses::MCParticle::sel_eta(6)(lep_cut_pt)")  # Leptons with |eta| < 6
            .Define("n_lep_cut_pt_eta", "lep_cut_pt_eta.size()")  # Number of leptons passing cuts 
            .Define("eff_lep_pt_eta", "n_lep_cut_pt_eta/n_truth_leptons_final")  # Efficiency of leptons passing cuts 
            # Truth leptons from Z decay
            .Define("truth_ll", "AnalysisFCChh::getTruthll_from_Z(mc_particles, mc_daughters)")  # Truth leptons from Z decay
         
            
            # Prompt and non-prompt lepton categorization
            .Define("truth_prompt_leptons", "FCCAnalyses::MCParticle::getWLeptons(mc_particles, lepton_truth_final, mc_parents)")  # Prompt lepton pairs
            .Define("truth_prompt_leptons_size", "truth_prompt_leptons.size()")
            .Define("parent_leptons", "FCCAnalyses::MCParticle::get_parent_pdg(lepton_truth_final, mc_particles, mc_parents)")
            .Define("truth_prompt_electrons", "FCCAnalyses::MCParticle::getWLeptons(mc_particles, electrons_truth_final, mc_parents)")  # Prompt electrons
            .Define("truth_prompt_electrons_size", "truth_prompt_electrons.size()")
            .Define("truth_prompt_muons", "FCCAnalyses::MCParticle::getWLeptons(mc_particles, muons_truth_final, mc_parents)")  # Prompt muons
            .Define("truth_prompt_muons_size", "truth_prompt_muons.size()")

            .Define("truth_non_prompt_electrons", "FCCAnalyses::MCParticle::remove(electrons_truth_final, truth_prompt_electrons)")  # Non-prompt electrons
            .Define("truth_non_prompt_muons", "FCCAnalyses::MCParticle::remove(muons_truth_final, truth_prompt_muons)")  # Non-prompt muons
            .Define("truth_non_prompt_leptons", "FCCAnalyses::MCParticle::remove(lepton_truth_final, truth_prompt_leptons)") 
            .Define("truth_non_prompt_lep_size", "truth_non_prompt_leptons.size()")
            .Define("truth_non_prompt_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_non_prompt_leptons)")
            .Define("truth_non_prompt_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_non_prompt_leptons)")
            #--------------------------------reco level--------------------------------
            .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(MuonNoIso_objIdx.index, ReconstructedParticles)") 

            .Define("muon_noiso_var", "MuonNoIso_IsolationVar")
            .Define("muon_iso_var", "Muon_IsolationVar")
            .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
            .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
            .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") #sort by pT
            .Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
            .Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")
            .Define("type_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_type(sel_muons)")

            # select electrons
            .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso_objIdx.index, ReconstructedParticles)")

            .Define("electron_noiso_var", "ElectronNoIso_IsolationVar")
            .Define("electron_iso_var", "Electron_IsolationVar")
            .Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
            .Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
            .Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)") #sort by pT

            .Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
            .Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")

        
            # merge leptons
            .Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons, sel_electrons)")
            .Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)") #sort by pT
            .Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")
           
           
            .Define("of_ss_sf_leptons",  "AnalysisFCChh::findOppositeFlavorSameSign(sel_electrons, sel_muons)")
            .Define("n_of_ss_sf_leptons",  "FCCAnalyses::ReconstructedParticle::get_n(of_ss_sf_leptons)")

            #.Define('Second_Pair_size', 'Z_ll_and_second_pairs.size()')
           # Reco matching
            .Define("matched_prompt_electrons", "AnalysisFCChh::find_reco_matches(truth_prompt_electrons, sel_electrons, 0.1)")  # Matched prompt electrons
            #.Define("matched_prompt_electrons_size", "matched_prompt_electrons.size()")  # Size of matched prompt electrons 
            .Define("matched_non_prompt_electrons", "AnalysisFCChh::find_reco_matches(truth_non_prompt_electrons, sel_electrons, 0.1)")  # Matched non-prompt electrons
            #.Define("matched_non_prompt_electrons_size", "matched_non_prompt_electrons.size()")  # Size of matched non-prompt electrons 
            .Define("matched_prompt_muons", "AnalysisFCChh::find_reco_matches(truth_prompt_muons, sel_muons, 0.1)")  # Matched prompt muons
           # .Define("matched_prompt_muons_size", "matched_prompt_muons.size()")  # Size of matched prompt muons 
            .Define("matched_non_prompt_muons", "AnalysisFCChh::find_reco_matches(truth_non_prompt_muons, sel_muons, 0.1)")  # Matched non-prompt muons
            #.Define("matched_non_prompt_muons_size", "matched_non_prompt_muons.size()")  # Size of matched non-prompt muons

            .Define("matched_prompt_lep", "FCCAnalyses::ReconstructedParticle::merge(matched_prompt_electrons, matched_prompt_muons)")
            .Define("matched_prompt_lep_size", "matched_prompt_lep.size()")
            .Define("matched_non_prompt_lep", "FCCAnalyses::ReconstructedParticle::merge(matched_non_prompt_electrons, matched_non_prompt_muons)")
            .Define("matched_non_prompt_lep_size", "matched_non_prompt_lep.size()")
            # .Define("D0_prompt_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(matched_prompt_electrons, _EFlowTrack_trackStates)")
            # .Define("D0_prompt_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(matched_prompt_muons, _EFlowTrack_trackStates)")
            # .Define("D0_prompt_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(matched_prompt_lep, _EFlowTrack_trackStates)")
            # .Define("D0_non_prompt_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(matched_non_prompt_electrons, _EFlowTrack_trackStates)")
            # .Define("D0_non_prompt_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(matched_non_prompt_muons, _EFlowTrack_trackStates)")
            # .Define("D0_non_prompt_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(matched_non_prompt_lep, _EFlowTrack_trackStates)")
            
            # .Define("D0_cov_prompt_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_cov(matched_prompt_electrons, _EFlowTrack_trackStates)")
            # .Define("D0_cov_prompt_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_cov(matched_prompt_muons, _EFlowTrack_trackStates)")
            # .Define("D0_cov_prompt_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_cov(matched_prompt_lep, _EFlowTrack_trackStates)")
            # .Define("D0_cov_non_prompt_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_cov(matched_non_prompt_electrons, _EFlowTrack_trackStates)")
            # .Define("D0_cov_non_prompt_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_cov(matched_non_prompt_muons, _EFlowTrack_trackStates)")
            # .Define("D0_cov_non_prompt_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_cov(matched_non_prompt_lep, _EFlowTrack_trackStates)")

            # .Define("D0_sig_prompt_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(matched_prompt_electrons, _EFlowTrack_trackStates)")
            # .Define("abs_D0_sig_prompt_electrons", "abs(D0_sig_prompt_electrons)")
            # .Define("D0_sig_prompt_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(matched_prompt_muons, _EFlowTrack_trackStates)")
            # .Define("D0_sig_prompt_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(matched_prompt_lep, _EFlowTrack_trackStates)")
            # .Define("D0_sig_non_prompt_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(matched_non_prompt_electrons, _EFlowTrack_trackStates)")
            # .Define("abs_D0_sig_non_prompt_electrons", "abs(D0_sig_non_prompt_electrons)")
            # .Define("D0_sig_non_prompt_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(matched_non_prompt_muons, _EFlowTrack_trackStates)")
            # .Define("D0_sig_non_prompt_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(matched_non_prompt_lep, _EFlowTrack_trackStates)")

            # .Define("D0_sig_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(sel_electrons, _EFlowTrack_trackStates)")
            # .Define("n_D0_sig_electrons", "D0_sig_electrons.size()")
            # .Define("abs_D0_sig_electrons", "abs(D0_sig_electrons)")
            # .Define("D0_sig_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(sel_muons, _EFlowTrack_trackStates)")
            # .Define("abs_D0_sig_muons", "abs(D0_sig_muons)")
            # .Define("D0_sig_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0_sig(sel_leptons, _EFlowTrack_trackStates)")

             .Define("n_leptons", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")
          

            # #Tracks 
            # .Define("D0_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(sel_electrons, _EFlowTrack_trackStates)")
            # .Define("n_D0_electrons", "D0_electrons.size()")
            # .Define("D0_muons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(sel_muons, _EFlowTrack_trackStates)")
            # .Define("n_D0_muons", "D0_muons.size()")
            # .Define("D0_leptons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(sel_leptons, _EFlowTrack_trackStates)")
            # .Define("n_D0_leptons", "D0_leptons.size()")
            #Iso
            .Define("RP_no_lep", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, sel_leptons)")
            .Define("iso_all_elec", "AnalysisFCChh::get_IP_delphes(sel_electrons, RP_no_lep, 0.2, 0.5)")
            .Define("n_iso_all_elec", "iso_all_elec.size()")

            .Define("iso_all_muon", "AnalysisFCChh::get_IP_delphes(sel_muons, RP_no_lep, 0.2, 0.5)")
            .Define("n_iso_all_muon", "iso_all_muon.size()")

            .Define("prompt_muons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, RP_no_lep, 0.2, 0.5)")  # Isolation for prompt muons (DR=0.2, 0.1)
            .Define("prompt_electrons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, RP_no_lep, 0.2, 0.5)")  # Isolation for prompt electrons (DR=0.2, 0.1)
            .Define("non_prompt_muons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, RP_no_lep, 0.2, 0.5)")  # Isolation for non-prompt muons (DR=0.2, 0.1)
            .Define("non_prompt_electrons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, RP_no_lep, 0.2, 0.5)")  # Isolation for non-prompt electrons (DR=0.2, 0.1)

            # .Define("prompt_muons_iso_d0", "AnalysisFCChh::computeD0Cut(D0_sig_prompt_muons, -0.3, 0.28)")
            # .Define("prompt_electrons_iso_d0", "AnalysisFCChh::computeD0Cut(D0_sig_prompt_electrons,  -0.13, 0.28)")
            # .Define("non_prompt_muons_iso_d0", "AnalysisFCChh::computeD0Cut(D0_sig_non_prompt_muons,  -0.13, 0.28)")
            # .Define("non_prompt_electrons_iso_d0", "AnalysisFCChh::computeD0Cut(D0_sig_non_prompt_electrons,  -0.13, 0.28)")

            ########################################### JETS ########################################### 

            # selected jets above a pT threshold of 30 GeV, eta < 4
            .Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
            .Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
            .Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)") 
            .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
            .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)")
            .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)")
            .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)")
            .Define("phi_jets",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)")
            # select jets
            .Define(
                "b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)"
            )  # bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            # select medium b-jets with pT > 30 GeV, |eta| < 4
            .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
            .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
            .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")  # sort by pT
            .Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
            .Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")

            
            # missing ET
            .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")

            .Define("HT", "ScalarHT")
            .Define("ht_tev", "HT/1000.")  # Scalar HT 
        )
        return dframe2
        
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            # "D0_electrons",
            # "D0_muons",
            # "D0_leptons",
            # "D0_prompt_electrons",
            # "D0_prompt_muons",
            # "D0_prompt_leptons",
            # "D0_non_prompt_electrons",
            # "D0_non_prompt_muons",
            # "D0_non_prompt_leptons",
            # "D0_sig_prompt_electrons",
            # "D0_sig_prompt_muons",
            # "D0_sig_prompt_leptons",
            # "D0_sig_non_prompt_electrons",
            # "D0_sig_non_prompt_muons",
            # "D0_sig_non_prompt_leptons",
            # "abs_D0_sig_prompt_electrons",
            # "abs_D0_sig_non_prompt_electrons",
            # "D0_sig_electrons",
            # "n_D0_sig_electrons",
            # "abs_D0_sig_electrons",
            # "D0_sig_muons",
            # "D0_sig_leptons",
            # "n_D0_electrons",
            # "n_D0_muons",
            # "n_D0_leptons",
            # "n_leptons",
            # "n_iso_all_elec",
            # "n_electrons_sel",
            # "n_iso_all_muon",
            # "iso_all_elec",
            # "iso_all_muon",
            # "matched_prompt_lep_size",
            # "matched_non_prompt_lep_size",
            # "truth_leptons_size",
            # "truth_prompt_leptons_size",
           
            

            # "prompt_muons_iso_dr02",
            # "prompt_electrons_iso_dr02",
            # "non_prompt_muons_iso_dr02",
            # "non_prompt_electrons_iso_dr02",
            # "prompt_muons_iso_d0",
            # "prompt_electrons_iso_d0",
            # "non_prompt_muons_iso_d0",
            # "non_prompt_electrons_iso_d0",
            "parent_leptons",
        ]
        return branch_list