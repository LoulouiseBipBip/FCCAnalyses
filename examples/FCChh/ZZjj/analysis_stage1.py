"""
Ntuple production for FCC-hh analysis of ZZjj production
"""

from argparse import ArgumentParser

fraction = 1

# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis:
    """
    differential ZZjj analysis
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
             'mgp8_pp_ZZjj_HF_5f_84TeV_zzlep': {"fraction": fraction, 'Chunks': 50},
            
            'mgp8_pp_ttz_5f_84TeV_ttzlep': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_tttt_5f_84TeV_4tlep': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_tth_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            
            'mgp8_pp_zzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_wzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_wwz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            
            'mgp8_pp_wwww_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_wwwz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_wwzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_wzzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_zzzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            
            'mgp8_pp_ttzz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
            'mgp8_pp_ttwz_5f_84TeV': {"fraction": fraction, 'Chunks': 50},
           
                }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/"

        # Optional: output directory, default is local running directory
        self.output_dir = "/eos/user/l/lberiet/ZZjj_results/results/"
        #self.output_dir = "/eos/user/s/selvaggi/analysis/ttbar_differential_v2/"

        # Optional: analysisName, default is ''
        self.analysis_name = "FCC-hh ZZjj analysis"

        # Optional: number of threads to run on, default is 'all available'
        self.ncpus = 4

        # Optional: running on HTCondor, default is False
        # self.run_batch = False
        self.run_batch = True

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
            # select muons 
            .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)") 

            .Define("muon_noiso_var", "MuonNoIso_IsolationVar")
            .Define("muon_iso_var", "Muon_IsolationVar")
            .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
            .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
            .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") #sort by pT
            .Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
            .Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")
            .Define("type_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_type(sel_muons)")

            # select electrons
            .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")

            .Define("electron_noiso_var", "ElectronNoIso_IsolationVar")
            .Define("electron_iso_var", "Electron_IsolationVar")
            .Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
            .Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
            .Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)") #sort by pT
            .Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
            .Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")

            # combine leptons
            #.Define("OS_ee_pairs", "AnalysisFCChh::getOSPairs(sel_muons)") 
            #.Define("OS_mm_pairs", "AnalysisFCChh::getOSPairs(sel_electrons)") 
            #.Define("Z_ll_candidate_unmerged", "AnalysisFCChh::getBestOSPair(OS_ee_pairs, OS_mm_pairs)") 
            #.Define("Z_ll_flavor", "Z_ll_candidate_unmerged[0].flavour_flag")

            
            
            # merge leptons
            .Define("sel_leptons_unsort", "FCCAnalyses::ReconstructedParticle::merge(sel_muons, sel_electrons)")
            .Define("sel_leptons", "AnalysisFCChh::SortParticleCollection(sel_leptons_unsort)") #sort by pT
            .Define("pT_leptons_sel", "FCCAnalyses::ReconstructedParticle::get_pt(sel_leptons)")
           
            #.Define("Zll_pairs", "AnalysisFCChh::build_Zll_pairs(sel_muons, sel_electrons)")
            #.Define("Zll_pairs_size", "Zll_pairs.size()")
            #.Define("Z_ll_1_mass", "FCCAnalyses::ReconstructedParticle::get_mass(Zll_pairs[0])")
            #.Define('Z_ll_2_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Zll_pairs[1])')
            .Define("Z_ll_and_second_pairs", "AnalysisFCChh::getZllAndSecondOSPair(sel_muons, sel_electrons)")
            .Define("Z_ll_and_second_pairs_size", "Z_ll_and_second_pairs.size()")
            .Define("Z_ll_and_second_pairs_merged", "AnalysisFCChh::merge_pairs(Z_ll_and_second_pairs)")
            
            .Define('Z_ll_1_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[0]')
            .Define('Z_ll_2_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[1]')
            .Define('Z_ll_1_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[0]')
            .Define('Z_ll_2_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[1]')
            .Define('Z_ll_2_flavor', 'Z_ll_and_second_pairs[1].flavour_flag') #1 or 2 foe SF
            #.Define('Z_ll_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[0]')
            #.Define('Z_ll_eta', 'FCCAnalyses::ReconstructedParticle::get_eta(Z_ll_and_second_pairs_merged)[0]')
            #.Define('Z_ll_flavor', 'Z_ll_and_second_pairs[0].flavour_flag')

            .Define('Second_Pair_mass', 'FCCAnalyses::ReconstructedParticle::get_mass(Z_ll_and_second_pairs_merged)[1]')
            .Define('Second_Pair_pt', 'FCCAnalyses::ReconstructedParticle::get_pt(Z_ll_and_second_pairs_merged)[1]')
            .Define('Second_Pair_eta', 'FCCAnalyses::ReconstructedParticle::get_eta(Z_ll_and_second_pairs_merged)[1]')
            .Define('Second_Pair_flavor', 'Z_ll_and_second_pairs[1].flavour_flag')

            .Define("n_leptons", "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")
            .Define('dR_ll', 'AnalysisFCChh::get_angularDist_pair(Z_ll_and_second_pairs, TString(\"dR\"))[0]')
            .Define('dR_second_pair', 'AnalysisFCChh::get_angularDist_pair(Z_ll_and_second_pairs, TString(\"dR\"))[1]')
            #.Define('dR_second_pair', 'AnalysisFCChh::get_angularDist_pair(Z_ll_and_second_pairs, TString(\"dR\"))[1]')

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
            .Define("pT_bjets", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
            
            # missing ET
            .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")

            # ######### cut on number of bjets and leptons
            #.Filter("n_leptons >= 3")
            #.Define(f"cut{len(selections)}", f"{len(selections)}")
           

            #.Filter("n_bjets == 2")
            #.Define(f"cut{len(selections)}", f"{len(selections)}")
        

            # calculate HT
            .Define("HT", "ScalarHT")
            .Define("ht_tev", "HT/1000.")
            

            
   
        )
        return dframe2

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        """
        Output variables which will be saved to output root file.
        """
        branch_list = [
            "weight",
            "n_jets",
            "n_bjets",
            "pT_bjets",
            "pT_jets",
            "n_leptons",
            "HT",
            "ht_tev",
            "MET",
            "Z_ll_and_second_pairs_size",
            "Z_ll_1_mass",
            "Z_ll_2_mass",
            "Z_ll_1_pt",
            "Z_ll_2_pt",
            "Z_ll_2_flavor",
            #"Z_ll_pt",
            #"Z_ll_eta",
            #"Second_Pair_flavor",
            #"Second_Pair_mass",
            #"Second_Pair_pt",
            #"Second_Pair_eta",
            "dR_ll",
            "dR_second_pair",
            "type_muons_sel",
            
            #"muon_noiso_var",
            #"muon_iso_var",
            #"electron_noiso_var",
            #"electron_iso_var",
            
            #"recoHT",
                       
        ]
        return branch_list