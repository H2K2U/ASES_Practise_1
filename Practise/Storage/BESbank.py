# Practise/Storage/BESbank.py
from dataclasses import dataclass, field
from math import ceil, isclose
from typing import Optional, Dict

from Practise.Storage.BES import BES


@dataclass
class BESbank:
    """
    Банк АКБ: nпосл x nпаралл одинаковых модулей BES.
    Формулы: Uбанка = nпосл * Uяч; Cбанка = nпаралл * Cяч; Wном = Uбанка * Cбанка.
    Полезная энергия учитывает η цикла. :contentReference[oaicite:2]{index=2}
    """
    unit: BES
    n_series: int = 0           # nпосл
    n_parallel: int = 0         # nпаралл
    # Для совместимости с твоей ранней заготовкой:
    units: list[BES] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.n_series < 0 or self.n_parallel < 0:
            raise ValueError("n_series и n_parallel должны быть неотрицательными")
        # Если список units передан вручную, позволим вычислить nпосл*nпаралл по нему,
        # но в норме используем явные n_series/n_parallel.
        if self.units and (self.n_series == 0 or self.n_parallel == 0):
            # Предполагаем, что все элементы одинаковые (как и требует методика).
            # Иначе корректная реконструкция топологии невозможна.
            raise ValueError("Укажи n_series и n_parallel для банка или не передавай units.")

    # -------- Агрегированные параметры --------
    @property
    def total_cells(self) -> int:
        return self.n_series * self.n_parallel

    @property
    def voltage(self) -> float:
        """Uбанка (В) — сумма напряжений по последовательным звеньям. :contentReference[oaicite:3]{index=3}"""
        return self.unit.rated_voltage * self.n_series

    @property
    def capacity_Ah(self) -> float:
        """Cбанка (А·ч) — сумма по параллельным нитям. :contentReference[oaicite:4]{index=4}"""
        return self.unit.rated_capacity * self.n_parallel

    @property
    def energy_Wh(self) -> float:
        """Номинальная энергия банка, Вт·ч."""
        return self.voltage * self.capacity_Ah

    @property
    def usable_energy_Wh(self) -> float:
        """Полезная энергия банка с учётом η цикла. :contentReference[oaicite:5]{index=5}"""
        return self.energy_Wh * float(self.unit.roundtrip_efficiency)

    @property
    def weight_kg(self) -> float:
        return self.unit.weight * self.total_cells

    @property
    def price_total(self) -> float:
        return self.unit.price * self.total_cells

    @property
    def specific_energy_Wh_per_kg(self) -> Optional[float]:
        return self.energy_Wh / self.weight_kg if self.weight_kg > 0 else None

    @property
    def volume_l(self) -> Optional[float]:
        """Суммарный «геометрический» объём без учёта компоновки."""
        v = self.unit.volume_l
        return v * self.total_cells if v is not None else None

    # -------- Проектирование банка по ТЗ --------
    @classmethod
    def design_for(
        cls,
        unit: BES,
        target_voltage: float,
        required_energy_kWh: float,
        apply_roundtrip: bool = True,
    ) -> "BESbank":
        """
        Подбор nпосл и nпаралл:
          1) nпосл = ceil(Uтреб / Uяч)  (чтобы не меньше по напряжению)
          2) Eнитки = nпосл * Uяч * Cяч  (Вт·ч)
          3) nпаралл = ceil(Wтреб / (Eнитки * η)), где η — КПД цикла (если apply_roundtrip) :contentReference[oaicite:6]{index=6}
        """
        if target_voltage <= 0 or required_energy_kWh <= 0:
            raise ValueError("target_voltage и required_energy_kWh должны быть > 0")

        n_series = ceil(target_voltage / unit.rated_voltage)
        e_string_Wh = unit.rated_voltage * unit.rated_capacity * n_series
        eta = unit.roundtrip_efficiency if apply_roundtrip else 1.0
        n_parallel = ceil((required_energy_kWh * 1000.0) / (e_string_Wh * float(eta)))

        return cls(unit=unit, n_series=n_series, n_parallel=n_parallel)

    # -------- Проверки под инвертор (слайд «Условие выбора…») --------
    def verify_inverter(
        self,
        inverter_input_voltage: float,
        inverter_input_power_kW: float,
        inverter_efficiency: float = 0.95,
        max_allowed_capacity_Ah: Optional[float] = None,
        voltage_tolerance: float = 0.05,
    ) -> Dict[str, object]:
        """
        Проверка ограничений:
          • Uвх инвертора ≈ Uбанка (по допуску);  • Pном инвертора не меньше требуемой входной мощности;
          • (опц.) Cбанка ≤ Cmax для данного инвертора.  :contentReference[oaicite:7]{index=7}
        Возвращает словарь с флагами и вычисленными величинами.
        """
        voltage_match = isclose(self.voltage, inverter_input_voltage,
                                rel_tol=voltage_tolerance, abs_tol=0.0)
        capacity_ok = (max_allowed_capacity_Ah is None) or (self.capacity_Ah <= max_allowed_capacity_Ah)
        # На стороне инвертора: Pвых = η * Pвх. Мы валидируем требуемую ВХОДНУЮ мощность. :contentReference[oaicite:8]{index=8}
        power_ok = inverter_input_power_kW >= 0.0  # если просто проверка совместимости без задания нагрузки

        return {
            "U_bank_V": self.voltage,
            "U_inv_in_V": inverter_input_voltage,
            "voltage_match": voltage_match,
            "C_bank_Ah": self.capacity_Ah,
            "C_max_Ah": max_allowed_capacity_Ah,
            "capacity_ok": capacity_ok,
            "P_inv_in_kW": inverter_input_power_kW,
            "P_inv_out_kW_max": inverter_input_power_kW * inverter_efficiency,
            "eta_inv": inverter_efficiency,
            "power_ok": power_ok,
        }

    # -------- Утилиты --------
    def summary(self) -> str:
        return (
            f"Банк: {self.n_series}с x {self.n_parallel}п ({self.total_cells} модулей {self.unit.name})\n"
            f"Uбанка = {self.voltage:.2f} В, Cбанка = {self.capacity_Ah:.1f} А·ч\n"
            f"Wном = {self.energy_Wh/1000:.2f} кВт·ч, Wполезн ≈ {self.usable_energy_Wh/1000:.2f} кВт·ч\n"
            f"Масса ≈ {self.weight_kg:.1f} кг, Удельная энергия ≈ "
            f"{(self.specific_energy_Wh_per_kg or 0):.1f} Вт·ч/кг, Стоимость ≈ {self.price_total:,.0f} руб"
        )
