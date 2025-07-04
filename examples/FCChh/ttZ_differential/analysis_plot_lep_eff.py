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
        self.run_batch = True
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
            .Define("muon_noiso_var", "MuonNoIso_IsolationVar")
            .Define("muon_iso_var", "Muon_IsolationVar")
            .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")  # pT > 30 GeV
            .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(3)(selpt_muons)")  # |eta| < 3
            .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)")
            .Define("n_muons_sel", "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)")
            .Define("pT_muons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")
            .Define("eta_muons_sel", "FCCAnalyses::ReconstructedParticle::get_eta(sel_muons)")
            .Define("type_muons_sel", "FCCAnalyses::ReconstructedParticle::get_type(sel_muons)")
            # Electrons
            .Define("electrons", "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
            .Define("electron_noiso_var", "ElectronNoIso_IsolationVar")
            .Define("electron_iso_var", "Electron_IsolationVar")
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
            'n_muons_genmatched_l', 'pT_muons_genmatched_l', 'eta_muons_genmatched_l',
            'n_electrons_genmatched_l', 'pT_electrons_genmatched_l', 'eta_electrons_genmatched_l',
            'n_leptons_genmatched_l', 'pT_leptons_genmatched_l', 'eta_leptons_genmatched_l',
            'n_MC_l', 'pT_MC_l', 'eta_MC_l'  # Denominator branches
        ]
        return branch_list