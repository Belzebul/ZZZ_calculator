import json
from model_ZZZ import Character

CHAR_LIST_CODES = ['Corin', 'QingYi', 'Jane', 'Soukaku', 'Harumasa', 'Billy', 'Grace', 'Wise', 'Anby', 'Caesar', 'Belle', 'Nicole', 'Piper', 'Nekomata', 'Zhu Yuan', 'Lycaon', 'Lighter', 'Anton', 'Soldier 11', 'Miyabi', 'Ben', 'Rina', 'Avatar_Female_Size03_Pulchra_En', 'Lucy', 'Koleda', 'Yanagi', 'Seth', 'Burnice', 'Ellen']

class CharacterBuilder():
    def __init__(self, code, char_lvl, *skills_lvl) -> None:
        self.char = Character()

        servicesHakushin = ServicesHakushin()
        self.char_base_dict = servicesHakushin.char_base_stats[code]
        self.set_stats_base(char_lvl)

    def build(self):
        return self.char

    def set_stats_base(self, lvl):
        self.char.atk_base = self.find_stat_base(lvl,'Attack','AttackGrowth')
        self.char.def_base = self.find_stat_base(lvl,'Defence','DefenceGrowth')
        self.char.hp_base = self.find_stat_base(lvl,'HpMax','HpGrowth')
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

      for names in CHAR_LIST_CODES:
          url = f'character_database/{names}.json'
          char_data = self.load_json(url)
          self.char_base_stats[names] = char_data

    def load_json(self, json_url):
        with open(json_url, 'r', encoding="utf-8") as file:
            raw_data = json.load(file)

        return raw_data
    
if __name__ == '__main__':
    characterBuilder = CharacterBuilder('Grace',60,1)
    char = characterBuilder.build()
    pass
    