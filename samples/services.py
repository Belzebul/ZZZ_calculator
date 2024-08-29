from model_ZZZ import Character, Disc, WEngine
import json
import re

URL = 'Piper_data.json'


class DiscSetID():
    PUFFER_ELECTRO = 31100
    FREEDOM_BLUE = 31300
    SWING_JAZZ = 31600

class AttributeID():
    PEN_FLAT = 23203
    PEN = 23103
    ATK_BASE = 12101
    ATK = 12102
    ATK_FLAT = 12103
    HP_FLAT = 11103
    HP = 11102
    ANOMALY_PROF = 31203
    ANOMALY_MAST = 31402
    CRIT_RATE = 20103
    CRIT_DMG = 21103
    DEF = 13102
    DEF_FLAT = 13103
    PHYS_DMG = 31503
    

def load_json(json_url):
        with open(json_url, 'r', encoding="utf-8") as file:
            raw_data = json.load(file)

        return raw_data

def remove_perc(attr_str):
        pattern = re.compile(r'[\d\.]*')
        attr = pattern.findall(attr_str)[0]
        return float(attr) if attr != '' else 0.0



class ServiceCharacter():
    def __init__(self, url):
        raw_data = load_json(url)
        self.equip_data = raw_data['data']['avatar_list'][0]
        self.atk_weapon_base = int(raw_data['data']['avatar_list'][0]['weapon']['main_properties'][0]['base'])

    def build_character(self):
        serviceDiscs = ServiceDiscs(self.equip_data['equip'])
        serviceWEngine = ServiceWEngine(self.equip_data['weapon'])

        disc:Disc = serviceDiscs.build_discs_data()
        wengine:WEngine = serviceWEngine.build_wengine_data()
        char:Character = self.build_char_base_data()
        char.equip_discs(disc)
        char.equip_wengine(wengine)
        char = self.fix_data(char)

        return char


    def fix_data(self, char: Character):
        char.atk_base -= char.wengine.atk_base
        char.anomaly_prof -= char.discs.anomaly_prof
        char.impact -= char.discs.impact

        return char

    def build_char_base_data(self) -> Character:
        char = Character({'LVL':60})

        for prop in self.equip_data['properties']:
            attr_base = remove_perc(prop['base'])
            attr_final =remove_perc(prop['final'])
            match prop['property_name']:
                case "HP": char.hp_base = attr_base
                case "ATK": char.atk_base = attr_base
                case "DEF": char.def_base = attr_base
                case "Impact": char.impact = attr_final
                case "CRIT Rate": char.crit_rate += attr_base
                case "CRIT DMG": char.crit_dmg += attr_base
                case "Anomaly Mastery": char.anomaly_mastery = attr_base
                case "Anomaly Proficiency": char.anomaly_prof = attr_final
                case "PEN Ratio": char.pen = attr_base  
                case "Energy Regen": char.energy_regen = attr_base
                case "PEN": char.pen = attr_base
                case "Physical DMG Bonus": char.dm = attr_base
        
        return char


class ServiceWEngine():
    def __init__(self, json_data) -> None:
        self.equip_data = json_data

    def build_wengine_data(self) -> WEngine:
        wEngine = WEngine({})
        main_stat = self.equip_data['main_properties'][0]['base']
        wEngine.atk_base = remove_perc(main_stat)

        second_stat = self.equip_data['properties'][0]
        attr = remove_perc(second_stat['base'])

        match second_stat['property_id']:
            case AttributeID.ANOMALY_MAST: wEngine.anomaly_mastery += attr
            case AttributeID.ANOMALY_PROF: wEngine.anomaly_prof += attr
            case AttributeID.ATK_BASE: wEngine.atk_base += attr
            case AttributeID.ATK: wEngine.atk += attr
            case AttributeID.CRIT_DMG: wEngine.crit_dmg += attr
            case AttributeID.CRIT_RATE: wEngine.crit_rate += attr
            case AttributeID.DEF: wEngine.defense += attr
            case AttributeID.DEF_FLAT: wEngine.defense_flat += attr
            case AttributeID.HP: wEngine.hp += attr
            case AttributeID.PEN: wEngine.pen += attr
            case AttributeID.PEN_FLAT: wEngine.pen_flat += attr
            case AttributeID.PHYS_DMG: wEngine.dmg_bonus += attr
        
        return wEngine

class ServiceDiscs():
    def __init__(self,json_data) -> None:
        self.equip_data = json_data
    

    def build_discs_data(self) -> Disc:
        disc = Disc({})
        equip_suit_list = []
        sets = {}
        for equip in self.equip_data:
            for attr in equip['properties']:
                disc = self.add_attribute(disc, attr)
            disc = self.add_attribute(disc, equip['main_properties'][0])
            equip_suit_list.append(equip["equip_suit"])

        for equip_suit in equip_suit_list:
            key = equip_suit['suit_id']
            sets[key] = equip_suit['own']

        disc = self.add_equip_set_stats(disc, sets)
        return disc

    def add_equip_set_stats(self, disc: Disc, sets):
        if sets.get(DiscSetID.FREEDOM_BLUE) == 2 or sets.get(DiscSetID.FREEDOM_BLUE) == 4:
            disc.anomaly_prof += 30
        if sets.get(DiscSetID.SWING_JAZZ) == 2:
            disc.energy_regen = 20
        if sets.get(DiscSetID.PUFFER_ELECTRO) == 2:
            disc.pen = 8

        return disc

    def add_attribute(self, disc: Disc, attr_dict):
        attr = remove_perc(attr_dict['base'])
        match attr_dict['property_id']:
            case AttributeID.ANOMALY_MAST: disc.anomaly_mastery += attr
            case AttributeID.ANOMALY_PROF: disc.anomaly_prof += attr
            case AttributeID.ATK: disc.atk += attr
            case AttributeID.ATK_FLAT: disc.atk_flat += attr
            case AttributeID.CRIT_DMG: disc.crit_dmg += attr
            case AttributeID.CRIT_RATE: disc.crit_rate += attr
            case AttributeID.DEF: disc.defense += attr
            case AttributeID.DEF_FLAT: disc.defense_flat += attr
            case AttributeID.HP_FLAT: disc.hp_flat += attr
            case AttributeID.HP: disc.hp += attr
            case AttributeID.PEN: disc.pen += attr
            case AttributeID.PEN_FLAT: disc.pen_flat += attr
            case AttributeID.PHYS_DMG: disc.dmg_bonus += attr

        return disc
    

    def get_equip_data(self, raw_data):
        # return self.equips_data
        pass


if __name__ == '__main__':
    serviceCharacter = ServiceCharacter(URL)
    char = serviceCharacter.build_character()
    print("")
