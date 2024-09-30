from ast import Mult
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

import consts
from consts import HOYO_MAP, AnomalyType, AttributeID
from models.character import Character, Hit, Multiplier, Skill, SubSkill


@dataclass(kw_only=False)
class CharacterBuilder:
    name: str
    char_lvl: int
    basic_lvl: int
    dodge_lvl: int
    assist_lvl: int
    special_lvl: int
    chain_lvl: int
    core_lvl: int

    def build(self):
        self.char = Character()
        services_hakushin = ServicesHakushin()
        self.char_base_dict = services_hakushin.load_char_json(self.name)
        self.__set_stats_base(self.char_lvl)
        anomaly_type = int(list(self.char_base_dict["ElementType"].keys())[0])
        self.char.basic = self.__set_skill(
            self.basic_lvl, "Basic", AnomalyType.PHYSICAL
        )
        self.char.dodge = self.__set_skill(self.dodge_lvl, "Dodge", anomaly_type)
        self.char.assist = self.__set_skill(self.assist_lvl, "Assist", anomaly_type)
        self.char.special = self.__set_skill(self.special_lvl, "Special", anomaly_type)
        self.char.chain = self.__set_skill(self.chain_lvl, "Chain", anomaly_type)
        self.char.core = Skill(self.core_lvl)
        self.__set_core_stats_base(self.core_lvl)

        return self.char

    def __set_stats_base(self, lvl):
        self.char.lvl = lvl
        self.char.base.atk = self.__find_stat_base(lvl, "Attack", "AttackGrowth")
        self.char.base.defense = self.__find_stat_base(lvl, "Defence", "DefenceGrowth")
        self.char.base.hp = self.__find_stat_base(lvl, "HpMax", "HpGrowth")
        self.char.base.anomaly_mastery = self.char_base_dict["Stats"]["ElementAbnormalPower"]
        self.char.base.anomaly_prof = self.char_base_dict["Stats"]["ElementMystery"]
        self.char.base.crit_rate = self.char_base_dict["Stats"]["Crit"] / 100
        self.char.base.crit_dmg = self.char_base_dict["Stats"]["CritDamage"] / 100
        self.char.base.impact = self.char_base_dict["Stats"]["BreakStun"]
        self.char.base.energy_regen = self.char_base_dict["Stats"]["SpRecover"] / 100
        self.char.base.pen_p = self.char_base_dict["Stats"]["PenRate"] / 100

    def __find_stat_base(self, lvl, stat_name, growth_name) -> int:
        stat_base = self.char_base_dict["Stats"][stat_name]
        stat_growth = self.char_base_dict["Stats"][growth_name] / 10000
        lvl_range = self.__get_lvl_range(lvl)
        ascension_bonus:int = self.char_base_dict["Level"][lvl_range][stat_name]
        return int(stat_base + (lvl - 1) * stat_growth + ascension_bonus)

    def __set_skill(self, lvl, skill_code, anomalyType):
        skills_list: list = self.char_base_dict["Skill"][skill_code]["Description"]
        skill = Skill(lvl)
        for skill_dict in skills_list:
            if "Param" in skill_dict:
                skill = self.__load_skill_mult(
                    lvl, skill, skill_dict["Param"], anomalyType
                )

        return skill

    def __load_skill_mult(self, lvl, skill, skill_dict, anomalyType):
        total_hits = int(len(skill_dict) / 2)
        for index in range(total_hits):
            name = skill_dict[index]["Name"]
            dmg = self.__build_multiplier(skill_dict, index)
            daze = self.__build_multiplier(skill_dict, index + total_hits)
            hits = [Hit(1, anomalyType)]
            subSkill = SubSkill(name, lvl, dmg, daze, hits)
            skill.sub_skills.append(subSkill)

        return skill

    def __build_multiplier(self, skill_dict, index) -> Multiplier:
        mult = self.__find_multiplier(skill_dict[index]["Desc"])
        if mult == 1:
            return Multiplier(0,0,1)
        
        aux_dict: dict = skill_dict[index]["Param"]
        param_dict = list(aux_dict.values())[0]
        base = param_dict["Main"] / 100
        growth = param_dict["Growth"] / 100
        mult = Multiplier(base, growth, mult)
        return mult

    def __find_multiplier(self, desc) -> int:
        '''pattern pra pegar digitos depois de qqlr "}*"'''
        pattern = re.compile(r"\}\*(\d*)")
        matches = pattern.findall(desc)
        return int(matches[0]) if len(matches) != 0 else 1

    def __set_core_stats_base(self, lvl) -> None:
        core_stats = self.char_base_dict["ExtraLevel"][str(lvl)]["Extra"]
        for stat in core_stats.values():
            match stat["Prop"]:
                case (AttributeID.CRIT_RATE_BASE
                    | AttributeID.CRIT_DMG_BASE
                    | AttributeID.ENERGY_RATE):
                    stat["Value"] = stat["Value"]/100

            self.char.base.incr_attr(stat["Prop"], stat["Value"])

    def __get_lvl_range(self, lvl) -> str:
        return str(math.ceil(lvl / 10))


class ServicesHakushin:
    def __init__(self) -> None:
        self.char_base_stats = {}
        self.directory = (
            Path(__file__).parent.parent.parent.resolve() / "character_database"
        )

    def load_all_characters(self):
        for char_name in consts.CHAR_LIST_CODES:
            char_data = self.load_char_json(char_name)
            self.char_base_stats[char_name] = char_data

    def load_char_json(self, name_char):
        url = self.directory / f"{name_char}.json"
        with open(url, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        return raw_data


if __name__ == "__main__":
    characterBuilder = CharacterBuilder("Grace", 60, 12, 12, 12, 12, 12, 7)
    char = characterBuilder.build()
    char.print_stats()
    pass
