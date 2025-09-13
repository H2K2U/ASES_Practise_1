# Practise/Storage/BES.py
from dataclasses import dataclass, field
from typing import Tuple, Optional


@dataclass
class BES:
    """
    Единичная АКБ (ячейка/модуль).
    Поля соответствуют таблице данных из задания.
    """
    name: str
    rated_voltage: float                 # Uном, В
    rated_capacity: float                # Cном, А·ч
    specific_energy: float               # Удельная энергия, Вт·ч/кг
    weight: float                        # Масса, кг
    price: float                         # Цена, руб
    geometry: Tuple[float, float, float] = field(default_factory=tuple)  # (Д, Ш, В) в мм

    # Дополнительно для расчётов по практике
    chemistry: str = "li-ion"            # 'li-ion' | 'pb' (lead-acid) | иное описание
    roundtrip_efficiency: Optional[float] = None  # КПД цикла заряда-разряда, доли ед.

    def __post_init__(self) -> None:
        # Если КПД не задан — подставим типовые значения из методички:
        # η≈0.96 для Li-ion и ≈0.80 для Pb-acid. :contentReference[oaicite:1]{index=1}
        if self.roundtrip_efficiency is None:
            chem = self.chemistry.lower()
            if any(x in chem for x in ("li", "ion", "lipo", "lifepo", "lyp")):
                self.roundtrip_efficiency = 0.96
            elif any(x in chem for x in ("pb", "lead")):
                self.roundtrip_efficiency = 0.80
            else:
                # По умолчанию считаем как Li-ion, чтобы не занижать расчёт
                self.roundtrip_efficiency = 0.96

    # --- Удобные свойства ---
    @property
    def energy_Wh(self) -> float:
        """Номинальная энергия модуля, Вт·ч = U * C."""
        return self.rated_voltage * self.rated_capacity

    @property
    def energy_kWh(self) -> float:
        return self.energy_Wh / 1000.0

    @property
    def usable_energy_Wh(self) -> float:
        """Полезная энергия (с учётом η цикла)."""
        return self.energy_Wh * float(self.roundtrip_efficiency)

    @property
    def volume_l(self) -> Optional[float]:
        """Объём в литрах (из габаритов в мм)."""
        if not self.geometry:
            return None
        L, W, H = self.geometry
        return (L * W * H) / 1_000_000.0  # 1 л = 1e6 мм^3
