from dataclasses import dataclass, field


@dataclass
class PCS:
    name: str
    rated_active_power: float
    max_active_power: float
    peak_active_power: float
    input_voltage: float
    output_voltage: float
    max_capacity: float
    price: float