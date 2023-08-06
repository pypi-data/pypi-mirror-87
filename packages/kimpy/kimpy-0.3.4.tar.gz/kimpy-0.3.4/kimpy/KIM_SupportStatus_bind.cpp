// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_SupportStatus.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(support_status, module) {
  module.doc() = "Python binding to KIM_SupportStatus.hpp";

  // classes

  py::class_<SupportStatus> cl(module, "SupportStatus");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &SupportStatus::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &SupportStatus::ToString);


  // functions

  module.def("get_support_status",
    [](int const index) {
      SupportStatus supportStatus;
      int error = SUPPORT_STATUS::GetSupportStatus(index, &supportStatus);

      py::tuple re(2);
      re[0] = supportStatus;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(SupportStatus, error)"
  );

  module.def("get_number_of_support_statuses",
    []() {
      int numberOfSupportStatuses;
      SUPPORT_STATUS::GetNumberOfSupportStatuses(&numberOfSupportStatuses);
      return numberOfSupportStatuses;
    },
    "Return numberOfSupportStatuses"
  );


  // attributes

  module.attr("requiredByAPI") = SUPPORT_STATUS::requiredByAPI;
  module.attr("notSupported") = SUPPORT_STATUS::notSupported;
  module.attr("required") = SUPPORT_STATUS::required;
  module.attr("optional") = SUPPORT_STATUS::optional;


}

