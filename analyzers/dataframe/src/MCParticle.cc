#include "FCCAnalyses/MCParticle.h"
#include <iostream>
#include <algorithm>
#include <set>
#include "podio/ObjectID.h"
#include "TString.h"


namespace FCCAnalyses{

namespace MCParticle{

sel_genStatus::sel_genStatus(int arg_status) : m_status(arg_status) {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_genStatus::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (p.generatorStatus == m_status) {
      result.emplace_back(p);
    }
  }
  return result;
}

sel_pdgID::sel_pdgID(int arg_pdg, bool arg_chargeconjugate) : m_pdg(arg_pdg), m_chargeconjugate( arg_chargeconjugate )  {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_pdgID::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ( m_chargeconjugate ) {
        if ( std::abs( p.PDG ) == std::abs( m_pdg)  ) result.emplace_back(p);
    }
    else {
        if ( p.PDG == m_pdg ) result.emplace_back(p);
    }
  }
  return result;
}



get_decay::get_decay(int arg_mother, int arg_daughters, bool arg_inf){m_mother=arg_mother; m_daughters=arg_daughters; m_inf=arg_inf;};
bool get_decay::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in,  ROOT::VecOps::RVec<int> ind){

  bool result=false;
  for (size_t i = 0; i < in.size(); ++i) {
    if (in[i].PDG!=m_mother)continue;
    int ndaughters=0;
    for (unsigned j = in.at(i).daughters_begin; j != in.at(i).daughters_end; ++j) {
      if (std::abs(in[ind.at(j)].PDG)==m_daughters && m_inf==false)ndaughters+=1;
      else if (std::abs(in[ind.at(j)].PDG)<=m_daughters && m_inf==true)ndaughters+=1;
    }
    //if (ndaughters>1){
    if (ndaughters>=1){
      result=true;
      return result;
    }
  }
  return result;
}

sel_pt::sel_pt(float arg_min_pt) : m_min_pt(arg_min_pt) {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_pt::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}

//Sort MCParticles by transverse momentum
ROOT::VecOps::RVec<edm4hep::MCParticleData> SortParticleCollection(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> particles_in) {
  if (particles_in.size() < 2) {
    return particles_in;
  } else {
    auto sort_by_pT = [&](edm4hep::MCParticleData part_i,
                          edm4hep::MCParticleData part_j) {
      TLorentzVector tlv_i;
      tlv_i.SetXYZM(part_i.momentum.x, part_i.momentum.y, part_i.momentum.z, part_i.mass);
      TLorentzVector tlv_j;
      tlv_j.SetXYZM(part_j.momentum.x, part_j.momentum.y, part_j.momentum.z, part_j.mass);
      return (tlv_i.Pt() > tlv_j.Pt());
    };
    std::sort(particles_in.begin(), particles_in.end(), sort_by_pT);
    return particles_in;
  }
}


sel_eta::sel_eta(float arg_min_eta) : m_min_eta(arg_min_eta) {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_eta::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    if (std::abs(tlv.Eta()) < m_min_eta) {
      result.emplace_back(p);
    }
  }
  return result;
}




filter_pdgID::filter_pdgID(int arg_pdgid, bool arg_abs){m_pdgid = arg_pdgid; m_abs = arg_abs;};
bool  filter_pdgID::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ((m_abs && abs(p.PDG) == m_pdgid) || (p.PDG == m_pdgid)) return true;
  }
  return false;
}


get_EventPrimaryVertex::get_EventPrimaryVertex( int arg_genstatus) { m_genstatus = arg_genstatus; };
TVector3 get_EventPrimaryVertex::operator() ( ROOT::VecOps::RVec<edm4hep::MCParticleData> in )  {
  TVector3 result(-1e12,-1e12,-1e12);
  int i=0;
  for (auto & p: in) {
     i++;
     if ( p.generatorStatus == m_genstatus ) {   // generator status code for the incoming particles of the hardest subprocess
       TVector3 res( p.vertex.x, p.vertex.y, p.vertex.z );
       result = res;
       break;
     }
   }

  return result;
}

get_EventPrimaryVertexP4::get_EventPrimaryVertexP4() {};
TLorentzVector get_EventPrimaryVertexP4::operator() ( ROOT::VecOps::RVec<edm4hep::MCParticleData> in )  {
  TLorentzVector result(-1e12,-1e12,-1e12,-1e12);
  Bool_t found_py8 = false;
  //std::cout<<"-------------------------------------------"<<std::endl;
  // first try pythia8 gen status == 21 code;
  for (auto & p: in) {
     if ( p.generatorStatus == m_genstatus ) {   // generator status code for the incoming particles of the hardest subprocess
       // vertex.time is in s, convert in mm here.
       TLorentzVector res( p.vertex.x, p.vertex.y, p.vertex.z, p.time * 1.0e3 * 2.99792458e+8);
       result = res;
       found_py8 = true;
       break;
     }
   }

   if (!found_py8) {
     for (auto & p: in) {
        // std::cout<< p.generatorStatus<<", "<<p.PDG<<", "<<p.momentum.x<<", "<<p.momentum.y<<",     "<< p.vertex.y<<", "<< p.vertex.z<<", "<< p.time * 1.0e3 * 2.99792458e+8<<std::endl;
        if ( p.generatorStatus == 2 and abs(p.vertex.z) > 1.e-12 ) {   // generator status code for the incoming particles of the hardest subprocess
          // vertex.time is in s, convert in mm here.
          TLorentzVector res( p.vertex.x, p.vertex.y, p.vertex.z, p.time * 1.0e3 * 2.99792458e+8);
          result = res;
          break;
        }
      }
   }
  //std::cout<<result.X()<<", "<<result.Y()<<", "<<result.Z()<<", "<<result.T()<<std::endl;
  return result;
}

get_tree::get_tree(int arg_index) : m_index(arg_index) {};
ROOT::VecOps::RVec<int> get_tree::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind){
  ROOT::VecOps::RVec<int> result;
  auto & particle = in[m_index];

  //for (unsigned j = in.at(i).parents_begin; j != in.at(i).parents_end; ++j){
  //  if
  //  result.push_back(ind.at(j));


  std::cout << "Thomas logic"<<std::endl;

  for (size_t i = 0; i < in.size(); ++i) {
    // all the other cout
    std::cout << i  << " status " << in[i].generatorStatus << " pdg " << in[i].PDG << " p beg "<< in.at(i).parents_begin << " p end " <<in.at(i).parents_end << "  mc size " << in.size() << "  ind size "<<ind.size() << std::endl;
    for (unsigned j = in.at(i).parents_begin; j != in.at(i).parents_end; ++j) {
      std::cout << "   ==index " << j <<" parents " << ind.at(j) << std::endl;
    }
  }
  //std::cout << "END Thomas logic"<<std::endl;

  /*  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    std::cout <<  "here" << std::endl;

    if (p.generatorStatus != m_index) continue;
    ROOT::VecOps::RVec<int> tree;
    tree.push_back(in.at(ind.at(i)).parents_begin);
    while(true){
      std::cout <<  "tree back " << tree.back() << std::endl;
      //      std::cout <<
      tree.push_back(in.at(ind.at(tree.back())).parents_begin);
    }
    result.push_back(tree);
  }
  return result;*/
  return result;
}


ROOT::VecOps::RVec<float> get_total_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  float totalPt = 0.0;
  for (auto & p : in) {
    float pt = sqrt(p.momentum.x * p.momentum.x + p.momentum.y * p.momentum.y);
    totalPt += pt;
  }
  result.push_back(totalPt);
  return result;
}



ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].momentum.x * in[i].momentum.x + in[i].momentum.y * in[i].momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::MCParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData> x, ROOT::VecOps::RVec<edm4hep::MCParticleData> y) {
  //to be keept as std::vector
  std::vector<edm4hep::MCParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}


ROOT::VecOps::RVec<float> get_time(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.time);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pdg(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.PDG);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_genStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.generatorStatus);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_simStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.simulatorStatus);
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::Vector3d> get_vertex(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.vertex);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.z);
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::Vector3d> get_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.endpoint);
  }
  return result;
}

// E.P : "endpoint" is currenly not filled in the Particle block :-(
// hence retrieve the decay vertices differently :
ROOT::VecOps::RVec<edm4hep::Vector3d> get_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind )  {
        // ( carefull : if a Bs has oscillated into a Bsbar, this returns the production vertex of the Bsbar )
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    edm4hep::Vector3d vertex(1e12, 1e12, 1e12);  // a default value for stable particles
    int db = p.daughters_begin ;
    int de = p.daughters_end;
    if (db != de) { // particle unstable
        int d1 = ind[db] ;   // first daughter
        if ( d1 >= 0 && d1 < in.size() ) {
            vertex = in.at(d1).vertex ;
        }
    }
    result.push_back(vertex);
  }
  return result;
}



ROOT::VecOps::RVec<float> get_endPoint_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_endPoint_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_endPoint_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}
ROOT::VecOps::RVec<float> get_invariant_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  TLorentzVector total_tlv;
  for (auto & p : in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    total_tlv += tlv;
  }
  result.push_back(total_tlv.M());
  return result;
}


ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.E());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<TLorentzVector> get_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}

int get_n(ROOT::VecOps::RVec<edm4hep::MCParticleData> x) {
  int result =  x.size();
  return result;
}





ROOT::VecOps::RVec<int> get_parentid(ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents){
  ROOT::VecOps::RVec<int> result;
  /*std::cout <<"================== Full Truth=================" <<std::endl;
  for (size_t i = 0; i < mc.size(); ++i) {
    std::cout << "i= " << i << "  PDGID "<< mc.at(i).PDG  <<  "  status  " << mc.at(i).generatorStatus << std::endl;
    for (unsigned j = mc.at(i).parents_begin; j != mc.at(i).parents_end; ++j)
      std::cout << "   ==index " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;

  }*/

  //std::cout <<"================== NEW EVENT=================" <<std::endl;
  for (size_t i = 0; i < mcind.size(); ++i) {

    if (mcind.at(i)<0){
      result.push_back(-999);
      continue;
    }
    //std::cout << "mc ind " << mcind.at(i) << "  PDGID "<< mc.at(mcind.at(i)).PDG  << "  status  " << mc.at(mcind.at(i)).generatorStatus << std::endl;
    for (unsigned j = mc.at(mcind.at(i)).parents_begin; j != mc.at(mcind.at(i)).parents_end; ++j) {
      //std::cout << "   ==index " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;
      // result.push_back(parents.at(j));
    }
    //std::cout << mc.at(mcind.at(i)).parents_begin <<"---"<< mc.at(mcind.at(i)).parents_end<< std::endl;
    if (mc.at(mcind.at(i)).parents_end - mc.at(mcind.at(i)).parents_begin>1) {
      //std::cout << "-999" << std::endl;
      result.push_back(-999);
    }
    else {
      //std::cout << "not -999 "<< parents.at(mc.at(mcind.at(i)).parents_begin) << std::endl;
      result.push_back(parents.at(mc.at(mcind.at(i)).parents_begin));
    }
  }
  return result;
}


// ----------------------------------------------------------------------------------------------------------------------------------

// returns one MCParticle selected by its index in the particle block
edm4hep::MCParticleData sel_byIndex( int idx, ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
    edm4hep::MCParticleData dummy;
    if ( idx >= 0 && idx < in.size() ) {
           return in.at(idx) ;
    }
    else {
           std::cout << " !!!! in sel_byIndex : index = " << idx << " is larger than the size of the MCParticle block " << in.size() << std::endl;
    }
    return dummy;
}


// ----------------------------------------------------------------------------------------------------------------------------------

std::vector<int> get_list_of_stable_particles_from_decay( int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

  std::vector<int> res;
  // i = index of a MC particle in the Particle block
  // in = the Particle collection
  // ind = the block with the indices for the daughters, Particle#1.index

  // returns a vector with the indices (in the Particle block) of the stable daughters of the particle i,
  // from the complete decay chain.

  if ( i < 0 || i >= in.size() ) return res;

  int db = in.at(i).daughters_begin ;
  int de = in.at(i).daughters_end;

  if ( db != de ) {// particle is unstable
    //int d1 = ind[db] ;
    //int d2 = ind[de-1];
    //for (int idaughter = d1; idaughter <= d2; idaughter++) {
    for (int id = db; id < de; id++) {
      int idaughter = ind[ id ];
      std::vector<int> rr = get_list_of_stable_particles_from_decay( idaughter, in, ind) ;
      res.insert( res.end(), rr.begin(), rr.end() );
    }
  }
  else {    // particle is stable
     res.push_back( i ) ;
     return res ;
  }
  return res;
}

// ----------------------------------------------------------------------------------------------------------------------------------

std::vector<int> get_list_of_particles_from_decay(int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

  std::vector<int> res;

  // i = index of a MC particle in the Particle block
  // in = the Particle collection
  // ind = the block with the indices for the daughters, Particle#1.index

  // returns a vector with the indices (in the Particle block) of the daughters of the particle i

  if ( i < 0 || i >= in.size() ) return res;

  int db = in.at(i).daughters_begin ;
  int de = in.at(i).daughters_end;
  if  ( db == de ) return res;   // particle is stable
  //int d1 = ind[db] ;
  //int d2 = ind[de-1];
  //for (int idaughter = d1; idaughter <= d2; idaughter++) {
     //res.push_back( idaughter);
  for (int id = db; id < de; id++) {
     res.push_back( ind[id] ) ;
  }
  return res;
}


// ----------------------------------------------------------------------------------------------------------------------------------

// obsolete: keep for the while, for backward compatibility

std::vector<int> list_of_stable_particles_from_decay( int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {
   std::cout << " -------- OBSOLETE -----   call to get_list_of_stable_particles_from_decay , please update your code ----- " << std::endl;
   return get_list_of_stable_particles_from_decay( i, in, ind );
}

std::vector<int> list_of_particles_from_decay(int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {
   std::cout << " -------- OBSOLETE -----   call to get_list_of_particles_from_decay , please update your code ----- " << std::endl;
  return get_list_of_particles_from_decay( i, in, ind );
}






// ----------------------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<int>  get_indices_MotherByIndex ( int imother,
						     std::vector<int> m_pdg_daughters,
						     bool m_stableDaughters,
						     bool m_chargeConjugateDaughters,
						     bool m_inclusiveDecay,
						     ROOT::VecOps::RVec<edm4hep::MCParticleData> in,
						     ROOT::VecOps::RVec<int> ind) {

   // Look for a specific decay specified by the mother index in the Particle block,
   // and by the PDG_ids of the daughters
   // If m_inclusiveDecay is true, then at least this list of daughters must be included in the decay
   // Returns a vector with the indices, in the Particle block, of the mother and of
   // the daughters - in the order defined by std::vector<int> pdg_daughters.


  ROOT::VecOps::RVec<int>  result;

  std::vector<int> products ;
  if ( m_stableDaughters ) {
    products = get_list_of_stable_particles_from_decay( imother, in, ind ) ;
  }
  else {
    products = get_list_of_particles_from_decay( imother, in, ind ) ;
  }

  std::vector<int> found;
  for (auto & pdg_d: m_pdg_daughters ) {
    for (auto & idx_d: products) {
      if ( (m_chargeConjugateDaughters && abs(in[idx_d].PDG) == abs(pdg_d)) || in[idx_d].PDG == pdg_d) {
	// careful, there can be several particles with the same PDG !
	if (std::find(found.begin(), found.end(), idx_d) == found.end())  {  // idx_d has NOT already been "used"
	  found.push_back( idx_d );
          break;
	}
      }
    }
  }
  if ( (m_inclusiveDecay && found.size() >= m_pdg_daughters.size()  && products.size() >= m_pdg_daughters.size()) || //for inclusive decay: at least this list of daughters
       (!m_inclusiveDecay && found.size() == m_pdg_daughters.size()  && products.size() == m_pdg_daughters.size()) ) //for exclusive decay: exactly this list of daughters
    { // all daughters have been found. That's the decay mode looked for.
      result.push_back( imother );
      for ( auto & idx_d: found) {   // use "found" and not "products", to get the right ordering
	result.push_back( idx_d );
      }
    }

  return result;

}

ROOT::VecOps::RVec<int>  get_indices_ExclusiveDecay_MotherByIndex( int imother,
								     std::vector<int> m_pdg_daughters,
								     bool m_stableDaughters,
                     ROOT::VecOps::RVec<edm4hep::MCParticleData> in ,
								     ROOT::VecOps::RVec<int> ind) {
  return get_indices_MotherByIndex(
     imother,
	   m_pdg_daughters,
	   m_stableDaughters,
     false /* m_chargeConjuigateDaughters */,
	   false /* m_inclusiveDecay */,
	   in,
	   ind);
}
// ----------------------------------------------------------------------------------------------------------------------------------

MCParticle::get_indices::get_indices( int pdg_mother, std::vector<int> pdg_daughters, bool stableDaughters, bool chargeConjugateMother, bool chargeConjugateDaughters, bool inclusiveDecay) {
  m_pdg_mother = pdg_mother;
  m_pdg_daughters = pdg_daughters;
  m_stableDaughters = stableDaughters;
  m_chargeConjugateMother = chargeConjugateMother;
  m_chargeConjugateDaughters = chargeConjugateDaughters;
  m_inclusiveDecay = inclusiveDecay;
}

ROOT::VecOps::RVec<int> MCParticle::get_indices::operator() ( ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

   // Look for a specific decay specified by the mother PDG_id and
   // the PDG_ids of the daughters
   // Returns a vector with the indices, in the Particle block, of the mother and of
   // the daughters - in the order defined by std::vector<int> pdg_daughters.
   //
   // In case there are several such decays in the event, keep only the first one.

   ROOT::VecOps::RVec<int>  result;

   for ( int imother =0; imother < in.size(); imother ++){
     int pdg = in[imother].PDG ;
     bool found_a_mother = false;
     if ( ! m_chargeConjugateMother ) found_a_mother = ( pdg == m_pdg_mother );
     if ( m_chargeConjugateMother )   found_a_mother = ( abs(pdg) == abs(m_pdg_mother) ) ;
     if ( ! found_a_mother ) continue;

     ROOT::VecOps::RVec<int> a = get_indices_MotherByIndex( imother, m_pdg_daughters, m_stableDaughters, m_chargeConjugateDaughters, m_inclusiveDecay, in, ind );
     if ( a.size() != 0 ) {
        result = a;
        break;    // return the first decay found
     }

   }
   return result;
}

MCParticle::get_indices_ExclusiveDecay::get_indices_ExclusiveDecay( int pdg_mother, std::vector<int> pdg_daughters, bool stableDaughters, bool chargeConjugate) : get_indices(pdg_mother, pdg_daughters, stableDaughters, chargeConjugate, chargeConjugate, false)  {
};


// --------------------------------------------------------------------------------------------------


// get dR between two objects:
ROOT::VecOps::RVec<float> get_angularDist_MC(
  ROOT::VecOps::RVec<edm4hep::MCParticleData> particle_1,
  ROOT::VecOps::RVec<edm4hep::MCParticleData> particle_2,
  TString type) {

  ROOT::VecOps::RVec<float> out_vector;

  // if one of the input particles is empty, fill default value
  if (particle_1.size() < 1 || particle_2.size() < 1) {
    out_vector.push_back(-999.);
    return out_vector;
  }

  // else, for now, just take the first of each, should be the "best" one (by
  // user input) - flexibility to use all combinations is there, to be
  // implemented if needed
  TLorentzVector tlv_1;
  tlv_1.SetXYZM(particle_1.at(0).momentum.x, particle_1.at(0).momentum.y, 
                particle_1.at(0).momentum.z, particle_1.at(0).mass);
  TLorentzVector tlv_2;
  tlv_2.SetXYZM(particle_2.at(0).momentum.x, particle_2.at(0).momentum.y, 
                particle_2.at(0).momentum.z, particle_2.at(0).mass);

  if (type.Contains("dR")) {
    out_vector.push_back(tlv_1.DeltaR(tlv_2));
  }

  else if (type.Contains("dEta")) {
    out_vector.push_back(abs(tlv_1.Eta() - tlv_2.Eta()));
  }

  else if (type.Contains("dPhi")) {
    out_vector.push_back(tlv_1.DeltaPhi(tlv_2));
  }

  else {
    std::cout
        << " Error in AnalysisFCChh::get_angularDist_MC - requested unknown type "
        << type << "Returning default of -999." << std::endl;
    out_vector.push_back(-999.);
  }

  return out_vector;
}
ROOT::VecOps::RVec<float> AngleBetweenTwoMCParticles( ROOT::VecOps::RVec<edm4hep::MCParticleData> p1, ROOT::VecOps::RVec<edm4hep::MCParticleData> p2 ) {

  ROOT::VecOps::RVec<float> result;
  if ( p1.size() != p2.size() ) {
        //std::cout << "  !!! in AngleBetweenTwoMCParticles: the arguments p1 and p2 should have the same size " << std::endl;
        return result;
  }

  for (int i = 0; i < p1.size(); i++) {
     TLorentzVector tlv1;
     tlv1.SetXYZM(p1[i].momentum.x, p1[i].momentum.y, p1[i].momentum.z, p1[i].mass);
     TLorentzVector tlv2;
     tlv2.SetXYZM(p2[i].momentum.x, p2[i].momentum.y, p2[i].momentum.z, p2[i].mass);
     float dR = tlv1.DeltaR(tlv2);
     result.push_back(dR);
  }

  return result;
}

int get_lepton_origin(const edm4hep::MCParticleData &p,
                      const ROOT::VecOps::RVec<edm4hep::MCParticleData> &in,
                      const ROOT::VecOps::RVec<int> &ind){

 // std::cout  << std::endl << " enter in MCParticle::get_lepton_origin  PDG = " << p.PDG << std::endl;

 int pdg = std::abs( p.PDG ) ;
 if ( pdg != 11 && pdg != 13 && pdg  != 15 ) return -1;

 int result  = 0;

 // std::cout << " p.parents_begin p.parents_end " << p.parents_begin <<  " "  << p.parents_end << std::endl;
    for (unsigned j = p.parents_begin; j != p.parents_end; ++j) {
      int index = ind.at(j);
      int pdg_parent = in.at(index).PDG ;
      // std::cout  << " parent has pdg = " << in.at(index).PDG <<  "  status = " << in.at(index).generatorStatus << std::endl;

      if ( abs( pdg_parent ) == 23 || abs( pdg_parent ) == 24 ) {
        result = pdg_parent ;
        //std::cout <<  " ... Lepton is from W or Z ,  return code = " << result <<  std::endl;
        break;
      }

      if ( abs( pdg_parent ) == 22 ) {
        result = pdg_parent ;
        //std::cout <<  " ... Lepton is from a virtual photon ,  return code = " << result <<  std::endl;
        break;
      }

      if ( abs( pdg_parent ) == 15 ) {
         result = pdg_parent ;
         //std::cout <<  " ... Lepton is from a tau,  return code = " << result <<  std::endl;
         break;
      }

      if ( abs( pdg_parent ) == 11 ) {    // beam particle ?
			// beam particles should have generatorStatus = 4,
			// but that is not the case in files produced from Whizard + p6
        if ( in.at(index).generatorStatus == 4 || ind.at  ( in.at(index).parents_begin ) == 0 ) {
           result = 0;
           //std::cout <<  " ... Lepton is from the hard subprocess, return code = " << result <<  std::endl;
           break;
        }
      }

      if ( pdg == 11 && abs( pdg_parent ) == 13 ) {	// mu -> e
          result  = pdg_parent;
          //std::cout <<  " ... Electron from a muon decay, return code = " << result <<  std::endl;
          break;
      }

      if ( abs( pdg_parent ) == pdg  ) {
	//std::cout << " ... iterate ... " << std::endl;
	return get_lepton_origin( in.at(index),  in, ind  );
      }
      // This must come from a hadron decay
      result = pdg_parent;
      //std::cout <<  " ... Lepton from a hadron decay " << std::endl;
    }
 return result;
}
//return the PDG of the parent of a given list of MC particles
ROOT::VecOps::RVec<int> get_parent_pdg(
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles, 
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in, 
    const ROOT::VecOps::RVec<int>& ind) 
{
    ROOT::VecOps::RVec<int> result;
    result.reserve(particles.size());
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& particle = particles[i];
        int parent_pdg = -999; // Default value if no parent is found
        int current_index = -1;
        
       // std::cout << "Particle " << i << " PDG: " << particle.PDG << " - Parent chain:" << std::endl;
        
        // Start with the first parent
        for (unsigned j = particle.parents_begin; j != particle.parents_end; ++j) {
            current_index = ind.at(j);
            if (current_index >= 0 && current_index < in.size()) {
                parent_pdg = in.at(current_index).PDG;
               // std::cout << "  Parent at index " << current_index << " PDG: " << parent_pdg << std::endl;
                
                // Check if parent PDG is 21 (gluon) and print decay products if applicable
                if (abs(parent_pdg) == 21) {
                   // std::cout << "  Gluon (PDG=21) detected as parent. Decay products of this gluon:" << std::endl;
                    const auto& gluon = in.at(current_index);
                    for (unsigned k = gluon.daughters_begin; k != gluon.daughters_end; ++k) {
                        int daughter_index = ind.at(k);
                        if (daughter_index >= 0 && daughter_index < in.size()) {
                            int daughter_pdg = in.at(daughter_index).PDG;
                           // std::cout << "    Daughter at index " << daughter_index << " PDG: " << daughter_pdg << std::endl;
                        } else {
                          //  std::cout << "    Invalid daughter index: " << daughter_index << std::endl;
                        }
                    }
                }
                
                break; // Take the first parent by default
            } else {
               // std::cout << "  Invalid parent index: " << current_index << std::endl;
            }
        }
        // Check if there is more than one parent and print all parents if so
        if (particle.parents_end - particle.parents_begin > 1) {
            //std::cout << "  Multiple parents found for particle PDG " << particle.PDG << ":" << std::endl;
            for (unsigned j = particle.parents_begin; j != particle.parents_end; ++j) {
                int parent_index = ind.at(j);
                if (parent_index >= 0 && parent_index < in.size()) {
                    //std::cout << "    Parent at index " << parent_index << " PDG: " << in.at(parent_index).PDG << std::endl;
                } else {
                   // std::cout << "    Invalid parent index: " << parent_index << std::endl;
                }
            }
        }
        // If parent PDG is the same as particle PDG, go back one generation
        while (current_index >= 0 && current_index < in.size() && 
               parent_pdg != -999 && abs(parent_pdg) == abs(particle.PDG)) {
            const auto& current_parent = in.at(current_index);
            parent_pdg = -999; // Reset in case no further parent is found
            for (unsigned j = current_parent.parents_begin; j != current_parent.parents_end; ++j) {
                current_index = ind.at(j);
                if (current_index >= 0 && current_index < in.size()) {
                    parent_pdg = in.at(current_index).PDG;
                    // std::cout << "  Parent at index " << current_index << " PDG: " << parent_pdg << std::endl;
                    break; // Take the first parent of this generation
                } else {
                  // std::cout << "  Invalid parent index in chain: " << current_index << std::endl;
                }
            }
        }
        
        result.push_back(parent_pdg);
        //std::cout << "Final parent PDG for particle " << i << ": " << parent_pdg << std::endl;
    }
    return result;
}
// Function implemented to debug photon origin, traces back until a non photon,
// non-gluon parent is found
ROOT::VecOps::RVec<int> get_parent_pdg_photon(
  const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles, 
  const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in, 
  const ROOT::VecOps::RVec<int>& ind) 
{
  ROOT::VecOps::RVec<int> result;
  result.reserve(particles.size());
  for (size_t i = 0; i < particles.size(); ++i) {
      if (particles[i].PDG != 22) { // Ensure we process only photons
          result.push_back(-999);
          continue;
      }
      const auto& particle = particles[i];
      int parent_pdg = -999;
      int current_index = -1;
      
      // Start with the first parent
      for (unsigned j = particle.parents_begin; j != particle.parents_end; ++j) {
          current_index = ind.at(j);
          if (current_index >= 0 && current_index < in.size()) {
              parent_pdg = in.at(current_index).PDG;
              break;
          }
      }
      
      // Trace back until a non-photon, non-gluon parent is found
      while (current_index >= 0 && current_index < in.size() && parent_pdg != -999) {
          if (abs(parent_pdg) != 22 && abs(parent_pdg) != 21) { // Stop at non-photon, non-gluon
              break;
          }
          const auto& current_parent = in.at(current_index);
          parent_pdg = -999;
          for (unsigned j = current_parent.parents_begin; j != current_parent.parents_end; ++j) {
              current_index = ind.at(j);
              if (current_index >= 0 && current_index < in.size()) {
                  parent_pdg = in.at(current_index).PDG;
                  break;
              }
          }
      }
      
      result.push_back(parent_pdg);
  }
  return result;
}
// Function to return the PDG IDs of all direct daughters of a particle collection
ROOT::VecOps::RVec<int> get_direct_daughters(
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles, 
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in, 
    const ROOT::VecOps::RVec<int>& ind) 
{
    ROOT::VecOps::RVec<int> result;
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& particle = particles[i];
        // Iterate through the daughter indices of the current particle
        for (unsigned j = particle.daughters_begin; j != particle.daughters_end; ++j) {
            int daughter_index = ind.at(j);
            if (daughter_index >= 0 && daughter_index < in.size()) {
                result.push_back(in.at(daughter_index).PDG);
            }
        }
    }
    return result;
}

// Select particles from a collection based on the PDG ID of their parent
ROOT::VecOps::RVec<edm4hep::MCParticleData> sel_parent_pdg(
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles, 
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in, 
    const ROOT::VecOps::RVec<int>& ind, 
    int parent_pdg) 
{
    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& particle = particles[i];
        // Check if the particle has parents
        for (unsigned j = particle.parents_begin; j != particle.parents_end; ++j) {
            int parent_index = ind.at(j);
            if (parent_index >= 0 && parent_index < in.size()) {
                int pdg_parent = in.at(parent_index).PDG;
                if (abs(pdg_parent) == abs(parent_pdg)) {
                    result.push_back(particle);
                    break; // If we found a matching parent, no need to check further parents
                }
            }
        }
    }
    return result;
}

//Select leptons from a given parent pdg, returns the new collection of leptons
ROOT::VecOps::RVec<edm4hep::MCParticleData> sel_origin_lep(
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles, 
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in, 
    const ROOT::VecOps::RVec<int>& ind, 
    int parent_pdg) 
{
    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& particle = particles[i];
        int origin = get_lepton_origin(particle, in, ind);
        if (abs(origin) == abs(parent_pdg)) {
            result.push_back(particle);
        }
    }
    return result;
}



ROOT::VecOps::RVec<int> get_leptons_origin(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &particles,
                                           const ROOT::VecOps::RVec<edm4hep::MCParticleData> &in,
                                           const ROOT::VecOps::RVec<int> &ind)  {

  ROOT::VecOps::RVec<int> result;
  result.reserve(particles.size());
  for (size_t i = 0; i < particles.size(); ++i) {
    auto & p = particles[i];
    int origin = MCParticle::get_lepton_origin( p, in, ind );
    result.push_back( origin );
  }
  return result;
}


float scalarHT(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  float result = 0;
  float result_nomu = 0;
  float result_mu = 0;
  TLorentzVector tlv_tot;
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];

    // print particle characteristics, momenta and mothers and dauters, and status

    if (p.generatorStatus != 1 )
      continue;

    // std::cout << "i= " << i << "  PDGID "<< p.PDG  <<  "  status  " << p.generatorStatus << " momentum " << p.momentum.x << " " << p.momentum.y << " " << p.momentum.z << " " << p.mass << std::endl;
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result += tlv.Pt();
  }

  return result;
}
int get_lepton_origin(const edm4hep::MCParticleData &p,
  const ROOT::VecOps::RVec<edm4hep::MCParticleData> &in,
  const ROOT::VecOps::RVec<podio::ObjectID> &parent_ids){

// std::cout  << std::endl << " enter in MCParticle::get_lepton_origin  PDG = " << p.PDG << std::endl;

int pdg = std::abs( p.PDG ) ;
if ( pdg != 11 && pdg != 13 && pdg  != 15 ) return -1;

int result  = 0;

// std::cout << " p.parents_begin p.parents_end " << p.parents_begin <<  " "  << p.parents_end << std::endl;
for (unsigned j = p.parents_begin; j != p.parents_end; ++j) {
// retrieve the parent MC particle, by jumping through the index collections 
int index = parent_ids.at(j).index;
int pdg_parent = in.at(index).PDG;
//   int index = ind.at(j);
//   int pdg_parent = in.at(index).PDG ;
// std::cout  << " parent has pdg = " << in.at(index).PDG <<  "  status = " << in.at(index).generatorStatus << std::endl;

if ( abs( pdg_parent ) == 23 || abs( pdg_parent ) == 24 ) {
result = pdg_parent ;
//std::cout <<  " ... Lepton is from W or Z ,  return code = " << result <<  std::endl;
break;
}

if ( abs( pdg_parent ) == 22 ) {
result = pdg_parent ;
//std::cout <<  " ... Lepton is from a virtual photon ,  return code = " << result <<  std::endl;
break;
}

if ( abs( pdg_parent ) == 15 ) {
result = pdg_parent ;
//std::cout <<  " ... Lepton is from a tau,  return code = " << result <<  std::endl;
break;
}

// if ( abs( pdg_parent ) == 11 ) {    // beam particle ?
// // beam particles should have generatorStatus = 4,
// // but that is not the case in files produced from Whizard + p6
// if ( in.at(index).generatorStatus == 4 || parent_ids.at  ( in.at(index).parents_begin ) == 0 ) {
// result = 0;
// //std::cout <<  " ... Lepton is from the hard subprocess, return code = " << result <<  std::endl;
// break;
// }
// }

if ( pdg == 11 && abs( pdg_parent ) == 13 ) {    // mu -> e
result  = pdg_parent;
//std::cout <<  " ... Electron from a muon decay, return code = " << result <<  std::endl;
break;
}

if ( abs( pdg_parent ) == pdg  ) {
//std::cout << " ... iterate ... " << std::endl;
return get_lepton_origin( in.at(index),  in, parent_ids  );
}
// This must come from a hadron decay
result = pdg_parent;
//std::cout <<  " ... Lepton from a hadron decay " << std::endl;
}
return result;
}

ROOT::VecOps::RVec<int> get_leptons_origin(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &particles,
  const ROOT::VecOps::RVec<edm4hep::MCParticleData> &in,
  const ROOT::VecOps::RVec<podio::ObjectID> &parent_ids)  {

ROOT::VecOps::RVec<int> result;
result.reserve(particles.size());
for (size_t i = 0; i < particles.size(); ++i) {
auto & p = particles[i];
int origin = MCParticle::get_lepton_origin( p, in, parent_ids );
result.push_back( origin );
}
return result;
}
// Function to check for photon splitting events where a muon radiates a photon that splits into two electrons
int countMuonPhotonSplitting(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles,
                        const ROOT::VecOps::RVec<podio::ObjectID>& daughter_ids) {
    int splittingCount = 0;
    
    // Loop through all particles to find muons
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& particle = particles[i];
        if (abs(particle.PDG) == 13) { // Check if particle is a muon
            // Get daughters of the muon
            bool hasPhotonDaughter = false;
            for (size_t d = particle.daughters_begin; d < particle.daughters_end; ++d) {
                
                    auto daughter = particles[daughter_ids[d].index];
                    if (daughter.PDG == 22) { // Check if daughter is a photon
                        hasPhotonDaughter = true;
                        // Check daughters of the photon
                        bool hasElectronPair = false;
                        int electronCount = 0;
                        for (size_t gd = daughter.daughters_begin; gd < daughter.daughters_end; ++gd) {
                            if (gd < particles.size()) {
                                auto grandDaughter = particles[daughter_ids[gd].index];
                                if (abs(grandDaughter.PDG) == 11) { // Check for electrons/positrons
                                    electronCount++;
                                }
                            }
                        }
                        if (electronCount == 2) { // Two electrons/positrons from photon
                            hasElectronPair = true;
                        }
                        if (hasElectronPair) {
                            splittingCount++;
                            break; // Found a splitting event for this muon, move to next muon
                        }
                    
                }
            }
        }
    }
    return splittingCount;
}

int countElectronPhotonSplitting(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles,
    const ROOT::VecOps::RVec<podio::ObjectID>& daughter_ids) {
    int splittingCount = 0;

    // Loop through all particles to find electrons
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& particle = particles[i];
        if (abs(particle.PDG) == 11) { // Check if particle is an electron
         // Get daughters of the electron
           bool hasPhotonDaughter = false;
            for (size_t d = particle.daughters_begin; d < particle.daughters_end; ++d) {

                auto daughter = particles[daughter_ids[d].index];
                if (daughter.PDG == 22) { // Check if daughter is a photon
                  hasPhotonDaughter = true;
                 // Check daughters of the photon
                  bool hasElectronPair = false;
                  int electronCount = 0;
                  for (size_t gd = daughter.daughters_begin; gd < daughter.daughters_end; ++gd) {
                    if (gd < particles.size()) {
                        auto grandDaughter = particles[daughter_ids[gd].index];
                        if (abs(grandDaughter.PDG) == 11) { // Check for electrons/positrons
                            electronCount++;
                        }
                    }
                    }
                  if (electronCount == 2) { // Two electrons/positrons from photon
                      hasElectronPair = true;
                    }
                  if (hasElectronPair) {
                      splittingCount++;
                      break; // Found a splitting event for this electron, move to next electron
                    }
                }
            }
        }
    }
      return splittingCount;
}

// New function to trace photon splitting from muons, inspired by traceToFinalState
int tracePhotonSplitting(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles,
                        const ROOT::VecOps::RVec<podio::ObjectID>& daughter_ids) {
    int splittingCount = 0;
    
    // Loop through all particles to find muons
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& particle = particles[i];
        if (abs(particle.PDG) == 13) { // Check if particle is a muon
            // Trace daughters of the muon
            for (size_t d = particle.daughters_begin; d < particle.daughters_end; ++d) {
                if (d < daughter_ids.size() && d < particles.size()) {
                    auto daughter = particles[daughter_ids[d].index];
                    if (daughter.PDG == 22) { // Check if daughter is a photon
                        // Trace daughters of the photon
                        int electronCount = 0;
                        for (size_t gd = daughter.daughters_begin; gd < daughter.daughters_end; ++gd) {
                            if (gd < daughter_ids.size() && gd < particles.size()) {
                                auto grandDaughter = particles[daughter_ids[gd].index];
                                if (abs(grandDaughter.PDG) == 11) { // Check for electrons/positrons
                                    electronCount++;
                                }
                            }
                        }
                        if (electronCount == 2) { // Exactly two electrons/positrons from photon
                            splittingCount++;
                            break; // Found a splitting event for this muon, move to next muon
                        }
                    }
                }
            }
        }
    }
    return splittingCount;
}
// Function to return leptons originating from Z and W separately
std::pair<std::vector<edm4hep::MCParticleData>, std::vector<edm4hep::MCParticleData>> getPromptLeptons(
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& mcparticles, 
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& leptons,
    const ROOT::VecOps::RVec<int>& ind) 
{
    std::vector<edm4hep::MCParticleData> fromZ; // Leptons from Z (PDG 23)
    std::vector<edm4hep::MCParticleData> fromW; // Leptons from W (PDG 24, -24)
    for (size_t i = 0; i < leptons.size(); ++i) {
        const auto& lepton = leptons[i];
        int originPDG = get_lepton_origin(lepton, mcparticles, ind);
        if (originPDG == 23) {
            fromZ.push_back(lepton);
        } else if (originPDG == 24 || originPDG == -24) {
            fromW.push_back(lepton);
        }
    }
    return std::make_pair(fromZ, fromW);
}
// Function to return leptons originating from W
ROOT::VecOps::RVec<edm4hep::MCParticleData> getWLeptons(
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& mcparticles, 
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& leptons,
    const ROOT::VecOps::RVec<int>& ind) 
{
    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    for (size_t i = 0; i < leptons.size(); ++i) {
        const auto& lepton = leptons[i];
        int originPDG = get_lepton_origin(lepton, mcparticles, ind);
        if (abs(originPDG) == 24) { // W boson PDG ID is 24 or -24
            result.push_back(lepton);
        }
    }
    return result;
}
//substract y from x
ROOT::VecOps::RVec<edm4hep::MCParticleData> remove(
  ROOT::VecOps::RVec<edm4hep::MCParticleData> x,
  ROOT::VecOps::RVec<edm4hep::MCParticleData> y) {
//to be kept as ROOT::VecOps::RVec
std::vector<edm4hep::MCParticleData> result;
result.reserve( x.size() );
result.insert( result.end(), x.begin(), x.end() );
float epsilon = 1e-8;
for (size_t i = 0; i < y.size(); ++i) {
float mass1 = y.at(i).mass;
float px1 = y.at(i).momentum.x;
float py1 = y.at(i).momentum.y;
float pz1 = y.at(i).momentum.z;
for(std::vector<edm4hep::MCParticleData>::iterator
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
// Function to return leptons NOT originating from Z or W
std::vector<edm4hep::MCParticleData> getNonPromptLeptons(
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& mcparticles, 
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& leptons,
    const ROOT::VecOps::RVec<int>& ind) 
{
    std::vector<edm4hep::MCParticleData> notFromZorW;
    for (size_t i = 0; i < leptons.size(); ++i) {
        const auto& lepton = leptons[i];
        int originPDG = get_lepton_origin(lepton, mcparticles, ind);
        if (originPDG != 23 && originPDG != 24 && originPDG != -24) {
            notFromZorW.push_back(lepton);
        }
    }
    return notFromZorW;
}

// Function to find and return the closest particle in dR
edm4hep::MCParticleData getClosestParticle(
    const edm4hep::MCParticleData& particle,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& finalStateParticles) {
    float minDR = std::numeric_limits<float>::max();
    const edm4hep::MCParticleData* closestParticle = nullptr;
    TLorentzVector tlvParticle;
    tlvParticle.SetXYZM(particle.momentum.x, particle.momentum.y, particle.momentum.z, particle.mass);

    for (const auto& fsParticle : finalStateParticles) {
        TLorentzVector tlvFS;
        tlvFS.SetXYZM(fsParticle.momentum.x, fsParticle.momentum.y, fsParticle.momentum.z, fsParticle.mass);
        float dR = tlvParticle.DeltaR(tlvFS);
        if (dR < minDR && dR > 0) { // dR > 0 to avoid comparing particle with itself if it's in the collection
            minDR = dR;
            closestParticle = &fsParticle;
        }
    }

    if (closestParticle) {
        return *closestParticle;
    } else {
        // If no other particle is found, return a default-constructed MCParticleData
        return edm4hep::MCParticleData();
    }
}



// Function to calculate the dR distance to the closest particle
float getClosestParticleDR(
  const edm4hep::MCParticleData& particle,
  const ROOT::VecOps::RVec<edm4hep::MCParticleData>& finalStateParticles) {
  float minDR = std::numeric_limits<float>::max();
  TLorentzVector tlvParticle;
  tlvParticle.SetXYZM(particle.momentum.x, particle.momentum.y, particle.momentum.z, particle.mass);
  
  for (const auto& fsParticle : finalStateParticles) {
      TLorentzVector tlvFS;
      tlvFS.SetXYZM(fsParticle.momentum.x, fsParticle.momentum.y, fsParticle.momentum.z, fsParticle.mass);
      float dR = tlvParticle.DeltaR(tlvFS);
      if (dR < minDR && dR > 0) { // dR > 0 to avoid comparing particle with itself if it's in the collection
          minDR = dR;
      }
  }
  
  if (minDR == std::numeric_limits<float>::max()) {
      //std::cout << "Debug: No other particles found to calculate dR for particle with PDG " << particle.PDG << std::endl;
      return -1.0; // Return -1 if no other particles are found
  }
  
  //std::cout << "Debug: Closest dR for particle with PDG " << particle.PDG << " is " << minDR << std::endl;
  return minDR;
}

}//end NS MCParticle

}//end NS FCCAnalyses
