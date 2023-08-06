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
#include "LazyMp.hh"
#include "Tensor.hh"

namespace adcc {
/**
 *  \addtogroup AdcMatrix
 */
///@{
/** Class managing intermediate expressions of the ADC matrix,
 *  which are used frequently and/or expensive to compute.
 */
class AdcIntermediates {
 public:
  AdcIntermediates(std::shared_ptr<const LazyMp> ground_state_ptr)
        : m_ground_state_ptr(ground_state_ptr),
          m_cpol_ptr(ground_state_ptr->caching_policy_ptr()),
          m_timer{} {}

  /** Access to the ground state on top of which the ADC intermediates
   * have been computed */
  std::shared_ptr<const LazyMp> ground_state_ptr() const { return m_ground_state_ptr; }

  //
  // Intermediates
  //
  /** The ADC(2) i1 intermediate */
  std::shared_ptr<Tensor> adc2_i1_ptr;

  /** The ADC(2) i2 intermediate */
  std::shared_ptr<Tensor> adc2_i2_ptr;

  /** The ADC(3) N^6 intermediate A */
  std::shared_ptr<Tensor> adc3_pia_ptr;

  /** The ADC(3) N^6 intermediate B */
  std::shared_ptr<Tensor> adc3_pib_ptr;

  /** The ADC(3) m11 intermediate (== singles block of ADC(3) matrix */
  std::shared_ptr<Tensor> adc3_m11_ptr;

  /** The CVS-ADC(2) cv_p_oo intermediate for properties */
  std::shared_ptr<Tensor> cv_p_oo_ptr;

  /** The CVS-ADC(2) cv_p_ov intermediate for properties */
  std::shared_ptr<Tensor> cv_p_ov_ptr;

  /** The CVS-ADC(2) cv_p_vv intermediate for properties */
  std::shared_ptr<Tensor> cv_p_vv_ptr;

  /** The CVS-ADC(3) m11 intermediate (== singles block of CVS-ADC(3) matrix */
  std::shared_ptr<Tensor> cvs_adc3_m11_ptr;

  //
  // Cache functions
  //
  //@{
  /** \name Cache functions
   *
   * These functions compute the intermediates (if not already done)
   * and cache them inside the class if the CachingPolicy says so.
   * In this case another call to these functions will just return the
   * pointers to the appropriate object without extra computation.
   * In other words setting the pointers in this class to a nullptr
   * will always trigger another computation.
   */

  ///@copydoc adc2_i1_ptr
  std::shared_ptr<Tensor> compute_adc2_i1();
  ///@copydoc adc2_i2_ptr
  std::shared_ptr<Tensor> compute_adc2_i2();
  ///@copydoc adc3_pia_ptr
  std::shared_ptr<Tensor> compute_adc3_pia();
  ///@copydoc adc3_pib_ptr
  std::shared_ptr<Tensor> compute_adc3_pib();
  ///@copydoc adc3_m11_ptr
  std::shared_ptr<Tensor> compute_adc3_m11();
  ///@copydoc cv_p_oo_ptr
  std::shared_ptr<Tensor> compute_cv_p_oo();
  ///@copydoc cv_p_ov_ptr
  std::shared_ptr<Tensor> compute_cv_p_ov();
  ///@copydoc cv_p_vv_ptr
  std::shared_ptr<Tensor> compute_cv_p_vv();
  ///@copydoc cvs_adc3_m11_ptr
  std::shared_ptr<Tensor> compute_cvs_adc3_m11();
  //@}

  /** Obtain the timing info contained in this object */
  const Timer& timer() const { return m_timer; }

 private:
  std::shared_ptr<const LazyMp> m_ground_state_ptr;
  std::shared_ptr<CachingPolicy_i> m_cpol_ptr;
  mutable Timer m_timer;
};

/** Write a descriptive string for the AdcIntermediates object to the output stream.*/
std::ostream& operator<<(std::ostream& o, const AdcIntermediates& im);
///@}

}  // namespace adcc
