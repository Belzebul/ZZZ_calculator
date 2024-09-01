def getData(data,key):
    if key in data:
        return data[key]
    return 0

class AttributeID():
    HP_BASE = 11101
    HP_PERC = 11102
    HP_FLAT = 11103
    ATK_BASE = 12101
    ATK_PERC = 12102
    ATK_FLAT = 12103
    DEF_BASE = 13101
    DEF_PERC = 13102
    DEF_FLAT = 13103
    CRIT_RATE_BASE = 20101
    CRIT_RATE = 20103
    CRIT_DMG_BASE = 21101
    CRIT_DMG = 21103
    PEN_FLAT = 23203
    PEN_BASE = 23101
    PEN = 23103
    ANOMALY_PROF_BASE = 31201
    ANOMALY_PROF = 31203
    ANOMALY_MAST_BASE = 31401
    ANOMALY_MAST = 31402
    PHYS_DMG = 31503
    FIRE_DMG = 31603
    ICE_DMG = 31703
    ELEC_DMG = 31803
    ETHER_DMG = 31903

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
            case AttributeID.HP_BASE: self.hp_base += attr
            case AttributeID.HP_PERC: self.hp += attr
            case AttributeID.HP_FLAT: self.hp_flat += attr

            case AttributeID.ATK_BASE: self.atk_base += attr
            case AttributeID.ATK_PERC: self.atk += attr
            case AttributeID.ATK_FLAT: self.atk_flat += attr

            case AttributeID.DEF_BASE: self.defense_base += attr
            case AttributeID.DEF_PERC: self.defense += attr
            case AttributeID.DEF_FLAT: self.defense_flat += attr

            case AttributeID.CRIT_RATE_BASE: self.crit_rate += attr
            case AttributeID.CRIT_RATE: self.crit_rate += attr
            case AttributeID.CRIT_DMG_BASE: self.crit_dmg += attr
            case AttributeID.CRIT_DMG: self.crit_dmg += attr

            case AttributeID.PEN_BASE: self.pen += attr
            case AttributeID.PEN: self.pen += attr
            case AttributeID.PEN_FLAT: self.pen_flat += attr

            case AttributeID.ANOMALY_MAST_BASE: self.anomaly_mastery += attr
            case AttributeID.ANOMALY_MAST: self.anomaly_mastery += attr
            case AttributeID.ANOMALY_PROF_BASE: self.anomaly_prof += attr
            case AttributeID.ANOMALY_PROF: self.anomaly_prof += attr

            case AttributeID.PHYS_DMG: self.phys_dmg += attr
            case AttributeID.FIRE_DMG: self.fire_dmg += attr
            case AttributeID.ELEC_DMG: self.elec_dmg += attr
            case AttributeID.ICE_DMG: self.ice_dmg += attr
            case AttributeID.ETHER_DMG: self.ether_dmg += attr

        

class DamageType():
    PHYS = 0
    ELEC = 1 
    FIRE = 2

class Hit():
    def __init__(self, dmg_base = 0.0, dmg_growth = 0.0, daze_base = 0.0, daze_growth = 0.0, dmg_type = 0) -> None:
        self.dmg_base = dmg_base
        self.dmg_growth = dmg_growth
        self.daze_base = daze_base
        self.daze_growth = daze_growth
        self.dmg_type = dmg_type

class Skill():
    def __init__(self, lvl = 1, number_hits = 2) -> None:
       self.hits = []       

class Disc(ModelBase):
    def __init__(self) -> None:
        super().__init__()

class WEngine(ModelBase):
    def __init__(self) -> None:
        super().__init__()

class Character(ModelBase):

    def __init__(self) -> None:
        super().__init__()

        self.basic = Skill()
        self.dodge = Skill()
        self.assist = Skill()
        self.special = Skill()
        self.chain = Skill()
        self.core = Skill()
        
    
    def set_char_attr_from_id(self, property_id, attr_base, attr_final):
        match property_id:
            case CharAttributeID.HP: self.hp_base += attr_base
            case CharAttributeID.ATK: self.atk_base += attr_base
            case CharAttributeID.DEF: self.defense_base += attr_base
            case CharAttributeID.IMPACT: self.impact += attr_final
            case CharAttributeID.CRIT_RATE: self.crit_rate += attr_base
            case CharAttributeID.CRIT_DMG: self.crit_dmg += attr_base
            case CharAttributeID.ANOMALY_MAST: self.anomaly_mastery += attr_base
            case CharAttributeID.ANOMALY_PROF: self.anomaly_prof += attr_final
            case CharAttributeID.PEN: self.pen += attr_base  
            case CharAttributeID.ENERGY_REGEN: self.energy_regen += attr_base

    def equip_discs(self, disc:Disc):
        self.discs = disc

    def equip_wengine(self, wengine: WEngine):
        self.wengine = wengine

    def print_stats(self):
        print(f'HP = {self.get_hp()}')
        print(f'ATK = {self.get_atk()}')
        print(f'DEF = {self.get_def()}')
        print(f'impact = {self.impact}')
        print(f'CR = {self.get_crit_rate()}')
        print(f'CD = {self.get_crit_dmg()}')
        print(f'anomaly mastery = {self.get_anomaly_mastery()}')
        print(f'anomaly proficient = {self.get_anomaly_prof()}')
        print(f'PEN = {self.get_pen()}')
        print(f'ER = {self.get_energy_regen()}')
        print(f'PEN_FLAT = {self.get_pen_flat()}')
        print(f'electric dmg = {self.get_elec_dmg()}')

    def get_hp(self):
        return self.hp_base * (1 + (self.hp + self.wengine.hp + self.discs.hp)/100) + self.discs.hp_flat

    def get_atk(self):
        return (self.atk_base + self.wengine.atk_base) * (1 + (self.discs.atk + self.wengine.atk)/100) + self.discs.atk_flat
    
    def get_def(self):
        return self.defense_base * (1 + (self.defense + self.discs.defense + self.wengine.defense)/100) + self.discs.defense_flat
    
    def get_anomaly_prof(self):
        return (self.anomaly_prof + self.wengine.anomaly_prof + self.discs.anomaly_prof)
    
    def get_crit_rate(self):
        return self.crit_rate + self.wengine.crit_rate + self.discs.crit_rate

    def get_crit_dmg(self):
        return self.crit_dmg + self.wengine.crit_dmg + self.discs.crit_dmg

    def get_energy_regen(self):
        return self.energy_regen * (1 + (self.wengine.energy_perc + self.discs.energy_perc)/100)

    def get_anomaly_mastery(self):
        return self.anomaly_mastery * (1 + (self.wengine.anomaly_mastery + self.discs.anomaly_mastery)/100)

    def get_pen(self):
        return self.pen + self.wengine.pen + self.discs.pen

    def get_pen_flat(self):
        return self.wengine.pen_flat + self.discs.pen_flat

    def get_elec_dmg(self):
        return self.elec_dmg + self.wengine.elec_dmg + self.discs.elec_dmg

    def get_dmg_bonus(self):
        return self.dmg_bonus + self.wengine.dmg_bonus + self.discs.dmg_bonus

    def get_lvl_factor(self):
        return 0.1551 * self.lvl**2 + 3.141 * self.lvl + 47.2039
  