from dataclasses import dataclass, field


@dataclass
class HydroPowerPlant:
    name: str
    rated_active_power: float
    rated_voltage: float = field(default=0.4)
    active_power: float = field(default=0)

    def __post_init__(self):
        self.active_power = self.rated_active_power
