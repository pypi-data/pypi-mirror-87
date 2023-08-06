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
#include "Tensor.hh"
#include <vector>

namespace adcc {
/**
 *  \addtogroup AdcMatrix
 */
///@{

/** This class is effectively a list of Tensors, which can be thought
 *  of as blocks of the ADC amplitude vector */
class AmplitudeVector : public std::vector<std::shared_ptr<Tensor>> {
 public:
  using base_type = std::vector<std::shared_ptr<Tensor>>;
  using base_type::vector;
  using base_type::operator[];

  AmplitudeVector() : base_type{} {}

  AmplitudeVector(std::vector<std::shared_ptr<Tensor>> in) : base_type(in) {}

  std::shared_ptr<Tensor> operator[](const std::string& block) const {
    if (block == "s" && size() > 0) return this->at(0);
    if (block == "d" && size() > 1) return this->at(1);
    if (block == "t" && size() > 2) return this->at(2);
    throw std::out_of_range("Block specifier unknown: " + block);
  }

  std::shared_ptr<Tensor>& operator[](const std::string& block) {
    if (block == "s" && size() > 0) return this->at(0);
    if (block == "d" && size() > 1) return this->at(1);
    if (block == "t" && size() > 2) return this->at(2);
    throw std::out_of_range("Block specifier unknown: " + block);
  }
};

///@}
}  // namespace adcc
