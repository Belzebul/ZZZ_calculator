import json
import math
from pathlib import Path
import re
import consts
from consts import AnomalyType
from models import SubSkill, Character, Hit, Multiplier, Skill

class CharacterBuilder():
    def __init__(self, name, char_lvl:int, skills_lvl:tuple) -> None:
        '''skills lvl order: basic, special, dodge, chain, core, assist'''
        self.char = Character()        
        servicesHakushin = ServicesHakushin()
        self.char_base_dict = servicesHakushin.load_char_json(name)
        self.set_stats_base(char_lvl)
        anomalyType = int(list(self.char_base_dict['ElementType'].keys())[0])
        self.char.basic = self.set_skill(skills_lvl[0],'Basic', AnomalyType.PHYSICAL)
        self.char.dodge = self.set_skill(skills_lvl[2],'Dodge', anomalyType)
        self.char.assist = self.set_skill(skills_lvl[5],'Assist', anomalyType)
        self.char.special = self.set_skill(skills_lvl[1],'Special', anomalyType)
        self.char.chain = self.set_skill(skills_lvl[3],'Chain', anomalyType)
        self.char.core = Skill(skills_lvl[4])
        self.set_core_stats_base(skills_lvl[4])

    def build(self):
        return self.char

    def set_stats_base(self, lvl):
        self.char.lvl = lvl
        self.char.atk = self.find_stat_base(lvl,'Attack','AttackGrowth')
        self.char.defense = self.find_stat_base(lvl,'Defence','DefenceGrowth')
        self.char.hp = self.find_stat_base(lvl,'HpMax','HpGrowth')
        self.char.anomaly_mastery = self.char_base_dict['Stats']['ElementMystery']
        self.char.anomaly_prof = self.char_base_dict['Stats']['ElementAbnormalPower']
        self.char.crit_rate = self.char_base_dict['Stats']['Crit']/100
        self.char.crit_dmg = self.char_base_dict['Stats']['CritDamage']/100
        self.char.impact = self.char_base_dict['Stats']['BreakStun']
        self.char.energy_regen = self.char_base_dict['Stats']['SpRecover']/100
        self.char.pen = self.char_base_dict['Stats']['PenRate']/100

        return self

    def find_stat_base(self, lvl, stat_name, growth_name):
        stat_base = self.char_base_dict['Stats'][stat_name]
        stat_growth = self.char_base_dict['Stats'][growth_name]/10000
        lvl_range = self.get_lvl_range(lvl)
        ascension_bonus = self.char_base_dict['Level'][lvl_range][stat_name]
        return stat_base + (lvl-1) * stat_growth + ascension_bonus
    
    def set_skill(self, lvl, skill_code, anomalyType):
        skills_list:list = self.char_base_dict['Skill'][skill_code]['Description']
        skill = Skill(lvl)
        for skill_dict in skills_list:
            if 'Param' in skill_dict:
                skill = self.load_skill_mult(lvl, skill, skill_dict['Param'], anomalyType)
        
        return skill

    def load_skill_mult(self, lvl, skill, skill_dict, anomalyType):
        total_hits = int(len(skill_dict)/2)
        for index in range(total_hits):
            dmg = self.build_multiplier(skill_dict, index)
            daze = self.build_multiplier(skill_dict, index+total_hits)
            hits = Hit(1,anomalyType)
            subSkill = SubSkill(lvl, dmg, daze, hits)
            skill.subSkills.append(subSkill)

        return skill

    def build_multiplier(self, skill_dict, index):
        mult = self.find_multiplier(skill_dict[index]['Desc'])
        aux_dict:dict = skill_dict[index]['Param']
        param_dict = list(aux_dict.values())[0]
        base = param_dict['Main']/100
        growth = param_dict['Growth']/100
        mult = Multiplier(base, growth, mult)
        return mult
    
    def find_multiplier(self, desc):
        '''pattern pra pegar digitos depois de qqlr "}*"'''
        pattern = re.compile(r'\}\*(\d*)')
        matches = pattern.findall(desc)
        return int(matches[0]) if len(matches) != 0 else 1

    def set_core_stats_base(self, lvl):
        core_stats = self.char_base_dict['ExtraLevel'][str(lvl-1)]['Extra']
        for stat in core_stats.values():
            self.char.set_attr_from_id(stat['Prop'], stat['Value'])

    def get_lvl_range(self, lvl):
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
    characterBuilder = CharacterBuilder('Grace',60,(12,12,12,12,7,12))
    char = characterBuilder.build()
    char.print_stats()
    pass
    