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
#include "AdcMatrix/AdcMatrixCoreBase.hh"
#include "AmplitudeVector.hh"

namespace adcc {
/**
 *  \defgroup AdcMatrix "Adc matrix and related structures"
 */
///@{

/** Class representing an ADC matrix
 *
 * The ADC matrix is tiled into the following regions,
 *
 * ```
 * +------------+----------------+
 * | singles-   |     singles-   |
 * | singles    |     doubles    |
 * +------------+----------------+
 * | doubles-   |     doubles-   |
 * | singles    |     doubles    |
 * +------------+----------------+
 * ```
 *
 * where for ADC(0) and ADC(1) only the singles-singles part is present.
 * Calling functions, which compute or make use of the doubles part in such
 * cases leads to a std::invalid_argument.
 *
 * In case no intermediates are provided to the object prior to
 * the first payload function call, the class will automatically generate
 * the intermediates by itself and add them to the AdcIntermediates
 * structure referenced by intermediates_ptr. Such structure will be
 * created in case it does not exist.
 */
class AdcMatrix {
 public:
  /** Construct an AdcMatrix object.
   *
   * \param method            The ADC method to use
   * \param ground_state_ptr  The MP ground state to build upon
   */
  AdcMatrix(std::string method, std::shared_ptr<const LazyMp> ground_state_ptr);

  /** Return the shape of the represented matrix */
  std::vector<size_t> shape() const { return m_core->shape(); }

  /** Return true if the referenced block exists in this matrix*/
  bool has_block(const std::string& block) const { return m_core->has_block(block); }

  /** Return the list of blocks, which exist in this matrix */
  std::vector<std::string> blocks() const { return m_core->blocks(); }

  /** Return the list of spaces involved for a particular block of the matrix */
  std::vector<std::string> block_spaces(const std::string& block) const {
    return m_core->block_spaces(block);
  }

  /** Apply a block of the ADC matrix (e.g. the singles-singles block or
   *  the singles-doubles block. The result is stored in a pre-allocated tensor.
   *
   *  \param block   Block specification, may take the values "ss", "sd", "ds", "dd".
   *                 May not take all values for all ADC variants.
   *  \param in      Input tensor, rhs of the expression
   *  \param out     Output tensor, result of the application.
   */
  void compute_apply(std::string block, const std::shared_ptr<Tensor>& in,
                     const std::shared_ptr<Tensor>& out) const {
    m_core->compute_apply(block, in, out);
  }

  /** Return the diagonal of the matrix */
  std::shared_ptr<Tensor> diagonal(std::string block) const {
    return m_core->diagonal(block);
  }

  /** Compute the matrix-vector product of the ADC matrix
   *  with an excitation amplitude. The rhs amplitude parts are provided
   *  as std::vector, containing singles, doubles, ... part and so are
   *  resulting amplitudes. The result is stored in a pre-allocated tensor.
   *
   *  \param ins    Input tensors, one per amplitude part (singles, doubles)
   *  \param outs   Output tensors as a shared pointers
   */
  void compute_matvec(const AmplitudeVector& ins, const AmplitudeVector& outs) const {
    m_core->compute_matvec(ins, outs);
  }

  /** Access to the adc method this class represents */
  std::string method() const { return m_method; }

  /** Is the core-valence separation applied in this matrix */
  bool is_core_valence_separated() const { return m_cvs; }

  /** Access to the reference state on top of which the ADC calculation
   * has been started */
  std::shared_ptr<const ReferenceState> reference_state_ptr() const {
    return m_core->reference_state_ptr();
  }

  /** Obtain the pointer to the MP ground state upon which this ADC matrix is based. */
  std::shared_ptr<const LazyMp> ground_state_ptr() const {
    return m_core->ground_state_ptr();
  }

  /** Return the MoSpaces to which this LazyMp is set up */
  std::shared_ptr<const MoSpaces> mospaces_ptr() const {
    return reference_state_ptr()->mospaces_ptr();
  }

  /** Get the pointer to the AdcIntermediates cache for the precomputed intermediates */
  std::shared_ptr<AdcIntermediates> get_intermediates_ptr() const {
    return m_core->get_intermediates_ptr();
  }

  /** Replace the currently held AdcIntermediates cache object by the supplied one.
   *  This allows to reuse intermediates from a previous calculation. */
  void set_intermediates_ptr(std::shared_ptr<AdcIntermediates> im_ptr) {
    m_core->set_intermediates_ptr(im_ptr);
  }

  /** Obtain the timing info contained in this object */
  const Timer& timer() const { return m_core->timer(); }

 protected:
  /** The pointer to the core object, which really does the work. */
  std::shared_ptr<AdcMatrixCoreBase> m_core;

  /** The selected ADC method */
  std::string m_method;

  /** Flag to save whether this method has the CVS approximation */
  bool m_cvs;
};
///@}

}  // namespace adcc
