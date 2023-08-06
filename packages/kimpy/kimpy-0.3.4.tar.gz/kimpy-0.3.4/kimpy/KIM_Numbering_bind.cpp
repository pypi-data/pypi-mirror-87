// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_Numbering.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(numbering, module) {
  module.doc() = "Python binding to KIM_Numbering.hpp";

  // classes

  py::class_<Numbering> cl(module, "Numbering");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &Numbering::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &Numbering::ToString);


  // functions

  module.def("get_numbering",
    [](int const index) {
      Numbering numbering;
      int error = NUMBERING::GetNumbering(index, &numbering);

      py::tuple re(2);
      re[0] = numbering;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(Numbering, error)"
  );

  module.def("get_number_of_numberings",
    []() {
      int numberOfNumberings;
      NUMBERING::GetNumberOfNumberings(&numberOfNumberings);
      return numberOfNumberings;
    },
    "Return numberOfNumberings"
  );


  // attributes

  module.attr("zeroBased") = NUMBERING::zeroBased;
  module.attr("oneBased") = NUMBERING::oneBased;


}

