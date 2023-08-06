//
// Copyright (C) 2018 by the adcc authors
//
// This file is part of adcc.
//
// adcc is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// adcc is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with adcc. If not, see <http://www.gnu.org/licenses/>.
//

#pragma once
#include "CachingPolicy.hh"
#include "OneParticleOperator.hh"
#include "ReferenceState.hh"
#include "exceptions.hh"

namespace adcc {
/**
 *  \defgroup PerturbationTheory Objects for computing perturbation theory
 */
///@{

/** A lazy Møller-Plesset perturbation theory class.
 *  The first time a particular functionality is requested,
 *  it is computed */
struct LazyMp {
  /** Initialise a LazyMp object using a reference state.
   *  Will not compute anything unless explicitly requested */
  explicit LazyMp(std::shared_ptr<const ReferenceState> ref_ptr)
        : LazyMp(ref_ptr, std::make_shared<AlwaysCachePolicy>()) {}

  /** Initialise a LazyMp object using a reference state.
   *  Will not compute anything unless explicitly requested */
  LazyMp(std::shared_ptr<const ReferenceState> ref_ptr,
         std::shared_ptr<CachingPolicy_i> caching_policy_ptr)
        : m_ref_ptr(ref_ptr), m_cpol_ptr(caching_policy_ptr), m_timer{} {}

  /** Obtain the MP energy correction at a particular level */
  double energy_correction(int level) const;

  /** Delta Fock matrix */
  std::shared_ptr<Tensor> df(std::string space) const;

  /** T2 amplitudes */
  std::shared_ptr<Tensor> t2(std::string space) const;

  //  TODO Add more setter functions
  /** Set the t2 amplitudes tensor. This invalidates all data depending on the T2
   * amplitudes in this class.
   *
   * \note Potential other caches, such as computed ADC intermediates are *not*
   *       automatically invalidated.
   **/
  void set_t2(std::string space, std::shared_ptr<Tensor> tensor);

  /** Return the T^D_2 term */
  std::shared_ptr<Tensor> td2(std::string space) const;

  /** Return MP2 difference densities (in MOs)*/
  std::shared_ptr<Tensor> mp2_diffdm(std::string space) const {
    return mp2_diffdm_ptr()->block(space);
  }

  /** Return MP2 difference density relative to HF as a OneParticleOperator object */
  std::shared_ptr<const OneParticleOperator> mp2_diffdm_ptr() const;

  /** Return the T2 tensor with ERI tensor contraction intermediates
   *  (called pi1 to pi7 in adcman) */
  std::shared_ptr<Tensor> t2eri(const std::string& space,
                                const std::string& contraction) const;

  /** Access to the reference state on top of which the MP calculation
   * has been performed. */
  std::shared_ptr<const ReferenceState> reference_state_ptr() const { return m_ref_ptr; }

  /** Access to the caching policy used */
  std::shared_ptr<CachingPolicy_i> caching_policy_ptr() const { return m_cpol_ptr; }

  /** Set the caching policy used from now on */
  void set_caching_policy(std::shared_ptr<CachingPolicy_i> newcpol_ptr) {
    m_cpol_ptr = newcpol_ptr;
  }

  /** Return the MoSpaces to which this LazyMp is set up */
  std::shared_ptr<const MoSpaces> mospaces_ptr() const {
    return m_ref_ptr->mospaces_ptr();
  }

  /** Has this Mp container the core-valence separation applied */
  bool has_core_occupied_space() const { return m_ref_ptr->has_core_occupied_space(); }

  /** Obtain the timing info contained in this object */
  const Timer& timer() const { return m_timer; }

 private:
  /** The reference state */
  std::shared_ptr<const ReferenceState> m_ref_ptr;

  /** The Caching policy used */
  std::shared_ptr<CachingPolicy_i> m_cpol_ptr;

  /** The energy corrections indexed in the level. */
  mutable std::vector<double> m_energy_corrections;

  /** The cache for the delta-Fock matrices. Key: Space string */
  mutable std::map<std::string, std::shared_ptr<Tensor>> m_df;

  /** The cache for the T2 amplitudes. Key: Space string */
  mutable std::map<std::string, std::shared_ptr<Tensor>> m_t2;

  /** The cache for the T^D_2 terms. Key: Space string */
  mutable std::map<std::string, std::shared_ptr<Tensor>> m_td2;

  /** The OneParticleOperator object. Key: Space string */
  mutable std::shared_ptr<const OneParticleOperator> m_mp2_diffdm_ptr;

  //@{
  /** Precomputed contractions of the T2 tensor with the ERI tensor
   *  in various ways. Key: pair<Space string, Contraction string>
   */
  mutable std::map<std::pair<std::string, std::string>, std::shared_ptr<Tensor>> m_t2eri;
  //@}

  mutable Timer m_timer;
};

///@}
}  // namespace adcc
