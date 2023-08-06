// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_DataType.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(data_type, module) {
  module.doc() = "Python binding to KIM_DataType.hpp";

  // classes

  py::class_<DataType> cl(module, "DataType");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &DataType::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &DataType::ToString);


  // functions

  module.def("get_data_type",
    [](int const index) {
      DataType dataType;
      int error = DATA_TYPE::GetDataType(index, &dataType);

      py::tuple re(2);
      re[0] = dataType;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(DataType, error)"
  );

  module.def("get_number_of_data_types",
    []() {
      int numberOfDataTypes;
      DATA_TYPE::GetNumberOfDataTypes(&numberOfDataTypes);
      return numberOfDataTypes;
    },
    "Return numberOfDataTypes"
  );


  // attributes

  module.attr("Integer") = DATA_TYPE::Integer;
  module.attr("Double") = DATA_TYPE::Double;


}

