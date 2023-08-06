// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_TemperatureUnit.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(temperature_unit, module) {
  module.doc() = "Python binding to KIM_TemperatureUnit.hpp";

  // classes

  py::class_<TemperatureUnit> cl(module, "TemperatureUnit");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &TemperatureUnit::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &TemperatureUnit::ToString);


  // functions

  module.def("get_temperature_unit",
    [](int const index) {
      TemperatureUnit fieldName;
      int error = TEMPERATURE_UNIT::GetTemperatureUnit(index, &fieldName);

      py::tuple re(2);
      re[0] = fieldName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(TemperatureUnit, error)"
  );

  module.def("get_number_of_temperature_units",
    []() {
      int numberOfTemperatureUnits;
      TEMPERATURE_UNIT::GetNumberOfTemperatureUnits(&numberOfTemperatureUnits);
      return numberOfTemperatureUnits;
    },
    "Return numberOfTemperatureUnits"
  );


  // attributes

  module.attr("unused") = TEMPERATURE_UNIT::unused;
  module.attr("K") = TEMPERATURE_UNIT::K;


}

