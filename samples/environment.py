from enemy import Enemy, EnemyType
from model_ZZZ import Character
from services_hakushin import CharacterBuilder
from services_hoyolab import ServiceCharacter

URL_PIPER_DATA = 'hoyolab_data/Piper_data.json'
URL_GRACE_DATA = 'hoyolab_data/Grace_data.json'

janedoe = Character()
janedoe.lvl = 60
janedoe.hp_base = 7789
janedoe.atk_base = 881
janedoe.defense_base = 607
janedoe.impact = 86
janedoe.anomaly_mastery = 150
janedoe.anomaly_prof = 112
janedoe.energy_regen = 1.2

class Anomaly():
    BURN = 0.5
    SHOCK = 1.25
    CORRUPTION = 0.625
    SHATTER = 5.0
    ASSAULT = 7.13

def normal_hit(enemy:Enemy,char:Character, skill):
    '''dano de skills'''
    pass

def anomaly_hit(enemy:Enemy, char:Character, anomalyType:float):
    anomaly_base_DMG = anomalyType * char.get_atk()
    anomaly_prof_mult = char.get_anomaly_prof() / 100
    anomaly_lvl_mult = 1 + (1 / 59) * (char.lvl - 1)
    dmg_bonus_mult = 1 + (char.get_dmg_bonus() / 100)
    dmg = anomaly_base_DMG * anomaly_prof_mult * anomaly_lvl_mult * dmg_bonus_mult * enemy.get_defense(char) * enemy.RES_mult * enemy.DMG_TAKEN_MULT * enemy.STUN_MULT

    return dmg


if __name__ == '__main__':
    #importar dados do arquivo
    serviceCharacter = ServiceCharacter(URL_GRACE_DATA)
    serviceCharacter2 = ServiceCharacter(URL_PIPER_DATA)

    #estruturar dados do personagem
    char_grace = serviceCharacter.build_character()
    char_piper = serviceCharacter2.build_character()
    wengine = char_piper.wengine
    grace = CharacterBuilder('Grace',60, 5).build()
    grace.equip_discs(char_grace.discs)
    grace.equip_wengine(char_piper.wengine)

    #carrega inimigo
    durahan = Enemy(EnemyType.DURAHAN, 70)

    #output
    grace.print_stats()
    pass