
#ifndef  RECONSTRUCTEDPARTICLE_ANALYZERS_H
#define  RECONSTRUCTEDPARTICLE_ANALYZERS_H

// STL
#include <cmath>
#include <vector>

// ROOT
#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"

// EDM4hep
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/ParticleIDData.h"

namespace FCCAnalyses{

namespace ReconstructedParticle{

  /// build the resonance from 2 particles from an arbitrary list of input ReconstructedPartilces. Keep the closest to the mass given as input
  struct resonanceBuilder {
    float m_resonance_mass;
    resonanceBuilder(float arg_resonance_mass);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs);
  };

  /// build the recoil from an arbitrary list of input ReconstructedPartilces and the center of mass energy
  struct recoilBuilder {
    recoilBuilder(float arg_sqrts);
    float m_sqrts = 240.0;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) ;
  };

  /// return the angular separations (min / max / average) between a collection of particles
  struct angular_separationBuilder {
    angular_separationBuilder( int arg_delta); //  0, 1, 2 = max, min, average
    int m_delta = 0;
    float operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) ;
  };

  /// select ReconstructedParticles by type
  /// Note: type might not correspond to PDG ID
  struct sel_type {
    sel_type(const int type);
    const int m_type;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);
  };

  /// select ReconstructedParticles by type absolute value
  /// Note: type might not correspond to PDG ID
  struct sel_absType {
    sel_absType(const int type);
    const int m_type;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);

  };

  /// select ReconstructedParticles with transverse momentum greater than a minimum value [GeV]
  struct sel_pt {
    sel_pt(float arg_min_pt);
    float m_min_pt = 1.; //> transverse momentum threshold [GeV]
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);
  };

  /// select ReconstructedParticles with absolute pseudorapidity less than a maximum absolute value
  struct sel_eta {
    sel_eta(float arg_min_eta);
    float m_min_eta = 2.5; //> pseudorapidity threshold
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);
  };

  /// select ReconstructedParticles with momentum greater than a minimum value [GeV]
  struct sel_p {
    sel_p(float arg_min_p, float arg_max_p = 1e10);
    float m_min_p = 1.; //> momentum threshold [GeV]
    float m_max_p = 1e10; //< momentum threshold [GeV]
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);
  };

  /// select ReconstructedParticles with charge equal or in asolute value
  struct sel_charge {
    sel_charge(int arg_charge, bool arg_abs);
    float m_charge; //> charge condition
    bool  m_abs;//> absolute value of the charge
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);
  };

  /// select a list of reconstructed particles depending on the angle cosTheta axis
  struct sel_axis{
    bool m_pos = 0; //> Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0
    sel_axis(bool arg_pos);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<float> angle, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int> operator() (ROOT::VecOps::RVec<float> angle, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);
  };

  /// select a list of reconstructed particles depending on the status of a certain boolean flag
  struct sel_tag {
    bool m_pass; // if pass is true, select tagged jets. Otherwise select anti-tagged ones
    sel_tag(bool arg_pass);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<bool> tags, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<bool> tags, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx);
  };

  /// return reconstructed particles
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> get(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  // return other stuff
  ROOT::VecOps::RVec<float> get(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<float> in);

  // return the indices
  ROOT::VecOps::RVec<int> get_idx(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  // clean up the indices
  ROOT::VecOps::RVec<int> get_idx_clean(ROOT::VecOps::RVec<int> indices);

  /// return the transverse momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the pseudo-rapidity of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the rapidity of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the theta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the phi of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the energy of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the masses of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the charges of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the type of the input ReconstructedParticles
  ROOT::VecOps::RVec<int> get_type(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the TlorentzVector of the input ReconstructedParticles
  ROOT::VecOps::RVec<TLorentzVector> get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the TlorentzVector of the indexed input ReconstructedParticles
  TLorentzVector get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, int index);

  /// return the TlorentzVector of the one input ReconstructedParticle
  TLorentzVector get_tlv(edm4hep::ReconstructedParticleData in);

  /// return visible 4-momentum vector
  TLorentzVector get_P4vis(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// concatenate both input vectors and return the resulting vector
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> merge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

  /// remove elements of vector y from vector x
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> remove( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

  /// return the size of the input collection
  int get_n(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// returns the bjet flavour
  ROOT::VecOps::RVec<bool> getJet_btag(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid, ROOT::VecOps::RVec<float> values);

  /// get number of b-jets
  int getJet_ntags(ROOT::VecOps::RVec<bool> in);

  /// get electrons
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> getElectrons(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// get muons
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> getMuons(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);


struct coneIsolation {
    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2);
    float dr_min = 0;
    float dr_max = 0.4;
    ROOT::VecOps::RVec<float> operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> rps);
};

  /// sum the transverse momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> sumJetPt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets);

  /// get the minimum delta R between a prompt particle and any other particle in the event
  ROOT::VecOps::RVec<float> getMinDRToAny(
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> prompt_parts,
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_parts_all);

  /// calculate the delphes isolation criterion using only hadrons
  ROOT::VecOps::RVec<float> get_IP_delphes_hadrons(
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> test_parts,
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_parts_all,
      float dR_min, float pT_min, bool exclude_light_leps);

  struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<float> iso);
  };

  //#######################################################################//
//                            overlapRemoval                             //
//#######################################################################//
class overlapRemoval {
  private:
      float m_dR_threshold;
      
      // Helper function to calculate deltaR between two particles
      float deltaR(const edm4hep::ReconstructedParticleData& p1, 
                   const edm4hep::ReconstructedParticleData& p2) {
          TLorentzVector tlv1, tlv2;
          tlv1.SetXYZM(p1.momentum.x, p1.momentum.y, p1.momentum.z, p1.mass);
          tlv2.SetXYZM(p2.momentum.x, p2.momentum.y, p2.momentum.z, p2.mass);
          return tlv1.DeltaR(tlv2);
      }
  
  public:
      overlapRemoval(float dR_threshold = 0.2);
      
      // Individual step functions following your required order
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> removeElectronsNearMuons(
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> electrons,
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons);
      
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> removeJetsNearLeptons(
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons);
        
        
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> removeJetsNearLeptons_standalone(
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons,
          float dR_threshold = 0.2);

       ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> removeElectronsNearMuons_standalone(
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> electrons,
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons,
          float dR_threshold = 0.2);
        
  };
  
}//end NS ReconstructedParticle

}//end NS FCCAnalyses
#endif