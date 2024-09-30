import json
import re

from consts import CharacterId
from models import disc
from models.character import Character, StatsBase
from models.disc import Disc, DiscSet, Stat
from parsers.services_hakushin import CharacterBuilder


class DiscSetID:
    PUFFER_ELECTRO = 31100
    FREEDOM_BLUE = 31300
    SWING_JAZZ = 31600
    THUNDER_METAL = 32400


def load_json(json_url):
    with open(json_url, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return raw_data


def remove_perc(attr_str):
    pattern = re.compile(r"[\d\.]*")
    attr = pattern.findall(attr_str)[0]
    return float(attr) if attr != "" else 0.0


class ServiceCharacter:
    def __init__(self, url: str) -> None:
        self.avatars: list = load_json(url)

    def build_character(self, char_id):
        avatar = self.avatars[char_id][0]
        service_discs = ServiceDiscs(avatar["equip"])
        service_wengine = ServiceWEngine(avatar["weapon"])

        #discs: StatsBase = service_discs.build_discs_data()
        disc: DiscSet = service_discs.build_disc_set()
        wengine: StatsBase = service_wengine.build_wengine_data()
        char:Character = self.build_char_base_data(avatar)
        char.equip_disc_set(disc)
        #char.sum_discs = discs
        char.equip_wengine(wengine)

        return char

    def build_char_base_data(self, avatar) -> Character:
        code = avatar["name_mi18n"]
        lvl = avatar["level"]
        skills = self.__get_skill_lvl(avatar["skills"])
        char_aux = CharacterBuilder(
            code,
            lvl,
            basic_lvl=skills[0],
            special_lvl=skills[1],
            dodge_lvl=skills[2],
            chain_lvl=skills[3],
            core_lvl=skills[4],
            assist_lvl=skills[5],
        ).build()

        return char_aux

    def __get_skill_lvl(self, skills: dict):
        skills_list = []
        for skill in skills:
            skills_list.append(skill["level"])

        return skills_list


class ServiceWEngine:
    def __init__(self, json_data) -> None:
        self.equip_data = json_data

    def build_wengine_data(self) -> StatsBase:
        wengine = StatsBase()
        if self.equip_data is None:
            return wengine
        
        main_stat = self.equip_data["main_properties"][0]["base"]
        wengine.atk = remove_perc(main_stat)

        second_stat = self.equip_data["properties"][0]
        attr = remove_perc(second_stat["base"])
        wengine.incr_attr(second_stat["property_id"], attr)
        return wengine


class ServiceDiscs:
    def __init__(self, json_data) -> None:
        self.disc_set_json = json_data

    def build_disc_set(self) -> DiscSet:
        disc_set = DiscSet()
        for disc_json in self.disc_set_json:
            disc_set.discs.append(self.build_disc(disc_json))

        return disc_set


    def build_disc(self, disc_data:dict) -> Disc:
        disc = Disc()
        disc.lvl = disc_data["level"]
        disc.pos = disc_data["equipment_type"]
        main_prop = disc_data["main_properties"][0]
        disc.main_stats.id = main_prop["property_id"]
        disc.main_stats.value = remove_perc(main_prop["base"])

        for attr in disc_data["properties"]:
            stat = Stat()
            stat.id = attr["property_id"]
            stat.value = remove_perc(attr["base"])
            disc.substats.append(stat)

        return disc

    def build_discs_data(self) -> StatsBase:
        disc = StatsBase()
        equip_suit_list = []
        sets = {}
        for equip in self.disc_set_json:
            for attr_dict in equip["properties"]:
                attr = remove_perc(attr_dict["base"])
                disc.incr_attr(attr_dict["property_id"], attr)

            main_prop = equip["main_properties"][0]
            attr = remove_perc(main_prop["base"])
            disc.incr_attr(main_prop["property_id"], attr)
            equip_suit_list.append(equip["equip_suit"])

        for equip_suit in equip_suit_list:
            key = equip_suit["suit_id"]
            sets[key] = equip_suit["own"]

        disc = self.add_equip_set_stats(disc, sets)
        return disc

    def add_equip_set_stats(self, disc: StatsBase, sets) -> StatsBase:
        if (
            sets.get(DiscSetID.FREEDOM_BLUE) == 2
            or sets.get(DiscSetID.FREEDOM_BLUE) == 4
        ):
            disc.anomaly_prof += 30
        if sets.get(DiscSetID.SWING_JAZZ) == 2:
            disc.energy_perc += 20
        if sets.get(DiscSetID.PUFFER_ELECTRO) == 2:
            disc.pen_p += 8
        if (
            sets.get(DiscSetID.THUNDER_METAL) == 2
            or sets.get(DiscSetID.THUNDER_METAL) == 4
        ):
            disc.elec_bonus += 10
        return disc


if __name__ == "__main__":
    URL = "hoyolab_data/hoyolab_character.json"
    serviceCharacter = ServiceCharacter(URL)
    char = serviceCharacter.build_character(CharacterId.NEKOMATA)
    print("")


# basic, special, dodge, chain, core, assist
