from models import StatsBase, Character
from services_hakushin import CharacterBuilder
import json
import re

class DiscSetID():
    PUFFER_ELECTRO = 31100
    FREEDOM_BLUE = 31300
    SWING_JAZZ = 31600


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

        disc:StatsBase = serviceDiscs.build_discs_data()
        wengine:StatsBase = serviceWEngine.build_wengine_data()
        char = self.build_char_base_data()
        char.equip_discs(disc)
        char.equip_wengine(wengine)

        return char

    def build_char_base_data(self) -> Character:
        code = self.avatar_data['name_mi18n']
        lvl = self.avatar_data['level']
        skills = self.__getSkillsLvl(self.avatar_data['skills'])
        char = CharacterBuilder(code, lvl, basic_lvl=skills[0],special_lvl=skills[1],dodge_lvl=skills[2],chain_lvl=skills[3],core_lvl=skills[4],assist_lvl=skills[5]).build()
        
        return char
    
    def __getSkillsLvl(self, skills:dict):
        skillsList = []
        for skill in skills:
            skillsList.append(skill['level'])

        return skillsList


class ServiceWEngine():
    def __init__(self, json_data) -> None:
        self.equip_data = json_data

    def build_wengine_data(self) -> StatsBase:
        wEngine = StatsBase()
        main_stat = self.equip_data['main_properties'][0]['base']
        wEngine.atk = remove_perc(main_stat)

        second_stat = self.equip_data['properties'][0]
        attr = remove_perc(second_stat['base'])
        wEngine.set_attr_from_id(second_stat['property_id'], attr)

        return wEngine


class ServiceDiscs():
    def __init__(self,json_data) -> None:
        self.equip_data = json_data
    

    def build_discs_data(self) -> StatsBase:
        disc = StatsBase()
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

    def add_equip_set_stats(self, disc: StatsBase, sets):
        if sets.get(DiscSetID.FREEDOM_BLUE) == 2 or sets.get(DiscSetID.FREEDOM_BLUE) == 4:
            disc.anomaly_prof += 30
        if sets.get(DiscSetID.SWING_JAZZ) == 2:
            disc.energy_regen = 20
        if sets.get(DiscSetID.PUFFER_ELECTRO) == 2:
            disc.pen = 8

        return disc

if __name__ == '__main__':
    URL = 'hoyolab_data/Grace_data.json'
    serviceCharacter = ServiceCharacter(URL)
    char = serviceCharacter.build_character()
    print("")


#basic, special, dodge, chain, core, assist