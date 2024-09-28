from dataclasses import dataclass, field

from consts import AttributeID

main_stats = [
    AttributeID.HP_FLAT,
    AttributeID.HP_P,
    AttributeID.ATK_FLAT,
    AttributeID.ATK_P,
    AttributeID.DEF_FLAT,
    AttributeID.DEF_P,
    AttributeID.CRIT_RATE,
    AttributeID.CRIT_DMG,
    AttributeID.ANOMALY_PROF,
    AttributeID.ANOMALY_MAST,
    AttributeID.PEN_P,
    AttributeID.IMPACT_P,
    AttributeID.ENERGY_P,
    AttributeID.PHYS_DMG,
    AttributeID.FIRE_DMG,
    AttributeID.ICE_DMG,
    AttributeID.ELEC_DMG,
    AttributeID.ETHER_DMG,
]


@dataclass
class Stat:
    id: int
    value: float


@dataclass
class Disc:
    pos: int
    equip_set: int
    main_stats: Stat
    substats: list[Stat] = field(default_factory=list)


@dataclass
class Discs:
    discs: list[Disc] = field(default_factory=list)
