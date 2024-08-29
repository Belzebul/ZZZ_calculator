from model_ZZZ import Character, Disc, WEngine, ModelBase
import json
import re

URL = 'Piper_data.json'


class DiscSetID():
    PUFFER_ELECTRO = 31100
    FREEDOM_BLUE = 31300
    SWING_JAZZ = 31600

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
        self.avatar_data = raw_data['data']['avatar_list'][0]

    def build_character(self):
        serviceDiscs = ServiceDiscs(self.avatar_data['equip'])
        serviceWEngine = ServiceWEngine(self.avatar_data['weapon'])

        disc:Disc = serviceDiscs.build_discs_data()
        wengine:WEngine = serviceWEngine.build_wengine_data()
        char =self.build_char_base_data()
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
        char = Character()
        char.lvl = int(self.avatar_data['level'])

        for prop in self.avatar_data['properties']:
            attr_base = remove_perc(prop['base'])
            attr_final =remove_perc(prop['final'])
            char.set_attr_from_id(int(prop['property_id']), attr_base, attr_final)
        
        return char


class ServiceWEngine():
    def __init__(self, json_data) -> None:
        self.equip_data = json_data

    def build_wengine_data(self) -> WEngine:
        wEngine = WEngine()
        main_stat = self.equip_data['main_properties'][0]['base']
        wEngine.atk_base = remove_perc(main_stat)

        second_stat = self.equip_data['properties'][0]
        attr = remove_perc(second_stat['base'])
        wEngine.set_attr_from_id(second_stat['property_id'], attr)

        return wEngine

class ServiceDiscs():
    def __init__(self,json_data) -> None:
        self.equip_data = json_data
    

    def build_discs_data(self) -> Disc:
        disc = Disc()
        equip_suit_list = []
        sets = {}
        for equip in self.equip_data:
            for attr_dict in equip['properties']:
                attr = remove_perc(attr_dict['base'])
                property_id = attr_dict['property_id']
                disc.set_attr_from_id(property_id, attr)

            main_prop = equip['main_properties'][0]
            attr = remove_perc(main_prop['base'])
            disc.set_attr_from_id(main_prop['property_id'], attr)
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

if __name__ == '__main__':
    serviceCharacter = ServiceCharacter(URL)
    char = serviceCharacter.build_character()
    print("")
