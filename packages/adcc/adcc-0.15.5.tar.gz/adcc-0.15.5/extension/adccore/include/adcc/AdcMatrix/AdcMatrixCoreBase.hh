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
#include <adcc/AdcIntermediates.hh>
#include <adcc/AmplitudeVector.hh>
#include <adcc/LazyMp.hh>
#include <adcc/ReferenceState.hh>

namespace adcc {
/**
 *  \addtogroup AdcMatrix
 */
///@{

/** AdcMatrixCoreBase provides the interface to the actual implementations
 *  of the ADC matrix functionality */
class AdcMatrixCoreBase {
 public:
  /** Construct the AdcMatrixCoreBase object
   * \param name       Name of the ADC method
   * \param mp_ptr_    The LazyMp pointer describing the MP perturbation theory results
   */
  AdcMatrixCoreBase(std::string name, std::shared_ptr<const LazyMp> mp_ptr_)
        : m_ref_ptr(mp_ptr_->reference_state_ptr()),
          m_mp_ptr(mp_ptr_),
          m_im_ptr(std::make_shared<AdcIntermediates>(mp_ptr_)),
          m_name(name) {}

  /// @copydoc AdcMatrix::shape()
  virtual std::vector<size_t> shape() const = 0;
  /// @copydoc AdcMatrix::has_block()
  virtual bool has_block(const std::string& block) const = 0;
  /// Return true if the referenced block exists in this matrix
  bool has_block(char block) const { return has_block(std::string(1, block)); }
  /// @copydoc AdcMatrix::blocks()
  virtual std::vector<std::string> blocks() const = 0;
  /// @copydoc AdcMatrix::block_spaces()
  virtual std::vector<std::string> block_spaces(const std::string& block) const = 0;

  /** Compute the application of the singles-singles block to the vector \c in,
   *  returning the result in the vector \c out. */
  virtual void compute_apply_ss(const std::shared_ptr<Tensor>& in,
                                const std::shared_ptr<Tensor>& out) const = 0;
  /** Compute the application of the singles-doubles block to the vector \c in,
   *  returning the result in the vector \c out.
   *  \note Might not be implemented for all matrix cores. */
  virtual void compute_apply_sd(const std::shared_ptr<Tensor>& in,
                                const std::shared_ptr<Tensor>& out) const = 0;
  /** Compute the application of the doubles-singles block to the vector \c in,
   *  returning the result in the vector \c out.
   *  \note Might not be implemented for all matrix cores. */
  virtual void compute_apply_ds(const std::shared_ptr<Tensor>& in,
                                const std::shared_ptr<Tensor>& out) const = 0;
  /** Compute the application of the doubles-doubles block to the vector \c in,
   *  returning the result in the vector \c out.
   *  \note Might not be implemented for all matrix cores. */
  virtual void compute_apply_dd(const std::shared_ptr<Tensor>& in,
                                const std::shared_ptr<Tensor>& out) const = 0;
  /** Compute the application of the given block of the ADC matrix. */
  void compute_apply(std::string block, const std::shared_ptr<Tensor>& in,
                     const std::shared_ptr<Tensor>& out) const;

  /** Compute the singles diagonal of the ADC matrix and return it. */
  virtual std::shared_ptr<Tensor> diagonal_s() const = 0;
  /** Compute the doubles diagonal of the ADC matrix and return it.
   *  \note Might not be implemented for all matrix cores. */
  virtual std::shared_ptr<Tensor> diagonal_d() const = 0;
  /** Compute the block-wise diagonal of ADC matrix. */
  std::shared_ptr<Tensor> diagonal(std::string block) const;

  /** Compute the application of the ADC matrix to the amplitude vector supplied
   *  on \c ins and return the result in \c outs. */
  virtual void compute_matvec(const AmplitudeVector& ins,
                              const AmplitudeVector& outs) const;

  virtual ~AdcMatrixCoreBase() = default;

  /// @copydoc AdcMatrix::get_intermediates_ptr()
  std::shared_ptr<AdcIntermediates> get_intermediates_ptr() const { return m_im_ptr; }

  /// @copydoc AdcMatrix::set_intermediates_ptr()
  void set_intermediates_ptr(std::shared_ptr<AdcIntermediates> im_ptr);

  /// @copydoc AdcMatrix::reference_state_ptr()
  std::shared_ptr<const ReferenceState> reference_state_ptr() { return m_ref_ptr; }

  /// @copydoc AdcMatrix::ground_state_ptr()
  std::shared_ptr<const LazyMp> ground_state_ptr() { return m_mp_ptr; }

  /// @copydoc AdcMatrix::timer()
  const Timer& timer() const { return m_timer; }

 protected:
  std::shared_ptr<const ReferenceState> m_ref_ptr;     ///< SCF reference state
  std::shared_ptr<const LazyMp> m_mp_ptr;              ///< MP ground state
  mutable std::shared_ptr<AdcIntermediates> m_im_ptr;  ///< Intermediates cache
  std::string m_name;                                  ///< Name of the ADC method
  mutable Timer m_timer;                               ///< Timer to record timings in
};

///@}
}  // namespace adcc
