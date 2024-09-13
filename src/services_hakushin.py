from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import consts
from consts import AnomalyType
from character import SubSkill, Character, Hit, Multiplier, Skill

@dataclass(kw_only=False)
class CharacterBuilder():
    name:str
    char_lvl:int
    basic_lvl:int
    dodge_lvl:int
    assist_lvl:int
    special_lvl:int
    chain_lvl:int
    core_lvl:int

    def build(self):
        self.char = Character()        
        servicesHakushin = ServicesHakushin()
        self.char_base_dict = servicesHakushin.load_char_json(self.name)
        self.__set_stats_base(self.char_lvl)
        anomalyType = int(list(self.char_base_dict['ElementType'].keys())[0])
        self.char.basic = self.__set_skill(self.basic_lvl,'Basic', AnomalyType.PHYSICAL)
        self.char.dodge = self.__set_skill(self.dodge_lvl,'Dodge', anomalyType)
        self.char.assist = self.__set_skill(self.assist_lvl,'Assist', anomalyType)
        self.char.special = self.__set_skill(self.special_lvl,'Special', anomalyType)
        self.char.chain = self.__set_skill(self.chain_lvl,'Chain', anomalyType)
        self.char.core = Skill(self.core_lvl)
        self.__set_core_stats_base(self.core_lvl)

        return self.char

    def __set_stats_base(self, lvl):
        self.char.lvl = lvl
        self.char.base.atk = self.__find_stat_base(lvl,'Attack','AttackGrowth')
        self.char.base.defense = self.__find_stat_base(lvl,'Defence','DefenceGrowth')
        self.char.base.hp = self.__find_stat_base(lvl,'HpMax','HpGrowth')
        self.char.base.anomaly_mastery = self.char_base_dict['Stats']['ElementMystery']
        self.char.base.anomaly_prof = self.char_base_dict['Stats']['ElementAbnormalPower']
        self.char.base.crit_rate = self.char_base_dict['Stats']['Crit']/100
        self.char.base.crit_dmg = self.char_base_dict['Stats']['CritDamage']/100
        self.char.base.impact = self.char_base_dict['Stats']['BreakStun']
        self.char.base.energy_regen = self.char_base_dict['Stats']['SpRecover']/100
        self.char.base.pen = self.char_base_dict['Stats']['PenRate']/100

        return self

    def __find_stat_base(self, lvl, stat_name, growth_name):
        stat_base = self.char_base_dict['Stats'][stat_name]
        stat_growth = self.char_base_dict['Stats'][growth_name]/10000
        lvl_range = self.__get_lvl_range(lvl)
        ascension_bonus = self.char_base_dict['Level'][lvl_range][stat_name]
        return stat_base + (lvl-1) * stat_growth + ascension_bonus
    
    def __set_skill(self, lvl, skill_code, anomalyType):
        skills_list:list = self.char_base_dict['Skill'][skill_code]['Description']
        skill = Skill(lvl)
        for skill_dict in skills_list:
            if 'Param' in skill_dict:
                skill = self.__load_skill_mult(lvl, skill, skill_dict['Param'], anomalyType)
        
        return skill

    def __load_skill_mult(self, lvl, skill, skill_dict, anomalyType):
        total_hits = int(len(skill_dict)/2)
        for index in range(total_hits):
            name = skill_dict[index]['Name']
            dmg = self.__build_multiplier(skill_dict, index)
            daze = self.__build_multiplier(skill_dict, index+total_hits)
            hits = [Hit(1,anomalyType)]
            subSkill = SubSkill(name, lvl, dmg, daze, hits)
            skill.subSkills.append(subSkill)

        return skill

    def __build_multiplier(self, skill_dict, index):
        mult = self.__find_multiplier(skill_dict[index]['Desc'])
        aux_dict:dict = skill_dict[index]['Param']
        param_dict = list(aux_dict.values())[0]
        base = param_dict['Main']/100
        growth = param_dict['Growth']/100
        mult = Multiplier(base, growth, mult)
        return mult
    
    def __find_multiplier(self, desc):
        '''pattern pra pegar digitos depois de qqlr "}*"'''
        pattern = re.compile(r'\}\*(\d*)')
        matches = pattern.findall(desc)
        return int(matches[0]) if len(matches) != 0 else 1

    def __set_core_stats_base(self, lvl):
        core_stats = self.char_base_dict['ExtraLevel'][str(lvl-1)]['Extra']
        for stat in core_stats.values():
            self.char.base.set_attr(stat['Prop'], stat['Value'])

    def __get_lvl_range(self, lvl):
        return str(math.ceil(lvl/10))
    
class ServicesHakushin():
    def __init__(self) -> None:
      self.char_base_stats = {}
      self.directory = Path(__file__).parent.parent.resolve() / 'character_database'

    def load_all_characters(self):
        for char_name in consts.CHAR_LIST_CODES:
            char_data = self.load_char_json(char_name)
            self.char_base_stats[char_name] = char_data

    def load_char_json(self, name_char):
        url = self.directory / f'{name_char}.json'
        with open(url, 'r', encoding="utf-8") as file:
            raw_data = json.load(file)

        return raw_data
    
if __name__ == '__main__':
    characterBuilder = CharacterBuilder('Grace',60,12,12,12,12,12,7)
    char = characterBuilder.build()
    char.print_stats()
    pass
    