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
            'mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep': {"fraction": 1.0, 'Chunks': 50},
            'mgp8_pp_ttz_5f_Q_1000_3000_84TeV_ttzlep': {"fraction": 1.0, 'Chunks': 50},
            'mgp8_pp_ttz_5f_Q_3000_10000_84TeV_ttzlep': {"fraction": 1.0, 'Chunks': 50},
            'mgp8_pp_ttz_5f_Q_10000_84000_84TeV_ttzlep': {"fraction": 1.0, 'Chunks': 50},
        }

        self.input_dir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/"
        self.output_dir = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/result"
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
            
            .Define("p_Z_ll", "FCCAnalyses::MCParticle::get_p(Z_truth)")
         
            .Define("pz_Z_ll", "FCCAnalyses::MCParticle::get_pz(Z_truth)")
            .Define("eta_Z_ll", "FCCAnalyses::MCParticle::get_eta(Z_truth)")
            # Merging leptons and kinematic properties
            .Define("truth_leptons", "FCCAnalyses::MCParticle::mergeParticles(electron_truth, muon_truth)")  # Merge electrons and muons
            #.Define("truth_leptons", "FCCAnalyses::MCParticle::mergeParticles(truth_leptons_temp, tau_truth)")  # Commented out: unused tau merging
            .Define("truth_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_leptons)")  # Truth lepton pT 
            .Define("truth_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_leptons)")  # Truth lepton eta 
            .Define("electron_truth_tlv", "FCCAnalyses::MCParticle::get_tlv(electron_truth)")  # Electron truth four-vector 
            .Define("muon_truth_tlv", "FCCAnalyses::MCParticle::get_tlv(muon_truth)")  # Muon truth four-vector 
            
            # Counting truth particles
            .Define("n_truth_Zll", "truth_Zll.size()")  # Number of Z->ll decays 
            .Define("n_truth_electrons", "electron_truth.size()")  # Number of truth electrons 
            .Define("n_truth_muons", "muon_truth.size()")  # Number of truth muons 
            .Define("n_truth_leptons", "n_truth_electrons + n_truth_muons + n_truth_taus")  # Total number of leptons 
            #.Define("lepton_temp_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(truth_leptons_temp)")  # Unused temporary lepton selection
            #.Define("n_truth_leptons_temp_final", "lepton_temp_final.size()")  # Unused temporary lepton count
            .Define("lepton_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(truth_leptons)")  # Final state truth leptons
            .Define("n_truth_leptons_final", "lepton_truth_final.size()")  # Number of final state leptons 
            .Define("muons_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(muon_truth)")  # Final state truth muons
            .Define("electrons_truth_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(electron_truth)")  # Final state truth electrons
 
            # Additional truth tau selection (redundant, not used)
            .Define("truth_taus", "FCCAnalyses::MCParticle::sel_pdgID(15, true)(mc_particles)")  # Redundant tau selection 
            
            # Kinematic cuts on leptons
            .Define("lep_cut_pt", "FCCAnalyses::MCParticle::sel_pt(30.)(lepton_truth_final)")  # Leptons with pT > 30 GeV
            .Define("lep_cut_pt_eta", "FCCAnalyses::MCParticle::sel_eta(6)(lep_cut_pt)")  # Leptons with |eta| < 6
            .Define("n_lep_cut_pt_eta", "lep_cut_pt_eta.size()")  # Number of leptons passing cuts 
            .Define("eff_lep_pt_eta", "n_lep_cut_pt_eta/n_truth_leptons_final")  # Efficiency of leptons passing cuts 
            # Truth leptons from Z decay
            .Define("truth_ll", "AnalysisFCChh::getTruthll_from_Z(mc_particles, mc_daughters)")  # Truth leptons from Z decay
            .Define("truth_ll_genStatus", "FCCAnalyses::MCParticle::get_genStatus(truth_ll)")  # Gen status of Z decay leptons 
            .Define("truth_ll_pt", "FCCAnalyses::MCParticle::get_pt(truth_ll)")  # pT of Z decay leptons 
            #.Define("n_truth_ll", "truth_ll.size()")
            .Define("truth_ll_eta", "FCCAnalyses::MCParticle::get_eta(truth_ll)")  # eta of Z decay leptons 
            .Define("truth_ll_cut_eta", "FCCAnalyses::MCParticle::sel_eta(4)(truth_ll)")  # Z decay leptons with |eta| < 4 
            .Define("truth_ll_cut_pt", "FCCAnalyses::MCParticle::sel_pt(10.)(truth_ll)")  # Z decay leptons with pT > 10 
            .Define("truth_ll_cut_eta_pt", "FCCAnalyses::MCParticle::sel_eta(4)(FCCAnalyses::MCParticle::sel_pt(10.)(truth_ll))")  # Z decay leptons passing cuts
            .Define("n_truth_ll_cut_eta_pt", "truth_ll_cut_eta_pt.size()")  # Number of Z decay leptons passing cuts 
        )
        
        dframe3 = (
            dframe2
            # Lepton origin and kinematics
            .Define("lep_origin", "FCCAnalyses::MCParticle::get_leptons_origin(lepton_truth_final, mc_particles, mc_parents)")  # Origin of leptons 
            .Define("pt_leptons_origin", "FCCAnalyses::MCParticle::get_pt(lep_origin)")  # pT of leptons by origin 
            .Define("eta_leptons_origin", "FCCAnalyses::MCParticle::get_eta(lep_origin)")  # eta of leptons by origin 

            # Prompt and non-prompt lepton categorization
            .Define("prompt_leptons", "FCCAnalyses::MCParticle::getPromptLeptons(mc_particles, lepton_truth_final, mc_parents)")  # Prompt lepton pairs
         
            .Define("truth_prompt_electrons1", "FCCAnalyses::MCParticle::getPromptLeptons(mc_particles, electrons_truth_final, mc_parents)")  # Prompt electrons
            .Define("truth_prompt_e_first", "truth_prompt_electrons1.first")  # Prompt electrons
            .Define("truth_prompt_e_second", "truth_prompt_electrons1.second")  # Prompt electrons
            .Define("truth_prompt_electrons", "FCCAnalyses::MCParticle::mergeParticles(truth_prompt_e_first, truth_prompt_e_second)")  # Prompt electrons
            
            .Define("truth_prompt_muons1", "FCCAnalyses::MCParticle::getPromptLeptons(mc_particles, muons_truth_final, mc_parents)")  # Prompt muons
            .Define("truth_prompt_mu_first", "truth_prompt_muons1.first")  # Prompt muons
            .Define("truth_prompt_mu_second", "truth_prompt_muons1.second")  # Prompt muons
            .Define("truth_prompt_muons", "FCCAnalyses::MCParticle::mergeParticles(truth_prompt_mu_first, truth_prompt_mu_second)")  # Prompt muons

            .Define("truth_non_prompt_electrons", "FCCAnalyses::MCParticle::getNonPromptLeptons(mc_particles, electrons_truth_final, mc_parents)")  # Non-prompt electrons
           
            .Define("truth_non_prompt_muons", "FCCAnalyses::MCParticle::getNonPromptLeptons(mc_particles, muons_truth_final, mc_parents)")  # Non-prompt muons
           
            .Define("Z_truth_prompt_lep", "prompt_leptons.first")  # Prompt leptons from Z
            #.Define("truth_ll_mass", "FCCAnalyses::MCParticle::get_mass(truth_Zll)")
           # .Define("truth_ll_mass2", "Z_truth_prompt_lep.size() > 1 ? FCCAnalyses::MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Z_truth_prompt_lep[1]})[0] : 0.0")

            .Define("t_truth_prompt_lep", "prompt_leptons.second")  # Prompt leptons from top
            .Define("n_t_truth_prompt_lep", "t_truth_prompt_lep.size()")  # Number of top prompt leptons 
            .Define("pt_t_truth_prompt_lep", "FCCAnalyses::MCParticle::get_pt(t_truth_prompt_lep)")  # pT of top prompt leptons 
            .Define("eta_t_truth_prompt_lep", "FCCAnalyses::MCParticle::get_eta(t_truth_prompt_lep)")  # eta of top prompt leptons 
            .Define("truth_prompt_lep", "FCCAnalyses::MCParticle::mergeParticles(Z_truth_prompt_lep, t_truth_prompt_lep)")  # All prompt leptons
            .Define("truth_prompt_lep_size", "truth_prompt_lep.size()")  # Size of prompt leptons merged
            .Define("truth_prompt_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_prompt_lep)")  # pT of prompt leptons 
            .Define("truth_prompt_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_prompt_lep)")  # eta of prompt leptons 
          
            .Define("truth_non_prompt_lep", "FCCAnalyses::MCParticle::getNonPromptLeptons(mc_particles, lepton_truth_final, mc_parents)")  # Non-prompt leptons
            .Define("truth_non_prompt_lep_size", "truth_non_prompt_lep.size()")  # Size of non-prompt leptons 
            #.Define("truth_non_prompt_lep_pt", "FCCAnalyses::MCParticle::get_pt(truth_non_prompt_lep)")  # pT of non-prompt leptons (commented out)
            #.Define("truth_non_prompt_lep_eta", "FCCAnalyses::MCParticle::get_eta(truth_non_prompt_lep)")  # eta of non-prompt leptons (commented out)
            .Define("n_truth_prompt_lep", "truth_prompt_lep.size()")  # Number of prompt leptons 
            .Define("n_truth_non_prompt_lep", "truth_non_prompt_lep.size()")  # Number of non-prompt leptons 

            # Closest particle calculations for prompt leptons
            #.Define("min_DR_prompt", "ROOT::VecOps::RVec<float>{min_DR_prompt_lep_1, min_DR_prompt_lep_2, min_DR_prompt_lep_3, min_DR_prompt_lep_4}")  # Unused DR calculation
           # .Define("Electron_Photon_Splitting", "FCCAnalyses::MCParticle::countElectronPhotonSplitting(mc_particles, mc_daughters)")  # Photon splitting
            #--------------------------------reco level--------------------------------
            # Muon selection and kinematics
            .Define("muons", "FCCAnalyses::ReconstructedParticle::get(MuonNoIso_objIdx.index, ReconstructedParticles)")  # Reconstructed muons
            .Define("n_muons", "FCCAnalyses::ReconstructedParticle::get_n(muons)")  # Number of muons
            .Define("muons_noiso", "FCCAnalyses::ReconstructedParticle::get(MuonNoIso_objIdx.index, ReconstructedParticles)")  # Muons without isolation
            .Define("muon_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(muons)")  # Muon four-vector 
            .Define("muon_noiso_var", "MuonNoIso_IsolationVar")  # Unused isolation variable
            #.Define("muon_iso_var", "Muon_IsolationVar")  # Unused isolation variable
            .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")  # Muons with pT > 30 GeV
            .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")  # Muons with |eta| < 4
            .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)")  # Sort muons by pT
            .Define("n_muons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)")  # Number of selected muons 
            .Define("pT_muons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")  # pT of selected muons 
            .Define("eta_muons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_muons)")  # eta of selected muons 
            
            # Electron selection and kinematics
            .Define("electrons", "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso_objIdx.index, ReconstructedParticles)")  # Reconstructed electrons
            .Define("electrons_noiso", "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso_objIdx.index, ReconstructedParticles)")  # Electrons without isolation
            .Define("electron_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(electrons)")  # Electron four-vector 
            .Define("electron_noiso_var", "ElectronNoIso_IsolationVar")  # Isolation variable for electrons 
            #.Define("electron_iso_var", "Electron_IsolationVar")  # Unused isolation variable
            .Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")  # Electrons with pT > 30 GeV
            .Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")  # Electrons with |eta| < 4
            .Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)")  # Sort electrons by pT
            .Define("n_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")  # Number of selected electrons 
            .Define("pT_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")  # pT of selected electrons 
            .Define("eta_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_electrons)")  # eta of selected electrons 
        )
        
        dframe4 = (
            dframe3
            # Merged lepton collection
            .Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(muons, electrons)")  # Merge muons and electrons
            .Define("selpt_leptons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(sel_leptons_unsort)")  # Leptons with pT > 30 GeV
            .Define("sel_leptons", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_leptons)")  # Leptons with |eta| < 4
            #.Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)")  # Unused sorting by pT
            .Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")  # pT of selected leptons 
            .Define("n_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")  # Number of selected leptons 

            
               # select jets
            .Define("b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)")  # bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            # select medium b-jets with pT > 30 GeV, |eta| < 4
            .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
            .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
            .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")  # sort by pT
            .Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
            .Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")

            # Z->ll pair reconstruction
            .Define("Z_ll_and_second_pairs", "AnalysisFCChh::getZllAndSecondOSPair(sel_muons, sel_electrons)")  # Z->ll and second opposite-sign pair
            .Define('Z_ll_and_second_pairs_merged', 'AnalysisFCChh::merge_pairs(Z_ll_and_second_pairs)')  # Merge Z->ll pairs
            .Define("Z_ll_reco", "Z_ll_and_second_pairs_merged.size() > 0 ? Z_ll_and_second_pairs_merged[0] : edm4hep::ReconstructedParticleData{}")  # Reconstructed Z->ll
            .Define('Z_ll_flavor', 'Z_ll_and_second_pairs[0].flavour_flag')  # Flavor flag of Z->ll 
            .Define('Z_ll_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[0]')
            .Define('Z_ll_1', "Z_ll_and_second_pairs[0]")  # First Z->ll pair 
            .Define('Z_ll_2', "Z_ll_and_second_pairs[1]")  # Second Z->ll pair 
            .Define("Z_ll_pair_tlv_reco", "FCCAnalyses::ReconstructedParticle::get_tlv(Z_ll_reco)")  # Four-vector of Z->ll pair 
            .Define('Z_ll_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[0]')  # pT of Z->ll pair 

            #.Filter("Z_ll_pt > 1500")

            .Define("n_Zll_reco", "Z_ll_and_second_pairs_merged.size()")  # Number of Z->ll pairs 
            #.Define('Z_ll_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[0]')  # Mass of Z->ll pair 
            .Define("Second_Pair_flavor", "Z_ll_and_second_pairs[1].flavour_flag")  # Flavor flag of second pair 

            # Reco level matching between truth and reconstructed particles
            .Define("matched_electrons", "AnalysisFCChh::find_reco_matches(electron_truth, electrons, 0.4)")  # Matched electrons 
            .Define("matched_muons", "AnalysisFCChh::find_reco_matches(muon_truth, muons, 0.4)")  # Matched muons 
            .Define("matched_leptons_Zll", "AnalysisFCChh::find_reco_matches(truth_ll_cut_eta_pt, sel_leptons, 0.1)")  # Matched Z->ll leptons
            .Define("matched_leptons_Zll_mass", "FCCAnalyses::ReconstructedParticle::get_mass(matched_leptons_Zll)")
            .Define("matched_leptons_Zll_size", "matched_leptons_Zll.size()")  # Size of matched Z->ll leptons 

            # Matching for prompt and non-prompt leptons
            .Define("matched_prompt_electrons", "AnalysisFCChh::find_reco_matches(truth_prompt_electrons, sel_electrons, 0.1)")  # Matched prompt electrons
            .Define("matched_prompt_electrons_size", "matched_prompt_electrons.size()")  # Size of matched prompt electrons 
            .Define("matched_non_prompt_electrons", "AnalysisFCChh::find_reco_matches(truth_non_prompt_electrons, sel_electrons, 0.1)")  # Matched non-prompt electrons
            .Define("matched_non_prompt_electrons_size", "matched_non_prompt_electrons.size()")  # Size of matched non-prompt electrons 
            .Define("matched_prompt_muons", "AnalysisFCChh::find_reco_matches(truth_prompt_muons, sel_muons, 0.1)")  # Matched prompt muons
            .Define("matched_prompt_muons_size", "matched_prompt_muons.size()")  # Size of matched prompt muons 
            .Define("matched_non_prompt_muons", "AnalysisFCChh::find_reco_matches(truth_non_prompt_muons, sel_muons, 0.1)")  # Matched non-prompt muons
            .Define("matched_non_prompt_muons_size", "matched_non_prompt_muons.size()")  # Size of matched non-prompt muons

            .Define("matched_prompt_lep", "FCCAnalyses::ReconstructedParticle::merge(matched_prompt_electrons, matched_prompt_muons)")
            .Define("dR_prompt_lep", "AnalysisFCChh::get_angularDist(matched_prompt_lep, sel_leptons)")
            #.Define("pT_prompt_lep", "FCCAnalyses::ReconstructedParticle::get_pt(matched_prompt_lep)")
            .Define("matched_non_prompt_lep", "FCCAnalyses::ReconstructedParticle::merge(matched_non_prompt_electrons, matched_non_prompt_muons)")

            #Kinematic variables for prompt and non-prompt leptons
            .Define("prompt_lep_pt", "FCCAnalyses::ReconstructedParticle::get_pt(matched_prompt_lep)")
            
            .Define("prompt_lep_eta", "FCCAnalyses::ReconstructedParticle::get_eta(matched_prompt_lep)")
            .Define("non_prompt_lep_pt", "FCCAnalyses::ReconstructedParticle::get_pt(matched_non_prompt_lep)")
            .Define("non_prompt_lep_eta", "FCCAnalyses::ReconstructedParticle::get_eta(matched_non_prompt_lep)")
            .Define("prompt_lep_mass", "FCCAnalyses::ReconstructedParticle::get_mass(matched_prompt_lep)")
            .Define("non_prompt_lep_mass", "FCCAnalyses::ReconstructedParticle::get_mass(matched_non_prompt_lep)")
           # .Define("prompt_lep_dR", "matched_leptons_Zll.size() >= 2 ? AnalysisFCChh::get_angularDist(matched_leptons_Zll) : ROOT::VecOps::RVec<float>{}")
           
            # .Define("matched_prompt_leptons1", "AnalysisFCChh::mergeIntoPairs(matched_prompt_electrons, matched_prompt_muons)")
            # .Define("matched_prompt_lep", "AnalysisFCChh::find_reco_matches(truth_prompt_lep, sel_leptons, 0.1)")  # Matched prompt leptons
            # .Define("matched_non_prompt_lep", "AnalysisFCChh::find_reco_matches(truth_non_prompt_lep, sel_leptons, 0.1)")  # Matched non-prompt leptons
            .Define("matched_prompt_lep_size", "matched_prompt_lep.size()")  # Size of matched prompt leptons 
            .Define("matched_non_prompt_lep_size", "matched_non_prompt_lep.size()")  # Size of matched non-prompt leptons 
            .Define("matched_leptons_all", "FCCAnalyses::ReconstructedParticle::merge(matched_prompt_lep, matched_non_prompt_lep)")
            .Define("matched_leptons_all_size", "matched_leptons_all.size()")
            .Define("matched_muons_all", "FCCAnalyses::ReconstructedParticle::merge(matched_prompt_muons, matched_non_prompt_muons)")
            .Define("matched_muons_all_size", "matched_muons_all.size()")
            .Define("matched_electrons_all", "FCCAnalyses::ReconstructedParticle::merge(matched_prompt_electrons, matched_non_prompt_electrons)")
            .Define("matched_electrons_all_size", "matched_electrons_all.size()")
        )
        
        dframe5 = (
            dframe4
            # Isolation calculations for matched leptons
            .Define("Iso_Prompt", "AnalysisFCChh::get_IP_delphes(matched_prompt_lep, ReconstructedParticles, 0.3, 0.5)")
            .Define("Iso_Non_Prompt", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_lep, ReconstructedParticles, 0.3, 0.5)")

            .Define("Iso_Prompt_Zll", "Z_ll_and_second_pairs_merged.size() > 0 ? AnalysisFCChh::get_IP_delphes(Z_ll_and_second_pairs_merged, ReconstructedParticles, 0.3, 0.5) : ROOT::VecOps::RVec<float>{}")

            .Define("RP_no_lep", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, sel_leptons_unsort)")
            .Define("iso_all_muons", "AnalysisFCChh::get_IP_delphes(muons, RP_no_lep, 0.3, 0.5)")  # Isolation for prompt muons (DR=0.2, 0.1)
            .Define("iso_delphes_muons", "MuonNoIso_IsolationVar")
            .Define("iso_all_electrons", "AnalysisFCChh::get_IP_delphes(electrons, RP_no_lep, 0.3, 0.5)")
            .Define("iso_delphes_electrons", "ElectronNoIso_IsolationVar")
            .Define("n_iso_all_electrons", "iso_all_electrons.size()")
            .Define("n_iso_delphes_muons", "iso_delphes_muons.size()")
            .Define("n_iso_delphes_electrons", "iso_delphes_electrons.size()")
            .Define("n_iso_all_muons", "iso_all_muons.size()")
            .Filter("n_iso_delphes_muons == n_iso_all_muons")
            .Filter("n_iso_delphes_electrons == n_iso_all_electrons")
            .Define("diff_iso_muons", "iso_delphes_muons-iso_all_muons")
            .Define("diff_iso_electrons", "iso_delphes_electrons-iso_all_electrons")

            .Define("prompt_muons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, RP_no_lep, 0.1, 0.5)")  # Isolation for prompt muons (DR=0.1, 0.1)
            .Define("prompt_electrons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, RP_no_lep, 0.1, 0.5)")  # Isolation for prompt electrons (DR=0.1, 0.1)
            .Define("non_prompt_muons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, RP_no_lep, 0.1, 0.5)")  # Isolation for non-prompt muons (DR=0.1, 0.1)
            .Define("non_prompt_electrons_iso_dr01", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, RP_no_lep, 0.1, 0.5)")  # Isolation for non-prompt electrons (DR=0.1, 0.1)
            .Define("prompt_muons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, RP_no_lep, 0.2, 0.5)")  # Isolation for prompt muons (DR=0.2, 0.1)
            .Define("prompt_electrons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, RP_no_lep, 0.2, 0.5)")  # Isolation for prompt electrons (DR=0.2, 0.1)
            .Define("non_prompt_muons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, RP_no_lep, 0.2, 0.5)")  # Isolation for non-prompt muons (DR=0.2, 0.1)
            .Define("non_prompt_electrons_iso_dr02", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, RP_no_lep, 0.2, 0.5)")  # Isolation for non-prompt electrons (DR=0.2, 0.1)
            .Define("prompt_muons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, RP_no_lep, 0.3, 0.5)")  # Isolation for prompt muons (DR=0.3, 0.1)
            .Define("prompt_electrons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, RP_no_lep, 0.3, 0.5)")  # Isolation for prompt electrons (DR=0.3, 0.1)
            .Define("non_prompt_muons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, RP_no_lep, 0.3, 0.5)")  # Isolation for non-prompt muons (DR=0.3, 0.1)
            .Define("non_prompt_electrons_iso_dr03", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, RP_no_lep, 0.3, 0.5)")  # Isolation for non-prompt electrons (DR=0.3, 0.1)
            .Define("prompt_muons_iso_dr04", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, RP_no_lep, 0.4, 0.5)")  # Isolation for prompt muons (DR=0.4, 0.1)
            .Define("prompt_electrons_iso_dr04", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, RP_no_lep, 0.4, 0.5)")  # Isolation for prompt electrons (DR=0.4, 0.1)
            .Define("non_prompt_muons_iso_dr04", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, RP_no_lep, 0.4, 0.5)")  # Isolation for non-prompt muons (DR=0.4, 0.1)
            .Define("non_prompt_electrons_iso_dr04", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, RP_no_lep, 0.4, 0.5)")  # Isolation for non-prompt electrons (DR=0.4, 0.1)
            .Define("prompt_muons_iso_dr05", "AnalysisFCChh::get_IP_delphes(matched_prompt_muons, RP_no_lep, 0.5, 0.5)")  # Isolation for prompt muons (DR=0.5, 0.1)
            .Define("prompt_electrons_iso_dr05", "AnalysisFCChh::get_IP_delphes(matched_prompt_electrons, RP_no_lep, 0.5, 0.5)")  # Isolation for prompt electrons (DR=0.5, 0.1)
            .Define("non_prompt_muons_iso_dr05", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_muons, RP_no_lep, 0.5, 0.5)")  # Isolation for non-prompt muons (DR=0.5, 0.1)
            .Define("non_prompt_electrons_iso_dr05", "AnalysisFCChh::get_IP_delphes(matched_non_prompt_electrons, RP_no_lep, 0.5, 0.5)")  # Isolation for non-prompt electrons (DR=0.5, 0.1)
            #.Define("lepton_iso_test", "FCCAnalyses::ReconstructedParticle::coneIsolation(matched_leptons_Zll, sel_leptons, 0.1, 0.5)")  # Unused isolation test
            .Define("electron_iso_delphes", "ElectronNoIso_IsolationVar")
            .Define("n_electron_iso_delphes", "electron_iso_delphes.size()")
            .Define("electrons_iso", "AnalysisFCChh::get_IP_delphes(electrons, ReconstructedParticles, 0.3, 0.5)")
            .Define("n_electrons_iso", "electrons_iso.size()")
           # .Filter("n_electron_iso_delphes == n_prompt_electrons_iso_dr03")
           # .Define("diff_delphes_iso", "electrons_iso-electron_iso_delphes")
            .Define("muon_iso_delphes", "MuonNoIso_IsolationVar")
            .Define("n_muon_iso_delphes", "muon_iso_delphes.size()")
            .Define("n_prompt_muons_iso_dr03", "prompt_muons_iso_dr03.size()")
            #.Filter("n_muon_iso_delphes == n_prompt_muons_iso_dr03")
          #  .Define("diff_delphes_iso_muon", "prompt_muons_iso_dr03-muon_iso_delphes")
            # Minimum Delta R calculations for reconstructed leptons
            .Define("min_dR_reco_prompt", "matched_prompt_lep.size() > 0 ? ReconstructedParticle::getMinDRToAny(matched_prompt_lep,  ReconstructedParticles) : ROOT::VecOps::RVec<float>{}")  # Min DR for prompt leptons 
            .Define("min_dR_reco_prompt_test", "Z_ll_and_second_pairs_merged.size() > 0 ? ReconstructedParticle::getMinDRToAny(Z_ll_and_second_pairs_merged,  ReconstructedParticles) : ROOT::VecOps::RVec<float>{}")  # Min DR test for Z->ll 
            #.Define("min_dR_reco_non_prompt", "Z_ll_and_second_pairs_merged.size() > 0 ? ReconstructedParticle::getMinDRToAny(, sel_leptons) : ROOT::VecOps::RVec<float>{}")  # Incomplete and unused
            .Define("reco_truth_lep_dR", "truth_prompt_lep.size() > 0 ? ReconstructedParticle2MC::getClosestTrueLeptonDR(sel_leptons, truth_prompt_lep): ROOT::VecOps::RVec<float>{}")  # Min DR for truth leptons
            # Scalar HT calculation
            .Define("HT", "ScalarHT")  # Scalar HT 
        )
        return dframe5
        
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
        #     # 'weight',  # Event weight 
        
            "prompt_muons_iso_dr01",
            "prompt_electrons_iso_dr01",
            "non_prompt_muons_iso_dr01",
            "non_prompt_electrons_iso_dr01",
            "prompt_muons_iso_dr02",
            "prompt_electrons_iso_dr02",
            "non_prompt_muons_iso_dr02",
            "non_prompt_electrons_iso_dr02",
            "prompt_muons_iso_dr03",
            "prompt_electrons_iso_dr03",
            "non_prompt_muons_iso_dr03",
            "non_prompt_electrons_iso_dr03",
            "prompt_muons_iso_dr04",
            "prompt_electrons_iso_dr04",
            "non_prompt_muons_iso_dr04",
            "non_prompt_electrons_iso_dr04",
            "prompt_muons_iso_dr05",
            "prompt_electrons_iso_dr05",
            "non_prompt_muons_iso_dr05",
            "non_prompt_electrons_iso_dr05",
        #     # "Iso_Prompt",
        #     # "Iso_Non_Prompt",
        #     # "prompt_lep_pt",
        #     # "prompt_lep_eta",
        #     # "non_prompt_lep_pt",
        #     # "non_prompt_lep_eta",
        #     # "prompt_lep_mass",
        #     # "non_prompt_lep_mass",
        #     # "muon_iso",
        #     # "electron_iso",
        #     # #"prompt_lep_dR",
        #     # "pT_electrons_sel",
        #     # "pT_muons_sel",
        #     # "iso_all_muons",
        #     # "iso_delphes_muons",
        #     # "diff_iso_muons",
        #     # "n_iso_delphes_muons",
        #     # "n_muons",
        #     # "Iso_Prompt",
        #     # "Iso_Prompt_Zll",
        #     "dR_Zll_truth",
        #     "truth_ll_pt",
        #     #"truth_ll_mass",
        #     "matched_leptons_Zll_mass",
        #     "n_truth_ll",
   
        #     "Z_mass",
        #     "pt_tot_Z",
        #     "Z_mass_truth",
        #     "Z_pt_truth",
        #     "p_Z_ll",
        #     "pz_Z_ll",
        #     "eta_Z_ll",
          "truth_prompt_lep_size",
          "matched_prompt_lep_size",
        ]
        return branch_list