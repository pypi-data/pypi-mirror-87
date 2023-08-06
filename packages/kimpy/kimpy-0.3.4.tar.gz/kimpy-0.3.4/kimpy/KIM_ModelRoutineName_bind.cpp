// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_ModelRoutineName.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(model_routine_name, module) {
  module.doc() = "Python binding to KIM_ModelRoutineName.hpp";

  // classes

  py::class_<ModelRoutineName> cl(module, "ModelRoutineName");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &ModelRoutineName::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &ModelRoutineName::ToString);


  // functions

  module.def("get_model_routine_name",
    [](int const index) {
      ModelRoutineName modelRoutineName;
      int error = MODEL_ROUTINE_NAME::GetModelRoutineName(index, &modelRoutineName);

      py::tuple re(2);
      re[0] = modelRoutineName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(ModelRoutineName, error)"
  );

  module.def("get_number_of_model_routine_names",
    []() {
      int numberOfModelRoutineNames;
      MODEL_ROUTINE_NAME::GetNumberOfModelRoutineNames(&numberOfModelRoutineNames);
      return numberOfModelRoutineNames;
    },
    "Return numberOfModelRoutineNames"
  );


  // attributes

  module.attr("Create") = MODEL_ROUTINE_NAME::Create;
  module.attr("ComputeArgumentsCreate") = MODEL_ROUTINE_NAME::ComputeArgumentsCreate;
  module.attr("Compute") = MODEL_ROUTINE_NAME::Compute;
  module.attr("Extension") = MODEL_ROUTINE_NAME::Extension;
  module.attr("Refresh") = MODEL_ROUTINE_NAME::Refresh;
  module.attr("WriteParameterizedModel") = MODEL_ROUTINE_NAME::WriteParameterizedModel;
  module.attr("ComputeArgumentsDestroy") = MODEL_ROUTINE_NAME::ComputeArgumentsDestroy;
  module.attr("Destroy") = MODEL_ROUTINE_NAME::Destroy;


}

