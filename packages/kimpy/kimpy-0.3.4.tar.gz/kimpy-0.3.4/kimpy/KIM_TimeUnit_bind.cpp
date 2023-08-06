// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_TimeUnit.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(time_unit, module) {
  module.doc() = "Python binding to KIM_TimeUnit.hpp";

  // classes

  py::class_<TimeUnit> cl(module, "TimeUnit");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &TimeUnit::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &TimeUnit::ToString);


  // functions

  module.def("get_time_unit",
    [](int const index) {
      TimeUnit fieldName;
      int error = TIME_UNIT::GetTimeUnit(index, &fieldName);

      py::tuple re(2);
      re[0] = fieldName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(TimeUnit, error)"
  );

  module.def("get_number_of_time_units",
    []() {
      int numberOfTimeUnits;
      TIME_UNIT::GetNumberOfTimeUnits(&numberOfTimeUnits);
      return numberOfTimeUnits;
    },
    "Return numberOfTimeUnits"
  );


  // attributes

  module.attr("unused") = TIME_UNIT::unused;
  module.attr("fs") = TIME_UNIT::fs;
  module.attr("ps") = TIME_UNIT::ps;
  module.attr("ns") = TIME_UNIT::ns;
  module.attr("s") = TIME_UNIT::s;


}

