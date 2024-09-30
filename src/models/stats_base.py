
from dataclasses import dataclass
from consts import HOYO_MAP


@dataclass
class StatsBase:
    lvl: int = 1
    hp_perc: float = 0.0
    hp: float = 0.0
    atk_perc: float = 0.0
    atk: float = 0.0
    def_perc: float = 0.0
    defense: float = 0.0
    impact: float = 0.0
    impact_perc: float = 0.0
    crit_rate: float = 0.0
    crit_dmg: float = 0.0
    pen_p: float = 0.0
    pen_flat: float = 0.0
    energy_regen: float = 0.0
    energy_perc: float = 0.0
    anomaly_prof: float = 0.0
    anomaly_mastery: float = 0.0
    phys_bonus: float = 0.0
    fire_bonus: float = 0.0
    ice_bonus: float = 0.0
    elec_bonus: float = 0.0
    ether_bonus: float = 0.0

    def incr_attr(self, hoyo_id:int, value:float) -> None:
        self.__dict__[HOYO_MAP[hoyo_id]] += value

    def __add__(self, other) -> None:
        attrs:list = list(self.__dict__.keys())
        for attr in attrs:
            self.__dict__[attr] += other.__dict__[attr]

