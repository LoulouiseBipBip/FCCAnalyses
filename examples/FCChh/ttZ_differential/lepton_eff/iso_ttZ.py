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
            'mgp8_pp_ttz_5f_84TeV_ttzlep': {'fraction': 0.1, 'Chunks': 50},
        }

        self.input_dir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/"
        self.output_dir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/iso"
        self.analysis_name = 'ttZ lepton efficiency'
        self.nCPUS = 32
        self.n_chunks = 50
        self.run_batch = False
        self.do_weighted = False
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/hh/' \
                         'tutorials/edm4hep_tutorial_data/' \
                         'pwp8_pp_hh_5f_hhbbyy.root'

    def analyzers(self, dframe):
        """
        Analysis graph.
        """
        dframe2 = (
            dframe
            #--------------------------------truth level--------------------------------
            .Define("weight", "EventHeader.weight")
            .Define("mc_particles", "Particle")
            .Alias("mc_parents", "_Particle_parents.index")
            .Alias("mc_daughters", "_Particle_daughters.index") 
            .Define("truth_Zll", "AnalysisFCChh::getTruthZll(mc_particles, mc_daughters)")
            
            .Define("electron_truth", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(mc_particles)")
            .Define("muon_truth", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(mc_particles)")
            .Define("tau_truth", "FCCAnalyses::MCParticle::sel_pdgID(15, true)(mc_particles)")
            .Define("n_truth_taus", "tau_truth.size()")
            .Filter("n_truth_taus == 0", "no_tau")
            .Define("truth_leptons_temp", "FCCAnalyses::MCParticle::mergeParticles(electron_truth, muon_truth)")
            .Define("truth_leptons", "FCCAnalyses::MCParticle::mergeParticles(truth_leptons_temp, tau_truth)")
            .Define("truth_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_leptons)")
            .Define("truth_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_leptons)")
            .Define("truth_lep_phi", "FCCAnalyses::MCParticle::get_phi(truth_leptons)")
            .Define("electron_truth_tlv", "FCCAnalyses::MCParticle::get_tlv(electron_truth)")
            .Define("muon_truth_tlv", "FCCAnalyses::MCParticle::get_tlv(muon_truth)")
            
            .Define("n_truth_Zll", "truth_Zll.size()")
            .Define("n_truth_electrons", "electron_truth.size()")
            .Define("n_truth_muons", "muon_truth.size()")
            .Define("n_truth_leptons", "n_truth_electrons + n_truth_muons + n_truth_taus")
            .Define("lepton_temp_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(truth_leptons_temp)")
            .Define("n_truth_leptons_temp_final", "lepton_temp_final.size()")
            .Define("lepton_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(truth_leptons)")
            .Define("n_truth_leptons_final", "lepton_truth_final.size()")

            .Define("truth_taus", "FCCAnalyses::MCParticle::sel_pdgID(15, true)(mc_particles)")
            .Define("lep_cut_pt", "FCCAnalyses::MCParticle::sel_pt(10.)(lepton_truth_final)")
            .Define("lep_cut_pt_eta", "FCCAnalyses::MCParticle::sel_eta(4)(lep_cut_pt)")
            .Define("n_lep_cut_pt_eta", "lep_cut_pt_eta.size()")

            .Define("truth_ll", "AnalysisFCChh::getTruthll_from_Z(mc_particles, mc_daughters)")
            .Define("truth_ll_genStatus", "FCCAnalyses::MCParticle::get_genStatus(truth_ll)")
            .Define("truth_ll_pt", "FCCAnalyses::MCParticle::get_pt(truth_ll)")
            .Define("truth_ll_eta", "FCCAnalyses::MCParticle::get_eta(truth_ll)")
            .Define("flavour_Z_decay", "truth_Zll.size() > 0 ? AnalysisFCChh::checkZllDecay(truth_Zll[0], mc_daughters, mc_particles) : 0")
            #kinematic variables
            .Define("lepton_1", "truth_ll.size() > 0 ? truth_ll[0] : edm4hep::MCParticleData{}")
            .Define("lepton_2", "truth_ll.size() > 1 ? truth_ll[1] : edm4hep::MCParticleData{}")
            .Define("n_truth_ll", "truth_ll.size()")
            .Define("lepton_1_pt", "truth_ll.size() > 0 ? MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_1})[0] : 0.0")
            .Define("lepton_2_pt", "truth_ll.size() > 1 ? MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_2})[0] : 0.0")
            .Define("lepton_1_eta", "truth_ll.size() > 0 ? MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_1})[0] : 0.0")
            .Define("lepton_2_eta", "truth_ll.size() > 1 ? MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_2})[0] : 0.0")
            .Define("truth_l1_tlv", "truth_ll.size() > 0 ? MCParticle::get_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_1})[0] : TLorentzVector{}")
            .Define("truth_l2_tlv", "truth_ll.size() > 1 ? MCParticle::get_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_2})[0] : TLorentzVector{}")
            .Define("dR_ll", "truth_ll.size() >= 2 ? MCParticle::AngleBetweenTwoMCParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_1}, ROOT::VecOps::RVec<edm4hep::MCParticleData>{lepton_2})[0] : 0.0")
            
            .Define("lep_origin", "FCCAnalyses::MCParticle::get_leptons_origin(lepton_truth_final, mc_particles, mc_parents)")
            .Define("pt_leptons_origin", "FCCAnalyses::MCParticle::get_pt(lep_origin)")
            .Define("eta_leptons_origin", "FCCAnalyses::MCParticle::get_eta(lep_origin)")

            .Define("prompt_leptons", "FCCAnalyses::MCParticle::getPromptLeptons(mc_particles, lepton_truth_final, mc_parents)")
            .Define("Z_truth_prompt_lep", "prompt_leptons.first")
            .Define("gen_Z_truth_prompt_lep", "FCCAnalyses::MCParticle::get_genStatus(Z_truth_prompt_lep)")
            .Define("n_Z_truth_prompt_lep", "Z_truth_prompt_lep.size()")
            .Define("pt_Z_truth_prompt_lep", "FCCAnalyses::MCParticle::get_pt(Z_truth_prompt_lep)")
            .Define("eta_Z_truth_prompt_lep", "FCCAnalyses::MCParticle::get_eta(Z_truth_prompt_lep)")
            .Define("t_truth_prompt_lep", "prompt_leptons.second")
            .Define("n_t_truth_prompt_lep", "t_truth_prompt_lep.size()")
            .Define("pt_t_truth_prompt_lep", "FCCAnalyses::MCParticle::get_pt(t_truth_prompt_lep)")
            .Define("eta_t_truth_prompt_lep", "FCCAnalyses::MCParticle::get_eta(t_truth_prompt_lep)")
            .Define("truth_prompt_lep", "FCCAnalyses::MCParticle::mergeParticles(Z_truth_prompt_lep, t_truth_prompt_lep)")
            .Define("truth_prompt_lep_size", "truth_prompt_lep.size()")
            .Define("truth_prompt_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_prompt_lep)")
            .Define("truth_prompt_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_prompt_lep)")
            .Define("truth_prompt_lep_phi", "FCCAnalyses::MCParticle::get_phi(truth_prompt_lep)")
            .Define("truth_non_prompt_lep", "FCCAnalyses::MCParticle::getNonPromptLeptons(mc_particles, lepton_truth_final, mc_parents)")
            .Define("truth_non_prompt_lep_size", "truth_non_prompt_lep.size()")
            .Define("truth_non_prompt_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_non_prompt_lep)")
            .Define("truth_non_prompt_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_non_prompt_lep)")
            .Define("truth_non_prompt_lep_phi", "FCCAnalyses::MCParticle::get_phi(truth_non_prompt_lep)")
            .Define("n_truth_prompt_lep", "truth_prompt_lep.size()")
            .Define("n_truth_non_prompt_lep", "truth_non_prompt_lep.size()")

            # Reco level
            .Define("muons", "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)") 
            .Define("muons_noiso", "FCCAnalyses::ReconstructedParticle::get(MuonNoIso_objIdx.index, ReconstructedParticles)")
            .Define("muon_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(muons)")
            .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
            .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
            .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)")
            .Define("n_muons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
            .Define("pT_muons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")
            .Define("type_muons_sel", "FCCAnalyses::ReconstructedParticle::get_type(sel_muons)")

            .Define("electrons", "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
            .Define("electrons_noiso", "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso_objIdx.index, ReconstructedParticles)")
            .Define("electron_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(electrons)")
            .Define("electron_noiso_var", "ElectronNoIso_IsolationVar")
            .Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
            .Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
            .Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)")
            .Define("n_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
            .Define("pT_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")

            .Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(muons_noiso, electrons_noiso)")
            .Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)")
            .Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")
            .Define("phi_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_phi(sel_leptons)")
           
            .Define("Z_ll_and_second_pairs", "AnalysisFCChh::getZllAndSecondOSPair(sel_muons, sel_electrons)")
            .Define("Z_ll_and_second_pairs_merged", "AnalysisFCChh::merge_pairs(Z_ll_and_second_pairs)")
            .Define("Z_ll_reco", "Z_ll_and_second_pairs_merged.size() > 0 ? Z_ll_and_second_pairs_merged[0] : edm4hep::ReconstructedParticleData{}")
            .Define("Z_ll_pair_tlv_reco", "FCCAnalyses::ReconstructedParticle::get_tlv(Z_ll_reco)")

            # Reco level matching
            .Define("matched_electrons", "AnalysisFCChh::find_reco_matches(electron_truth, electrons, 0.4)")
            .Define("matched_muons", "AnalysisFCChh::find_reco_matches(muon_truth, muons, 0.4)")
            .Define("matched_leptons_Zll", "AnalysisFCChh::find_reco_matches(truth_ll, sel_leptons, 0.1)")
            .Define("matched_leptons_Zll_size", "matched_leptons_Zll.size()")
            .Define("matched_electrons_Zll", "AnalysisFCChh::find_reco_matches(truth_ll, electrons_noiso, 0.4)")
            .Define("matched_electrons_Zll_size", "matched_electrons_Zll.size()")
            .Define("matched_muons_Zll", "AnalysisFCChh::find_reco_matches(truth_ll, muons_noiso, 0.4)")
            .Define("matched_muons_Zll_size", "matched_muons_Zll.size()")
            .Define("matched_prompt_lep", "AnalysisFCChh::find_reco_matches(truth_prompt_lep, sel_leptons, 0.1)")
            .Define("matched_non_prompt_lep", "AnalysisFCChh::find_reco_matches(truth_non_prompt_lep, sel_leptons, 0.1)")
            .Define("matched_prompt_lep_size", "matched_prompt_lep.size()")
            .Define("matched_non_prompt_lep_size", "matched_non_prompt_lep.size()")
            .Define("matched_prompt_lep_phi", "FCCAnalyses::ReconstructedParticle::get_phi(matched_prompt_lep)")
            .Define("matched_non_prompt_lep_phi", "FCCAnalyses::ReconstructedParticle::get_phi(matched_non_prompt_lep)")

            # Isolation for matched reconstructed leptons
            .Define("matched_prompt_lep_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_prompt_lep, ReconstructedParticles, 0.1, 0.0, false)")
            .Define("matched_prompt_lep_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_prompt_lep, ReconstructedParticles, 0.2, 0.0, false)")
            .Define("matched_prompt_lep_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_prompt_lep, ReconstructedParticles, 0.3, 0.0, false)")
            .Define("matched_non_prompt_lep_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_lep, ReconstructedParticles, 0.1, 0.0, false)")
            .Define("matched_non_prompt_lep_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_lep, ReconstructedParticles, 0.2, 0.0, false)")
            .Define("matched_non_prompt_lep_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_lep, ReconstructedParticles, 0.3, 0.0, false)")

            # Separate matched muons and electrons
            .Define("matched_prompt_muons", "FCCAnalyses::ReconstructedParticle::sel_type(13, true)(matched_prompt_lep)")
            .Define("matched_prompt_electrons", "FCCAnalyses::ReconstructedParticle::sel_type(11, true)(matched_prompt_lep)")
            .Define("matched_non_prompt_muons", "FCCAnalyses::ReconstructedParticle::sel_type(13, true)(matched_non_prompt_lep)")
            .Define("matched_non_prompt_electrons", "FCCAnalyses::ReconstructedParticle::sel_type(11, true)(matched_non_prompt_lep)")
            .Define("matched_prompt_muons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, ReconstructedParticles, 0.1, 0.0, false)")
            .Define("matched_prompt_muons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, ReconstructedParticles, 0.2, 0.0, false)")
            .Define("matched_prompt_muons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, ReconstructedParticles, 0.3, 0.0, false)")
            .Define("matched_prompt_electrons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, ReconstructedParticles, 0.1, 0.0, false)")
            .Define("matched_prompt_electrons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, ReconstructedParticles, 0.2, 0.0, false)")
            .Define("matched_prompt_electrons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, ReconstructedParticles, 0.3, 0.0, false)")
            .Define("matched_non_prompt_muons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, ReconstructedParticles, 0.1, 0.0, false)")
            .Define("matched_non_prompt_muons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, ReconstructedParticles, 0.2, 0.0, false)")
            .Define("matched_non_prompt_muons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, ReconstructedParticles, 0.3, 0.0, false)")
            .Define("matched_non_prompt_electrons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, ReconstructedParticles, 0.1, 0.0, false)")
            .Define("matched_non_prompt_electrons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, ReconstructedParticles, 0.2, 0.0, false)")
            .Define("matched_non_prompt_electrons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, ReconstructedParticles, 0.3, 0.0, false)")
        )
        return dframe2
        
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'n_truth_Zll',
            'lepton_1_pt',
            'lepton_2_pt',
            'lepton_1_eta',
            'lepton_2_eta',
            'truth_ll_pt',
            'truth_ll_eta',
            'Z_truth_prompt_lep',
            't_truth_prompt_lep',
            'truth_prompt_lep',
            'truth_non_prompt_lep',
            'n_truth_prompt_lep',
            'n_truth_non_prompt_lep',
            'n_Z_truth_prompt_lep',
            'n_t_truth_prompt_lep',
            'pt_Z_truth_prompt_lep',
            'eta_Z_truth_prompt_lep',
            'pt_t_truth_prompt_lep',
            'eta_t_truth_prompt_lep',
            'truth_prompt_lep_size',
            'truth_prompt_lep_pt',
            'truth_prompt_lep_eta',
            'truth_prompt_lep_phi',
            'truth_non_prompt_lep_size',
            'truth_non_prompt_lep_pt',
            'truth_non_prompt_lep_eta',
            'truth_non_prompt_lep_phi',
            'truth_ll_genStatus',
            'gen_Z_truth_prompt_lep',
            'matched_prompt_lep_size',
            'matched_non_prompt_lep_size',
            'matched_prompt_lep_phi',
            'matched_non_prompt_lep_phi',
            'matched_prompt_lep_iso_dr01',
            'matched_prompt_lep_iso_dr02',
            'matched_prompt_lep_iso_dr03',
            'matched_non_prompt_lep_iso_dr01',
            'matched_non_prompt_lep_iso_dr02',
            'matched_non_prompt_lep_iso_dr03',
            'matched_prompt_muons_iso_dr01',
            'matched_prompt_muons_iso_dr02',
            'matched_prompt_muons_iso_dr03',
            'matched_prompt_electrons_iso_dr01',
            'matched_prompt_electrons_iso_dr02',
            'matched_prompt_electrons_iso_dr03',
            'matched_non_prompt_muons_iso_dr01',
            'matched_non_prompt_muons_iso_dr02',
            'matched_non_prompt_muons_iso_dr03',
            'matched_non_prompt_electrons_iso_dr01',
            'matched_non_prompt_electrons_iso_dr02',
            'matched_non_prompt_electrons_iso_dr03',
            'lep_origin'
        ]
        return branch_list