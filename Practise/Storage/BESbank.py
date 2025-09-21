from dataclasses import dataclass, field
from Practise.Storage.BES import BES


@dataclass
class BESbank:
    units: list[BES] = field(default_factory=list)
    dod: float = field(default=0.8)
    rated_voltage: float = field(default=3.2)
    efficiency: float = field(default=0.96) # li-ion, pb - 0.8

    def charge_energy(self, hourly_demand, hpp):
        hpp_power = hpp.rated_active_power
        days_in_month = hourly_demand.get_days_in_month()
        res_energy = 0
        hd_params = ["Плуто", 666]
        for month in days_in_month.keys():
            for day in range(1, days_in_month[month]+1):
                hd = hourly_demand(month, day)
                energy = sum(hpp_power - lp for lp in hd if hpp_power - lp > 0)
                if energy > res_energy:
                    res_energy = energy
                    hd_params = [month, day]
        return res_energy, hd_params

    def total_capacity(self, hourly_demand, hpp):
        res_energy, _ = self.charge_energy(hourly_demand, hpp)
        sum_capacity = res_energy / (
            self.rated_voltage * self.dod * self.efficiency
        )
        return sum_capacity

    def number_bes_parall(self, hourly_demand, hpp, bes_capacity):
        return self.total_capacity(hourly_demand, hpp) / bes_capacity

    def number_bes_series(self, bes_voltage):
        return self.rated_voltage / bes_voltage

    def number_of_bes(self, hourly_demand, hpp, bes_capacity, bes_voltage):
        return self.number_bes_parall(hourly_demand, hpp, bes_capacity) * self.number_bes_series(bes_voltage)
