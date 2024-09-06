from consts import AttributeID

class ModelBase():
    lvl:int = 1

    hp_perc:float = 0.0
    hp:float = 0.0

    atk_perc:float = 0.0
    atk:float = 0.0

    def_perc:float = 0.0
    defense:float = 0.0

    impact:float = 0.0
    impact_perc:float = 0.0

    crit_rate:float = 0.0
    crit_dmg:float = 0.0

    pen:float = 0.0
    pen_flat:float = 0.0

    energy_regen:float = 0.0
    energy_perc:float = 0.0

    anomaly_prof:float = 0.0
    anomaly_mastery:float = 0.0

    dmg_bonus:float = 0.0
    phys_dmg:float = 0.0
    elec_dmg:float = 0.0
    ether_dmg:float = 0.0
    fire_dmg:float = 0.0
    ice_dmg:float = 0.0

    def __init__(self) -> None:
        pass

    def set_attr_from_id(self, property_id, attr):
        match property_id:
            case AttributeID.HP_BASE: self.hp += attr
            case AttributeID.HP_PERC: self.hp_perc += attr
            case AttributeID.HP_FLAT: self.hp += attr

            case AttributeID.ATK_BASE: self.atk += attr
            case AttributeID.ATK_PERC: self.atk_perc += attr
            case AttributeID.ATK_FLAT: self.atk += attr

            case AttributeID.DEF_BASE: self.defense += attr
            case AttributeID.DEF_PERC: self.def_perc += attr
            case AttributeID.DEF_FLAT: self.defense += attr

            case AttributeID.IMPACT: self.impact += attr
            case AttributeID.IMPACT_PERC: self.impact_perc += attr

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

        
'''
TODO
class DamageType():
    PHYS = 0
    ELEC = 1 
    FIRE = 2
'''

class Hit():
    def __init__(self, mult_dmg, mult_daze, dmg_type = [0]) -> None:
        self.mult_dmg = mult_dmg
        self.mult_daze = mult_daze
        self.split = []
        self.dmg_type = dmg_type

class Skill():
    def __init__(self, lvl = 1) -> None:
       self.lvl = lvl
       self.hits = []       

class Equip:

    def __init__(self) -> None:
        #TODO
        discs = []
        pass

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

    def equip_discs(self, disc:Disc):
        self.discs = disc

    def equip_wengine(self, wengine: WEngine):
        self.wengine = wengine

    def get_hp(self):
        return self.hp * (1 + (self.hp_perc + self.wengine.hp_perc + self.discs.hp_perc)/100) + self.discs.hp

    def get_atk(self):
        atk = (self.atk + self.wengine.atk) * (1 + (self.discs.atk_perc + self.wengine.atk_perc)/100) + self.discs.atk
        return atk
    
    def get_def(self):
        return self.defense * (1 + (self.def_perc + self.discs.def_perc + self.wengine.def_perc)/100) + self.discs.defense
    
    def get_anomaly_prof(self):
        return (self.anomaly_prof + self.wengine.anomaly_prof + self.discs.anomaly_prof)
    
    def get_crit_rate(self):
        return (self.crit_rate + self.wengine.crit_rate + self.discs.crit_rate)/100

    def get_crit_dmg(self):
        return (self.crit_dmg + self.wengine.crit_dmg + self.discs.crit_dmg)/100

    def get_energy_regen(self):
        return self.energy_regen * (1 + (self.wengine.energy_perc + self.discs.energy_perc)/100)

    def get_anomaly_mastery(self):
        return self.anomaly_mastery * (1 + (self.wengine.anomaly_mastery + self.discs.anomaly_mastery)/100)

    def get_pen(self):
        return (self.pen + self.wengine.pen + self.discs.pen)/100

    def get_pen_flat(self):
        return self.wengine.pen_flat + self.discs.pen_flat

    def get_elec_dmg(self):
        return self.elec_dmg + self.wengine.elec_dmg + self.discs.elec_dmg

    def get_dmg_bonus(self):
        return self.dmg_bonus + self.wengine.dmg_bonus + self.discs.dmg_bonus

    def get_lvl_factor(self):
        return 0.1551 * self.lvl**2 + 3.141 * self.lvl + 47.2039
  
    def print_stats(self):
        print(f'HP = {self.get_hp():.0f}')
        print(f'ATK = {self.get_atk()*1.12:.0f}')
        print(f'DEF = {self.get_def():.0f}')
        print(f'impact = {self.impact:.0f}')
        print(f'CR = {self.get_crit_rate():.2f}')
        print(f'CD = {self.get_crit_dmg():.2f}')
        print(f'anomaly mastery = {self.get_anomaly_mastery():.0f}')
        print(f'anomaly proficient = {self.get_anomaly_prof():.0f}')
        print(f'PEN = {self.get_pen():.2f}')
        print(f'ER = {self.get_energy_regen():.2f}')
        print(f'PEN_FLAT = {self.get_pen_flat():.0f}')
        print(f'electric dmg = {self.get_elec_dmg():.2f}')