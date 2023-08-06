// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_LengthUnit.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(length_unit, module) {
  module.doc() = "Python binding to KIM_LengthUnit.hpp";

  // classes

  py::class_<LengthUnit> cl(module, "LengthUnit");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &LengthUnit::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &LengthUnit::ToString);


  // functions

  module.def("get_length_unit",
    [](int const index) {
      LengthUnit fieldName;
      int error = LENGTH_UNIT::GetLengthUnit(index, &fieldName);

      py::tuple re(2);
      re[0] = fieldName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(LengthUnit, error)"
  );

  module.def("get_number_of_length_units",
    []() {
      int numberOfLengthUnits;
      LENGTH_UNIT::GetNumberOfLengthUnits(&numberOfLengthUnits);
      return numberOfLengthUnits;
    },
    "Return numberOfLengthUnits"
  );


  // attributes

  module.attr("unused") = LENGTH_UNIT::unused;
  module.attr("A") = LENGTH_UNIT::A;
  module.attr("Bohr") = LENGTH_UNIT::Bohr;
  module.attr("cm") = LENGTH_UNIT::cm;
  module.attr("m") = LENGTH_UNIT::m;
  module.attr("nm") = LENGTH_UNIT::nm;


}

