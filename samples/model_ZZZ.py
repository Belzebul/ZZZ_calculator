def getData(data,key):
    if key in data:
        return data[key]
    return 0

class AttributeID():
    HP = 11102
    HP_FLAT = 11103
    ATK_BASE = 12101
    ATK = 12102
    ATK_FLAT = 12103
    DEF = 13102
    DEF_FLAT = 13103
    CRIT_RATE = 20103
    CRIT_DMG = 21103
    PEN_FLAT = 23203
    PEN = 23103
    ANOMALY_PROF = 31203
    ANOMALY_MAST = 31402
    PHYS_DMG = 31503

class CharAttributeID():
    HP = 1
    ATK = 2
    DEF = 3
    IMPACT = 4
    CRIT_RATE = 5
    CRIT_DMG = 6
    ANOMALY_MAST = 7
    ANOMALY_PROF = 8
    PEN = 9
    ENERGY_REGEN = 10

class ModelBase():
    lvl = 1
    hp = 0.0
    hp_base = 0.0
    hp_flat = 0.0
    atk = 0.0
    atk_base = 0.0
    atk_flat = 0.0
    defense = 0.0
    defense_base = 0.0
    defense_flat = 0.0

    impact = 0.0
    crit_rate = 0.0
    crit_dmg = 0.0
    pen = 0.0
    pen_flat = 0.0
    energy_regen = 0.0
    energy_perc = 0.0
    anomaly_prof = 0.0
    anomaly_mastery = 0.0

    dmg_bonus = 0.0
    phys_dmg = 0.0
    elec_dmg = 0.0
    ether_dmg = 0.0
    fire_dmg = 0.0
    ice_dmg = 0.0

    def __init__(self) -> None:
        pass

    def set_attr_from_id(self, property_id, attr):
        match property_id:
            case AttributeID.HP: self.hp += attr
            case AttributeID.HP_FLAT: self.hp_flat += attr
            case AttributeID.ATK_BASE: self.atk_base += attr
            case AttributeID.ATK: self.atk += attr
            case AttributeID.ATK_FLAT: self.atk_flat += attr
            case AttributeID.DEF: self.defense += attr
            case AttributeID.DEF_FLAT: self.defense_flat += attr
            case AttributeID.CRIT_RATE: self.crit_rate += attr
            case AttributeID.CRIT_DMG: self.crit_dmg += attr
            case AttributeID.PEN: self.pen += attr
            case AttributeID.PEN_FLAT: self.pen_flat += attr
            case AttributeID.ANOMALY_MAST: self.anomaly_mastery += attr
            case AttributeID.ANOMALY_PROF: self.anomaly_prof += attr
            case AttributeID.PHYS_DMG: self.dmg_bonus += attr

class DamageType():
    ELECTRIC = 0 
    FIRE = 1

class Hit():
    def __init__(self, data) -> None:
        self.mult = data.mult
        self.dmg_type = DamageType.ELECTRIC
        pass

class Skill():
    def __init__(self, lvl) -> None:
       hit = Hit(lvl)
       

class Disc(ModelBase):
    def __init__(self) -> None:
        super().__init__()

class WEngine(ModelBase):
    def __init__(self) -> None:
        super().__init__()

class Character(ModelBase):
    def __init__(self) -> None:
        super().__init__()

    def set_attr_from_id(self, property_id, attr_base, attr_final):
        match property_id:
            case CharAttributeID.HP: self.hp_base = attr_base
            case CharAttributeID.ATK: self.atk_base = attr_base
            case CharAttributeID.DEF: self.def_base = attr_base
            case CharAttributeID.IMPACT: self.impact = attr_final
            case CharAttributeID.CRIT_RATE: self.crit_rate += attr_base
            case CharAttributeID.CRIT_DMG: self.crit_dmg += attr_base
            case CharAttributeID.ANOMALY_MAST: self.anomaly_mastery = attr_base
            case CharAttributeID.ANOMALY_PROF: self.anomaly_prof = attr_final
            case CharAttributeID.PEN: self.pen = attr_base  
            case CharAttributeID.ENERGY_REGEN: self.energy_regen = attr_base

    def equip_discs(self, disc:Disc):
        self.discs = disc

    def equip_wengine(self, wengine: WEngine):
        self.wengine = wengine

    def get_atk(self):
        return (self.atk_base + self.wengine.atk_base) * (1 + (self.discs.atk + self.wengine.atk)/100) + self.discs.atk_flat
    
    def get_anomaly_prof(self):
        return (self.anomaly_prof + self.wengine.anomaly_prof + self.discs.anomaly_prof)
    
    def get_crit_rate(self):
        return self.crit_rate + self.wengine.crit_rate + self.discs.crit_rate

    def get_crit_dmg(self):
        return self.crit_dmg + self.wengine.crit_dmg + self.discs.crit_dmg

    def get_energy_regen(self):
        return self.energy * (1 + (self.wengine.energy_regen + self.discs.energy_regen)/100)

    def get_anomaly_mastery(self):
        return self.anomaly_mastery + self.wengine.anomaly_mastery + self.discs.anomaly_mastery

    def get_pen(self):
        return self.pen + self.wengine.pen + self.discs.pen

    def get_pen_flat(self):
        return self.wengine.pen_flat + self.discs.pen_flat

    def get_dmg_bonus(self):
        return self.dmg_bonus + self.wengine.dmg_bonus + self.discs.dmg_bonus

    def get_lvl_factor(self):
        return 0.1551 * self.lvl**2 + 3.141 * self.lvl + 47.2039
  