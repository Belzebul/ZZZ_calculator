import json
import re

from consts import CharacterId
from models.character import Character, StatsBase
from models.disc import Disc, DiscSet, Stat
from parsers.services_hakushin import CharacterBuilder


def load_json(json_url:str) -> dict:
    with open(json_url, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return raw_data


def remove_perc(attr_str):
    pattern = re.compile(r"[\d\.]*")
    attr = pattern.findall(attr_str)[0]
    return float(attr) if attr != "" else 0.0


class ServiceCharacter:
    def __init__(self, url: str) -> None:
        self.avatars: dict = load_json(url)

    def build_character(self, char_id) -> Character:
        avatar = self.avatars[char_id][0]
        service_wengine = ServiceWEngine(avatar["weapon"])
        wengine: StatsBase = service_wengine.build_wengine_data()

        service_discs = ServiceDiscs(avatar["equip"])
        discs_set: DiscSet = service_discs.build_disc_set()

        character:Character = self.build_char_base_data(avatar)
        character.equip_disc_set(discs_set)
        character.equip_wengine(wengine)

        return character

    def build_char_base_data(self, avatar) -> Character:
        name_code = avatar["name_mi18n"]
        lvl = avatar["level"]
        skills = self.__get_skill_lvl(avatar["skills"])
        char_aux = CharacterBuilder(
            name_code,
            lvl,
            basic_lvl=skills[0],
            special_lvl=skills[1],
            dodge_lvl=skills[2],
            chain_lvl=skills[3],
            core_lvl=skills[4]-1,
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
        disc.equip_set = disc_data["equip_suit"]["suit_id"]
        main_prop = disc_data["main_properties"][0]
        disc.main_stats = Stat(
            main_prop["property_id"],
            remove_perc(main_prop["base"])
        )
        disc.substats = self.__build_substats(disc_data["properties"])

        return disc

    def __build_substats(self, json_substats) -> list[Stat]:
        substats:list[Stat] = []
        for attr in json_substats:
            stat = Stat(attr["property_id"], remove_perc(attr["base"]))
            substats.append(stat)

        return substats


if __name__ == "__main__":
    URL = "hoyolab_data/hoyolab_character.json"
    serviceCharacter = ServiceCharacter(URL)
    char = serviceCharacter.build_character(CharacterId.NEKOMATA)
    print("")


# basic, special, dodge, chain, core, assist
