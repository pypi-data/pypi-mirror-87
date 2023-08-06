//
// Copyright (C) 2019 by the adcc authors
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
#include <string>

namespace adcc {
/**
 *  \addtogroup PerturbationTheory
 */
///@{

/** Policy class determining, which tensors are cached and which are not */
struct CachingPolicy_i {
  /** Should a tensor be stored i.e. cached in memory according to this
   *  policy object (true) or not (false).
   *
   *  \param tensor_label  Label of the tensor object (e.g. t2, t2eri, ...)
   *  \param tensor_space  The spaces string of the tensor to estimate memory requirement
   *                       (e.g. "o1o1v1v1" for "t2_o1o1v1v1")
   *  \param leading_order_contraction   The spaces involved in the most expensive
   *                                     contraction to compute this tensor to estimate
   *                                     computational scaling for computing the tensor.
   *                                     (e.g. "o1o1v1v1" for "t2_o1o1v1v1")
   */
  virtual bool should_cache(const std::string& tensor_label,
                            const std::string& tensor_space,
                            const std::string& leading_order_contraction) = 0;

  // TODO It would be nice to pass some estimated usage count or "importance",
  //      but I have no reliable and meaningful idea how to do this.

  virtual ~CachingPolicy_i() = default;
};

/** Policy class, which always caches everything */
class AlwaysCachePolicy : public CachingPolicy_i {
  bool should_cache(const std::string&, const std::string&, const std::string&) override {
    return true;
  }
};

///@}
}  // namespace adcc

