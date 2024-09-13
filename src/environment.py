from pathlib import Path
from enemy import Enemy, EnemyType
from models import SubSkill, Character
from consts import CharacterNames
from services_hoyolab import ServiceCharacter

URL_GRACE_DATA = 'hoyolab_data/Grace_data.json'

janedoe = Character()
janedoe.lvl = 60
janedoe.hp = 7789
janedoe.atk = 881
janedoe.defense = 607
janedoe.impact = 86
janedoe.anomaly_mastery = 150
janedoe.anomaly_prof = 112
janedoe.energy_regen = 1.2

def normal_hit(enemy:Enemy,char:Character, skill):
    '''dano de skills TODO'''
    pass

def anomaly_hit_dmg(enemy:Enemy, char:Character, anomaly_type_mult:float):
    anomaly_base_DMG = anomaly_type_mult * char.get_atk()
    anomaly_prof_mult = char.get_anomaly_prof() / 100
    anomaly_lvl_mult = 1 + (1 / 59) * (char.lvl - 1)
    dmg_bonus_mult = 1 + (char.get_bonus_mult(anomaly_type_mult) / 100)
    dmg = anomaly_base_DMG * anomaly_prof_mult * anomaly_lvl_mult * dmg_bonus_mult * enemy.get_defense(char) * enemy.RES_mult * enemy.DMG_TAKEN_MULT * enemy.STUN_MULT

    return dmg

def skill_hit_dmg(enemy:Enemy, char:Character, subSkill:SubSkill):
    base_dmg = subSkill.dmg.get_mult(subSkill.lvl) * char.get_atk()
    dmg_bonus_mult = char.get_bonus_mult(subSkill.hits[0].anomaly)
    crit_mult = 1 #+ (char.get_crit_rate()*char.get_crit_dmg())
    enemy_def = enemy.get_defense(char)
    dmg = base_dmg * dmg_bonus_mult * crit_mult * enemy_def * enemy.RES_mult * enemy.DMG_TAKEN_MULT * enemy.STUN_MULT

    return dmg

def get_hoyo_file(char_id:str):
    file_name = char_id + '_data.json'
    path = Path(__file__).parent.parent.resolve() / 'hoyolab_data' / file_name
    return path


if __name__ == '__main__':
    #casos de teste

    #importar dados do arquivo do meu "hoyolab conquistas"
    serviceCharacter = ServiceCharacter( get_hoyo_file(CharacterNames.GRACE))

    #estruturar dados do personagens
    grace = serviceCharacter.build_character()

    #carrega inimigo
    durahan = Enemy(EnemyType.DURAHAN, 70)

    #calcular dano de teste
    ELECTRO_DMG_BONUS = 1.3
    WENGINE_SKILL = 1.12
    dmg = [skill_hit_dmg(durahan, grace, subSkill)*WENGINE_SKILL for subSkill in grace.basic.subSkills]
    
    dmg3_1 = dmg[2] * 2/5
    dmg3_2 = dmg[2] * 3/5 * ELECTRO_DMG_BONUS

    dmg_special = skill_hit_dmg(durahan, grace, grace.special.subSkills[1])*WENGINE_SKILL

    grace.print_stats()
    print(f'dmg basic 1: 3 x {dmg[0]/3:.2f}')
    print(f'dmg basic 2: 3 x {dmg[1]/3:.2f}')
    print(f'dmg basic 3-1: 5 x {dmg3_1/5:.2f}')
    print(f'dmg basic 3-2: 2 x {dmg3_2/2:.2f}')
    print(f'dmg basic 4: 8 x {dmg[3]/8:.2f}')
    print(f'dmg basic rapidfire: 3 x {dmg[4]/3:.2f}')
    print(f'dmg ex: 6 x {dmg_special/6:.2f}')
    pass