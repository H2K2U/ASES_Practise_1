from dataclasses import dataclass, field
from Practise.Generators.Diesel.DieselPowerUnit import DieselPowerUnit
import re
import pandas as pd


@dataclass
class DieselGenerator:
    name: str
    assembly_type: str
    units: list[DieselPowerUnit] = field(default_factory=list)
    rated_apparent_power: float = field(default=0)

    def total_fuel_cons(self):
        total_fuel_cons = sum(unit.actual_spec_fuel_cons() * \
                              unit.active_power for unit in self.units)
        return total_fuel_cons

    def auto_assembly_dg(self, dpu_base, total_apparent_lp):
        m = re.fullmatch(r"(\d+)x(\d+)(?:\+(\d+))?", self.assembly_type.strip())
        if not m:
            raise ValueError(f"Неверный формат assembly_type: {self.assembly_type}")

        n = int(m.group(1))
        M = int(m.group(2))
        K = int(m.group(3) or 0)

        if n*M + K != 100:
            raise ValueError(f"Суммарный процентаж ДЭС должнен быть 100, а получен {n*M + K}")

        for dpu in dpu_base:
            if dpu.rated_apparent_power >= total_apparent_lp * M/100:
                self.units.extend(n*[dpu])
                break

        if K != 0:
            for dpu in dpu_base:
                if dpu.rated_apparent_power >= total_apparent_lp * K / 100:
                    self.units.append(dpu)
                    break

        self.rated_apparent_power = sum(u.rated_apparent_power for u in self.units)

    def show_table(self):
        # создаём список словарей для DataFrame
        rows = []
        for i, u in enumerate(self.units, start=1):
            rows.append({
                "№": i,
                "Наименование": u.name,
                "Pном, кВт": u.rated_active_power,
                "Sном, кВА": u.rated_apparent_power,
                "Pпик, кВт": u.peak_active_power,
                "Кол-во фаз, шт": u.number_of_phases,
                "U, кВ": u.rated_voltage,
                "q, л/кВт·ч": u.spec_fuel_cons
            })

        df = pd.DataFrame(rows)
        print(f"\nДЭС': {self.name}  |  Компоновка: {self.assembly_type}\n")
        print(df.to_string(index=False))  # красивый вывод без индекса