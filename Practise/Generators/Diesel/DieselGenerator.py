from dataclasses import dataclass, field
from Practise.Generators.Diesel.DieselPowerUnit import DieselPowerUnit

@dataclass
class DieselGenerator:
    name: str
    assembly_type: str
    units: list[DieselPowerUnit] = field(default_factory=list)

    def total_fuel_cons(self):
        total_fuel_cons = sum(unit.actual_spec_fuel_cons() * \
                              unit.active_power for unit in self.units)
        return total_fuel_cons

    def auto_assembly_dg(self, total_apparent_lp):
        if self.assembly_type == "2x50":
            pass
        if self.assembly_type == "2x40+20":
            pass
