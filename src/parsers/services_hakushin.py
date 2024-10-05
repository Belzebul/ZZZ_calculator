import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from consts import CHAR_LIST_CODES, AnomalyType, AttributeID
from models.character import Character, Hit, Multiplier, Skill, SkillDesc, SubSkill
from models.stats_base import StatsBase



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
    char_base = Character()
    char_raw:dict = field(default_factory=dict)

    def build(self) -> Character:
        self.char_base = Character()
        services_hakushin = ServicesHakushin()
        self.char_raw = services_hakushin.load_char_json(self.name)
        self.__set_stats_base()
        self.__build_skills()

        return self.char_base

    def __set_stats_base(self) -> None:
        base:StatsBase = StatsBase()
        base.lvl = self.char_lvl
        base.atk = self.__calc_stat_growth(base.lvl, "Attack", "AttackGrowth")
        base.defense = self.__calc_stat_growth(base.lvl, "Defence", "DefenceGrowth")
        base.hp = self.__calc_stat_growth(base.lvl, "HpMax", "HpGrowth")
        base.anomaly_mastery = self.char_raw["Stats"]["ElementAbnormalPower"]
        base.anomaly_prof = self.char_raw["Stats"]["ElementMystery"]
        base.crit_rate = self.char_raw["Stats"]["Crit"] / 100
        base.crit_dmg = self.char_raw["Stats"]["CritDamage"] / 100
        base.impact = self.char_raw["Stats"]["BreakStun"]
        base.energy_regen = self.char_raw["Stats"]["SpRecover"] / 100
        base.pen_p = self.char_raw["Stats"]["PenRate"] / 100
        self.char_base.base = base

    def __calc_stat_growth(self, lvl:int, name_tag:str, growth_tag:str) -> int:
        stat_base = self.char_raw["Stats"][name_tag]
        stat_growth = self.char_raw["Stats"][growth_tag] / 10000
        lvl_range = self.__get_lvl_range(lvl)
        ascension_bonus:int = self.char_raw["Level"][lvl_range][name_tag]
        return int(stat_base + (lvl - 1) * stat_growth + ascension_bonus)

    def __build_skills(self) -> None:
        anomaly_type = int(list(self.char_raw["ElementType"])[0])
        self.char_base.basic = self.__build_skill(self.basic_lvl, "Basic", AnomalyType.PHYSICAL)
        self.char_base.dodge = self.__build_skill(self.dodge_lvl, "Dodge", anomaly_type)
        self.char_base.assist = self.__build_skill(self.assist_lvl, "Assist", anomaly_type)
        self.char_base.special = self.__build_skill(self.special_lvl, "Special", anomaly_type)
        self.char_base.chain = self.__build_skill(self.chain_lvl, "Chain", anomaly_type)
        self.char_base.core = Skill(self.core_lvl)
        self.__set_core_stats_base(self.core_lvl)

    def __build_skill(self, lvl:int, skill_code:str, anomaly_type:int) -> Skill:
        sub_skills_list: list = self.char_raw["Skill"][skill_code]["Description"]
        skill = Skill(lvl)
        skill.sub_skills = []
        for skill_raw in sub_skills_list:
            if "Desc" in skill_raw:
                skill.description.append(SkillDesc(skill_raw["Name"], skill_raw["Desc"]))

            if "Param" in skill_raw:
                #skill.name = skill_raw["Name"]
                skill = self.__build_sub_skills(skill, skill_raw["Param"],anomaly_type)

        return skill

    def __build_sub_skills(self, skill:Skill, sub_skills_raw:dict, anomaly_type:int) -> Skill:
        sub_skills_aux:list[SubSkill] = []
        sub_skills_final:list[SubSkill] = []
        for multipliers_raw in sub_skills_raw:
            sub_skill = SubSkill(skill.lvl)
            mult_aux = self.__build_multiplier(multipliers_raw)
            if isinstance(mult_aux, Multiplier):
                mult_aux.calc_mult(skill.lvl)
                mult_or_subskill = self.__find_multplier_id(sub_skills_aux, mult_aux)

                if isinstance(mult_or_subskill, SubSkill):
                    sub_skills_final.append(mult_or_subskill)
                else:
                    sub_skill.hits = [Hit(1, anomaly_type)] #hardcoded
                    sub_skill.dmg = mult_aux
                    sub_skills_aux.append(sub_skill)

        skill.sub_skills += sub_skills_final
        return skill

    def __find_multplier_id(self,
        sub_skills_aux:list[SubSkill],
        mult_aux:Multiplier
    ) -> SubSkill | Multiplier:
        for sub_skill in sub_skills_aux:
            if sub_skill.dmg.param_id[0] == mult_aux.param_id[0]:
                sub_skill.daze = mult_aux
                return sub_skill

        return mult_aux

    def __build_multiplier(self, sub_skills_raw) -> Multiplier | SkillDesc:
        if "Param" not in sub_skills_raw:
            return SkillDesc(sub_skills_raw["Name"], sub_skills_raw["Desc"])

        base:list[float] = []
        growth:list[float] = []
        param_id:list[str] = []

        for key, param in sub_skills_raw["Param"].items():
            base.append(param["Main"] / 100)
            growth.append(param["Growth"] / 100)
            param_id.append(key)

        mult = Multiplier(param_id, sub_skills_raw["Name"], sub_skills_raw["Desc"], base, growth)
        return mult

    def __set_core_stats_base(self, lvl:int) -> None:
        core_stats = self.char_raw["ExtraLevel"][str(lvl+1)]["Extra"]
        for stat in core_stats.values():
            match stat["Prop"]:
                case (AttributeID.CRIT_RATE_BASE
                    | AttributeID.CRIT_DMG_BASE
                    | AttributeID.ENERGY_RATE):
                    stat["Value"] = stat["Value"]/100

            self.char_base.base.incr_attr(stat["Prop"], stat["Value"])

    def __get_lvl_range(self, lvl) -> str:
        return str(math.ceil(lvl / 10))


class ServicesHakushin:
    def __init__(self) -> None:
        self.char_base_stats = {}
        self.directory = (
            Path(__file__).parent.parent.parent.resolve() / "character_database"
        )

    def load_all_characters(self):
        for char_name in CHAR_LIST_CODES:
            char_data = self.load_char_json(char_name)
            self.char_base_stats[char_name] = char_data

    def load_char_json(self, name_char):
        url = self.directory / f"{name_char}.json"
        with open(url, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        return raw_data


if __name__ == "__main__":
    characterBuilder = CharacterBuilder("Grace", 60, 12, 12, 12, 12, 12, 7)
    character = characterBuilder.build()
    character.print_stats()
