// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_ChargeUnit.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(charge_unit, module) {
  module.doc() = "Python binding to KIM_ChargeUnit.hpp";

  // classes

  py::class_<ChargeUnit> cl(module, "ChargeUnit");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &ChargeUnit::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &ChargeUnit::ToString);


  // functions

  module.def("get_charge_unit",
    [](int const index) {
      ChargeUnit fieldName;
      int error = CHARGE_UNIT::GetChargeUnit(index, &fieldName);

      py::tuple re(2);
      re[0] = fieldName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(ChargeUnit, error)"
  );

  module.def("get_number_of_charge_units",
    []() {
      int numberOfChargeUnits;
      CHARGE_UNIT::GetNumberOfChargeUnits(&numberOfChargeUnits);
      return numberOfChargeUnits;
    },
    "Return numberOfChargeUnits"
  );


  // attributes

  module.attr("unused") = CHARGE_UNIT::unused;
  module.attr("C") = CHARGE_UNIT::C;
  module.attr("e") = CHARGE_UNIT::e;
  module.attr("statC") = CHARGE_UNIT::statC;


}

