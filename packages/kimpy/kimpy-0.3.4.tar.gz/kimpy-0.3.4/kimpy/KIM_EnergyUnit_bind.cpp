// This file is generated automatically by scripts
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <string>

#include "KIM_EnergyUnit.hpp"

namespace py = pybind11;
using namespace KIM;


PYBIND11_MODULE(energy_unit, module) {
  module.doc() = "Python binding to KIM_EnergyUnit.hpp";

  // classes

  py::class_<EnergyUnit> cl(module, "EnergyUnit");
  
  cl.def(py::init<>())
    .def(py::init<int const>())
    .def(py::init<std::string const>())
    .def("known", &EnergyUnit::Known)
    .def(py::self == py::self)
    .def(py::self != py::self)
    .def("__repr__", &EnergyUnit::ToString);


  // functions

  module.def("get_energy_unit",
    [](int const index) {
      EnergyUnit fieldName;
      int error = ENERGY_UNIT::GetEnergyUnit(index, &fieldName);

      py::tuple re(2);
      re[0] = fieldName;
      re[1] = error;
      return re;
    },
    py::arg("index"),
    "Return(EnergyUnit, error)"
  );

  module.def("get_number_of_energy_units",
    []() {
      int numberOfEnergyUnits;
      ENERGY_UNIT::GetNumberOfEnergyUnits(&numberOfEnergyUnits);
      return numberOfEnergyUnits;
    },
    "Return numberOfEnergyUnits"
  );


  // attributes

  module.attr("unused") = ENERGY_UNIT::unused;
  module.attr("amu_A2_per_ps2") = ENERGY_UNIT::amu_A2_per_ps2;
  module.attr("erg") = ENERGY_UNIT::erg;
  module.attr("eV") = ENERGY_UNIT::eV;
  module.attr("Hartree") = ENERGY_UNIT::Hartree;
  module.attr("J") = ENERGY_UNIT::J;
  module.attr("kcal_mol") = ENERGY_UNIT::kcal_mol;


}

