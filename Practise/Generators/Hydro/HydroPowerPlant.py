from dataclasses import dataclass, field


@dataclass
class HydroPowerPlant:
    name: str
    rated_active_power: float
    rated_apparent_power: float = field(init=False)
    rated_voltage: float = field(default=0.4)
    active_power: float = field(init=False)

    def __post_init__(self):
        self.active_power = self.rated_active_power
        # в данной задаче мощности активная и полная равны
        self.rated_apparent_power = self.rated_active_power