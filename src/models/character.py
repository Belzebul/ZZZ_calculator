from dataclasses import dataclass, field
import re

from consts import AnomalyType
from models.disc import DiscSet
from models.stats_base import StatsBase

@dataclass(slots=True)
class Hit:
    quantity: int = 1
    anomaly: int = AnomalyType.PHYSICAL


@dataclass(slots=True)
class Multiplier:
    param_id: list[str]
    name:str
    desc: str
    base: list[float]
    growth: list[float]
    mult: float = field(init=False)

    def calc_mult(self, lvl) -> None:
        find_mult_pattern = re.compile(r"\{(\w*\:\d*\, \w*\:\d*)\}")
        mult = self.desc
        for index, _ in enumerate(self.base):
            mult = find_mult_pattern.sub(self.__mount_mult_base(lvl, index), mult, count=1)

        mult = re.sub(r"[\{\}]","", mult)
        self.mult = round(eval(mult), 2)

    def __mount_mult_base(self, lvl, index) -> str:
        return str(self.base[index] + (lvl - 1) * self.growth[index])



@dataclass(slots=True)
class SubSkill:
    lvl: int
    dmg: Multiplier = field(init=False)
    daze: Multiplier = field(init=False)
    hits: list[Hit] = field(init=False)

@dataclass(slots=True)
class SkillDesc:
    name:str
    desc:str

@dataclass(slots=True)
class Skill:
    lvl: int = 1
    description: list[SkillDesc] = field(default_factory=list)
    sub_skills: list[SubSkill] = field(default_factory=list)


@dataclass
class Character(StatsBase):
    basic = Skill()
    dodge = Skill()
    assist = Skill()
    special = Skill()
    chain = Skill()
    core = Skill()
    base = StatsBase()
    wengine = StatsBase()
    disc_sets = DiscSet()
    sum_discs = StatsBase()

    def equip_disc_set(self, disc_set: DiscSet) -> None:
        self.disc_sets = disc_set
        self.sum_discs = disc_set.sum_stats()

    def equip_wengine(self, wengine: StatsBase) -> None:
        self.wengine = wengine

    def get_hp(self) -> float:
        percents = 1 + (self.base.hp_perc + self.wengine.hp_perc + self.sum_discs.hp_perc) / 100
        self.hp = (self.base.hp * percents) + self.sum_discs.hp
        return self.hp

    def get_atk(self) -> float:
        atk_base = self.base.atk + self.wengine.atk
        atk_percents = round(1 + (self.sum_discs.atk_perc + self.wengine.atk_perc)/100, 2)
        self.atk = atk_base * atk_percents + self.sum_discs.atk
        return int(self.atk)

    def get_def(self) -> float:
        def_percents = 1 + (self.base.def_perc + self.sum_discs.def_perc + self.wengine.def_perc)/ 100
        self.defense = self.base.defense * def_percents + self.sum_discs.defense
        return self.defense

    def get_impact(self) -> float:
        impact_percents = 1 + (self.wengine.impact_perc + self.sum_discs.impact_perc)/100
        self.impact = self.base.impact * impact_percents + self.wengine.impact
        return self.impact

    def get_anomaly_prof(self) -> float:
        self.anomaly_prof = self.base.anomaly_prof + self.wengine.anomaly_prof + self.sum_discs.anomaly_prof
        return self.anomaly_prof

    def get_crit_rate(self) -> float:
        return self.base.crit_rate + self.wengine.crit_rate + self.sum_discs.crit_rate

    def get_crit_dmg(self) -> float:
        return self.base.crit_dmg + self.wengine.crit_dmg + self.sum_discs.crit_dmg

    def get_energy_regen(self) -> float:
        energy_percents = 1 + (self.wengine.energy_perc + self.sum_discs.energy_perc)/100
        self.energy_regen = self.base.energy_regen * energy_percents
        return self.energy_regen

    def get_anomaly_mastery(self) -> float:
        anom_mast_percents = 1 + (self.wengine.anomaly_mastery + self.sum_discs.anomaly_mastery) / 100
        self.anomaly_mastery = self.base.anomaly_mastery * anom_mast_percents
        return self.anomaly_mastery

    def get_pen(self) -> float:
        self.pen_p = self.base.pen_p + self.wengine.pen_p + self.sum_discs.pen_p
        return self.pen_p

    def get_pen_flat(self) -> float:
        self.pen_flat = self.wengine.pen_flat + self.sum_discs.pen_flat
        return self.pen_flat

    def get_phys_bonus(self) -> float:
        self.phys_bonus = self.base.phys_bonus + self.wengine.phys_bonus + self.sum_discs.phys_bonus
        return self.phys_bonus

    def get_fire_bonus(self) -> float:
        self.fire_bonus = self.base.fire_bonus + self.wengine.fire_bonus + self.sum_discs.fire_bonus
        return self.fire_bonus

    def get_ice_bonus(self) -> float:
        self.ice_bonus = self.base.ice_bonus + self.wengine.ice_bonus + self.sum_discs.ice_bonus
        return self.ice_bonus

    def get_elec_bonus(self) -> float:
        self.elec_bonus = self.base.elec_bonus + self.wengine.elec_bonus + self.sum_discs.elec_bonus
        return self.elec_bonus

    def get_ether_bonus(self) -> float:
        self.ether_bonus = (
            self.base.ether_bonus + self.wengine.ether_bonus + self.sum_discs.ether_bonus
        )
        return self.ether_bonus

    def get_lvl_factor(self) -> float:
        return 0.1551 * self.lvl**2 + 3.141 * self.lvl + 47.2039

    def get_bonus_mult(self, anomaly_type:int) -> float:
        match anomaly_type:
            case AnomalyType.PHYSICAL:
                return 1 + self.get_phys_bonus() / 100
            case AnomalyType.FIRE:
                return 1 + self.get_fire_bonus() / 100
            case AnomalyType.ICE:
                return 1 + self.get_ice_bonus() / 100
            case AnomalyType.ELECTRO:
                return 1 + self.get_elec_bonus() / 100
            case AnomalyType.ETHER:
                return 1 + self.get_ether_bonus() / 100
        return 1.0

    def print_stats(self) -> None:
        print(f"HP = {self.get_hp():.0f}")
        print(f"ATK = {self.get_atk():.0f}")
        print(f"DEF = {self.get_def():.0f}")
        print(f"impact = {self.get_impact():.0f}")
        print(f"CR = {self.get_crit_rate():.2f}")
        print(f"CD = {self.get_crit_dmg():.2f}")
        print(f"anomaly mastery = {self.get_anomaly_mastery():.0f}")
        print(f"anomaly proficient = {self.get_anomaly_prof():.0f}")
        print(f"PEN = {self.get_pen():.2f}")
        print(f"ER = {self.get_energy_regen():.2f}")
        print(f"PEN_FLAT = {self.get_pen_flat():.0f}")
        print(f"phys dmg = {self.get_phys_bonus():.2f}")
        print(f"fire dmg = {self.get_fire_bonus():.2f}")
        print(f"ice dmg = {self.get_ice_bonus():.2f}")
        print(f"electric dmg = {self.get_elec_bonus():.2f}")
        print(f"ether dmg = {self.get_ether_bonus():.2f}")
