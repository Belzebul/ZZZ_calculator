from jane_doe import JaneDoe
from enemy import Enemy, EnemyType
from model_ZZZ import Character,Disc,WEngine
from services import ServiceCharacter

URL_PIPER_DATA = 'Piper_data.json'

JANE_DOE_DATA = {
    'LVL': 60,
    'HP_BASE': 7789,
    'DEF_BASE': 607,
    'ATK_BASE': 881,
    'IMPACT': 86,
    'ANOMALY_PROF': 112,
    'ANOMALY_MASTERY': 150,
    'ER':1.2
}

PIPER_DISCS_DATA = {
    'HP_FLAT': 2200 + 112 + 224,
    'HP': 6,
    'ATK_FLAT': 316 + 19,
    'ATK': 3 + 6 + 9 + 9,
    'CR': 7.2 + 7.2 + 2.4,
    'CD': 9.6,
    'DEF_FLAT': 184 + 45 + 15 + 45 + 30,
    'DEF': 4.8,
    'PEN_FLAT':27 + 18 + 18,
    'DMG_BONUS':30,
    'ANOMALY_PROF': 30 + 18 + 18 + 18 + 92 + 27,
    'ANOMALY_MASTERY': 30,
    'ER': 20
}

PIPER_WENGINE_DATA = {
    'ATK_BASE': 624,
    'ATK': 25
}

class Anomaly():
    BURN = 0.5
    SHOCK = 1.25
    CORRUPTION = 0.625
    SHATTER = 5.0
    ASSAULT = 7.13

def normal_hit(enemy:Enemy,char:Character, skill):
    '''dano'''
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
    janedoe = Character(JANE_DOE_DATA)

    #estruturar dados do personagem
    char = serviceCharacter.build_character()
    janedoe.equip_discs(char.discs)
    janedoe.equip_wengine(char.wengine)

    #carrega inimigo
    durahan = Enemy(EnemyType.DURAHAN, 70)

    # dmg1 = normal_hit(durahan, janedoe, janedoe.skill())

    #calcula o dano
    dmg = anomaly_hit(durahan, janedoe, Anomaly.ASSAULT)

    #output
    print(f'dmg: {dmg:.2f}')
