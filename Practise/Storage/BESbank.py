from dataclasses import dataclass, field
from Practise.Storage.BES import BES


@dataclass
class BESbank:
    units: list[BES] = field(default_factory=list)

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
                    hd_params[0] = month
                    hd_params[1] = day
        return res_energy, hd_params

    def total_capatice(self):
        pass