
from dataclasses import dataclass

from consts import AnomalyType
from models.character import Character, StatsBase


@dataclass
class ConditionalStats:
    conditional_buffs = StatsBase()
    char = Character()

    def get_hp(self) -> float:
        return self.char.get_hp() * (1 + self.conditional_buffs.hp_perc) + self.conditional_buffs.hp

    def get_atk(self) -> float:
        return self.char.get_atk() * (1 + self.conditional_buffs.atk_perc/100) + self.conditional_buffs.atk

    def get_def(self) -> float:
        return self.char.get_def() * (1 + self.conditional_buffs.def_perc) + self.conditional_buffs.defense

    def get_impact(self) -> float:
        return self.char.get_impact() * (1 + self.conditional_buffs.impact_perc) + self.conditional_buffs.impact

    def get_anomaly_prof(self) -> float:
        return self.char.get_anomaly_prof() + self.conditional_buffs.anomaly_prof

    def get_crit_rate(self) -> float:
        return (self.char.get_crit_rate() + self.conditional_buffs.crit_rate)/100

    def get_crit_dmg(self) -> float:
        return (self.char.get_crit_dmg() + self.conditional_buffs.crit_dmg)/100

    def get_energy_regen(self) -> float:
        return self.char.get_energy_regen() * (1 + self.conditional_buffs.energy_perc) + self.conditional_buffs.energy_regen

    def get_anomaly_mastery(self) -> float:
        return self.char.get_anomaly_mastery() * (1 + self.conditional_buffs.anomaly_mastery)

    def get_pen(self) -> float:
        return (self.char.get_pen() + self.conditional_buffs.pen)/100

    def get_pen_flat(self) -> float:
        return self.char.get_pen_flat() + self.conditional_buffs.pen_flat

    def get_phys_bonus(self) -> float:
        return self.char.get_phys_bonus() + self.conditional_buffs.phys_bonus

    def get_fire_bonus(self) -> float:
        return self.char.get_fire_bonus() + self.conditional_buffs.fire_bonus

    def get_ice_bonus(self) -> float:
        return self.char.get_ice_bonus() + self.conditional_buffs.ice_bonus

    def get_elec_bonus(self) -> float:
        return self.char.get_elec_bonus() + self.conditional_buffs.elec_bonus

    def get_ether_bonus(self) -> float:
        return self.char.get_ether_bonus() + self.conditional_buffs.ether_bonus

    def get_bonus_mult(self, anomaly_type:AnomalyType) -> float:
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
        print(f"CR = {self.get_crit_rate():.4f}")
        print(f"CD = {self.get_crit_dmg():.4f}")
        print(f"anomaly mastery = {self.get_anomaly_mastery():.0f}")
        print(f"anomaly proficient = {self.get_anomaly_prof():.0f}")
        print(f"PEN = {self.get_pen():.4f}")
        print(f"ER = {self.get_energy_regen():.2f}")
        print(f"PEN_FLAT = {self.get_pen_flat():.0f}")
        print(f"phys dmg = {self.get_phys_bonus():.2f}")
        print(f"fire dmg = {self.get_fire_bonus():.2f}")
        print(f"ice dmg = {self.get_ice_bonus():.2f}")
        print(f"electric dmg = {self.get_elec_bonus():.2f}")
        print(f"ether dmg = {self.get_ether_bonus():.2f}")
