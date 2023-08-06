// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_LogVerbosity.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(log_verbosity, module) {
  module.doc() = "Python binding to KIM_LogVerbosity.hpp";

  // classes

  py::class_<LogVerbosity> cl(module, "LogVerbosity");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &LogVerbosity::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &LogVerbosity::ToString);


  // functions

  module.def("get_log_verbosity",
    [](int const index) {
      LogVerbosity logVerbosity;
      int error = LOG_VERBOSITY::GetLogVerbosity(index, &logVerbosity);

      py::tuple re(2);
      re[0] = logVerbosity;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(LogVerbosity, error)"
  );

  module.def("get_number_of_log_verbosities",
    []() {
      int numberOfLogVerbosities;
      LOG_VERBOSITY::GetNumberOfLogVerbosities(&numberOfLogVerbosities);
      return numberOfLogVerbosities;
    },
    "Return numberOfLogVerbosities"
  );


  // attributes

  module.attr("silent") = LOG_VERBOSITY::silent;
  module.attr("fatal") = LOG_VERBOSITY::fatal;
  module.attr("error") = LOG_VERBOSITY::error;
  module.attr("warning") = LOG_VERBOSITY::warning;
  module.attr("information") = LOG_VERBOSITY::information;
  module.attr("debug") = LOG_VERBOSITY::debug;


}

