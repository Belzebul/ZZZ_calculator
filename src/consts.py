from enum import IntEnum, StrEnum


class AttributeID(IntEnum):
    HP_BASE = 11101
    HP_P = 11102
    HP_FLAT = 11103
    ATK_BASE = 12101
    ATK_P = 12102
    ATK_FLAT = 12103
    IMPACT = 12201
    IMPACT_P = 12202
    DEF_BASE = 13101
    DEF_P = 13102
    DEF_FLAT = 13103
    CRIT_RATE_BASE = 20101
    CRIT_RATE = 20103
    CRIT_DMG_BASE = 21101
    CRIT_DMG = 21103
    PEN_BASE = 23101
    PEN_P = 23103
    PEN_FLAT = 23203
    ENERGY_RATE = 1
    ENERGY_P = 2
    ANOMALY_PROF_BASE = 31201
    ANOMALY_PROF = 31203
    ANOMALY_MAST_BASE = 31401
    ANOMALY_MAST = 31402
    PHYS_DMG = 31503
    FIRE_DMG = 31603
    ICE_DMG = 31703
    ELEC_DMG = 31803
    ETHER_DMG = 31903


class EnemyType(IntEnum):
    DURAHAN = 58
    TYRFING = 36
    THUG_ASSAULT = 37
    RANGE_SOLDIER = 33
    METAL_GORILLA = 60
    DEATH_XIII = 45
    # TODO


class AnomalyType(IntEnum):
    PHYSICAL = 200
    FIRE = 201
    ICE = 202
    ELECTRO = 203
    ETHER = 205


class AnomalyMult:
    ASSAULT = 7.13
    BURN = 0.5
    SHATTER = 5.0
    SHOCK = 1.25
    CORRUPTION = 0.625


ANOMALY_MULT = {
    AnomalyType.PHYSICAL: AnomalyMult.ASSAULT,
    AnomalyType.FIRE: AnomalyMult.BURN,
    AnomalyType.ICE: AnomalyMult.SHATTER,
    AnomalyType.ELECTRO: AnomalyMult.SHOCK,
    AnomalyType.ETHER: AnomalyMult.CORRUPTION,
}


class CharacterNames(StrEnum):
    CORIN = "Corin"
    QINGYI = "QingYi"
    JANE = "Jane"
    SOUKAKU = "Soukaku"
    BILLY = "Billy"
    GRACE = "Grace"
    ANBY = "Anby"
    NICOLE = "Nicole"
    PIPER = "Piper"
    NEKOMATA = "Nekomata"
    ZHUYUAN = "Zhu Yuan"
    LYCAON = "Lycaon"
    ANTON = "Anton"
    SOLDIER_11 = "Soldier 11"
    BEN = "Ben"
    RINA = "Rina"
    LUCY = "Lucy"
    KOLEDA = "Koleda"
    SETH = "Seth"
    BURNICE = "Burnice"
    ELLEN = "Ellen"


class CharacterId(StrEnum):
    CORIN = "1061"
    QINGYI = "QingYi"
    JANE = "1261"
    SOUKAKU = "1131"
    BILLY = "1081"
    GRACE = "1181"
    ANBY = "1011"
    NICOLE = "1031"
    PIPER = "1281"
    NEKOMATA = "1021"
    NEKOMATA_2 = "1022"
    ZHUYUAN = "Zhu Yuan"
    LYCAON = "Lycaon"
    ANTON = "1111"
    SOLDIER_11 = "1041"
    BEN = "1121"
    RINA = "Rina"
    LUCY = "1151"
    KOLEDA = "Koleda"
    SETH = "1271"
    BURNICE = "Burnice"
    ELLEN = "Ellen"


CHAR_LIST_CODES = [
    "Corin",
    "QingYi",
    "Jane",
    "Soukaku",
    "Harumasa",
    "Billy",
    "Grace",
    "Wise",
    "Anby",
    "Caesar",
    "Belle",
    "Nicole",
    "Piper",
    "Nekomata",
    "Zhu Yuan",
    "Lycaon",
    "Lighter",
    "Anton",
    "Soldier 11",
    "Miyabi",
    "Ben",
    "Rina",
    "Avatar_Female_Size03_Pulchra",
    "Lucy",
    "Koleda",
    "Yanagi",
    "Seth",
    "Burnice",
    "Ellen",
]
