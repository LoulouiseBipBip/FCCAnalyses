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
            'mgp8_pp_ttz_5f_84TeV_ttzlep': {'Chunks': 50},
        }

        self.input_dir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/"
        self.output_dir = '/eos/user/l/lberiet/ttZ_diff_results/lepton_eff'
        self.analysis_name = 'ttZ lepton efficiency'
        self.n_threads = 4
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
            .Define("weight", "EventHeader.weight")
            # Muons
            .Define("muons", "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)")
            .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")  # pT > 30 GeV
            .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(3)(selpt_muons)")  # |eta| < 3
            .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)")
            .Define("n_muons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)")
            .Define("pT_muons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")
            .Define("eta_muons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_muons)")
            .Define("type_muons_sel", "FCCAnalyses::ReconstructedParticle::get_type(sel_muons)")
            # Electrons
            .Define("electrons", "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
            .Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")  # pT > 30 GeV
            .Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(3)(selpt_electrons)")  # |eta| < 3
            .Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)")
            .Define("n_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
            .Define("pT_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")
            .Define("eta_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_electrons)")
            # Merge Leptons
            .Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons, sel_electrons)")
            .Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)")
            .Define("pT_leptons", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")
            .Define("eta_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_leptons)")
            .Define("n_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")
            # MC particles
            .Define("mc_particles", "Particle")
            .Alias("mc_parents", "_Particle_parents.index")
            .Alias("mc_daughters", "_Particle_daughters.index")
            # Generated leptons (final-state electrons and muons)
            .Define("mc_particles_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(mc_particles)")  # Final-state particles
            .Define("MC_l_electrons", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(mc_particles_final)")  # Electrons and positrons
            .Define("MC_l_muons", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(mc_particles_final)")  # Muons and antimuons
            .Define("MC_l", "FCCAnalyses::MCParticle::mergeParticles(MC_l_electrons, MC_l_muons)")  # Combine electrons and muons
            .Define("n_MC_l", "FCCAnalyses::MCParticle::get_n(MC_l)")
            .Define("pT_MC_l", "FCCAnalyses::MCParticle::get_pt(MC_l)")
            .Define("eta_MC_l", "FCCAnalyses::MCParticle::get_eta(MC_l)")
            # Gen-matching
            .Define("muons_genmatched_l", "AnalysisFCChh::find_reco_matches(MC_l, sel_muons, 0.5)")  # deltaR = 0.5
            .Define("electrons_genmatched_l", "AnalysisFCChh::find_reco_matches(MC_l, sel_electrons, 0.5)")
            .Define("leptons_genmatched_l", "FCCAnalyses::ReconstructedParticle::merge(muons_genmatched_l, electrons_genmatched_l)")
            # Gen-matched counts and kinematics
            .Define("n_muons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_n(muons_genmatched_l)")
            .Define("pT_muons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_pt(muons_genmatched_l)")
            .Define("eta_muons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_eta(muons_genmatched_l)")
            .Define("n_electrons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_n(electrons_genmatched_l)")
            .Define("pT_electrons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_pt(electrons_genmatched_l)")
            .Define("eta_electrons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_eta(electrons_genmatched_l)")
            .Define("n_leptons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_n(leptons_genmatched_l)")
            .Define("pT_leptons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_pt(leptons_genmatched_l)")
            .Define("eta_leptons_genmatched_l", "FCCAnalyses::ReconstructedParticle::get_eta(leptons_genmatched_l)")
            # Separate into prompt and non-prompt at truth level
            .Define("MC_l_origins", "FCCAnalyses::MCParticle::get_leptons_origin(MC_l, mc_particles, mc_parents)")
            .Define("MC_l_prompt", """
                ROOT::VecOps::RVec<edm4hep::MCParticleData> prompt;
                prompt.reserve(MC_l.size());
                for(size_t i = 0; i < MC_l.size(); ++i) {
                    if(abs(MC_l_origins[i]) == 23) 
                        prompt.push_back(MC_l[i]);
                }
                return prompt;
            """)
            .Define("MC_l_nonprompt", """
                ROOT::VecOps::RVec<edm4hep::MCParticleData> nonprompt;
                nonprompt.reserve(MC_l.size());
                for(size_t i = 0; i < MC_l.size(); ++i) {
                    if(abs(MC_l_origins[i]) != 23 && abs(MC_l_origins[i]) != 24 && abs(MC_l_origins[i]) != 25)
                        nonprompt.push_back(MC_l[i]);
                }
                return nonprompt;
            """)
            .Define("n_MC_l_prompt", "FCCAnalyses::MCParticle::get_n(MC_l_prompt)")
            .Define("pT_MC_l_prompt", "FCCAnalyses::MCParticle::get_pt(MC_l_prompt)")
            .Define("eta_MC_l_prompt", "FCCAnalyses::MCParticle::get_eta(MC_l_prompt)")
            .Define("n_MC_l_nonprompt", "FCCAnalyses::MCParticle::get_n(MC_l_nonprompt)")
            .Define("pT_MC_l_nonprompt", "FCCAnalyses::MCParticle::get_pt(MC_l_nonprompt)")
            .Define("eta_MC_l_nonprompt", "FCCAnalyses::MCParticle::get_eta(MC_l_nonprompt)")
            # Gen-matched reco leptons separated by promptness
            .Define("muons_genmatched_l_prompt", "AnalysisFCChh::find_reco_matches(MC_l_prompt, sel_muons, 0.5)")
            .Define("muons_genmatched_l_nonprompt", "AnalysisFCChh::find_reco_matches(MC_l_nonprompt, sel_muons, 0.5)")
            .Define("electrons_genmatched_l_prompt", "AnalysisFCChh::find_reco_matches(MC_l_prompt, sel_electrons, 0.5)")
            .Define("electrons_genmatched_l_nonprompt", "AnalysisFCChh::find_reco_matches(MC_l_nonprompt, sel_electrons, 0.5)")
            .Define("leptons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::merge(muons_genmatched_l_prompt, electrons_genmatched_l_prompt)")
            .Define("leptons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::merge(muons_genmatched_l_nonprompt, electrons_genmatched_l_nonprompt)")
            # Gen-matched counts and kinematics
            .Define("n_muons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_n(muons_genmatched_l_prompt)")
            .Define("pT_muons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_pt(muons_genmatched_l_prompt)")
            .Define("eta_muons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_eta(muons_genmatched_l_prompt)")
            .Define("n_muons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_n(muons_genmatched_l_nonprompt)")
            .Define("pT_muons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_pt(muons_genmatched_l_nonprompt)")
            .Define("eta_muons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_eta(muons_genmatched_l_nonprompt)")
            .Define("n_electrons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_n(electrons_genmatched_l_prompt)")
            .Define("pT_electrons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_pt(electrons_genmatched_l_prompt)")
            .Define("eta_electrons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_eta(electrons_genmatched_l_prompt)")
            .Define("n_electrons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_n(electrons_genmatched_l_nonprompt)")
            .Define("pT_electrons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_pt(electrons_genmatched_l_nonprompt)")
            .Define("eta_electrons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_eta(electrons_genmatched_l_nonprompt)")
            .Define("n_leptons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_n(leptons_genmatched_l_prompt)")
            .Define("pT_leptons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_pt(leptons_genmatched_l_prompt)")
            .Define("eta_leptons_genmatched_l_prompt", "FCCAnalyses::ReconstructedParticle::get_eta(leptons_genmatched_l_prompt)")
            .Define("n_leptons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_n(leptons_genmatched_l_nonprompt)")
            .Define("pT_leptons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_pt(leptons_genmatched_l_nonprompt)")
            .Define("eta_leptons_genmatched_l_nonprompt", "FCCAnalyses::ReconstructedParticle::get_eta(leptons_genmatched_l_nonprompt)")
            # New cone isolation for dR = 0.1, 0.2, 0.3
            .Define("muon_iso_dr01", "FCCAnalyses::ReconstructedParticle::coneIsolation(0.0, 0.1)(sel_muons, ReconstructedParticles)")
            .Define("muon_iso_dr02", "FCCAnalyses::ReconstructedParticle::coneIsolation(0.0, 0.2)(sel_muons, ReconstructedParticles)")
            .Define("muon_iso_dr03", "FCCAnalyses::ReconstructedParticle::coneIsolation(0.0, 0.3)(sel_muons, ReconstructedParticles)")
            .Define("electron_iso_dr01", "FCCAnalyses::ReconstructedParticle::coneIsolation(0.0, 0.1)(sel_electrons, ReconstructedParticles)")
            .Define("electron_iso_dr02", "FCCAnalyses::ReconstructedParticle::coneIsolation(0.0, 0.2)(sel_electrons, ReconstructedParticles)")
            .Define("electron_iso_dr03", "FCCAnalyses::ReconstructedParticle::coneIsolation(0.0, 0.3)(sel_electrons, ReconstructedParticles)")
            # Indices for gen-matched leptons
            .Define("muons_genmatched_l_prompt_idx", """
                ROOT::VecOps::RVec<int> idx;
                for (size_t i = 0; i < sel_muons.size(); ++i) {
                    for (size_t j = 0; j < muons_genmatched_l_prompt.size(); ++j) {
                        if (sel_muons[i].momentum.x == muons_genmatched_l_prompt[j].momentum.x &&
                            sel_muons[i].momentum.y == muons_genmatched_l_prompt[j].momentum.y &&
                            sel_muons[i].momentum.z == muons_genmatched_l_prompt[j].momentum.z) {
                            idx.push_back(i);
                            break;
                        }
                    }
                }
                return idx;
            """)
            .Define("muons_genmatched_l_nonprompt_idx", """
                ROOT::VecOps::RVec<int> idx;
                for (size_t i = 0; i < sel_muons.size(); ++i) {
                    for (size_t j = 0; j < muons_genmatched_l_nonprompt.size(); ++j) {
                        if (sel_muons[i].momentum.x == muons_genmatched_l_nonprompt[j].momentum.x &&
                            sel_muons[i].momentum.y == muons_genmatched_l_nonprompt[j].momentum.y &&
                            sel_muons[i].momentum.z == muons_genmatched_l_nonprompt[j].momentum.z) {
                            idx.push_back(i);
                            break;
                        }
                    }
                }
                return idx;
            """)
            .Define("electrons_genmatched_l_prompt_idx", """
                ROOT::VecOps::RVec<int> idx;
                for (size_t i = 0; i < sel_electrons.size(); ++i) {
                    for (size_t j = 0; j < electrons_genmatched_l_prompt.size(); ++j) {
                        if (sel_electrons[i].momentum.x == electrons_genmatched_l_prompt[j].momentum.x &&
                            sel_electrons[i].momentum.y == electrons_genmatched_l_prompt[j].momentum.y &&
                            sel_electrons[i].momentum.z == electrons_genmatched_l_prompt[j].momentum.z) {
                            idx.push_back(i);
                            break;
                        }
                    }
                }
                return idx;
            """)
            .Define("electrons_genmatched_l_nonprompt_idx", """
                ROOT::VecOps::RVec<int> idx;
                for (size_t i = 0; i < sel_electrons.size(); ++i) {
                    for (size_t j = 0; j < electrons_genmatched_l_nonprompt.size(); ++j) {
                        if (sel_electrons[i].momentum.x == electrons_genmatched_l_nonprompt[j].momentum.x &&
                            sel_electrons[i].momentum.y == electrons_genmatched_l_nonprompt[j].momentum.y &&
                            sel_electrons[i].momentum.z == electrons_genmatched_l_nonprompt[j].momentum.z) {
                            idx.push_back(i);
                            break;
                        }
                    }
                }
                return idx;
            """)
            # Isolation for gen-matched leptons
            .Define("muons_genmatched_l_prompt_iso_dr01", "ROOT::VecOps::Take(muon_iso_dr01, muons_genmatched_l_prompt_idx)")
            .Define("muons_genmatched_l_nonprompt_iso_dr01", "ROOT::VecOps::Take(muon_iso_dr01, muons_genmatched_l_nonprompt_idx)")
            .Define("muons_genmatched_l_prompt_iso_dr02", "ROOT::VecOps::Take(muon_iso_dr02, muons_genmatched_l_prompt_idx)")
            .Define("muons_genmatched_l_nonprompt_iso_dr02", "ROOT::VecOps::Take(muon_iso_dr02, muons_genmatched_l_nonprompt_idx)")
            .Define("muons_genmatched_l_prompt_iso_dr03", "ROOT::VecOps::Take(muon_iso_dr03, muons_genmatched_l_prompt_idx)")
            .Define("muons_genmatched_l_nonprompt_iso_dr03", "ROOT::VecOps::Take(muon_iso_dr03, muons_genmatched_l_nonprompt_idx)")
            .Define("electrons_genmatched_l_prompt_iso_dr01", "ROOT::VecOps::Take(electron_iso_dr01, electrons_genmatched_l_prompt_idx)")
            .Define("electrons_genmatched_l_nonprompt_iso_dr01", "ROOT::VecOps::Take(electron_iso_dr01, electrons_genmatched_l_nonprompt_idx)")
            .Define("electrons_genmatched_l_prompt_iso_dr02", "ROOT::VecOps::Take(electron_iso_dr02, electrons_genmatched_l_prompt_idx)")
            .Define("electrons_genmatched_l_nonprompt_iso_dr02", "ROOT::VecOps::Take(electron_iso_dr02, electrons_genmatched_l_nonprompt_idx)")
            .Define("electrons_genmatched_l_prompt_iso_dr03", "ROOT::VecOps::Take(electron_iso_dr03, electrons_genmatched_l_prompt_idx)")
            .Define("electrons_genmatched_l_nonprompt_iso_dr03", "ROOT::VecOps::Take(electron_iso_dr03, electrons_genmatched_l_nonprompt_idx)")
            # Debug counts
            .Define("n_mc_l_origins", "MC_l_origins.size()")
        )
        return dframe2

    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'weight',
            'n_muons_sel', 'pT_muons_sel', 'eta_muons_sel',
            'n_electrons_sel', 'pT_electrons_sel', 'eta_electrons_sel',
            'n_leptons_sel', 'pT_leptons', 'eta_leptons_sel',
            'n_MC_l', 'pT_MC_l', 'eta_MC_l',
            'n_muons_genmatched_l', 'pT_muons_genmatched_l', 'eta_muons_genmatched_l',
            'n_electrons_genmatched_l', 'pT_electrons_genmatched_l', 'eta_electrons_genmatched_l',
            'n_leptons_genmatched_l', 'pT_leptons_genmatched_l', 'eta_leptons_genmatched_l',
            'n_MC_l_prompt', 'pT_MC_l_prompt', 'eta_MC_l_prompt',
            'n_MC_l_nonprompt', 'pT_MC_l_nonprompt', 'eta_MC_l_nonprompt',
            'n_muons_genmatched_l_prompt', 'pT_muons_genmatched_l_prompt', 'eta_muons_genmatched_l_prompt',
            'n_muons_genmatched_l_nonprompt', 'pT_muons_genmatched_l_nonprompt', 'eta_muons_genmatched_l_nonprompt',
            'n_electrons_genmatched_l_prompt', 'pT_electrons_genmatched_l_prompt', 'eta_electrons_genmatched_l_prompt',
            'n_electrons_genmatched_l_nonprompt', 'pT_electrons_genmatched_l_nonprompt', 'eta_electrons_genmatched_l_nonprompt',
            'n_leptons_genmatched_l_prompt', 'pT_leptons_genmatched_l_prompt', 'eta_leptons_genmatched_l_prompt',
            'n_leptons_genmatched_l_nonprompt', 'pT_leptons_genmatched_l_nonprompt', 'eta_leptons_genmatched_l_nonprompt',
            'muon_iso_dr01', 'muon_iso_dr02', 'muon_iso_dr03',
            'electron_iso_dr01', 'electron_iso_dr02', 'electron_iso_dr03',
            'muons_genmatched_l_prompt_iso_dr01', 'muons_genmatched_l_nonprompt_iso_dr01',
            'muons_genmatched_l_prompt_iso_dr02', 'muons_genmatched_l_nonprompt_iso_dr02',
            'muons_genmatched_l_prompt_iso_dr03', 'muons_genmatched_l_nonprompt_iso_dr03',
            'electrons_genmatched_l_prompt_iso_dr01', 'electrons_genmatched_l_nonprompt_iso_dr01',
            'electrons_genmatched_l_prompt_iso_dr02', 'electrons_genmatched_l_nonprompt_iso_dr02',
            'electrons_genmatched_l_prompt_iso_dr03', 'electrons_genmatched_l_nonprompt_iso_dr03',
            'MC_l_origins', 'n_mc_l_origins'
        ]
        return branch_list