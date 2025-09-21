from dataclasses import dataclass, field
import math


@dataclass
class LoadType:
    lp_type: str
    __load_power: float
    cosf: float
    rated_voltage: float = field(default=0.4)

    @property
    def load_power(self): return self.__load_power

    @load_power.setter
    def load_power(self, load_power): self.__load_power = load_power

    def apparent_lp(self):
        return self.__load_power * self.cosf

    def reactive_lp(self):
        return math.sqrt(self.apparent_lp() ** 2 - self.__load_power ** 2)
