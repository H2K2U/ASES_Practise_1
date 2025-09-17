from dataclasses import dataclass, field


@dataclass
class BES:
    name: str
    rated_voltage: float
    rated_capacity: float
    specific_energy: float
    weight: float
    price: float
    geometry: tuple[float, float, float] = field(default_factory=tuple)
