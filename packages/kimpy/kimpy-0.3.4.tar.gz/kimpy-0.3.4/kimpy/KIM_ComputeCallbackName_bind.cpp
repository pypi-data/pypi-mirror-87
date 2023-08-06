// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_ComputeCallbackName.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(compute_callback_name, module) {
  module.doc() = "Python binding to KIM_ComputeCallbackName.hpp";

  // classes

  py::class_<ComputeCallbackName> cl(module, "ComputeCallbackName");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &ComputeCallbackName::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &ComputeCallbackName::ToString);


  // functions

  module.def("get_compute_callback_name",
    [](int const index) {
      ComputeCallbackName computeCallbackName;
      int error = COMPUTE_CALLBACK_NAME::GetComputeCallbackName(index, &computeCallbackName);

      py::tuple re(2);
      re[0] = computeCallbackName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(ComputeCallbackName, error)"
  );

  module.def("get_number_of_compute_callback_names",
    []() {
      int numberOfComputeCallbackNames;
      COMPUTE_CALLBACK_NAME::GetNumberOfComputeCallbackNames(&numberOfComputeCallbackNames);
      return numberOfComputeCallbackNames;
    },
    "Return numberOfComputeCallbackNames"
  );


  // attributes

  module.attr("GetNeighborList") = COMPUTE_CALLBACK_NAME::GetNeighborList;
  module.attr("ProcessDEDrTerm") = COMPUTE_CALLBACK_NAME::ProcessDEDrTerm;
  module.attr("ProcessD2EDr2Term") = COMPUTE_CALLBACK_NAME::ProcessD2EDr2Term;


}

