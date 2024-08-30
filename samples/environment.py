from enemy import Enemy, EnemyType
from model_ZZZ import Character
from services_hoyolab import ServiceCharacter

URL_PIPER_DATA = 'Piper_data.json'

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
    serviceCharacter = ServiceCharacter(URL_PIPER_DATA)

    #estruturar dados do personagem
    char = serviceCharacter.build_character()
    janedoe.equip_discs(char.discs)
    janedoe.equip_wengine(char.wengine)

    #carrega inimigo
    durahan = Enemy(EnemyType.DURAHAN, 70)

    # dmg1 = normal_hit(durahan, janedoe, janedoe.skill())

    #calcula o dano
    dmg = anomaly_hit(durahan, janedoe, Anomaly.ASSAULT)
    dmg_piper = anomaly_hit(durahan, char, Anomaly.ASSAULT)

    #output
    print(f'dmg: {dmg:.2f}')
    print(f'dmg: {dmg_piper:.2f}')