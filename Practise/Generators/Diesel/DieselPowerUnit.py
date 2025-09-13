from dataclasses import dataclass, field


@dataclass
class DieselPowerUnit:
    name: str
    rated_active_power: float
    rated_apparent_power: float
    peak_active_power: float
    number_of_phases: int
    rated_voltage: float
    spec_fuel_cons: float
    coeff_fc: float = field(default=0.3)
    active_power: float = field(default=0)
    min_active_power: float = field(init=False)

    def __post_init__(self):
        self.min_active_power = 0.4*self.rated_active_power

    def actual_spec_fuel_cons(self):
        actual_spec_fuel_cons = self.coeff_fc * self.spec_fuel_cons + \
                                (1 - self.coeff_fc) * self.spec_fuel_cons * \
                                (self.active_power / self.rated_active_power)
        return actual_spec_fuel_cons
