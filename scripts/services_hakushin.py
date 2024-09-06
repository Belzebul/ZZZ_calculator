import json
from models import Character, Hit, Skill
import consts

class CharacterBuilder():
    def __init__(self, name, char_lvl:int, skills_lvl:tuple) -> None:
        '''skills lvl order: basic, special, dodge, chain, core, assist'''
        self.char = Character()
        
        servicesHakushin = ServicesHakushin()
        self.char_base_dict = servicesHakushin.char_base_stats[name]
        self.set_stats_base(char_lvl)
        self.char.basic = self.set_skill(skills_lvl[0],'Basic')
        self.char.dodge = self.set_skill(skills_lvl[2],'Dodge')
        self.char.assist = self.set_skill(skills_lvl[5],'Assist')
        self.char.special = self.set_skill(skills_lvl[1],'Special')
        self.char.chain = self.set_skill(skills_lvl[3],'Chain')
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
    
    def set_skill(self, lvl, skill_code):
        skills_list:list = self.char_base_dict['Skill'][skill_code]['Description']
        skill = Skill(lvl)
        for skill_dict in skills_list:
            if 'Param' in skill_dict:
                skill = self.load_skill_mult(skill, skill_dict['Param'], lvl)
        
        return skill

    def load_skill_mult(self, skill, skill_dict, lvl):
        total_hits = int(len(skill_dict)/2)
        for index in range(total_hits):
            mult_dmg = self.get_mult(lvl, skill_dict, index)
            mult_daze = self.get_mult(lvl, skill_dict, index+total_hits)
            skill.hits.append(Hit(mult_dmg,mult_daze))

        return skill

    def get_mult(self, lvl, skill_dict, index):
        aux_dict:dict = skill_dict[index]['Param']
        param_dict = list(aux_dict.values())[0]
        base = param_dict['Main']
        growth = param_dict['Growth']
        mult = base + (lvl - 1) * growth
        return mult/100



    def set_core_stats_base(self, lvl):
        core_stats = self.char_base_dict['ExtraLevel'][str(lvl-1)]['Extra']
        for stat in core_stats.values():
            self.char.set_attr_from_id(stat['Prop'], stat['Value'])


    def get_lvl_range(self, lvl):
        if lvl > 50: return '6'
        if lvl > 40: return '5'
        if lvl > 30: return '4'
        if lvl > 20: return '3'
        if lvl > 10: return '2'
        return '1'

class ServicesHakushin():

    def __init__(self) -> None:
      self.char_base_stats = {}

      for names in consts.CHAR_LIST_CODES:
          url = f'character_database/{names}.json'
          char_data = self.load_json(url)
          self.char_base_stats[names] = char_data

    def load_json(self, json_url):
        with open(json_url, 'r', encoding="utf-8") as file:
            raw_data = json.load(file)

        return raw_data
    
if __name__ == '__main__':
    characterBuilder = CharacterBuilder('Grace',60,12,12,12,12,12,6)
    char = characterBuilder.build()
    pass
    