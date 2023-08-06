// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_LanguageName.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(language_name, module) {
  module.doc() = "Python binding to KIM_LanguageName.hpp";

  // classes

  py::class_<LanguageName> cl(module, "LanguageName");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &LanguageName::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &LanguageName::ToString);


  // functions

  module.def("get_language_name",
    [](int const index) {
      LanguageName languageName;
      int error = LANGUAGE_NAME::GetLanguageName(index, &languageName);

      py::tuple re(2);
      re[0] = languageName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(LanguageName, error)"
  );

  module.def("get_number_of_language_names",
    []() {
      int numberOfLanguageNames;
      LANGUAGE_NAME::GetNumberOfLanguageNames(&numberOfLanguageNames);
      return numberOfLanguageNames;
    },
    "Return numberOfLanguageNames"
  );


  // attributes

  module.attr("cpp") = LANGUAGE_NAME::cpp;
  module.attr("c") = LANGUAGE_NAME::c;
  module.attr("fortran") = LANGUAGE_NAME::fortran;


}

