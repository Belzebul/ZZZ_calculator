from dataclasses import dataclass, field

from consts import AnomalyType, AttributeID


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
    pen: float = 0.0
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


    def set_attr(self, property_id: int, attr: float) -> None:
        match property_id:
            case AttributeID.HP_BASE: self.hp += attr
            case AttributeID.HP_P: self.hp_perc += attr
            case AttributeID.HP_FLAT: self.hp += attr
            case AttributeID.ATK_BASE: self.atk += attr
            case AttributeID.ATK_P: self.atk_perc += attr
            case AttributeID.ATK_FLAT: self.atk += attr
            case AttributeID.DEF_BASE: self.defense += attr
            case AttributeID.DEF_P: self.def_perc += attr
            case AttributeID.DEF_FLAT: self.defense += attr
            case AttributeID.IMPACT: self.impact += attr
            case AttributeID.IMPACT_P: self.impact_perc += attr
            case AttributeID.CRIT_RATE_BASE: self.crit_rate += attr
            case AttributeID.CRIT_RATE: self.crit_rate += attr
            case AttributeID.CRIT_DMG_BASE: self.crit_dmg += attr
            case AttributeID.CRIT_DMG: self.crit_dmg += attr
            case AttributeID.PEN_BASE: self.pen += attr
            case AttributeID.PEN_P: self.pen += attr
            case AttributeID.PEN_FLAT: self.pen_flat += attr
            case AttributeID.ANOMALY_MAST_BASE: self.anomaly_mastery += attr
            case AttributeID.ANOMALY_MAST: self.anomaly_mastery += attr
            case AttributeID.ANOMALY_PROF_BASE: self.anomaly_prof += attr
            case AttributeID.ANOMALY_PROF: self.anomaly_prof += attr
            case AttributeID.PHYS_DMG: self.phys_bonus += attr
            case AttributeID.FIRE_DMG: self.fire_bonus += attr
            case AttributeID.ICE_DMG: self.ice_bonus += attr
            case AttributeID.ELEC_DMG: self.elec_bonus += attr
            case AttributeID.ETHER_DMG: self.ether_bonus += attr


@dataclass(slots=True)
class Hit:
    quantity: int = 1
    anomaly: int = AnomalyType.PHYSICAL


@dataclass(slots=True)
class Multiplier:
    base: float
    growth: float
    mult: float

    def get_mult(self, lvl):
        return (self.base + (lvl - 1) * self.growth) * self.mult / 100


@dataclass(slots=True)
class SubSkill:
    name: str
    lvl: int
    dmg: Multiplier
    daze: Multiplier
    hits: list[Hit]


@dataclass(slots=True)
class Skill:
    lvl: int = 1
    sub_skills: list[SubSkill] = field(default_factory=list)


@dataclass(slots=True)
class Equip:
    discs: list = field(default_factory=list)
    # TODO


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
    discs = StatsBase()

    def equip_discs(self, disc: StatsBase) -> None:
        self.discs = disc

    def equip_wengine(self, wengine: StatsBase) -> None:
        self.wengine = wengine

    def get_hp(self) -> float:
        self.hp = (
            self.base.hp
            * (
                1
                + (self.base.hp_perc + self.wengine.hp_perc + self.discs.hp_perc) / 100
            )
            + self.discs.hp
        )
        return self.hp

    def get_atk(self) -> float:
        atk_base = self.base.atk + self.wengine.atk
        self.atk = atk_base * (1 + (self.discs.atk_perc + self.wengine.atk_perc) / 100) + self.discs.atk
        return self.atk

    def get_def(self) -> float:
        self.defense = (
            self.base.defense
            * (
                1
                + (self.base.def_perc + self.discs.def_perc + self.wengine.def_perc)
                / 100
            )
            + self.discs.defense
        )
        return self.defense

    def get_impact(self) -> float:
        self.impact = (
            self.base.impact * (1 + self.wengine.impact_perc + self.discs.impact_perc)
            + self.wengine.impact
        )
        return self.impact

    def get_anomaly_prof(self) -> float:
        self.anomaly_prof = (
            self.base.anomaly_prof + self.wengine.anomaly_prof + self.discs.anomaly_prof
        )
        return self.anomaly_prof

    def get_crit_rate(self) -> float:
        return self.base.crit_rate + self.wengine.crit_rate + self.discs.crit_rate

    def get_crit_dmg(self) -> float:
        return self.base.crit_dmg + self.wengine.crit_dmg + self.discs.crit_dmg

    def get_energy_regen(self) -> float:
        self.energy_regen = self.base.energy_regen * (
            1 + (self.wengine.energy_perc + self.discs.energy_perc) / 100
        )
        return self.energy_regen

    def get_anomaly_mastery(self) -> float:
        self.anomaly_mastery = self.base.anomaly_mastery * (
            1 + (self.wengine.anomaly_mastery + self.discs.anomaly_mastery) / 100
        )
        return self.anomaly_mastery

    def get_pen(self) -> float:
        self.pen = (self.base.pen + self.wengine.pen + self.discs.pen)
        return self.pen

    def get_pen_flat(self) -> float:
        self.pen_flat = self.wengine.pen_flat + self.discs.pen_flat
        return self.pen_flat

    def get_phys_bonus(self) -> float:
        self.phys_bonus = (
            self.base.phys_bonus + self.wengine.phys_bonus + self.discs.phys_bonus
        )
        return self.phys_bonus

    def get_fire_bonus(self) -> float:
        self.fire_bonus = (
            self.base.fire_bonus + self.wengine.fire_bonus + self.discs.fire_bonus
        )
        return self.fire_bonus

    def get_ice_bonus(self) -> float:
        self.ice_bonus = (
            self.base.ice_bonus + self.wengine.ice_bonus + self.discs.ice_bonus
        )
        return self.ice_bonus

    def get_elec_bonus(self) -> float:
        self.elec_bonus = (
            self.base.elec_bonus + self.wengine.elec_bonus + self.discs.elec_bonus
        )
        return self.elec_bonus

    def get_ether_bonus(self) -> float:
        self.ether_bonus = (
            self.base.ether_bonus + self.wengine.ether_bonus + self.discs.ether_bonus
        )
        return self.ether_bonus

    def get_lvl_factor(self) -> float:
        return 0.1551 * self.lvl**2 + 3.141 * self.lvl + 47.2039

    def get_bonus_mult(self, anomalyType) -> float:
        match anomalyType:
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
