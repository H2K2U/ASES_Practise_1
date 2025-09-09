from dataclasses import dataclass, field
from Practise.LoadGraph.LoadType import LoadType


@dataclass
class TotalLoad:
    load_list: list[LoadType] = field(default_factory=list)

    def total_active_lp(self):
        return sum(self.load_list[i].load_power for i in range(len(self.load_list)))

    def total_reactive_lp(self):
        return sum(self.load_list[i].reactive_lp() for i in range(len(self.load_list)))

    def total_apparent_lp(self):
        return sum(self.load_list[i].apparent_lp() for i in range(len(self.load_list)))

    def append_load(self, load: LoadType):
        self.load_list.append(load)

    def delete_load(self, idx: int):
        self.load_list.pop(idx)

    def extend_load(self, load_lst: list[LoadType]):
        self.load_list.extend(load_lst)