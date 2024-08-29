def getData(data,key):
    if key in data:
        return data[key]
    return 0

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
    energy_base = 0.0
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
    def __init__(self, data) -> None:
        super().__init__(data)

class WEngine(ModelBase):
    def __init__(self, data) -> None:
        super().__init__(data)

class Character(ModelBase):
    def __init__(self, data) -> None:
        super().__init__(data)

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
        return self.energy_base * (1 + (self.wengine.energy_regen + self.discs.energy_regen)/100)

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
  