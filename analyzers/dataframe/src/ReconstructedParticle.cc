#include "FCCAnalyses/ReconstructedParticle.h"
#include "TMath.h"
#include "TLorentzVector.h"

// std
#include <cstdlib>
#include <stdexcept>
#include <limits>

// ROOT
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RLogger.hxx>

// EDM4hep
#include "edm4hep/EDM4hepVersion.h"

namespace FCCAnalyses{

namespace ReconstructedParticle{

//#######################################################################//
//                                 sel_type                              //
//#######################################################################//
sel_type::sel_type(const int type) : m_type(type) {}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_type::operator()(
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
    if (in.at(i).PDG == m_type) {
#else
    if (in.at(i).type == m_type) {
#endif
      result.emplace_back(in.at(i));
    }
  }

  return result;
}

ROOT::VecOps::RVec<int> sel_type::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx) {
  
  ROOT::VecOps::RVec<int> idx_result;
  idx_result.reserve(in.size()); 
  
  for (size_t i = 0; i < in.size(); ++i) {
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
    if (in.at(i).PDG == m_type) {
#else
    if (in.at(i).type == m_type) {
#endif
      idx_result.emplace_back(idx.at(i));
    }
  }
  return idx_result;
}


//#######################################################################//
//                               sel_absType                             //
//#######################################################################//

sel_absType::sel_absType(const int type) : m_type(type) {
  if (m_type < 0) {
    throw std::invalid_argument(
        "ReconstructedParticle::sel_absType: Received negative value!");
  }
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_absType::operator()(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
    if (std::abs(in.at(i).PDG) == m_type) {
#else
    if (std::abs(in.at(i).type) == m_type) {
#endif
      result.emplace_back(in.at(i));
    }
  }

  return result;
}

ROOT::VecOps::RVec<int> sel_absType::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx) {
  
  ROOT::VecOps::RVec<int> idx_result;
  idx_result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
    if (std::abs(in.at(i).PDG) == m_type) {
#else
    if (std::abs(in.at(i).type) == m_type) {
#endif
      idx_result.emplace_back(idx.at(i));
    }
  }
  return idx_result;
}

//#######################################################################//
//                                  sel_pt                               //
//#######################################################################//
sel_pt::sel_pt(float arg_min_pt) : m_min_pt(arg_min_pt) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_pt::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in.at(i);
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}
ROOT::VecOps::RVec<int>  sel_pt::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx) {
  assert (in.size() == idx.size());
  ROOT::VecOps::RVec<int> idx_result;
  idx_result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in.at(i);
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      idx_result.emplace_back(idx.at(i));
    }
  }
  return idx_result;
}

//#######################################################################//
//                                 sel_eta                               //
//#######################################################################//
sel_eta::sel_eta(float arg_min_eta) : m_min_eta(arg_min_eta) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_eta::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in.at(i);
    TLorentzVector tv1;
    tv1.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    if (abs(tv1.Eta()) < abs(m_min_eta)){
      result.emplace_back(p);
    }
  }
  return result;
}

ROOT::VecOps::RVec<int>  sel_eta::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx) {
  ROOT::VecOps::RVec<int> idx_result;
  idx_result.reserve(in.size());
  for (size_t i = 0; i < idx.size(); ++i) {
    auto & p = in.at(i);
    TLorentzVector tv1;
    tv1.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    if (abs(tv1.Eta()) < abs(m_min_eta)){
      idx_result.emplace_back(idx.at(i));
    }
  }
  return idx_result;
}

//#######################################################################//
//                                  sel_p                                //
//#######################################################################//
sel_p::sel_p(float arg_min_p, float arg_max_p) : m_min_p(arg_min_p), m_max_p(arg_max_p)  {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_p::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in.at(i);
    float momentum = std::sqrt(   std::pow(p.momentum.x,2)
                                + std::pow(p.momentum.y,2)
                                + std::pow(p.momentum.z,2) );
    if ( momentum > m_min_p && momentum < m_max_p ) {
      result.emplace_back(p);
    }
  }
  return result;
}

ROOT::VecOps::RVec<int>  sel_p::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx) {
  ROOT::VecOps::RVec<int> idx_result; 
  idx_result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in.at(i);
    float momentum = std::sqrt(   std::pow(p.momentum.x,2)
                                + std::pow(p.momentum.y,2)
                                + std::pow(p.momentum.z,2) );
    if ( momentum > m_min_p && momentum < m_max_p ) {
      idx_result.emplace_back(idx.at(i));
    }
  }
  return idx_result;
}


//#######################################################################//
//                               sel_charge                              //
//#######################################################################//
sel_charge::sel_charge(int arg_charge, bool arg_abs){m_charge = arg_charge; m_abs = arg_abs;};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_charge::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in.at(i);
    if ((m_abs && abs(in.at(i).charge)==m_charge) || (m_charge==in.at(i).charge) ) {
      result.emplace_back(p);
    }
  }
  return result;
}

ROOT::VecOps::RVec<int>  sel_charge::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<int> idx) {
  ROOT::VecOps::RVec<int> idx_result;
  idx_result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in.at(i);
    if ((m_abs && abs(in.at(i).charge)==m_charge) || (m_charge==in.at(i).charge) ) {
      idx_result.emplace_back(idx.at(i));
    }
  }
  return idx_result;
}

//#######################################################################//
//                            ResonanceBuilder                           //
//#######################################################################//
resonanceBuilder::resonanceBuilder(float arg_resonance_mass) {m_resonance_mass = arg_resonance_mass;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> resonanceBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      TLorentzVector reso_lv;
      for (int i = 0; i < n; ++i) {
          if (v.at(i)) {
            reso.charge += legs.at(i).charge;
            TLorentzVector leg_lv;
            leg_lv.SetXYZM(legs.at(i).momentum.x, legs.at(i).momentum.y, legs.at(i).momentum.z, legs.at(i).mass);
            reso_lv += leg_lv;
          }
      }
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
    std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}


recoilBuilder::recoilBuilder(float arg_sqrts) : m_sqrts(arg_sqrts) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  recoilBuilder::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
  for (auto & v1: in) {
    TLorentzVector tv1;
    tv1.SetXYZM(v1.momentum.x, v1.momentum.y, v1.momentum.z, v1.mass);
    recoil_p4 -= tv1;
  }
  auto recoil_fcc = edm4hep::ReconstructedParticleData();
  recoil_fcc.momentum.x = recoil_p4.Px();
  recoil_fcc.momentum.y = recoil_p4.Py();
  recoil_fcc.momentum.z = recoil_p4.Pz();
  recoil_fcc.mass = recoil_p4.M();
  result.push_back(recoil_fcc);
  return result;
};


sel_axis::sel_axis(bool arg_pos): m_pos(arg_pos) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_axis::operator()(ROOT::VecOps::RVec<float> angle, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < angle.size(); ++i) {
    if (m_pos==1 && angle.at(i)>0.) result.push_back(in.at(i));
    if (m_pos==0 && angle.at(i)<0.) result.push_back(in.at(i));;
  }
  return result;
}


sel_tag::sel_tag(bool arg_pass): m_pass(arg_pass) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_tag::operator()(ROOT::VecOps::RVec<bool> tags, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < in.size(); ++i) {
    if (m_pass) {
      if (tags.at(i)) result.push_back(in.at(i));
    }
    else {
      if (!tags.at(i)) result.push_back(in.at(i));
    }
  }
  return result;
}



// Angular separation between the particles of a collection:
//   arg_delta = 0 / 1 / 2 :   return delta_max, delta_min, delta_average

angular_separationBuilder::angular_separationBuilder( int  arg_delta) : m_delta(arg_delta) {};
float angular_separationBuilder::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {

 float result = -9999;

 float dmax = -999;
 float dmin = 999;
 float sum = 0;
 float npairs = 0;
 for (int i=0; i < in.size(); i++) {
  if ( in.at(i).energy < 0) continue;    // "dummy" particle - cf selRP_matched_to_list
  TVector3 p1( in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z );
  for (int j=i+1; j < in.size(); j++) {
    if ( in.at(j).energy < 0) continue;   // "dummy" particle
    TVector3 p2( in.at(j).momentum.x, in.at(j).momentum.y, in.at(j).momentum.z );
    float delta_ij = fabs( p1.Angle( p2 ) );
    if ( delta_ij > dmax) dmax = delta_ij;
    if ( delta_ij < dmin) dmin = delta_ij;
    sum = sum + delta_ij;
    npairs ++;
  }
 }
 float delta_max = dmax;
 float delta_min = dmin;
 float delta_ave = sum / npairs;

 if (m_delta == 0 ) result = delta_max;
 if (m_delta == 1 ) result = delta_min;
 if (m_delta == 2 ) result = delta_ave;

 return result;
}

ROOT::VecOps::RVec<int> get_idx(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<int> result;
  for (size_t i = 0; i < in.size(); ++i) {
    result.push_back(i);
  }
  return result;
 }

 ROOT::VecOps::RVec<int> get_idx_clean(ROOT::VecOps::RVec<int> indices){
  ROOT::VecOps::RVec<int> result;
  for (size_t i = 0; i < indices.size(); ++i) {
    if (indices.at(i)>-1)
      result.push_back(indices.at(i, -1));
    //else
    //  std::cout << "electron index negative " << index.at(i)<<std::endl;
  }
  return result;
 }

ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in.at(i).momentum.x * in.at(i).momentum.x + in.at(i).momentum.y * in.at(i).momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> merge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y) {
  //to be keept as ROOT::VecOps::RVec
  std::vector<edm4hep::ReconstructedParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}


ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> remove(
  		ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x,
  		ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y) {
  //to be kept as ROOT::VecOps::RVec
  std::vector<edm4hep::ReconstructedParticleData> result;
  result.reserve( x.size() );
  result.insert( result.end(), x.begin(), x.end() );
  float epsilon = 1e-8;
  for (size_t i = 0; i < y.size(); ++i) {
    float mass1 = y.at(i).mass;
    float px1 = y.at(i).momentum.x;
    float py1 = y.at(i).momentum.y;
    float pz1 = y.at(i).momentum.z;
    for(std::vector<edm4hep::ReconstructedParticleData>::iterator
          it = std::begin(result); it != std::end(result); ++it) {
      float mass2 = it->mass;
      float px2 = it->momentum.x;
      float py2 = it->momentum.y;
      float pz2 = it->momentum.z;
      if ( abs(mass1-mass2) < epsilon &&
	   abs(px1-px2) < epsilon &&
	   abs(py1-py2) < epsilon &&
	   abs(pz1-pz2) < epsilon ) {
        result.erase(it);
        break;
      }
    }
  }
  return ROOT::VecOps::RVec(result);
}




ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> get(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < index.size(); ++i) {
    if (index.at(i)>-1)
      result.push_back(in.at(index.at(i)));
    //else
    //  std::cout << "electron index negative " << index.at(i)<<std::endl;
  }
  return result;
}

ROOT::VecOps::RVec<float> get(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<float> in){

  ROOT::VecOps::RVec<float> result;
  // assert(*std::max_element(index.begin(),index.end()) < in.size());

  for (size_t i = 0; i < index.size(); ++i) {
    if (index.at(i)>-1)
      result.push_back(in.at(index.at(i)));
    //else
    //  std::cout << "electron index negative " << index.at(i)<<std::endl;
  }
  return result;
}


TLorentzVector get_P4vis(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
    TLorentzVector P4sum;
    for (auto & p: in) {
      TLorentzVector tlv;
      tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
      P4sum += tlv;
    }
    return P4sum;
  }


ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}


ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<TLorentzVector> get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}

TLorentzVector get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, int index) {
  TLorentzVector result;
  auto & p = in[index];
  result.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
  return result;
}

TLorentzVector get_tlv(edm4hep::ReconstructedParticleData in) {
  TLorentzVector result;
  result.SetXYZM(in.momentum.x, in.momentum.y, in.momentum.z, in.mass);
  return result;
}

ROOT::VecOps::RVec<int>
get_type(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in) {
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
    result.push_back(p.PDG);
#else
    result.push_back(p.type);
#endif
  }
  return result;
}


int get_n(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x) {
  int result =  x.size();
  return result;
}


ROOT::VecOps::RVec<bool> getJet_btag(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid, ROOT::VecOps::RVec<float> values){
  ROOT::VecOps::RVec<bool> result;
  //std::cout << "========================new event=======================" <<std::endl;
  for (size_t i = 0; i < index.size(); ++i) {
    result.push_back(values.at(pid.at(index.at(i)).parameters_begin));

    //std::cout << pid.at(index.at(i)).parameters_begin << "  ==  " << pid.at(index.at(i)).parameters_end << std::endl;
    //for (unsigned j = pid.at(index.at(i)).parameters_begin; j != pid.at(index.at(i)).parameters_end; ++j) {
    //  std::cout << " values : " << values.at(j) << std::endl;
    //}
  }
  return result;
}

int getJet_ntags(ROOT::VecOps::RVec<bool> in) {
  int result =  0;
  for (size_t i = 0; i < in.size(); ++i)
    if (in.at(i))result+=1;
  return result;
}

//#######################################################################//
//                              getElectrons                             //
//#######################################################################//
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> getElectrons(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
    if (std::abs(in.at(i).PDG) == 11) {
#else
    if (std::abs(in.at(i).type) == 11) {
#endif
      result.emplace_back(in.at(i));
    }
  }
  return result;
}

//#######################################################################//
//                                getMuons                               //
//#######################################################################//
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> getMuons(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
    if (std::abs(in.at(i).PDG) == 13) {
#else
    if (std::abs(in.at(i).type) == 13) {
#endif
      result.emplace_back(in.at(i));
    }
  }
  return result;
}
// compute the cone isolation for reco particles
coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max(arg_dr_max) {}

double coneIsolation::deltaR(double eta1, double phi1, double eta2, double phi2) {
    return TMath::Sqrt(TMath::Power(eta1 - eta2, 2) + TMath::Power(phi1 - phi2, 2));
}

ROOT::VecOps::RVec<float> coneIsolation::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> rps) {
    ROOT::VecOps::RVec<float> result;
    result.reserve(in.size());

    // If input vector is empty, return a vector with -999
    if (in.size() == 0) {
        result.emplace_back(-999.0);
        return result;
    }

    std::vector<TLorentzVector> lv_reco;
    std::vector<TLorentzVector> lv_charged;
    std::vector<TLorentzVector> lv_neutral;

    for (size_t i = 0; i < rps.size(); ++i) {
        TLorentzVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);
        if (rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }

    for (size_t i = 0; i < in.size(); ++i) {
        TLorentzVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
        lv_reco.push_back(tlv);
    }

    // compute the isolation
    for (auto &lv_reco_ : lv_reco) {
        double sumNeutral = 0.0;
        double sumCharged = 0.0;

        // charged
        for (auto &lv_charged_ : lv_charged) {
            double dr = this->deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if (dr > this->dr_min && dr < this->dr_max) {
                sumCharged += lv_charged_.P();
                std::cout << "Charged particle in cone: dR=" << dr << ", P=" << lv_charged_.P() << std::endl;
            }
        }

        // neutral
        for (auto &lv_neutral_ : lv_neutral) {
            double dr = this->deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if (dr > this->dr_min && dr < this->dr_max) {
                sumNeutral += lv_neutral_.P();
                std::cout << "Neutral particle in cone: dR=" << dr << ", P=" << lv_neutral_.P() << std::endl;
            }
        }

        double sum = sumCharged + sumNeutral;
        if (lv_reco_.Pt() == 0) {
            std::cout << "Warning: Particle pT is 0, isolation ratio cannot be computed properly." << std::endl;
        }
        double ratio = sum / lv_reco_.P();
        std::cout << "Isolation calculation for particle: pT=" << lv_reco_.Pt() 
                  << ", Total P=" << lv_reco_.P() 
                  << ", Sum Charged=" << sumCharged 
                  << ", Sum Neutral=" << sumNeutral 
                  << ", Isolation Ratio=" << ratio << std::endl;
        result.emplace_back(ratio);
    }
    return result;
}
ROOT::VecOps::RVec<float> sumJetPt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets) {
    ROOT::VecOps::RVec<float> result;
    float totalPt = 0.0;
    for (const auto& jet : jets) {
        TLorentzVector tlv;
        tlv.SetPxPyPzE(jet.momentum.x, jet.momentum.y, jet.momentum.z, jet.energy);
        totalPt += tlv.Pt();
    }
    result.emplace_back(totalPt);
    return result;
}

/**
 * Compute the minimum delta R (dR) between each prompt reconstructed particle 
 * and any other reconstructed particle in the event.
 * 
 * @param prompt_parts Vector of prompt reconstructed particles to evaluate.
 * @param reco_parts_all Vector of all reconstructed particles in the event.
 * @return A vector of minimum dR values for each prompt particle.
 */
ROOT::VecOps::RVec<float> getMinDRToAny(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> prompt_parts,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_parts_all) {
    
    ROOT::VecOps::RVec<float> min_dR_values;
    
    // If no prompt particles, return empty vector
    if (prompt_parts.size() < 1) {
        return min_dR_values;
    }
    
    // Loop over each prompt particle
    for (const auto& prompt_part : prompt_parts) {
        TLorentzVector tlv_prompt;
        tlv_prompt.SetPxPyPzE(prompt_part.momentum.x, prompt_part.momentum.y, 
                             prompt_part.momentum.z, prompt_part.energy);
        float eps = 1e-6;

        float min_dR = 999.0; // Initialize with a large value
        
        // Loop over all reconstructed particles to find minimum dR
        for (const auto& reco_part : reco_parts_all) {
            TLorentzVector tlv_reco;
            tlv_reco.SetPxPyPzE(reco_part.momentum.x, reco_part.momentum.y, 
                               reco_part.momentum.z, reco_part.energy);
            // skip if the prompt and reco particles have the same pt  (same particle)                 
            if (std::abs(tlv_prompt.Pt() - tlv_reco.Pt()) < eps) continue;

            float dR = tlv_prompt.DeltaR(tlv_reco);
            
            
            if (dR < min_dR) {
                min_dR = dR;
            }
        }
        
        min_dR_values.push_back(min_dR);
    }
    
    return min_dR_values;
}

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>in, ROOT::VecOps::RVec<float> iso) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
      auto & p = in[i];
      if (iso[i] < m_max_iso) {
          result.emplace_back(p);
      }
  }
  return result;
}

//#######################################################################//
//                            overlapRemoval                             //
//#######################################################################//

overlapRemoval::overlapRemoval(float dR_threshold) : m_dR_threshold(dR_threshold) {}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> overlapRemoval::removeElectronsNearMuons(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> electrons,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons) {
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    result.reserve(electrons.size());
    
    for (const auto& electron : electrons) {
        bool keepElectron = true;
        
        // Check against muons
        for (const auto& muon : muons) {
            if (deltaR(electron, muon) < m_dR_threshold) {
                keepElectron = false;
                break;
            }
        }
        
        if (keepElectron) {
            result.emplace_back(electron);
        }
    }
    
    return result;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> overlapRemoval::removeJetsNearLeptons(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons) {
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    result.reserve(jets.size());
    
    for (const auto& jet : jets) {
        bool keepJet = true;
        
        // Check against all leptons
        for (const auto& lepton : leptons) {
            if (deltaR(jet, lepton) < m_dR_threshold) {
                keepJet = false;
                break;
            }
        }
        
        if (keepJet) {
            result.emplace_back(jet);
        }
    }
    
    return result;
}

// Convenience standalone functions (can be used directly in DataFrame operations)
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> removeElectronsNearMuons_standalone(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> electrons,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons,
    float dR_threshold = 0.2) {
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    result.reserve(electrons.size());
    
    for (const auto& electron : electrons) {
        bool keepElectron = true;
        
        for (const auto& muon : muons) {
            TLorentzVector tlv_electron, tlv_muon;
            tlv_electron.SetXYZM(electron.momentum.x, electron.momentum.y, electron.momentum.z, electron.mass);
            tlv_muon.SetXYZM(muon.momentum.x, muon.momentum.y, muon.momentum.z, muon.mass);
            
            if (tlv_electron.DeltaR(tlv_muon) < dR_threshold) {
                keepElectron = false;
                break;
            }
        }
        
        if (keepElectron) {
            result.emplace_back(electron);
        }
    }
    
    return result;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> removeJetsNearLeptons_standalone(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons,
    float dR_threshold = 0.2) {
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    result.reserve(jets.size());
    
    for (const auto& jet : jets) {
        bool keepJet = true;
        
        for (const auto& lepton : leptons) {
            TLorentzVector tlv_jet, tlv_lepton;
            tlv_jet.SetXYZM(jet.momentum.x, jet.momentum.y, jet.momentum.z, jet.mass);
            tlv_lepton.SetXYZM(lepton.momentum.x, lepton.momentum.y, lepton.momentum.z, lepton.mass);
            
            if (tlv_jet.DeltaR(tlv_lepton) < dR_threshold) {
                keepJet = false;
                break;
            }
        }
        
        if (keepJet) {
            result.emplace_back(jet);
        }
    }
    
    return result;
}


}//end NS ReconstructedParticle

}//end NS FCCAnalyses