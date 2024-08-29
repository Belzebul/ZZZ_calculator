from model_ZZZ import Character
class EnemyType():
    DURAHAN = 58

class Enemy():
    #enemy
    ENEMY_LVL = 60 # max scaling 60 # between 36 and 60
    RES_mult = 1 # durahan
    DMG_TAKEN_MULT = 1
    STUN_MULT = 1
    
    def __init__(self, enemy_type_def_base, enemy_lvl) -> None:
        self.enemy_lvl = enemy_lvl if enemy_lvl <= 60 else 60
        self.enemy_def_base = enemy_type_def_base

    def get_enemy_def_raw(self):
        return (0.1551 * self.enemy_lvl**2 + 3.141 * self.enemy_lvl + 47.2039) * 2 * self.enemy_def_base / 100

    def get_defense(self, char:Character):
        def_target = self.get_enemy_def_raw() * (1 - char.get_pen()/100) - char.get_pen_flat()
        def_target = def_target if def_target > 0 else 0
        return char.get_lvl_factor() / (def_target + char.get_lvl_factor())

if __name__ == '__main__':
    enemy = Enemy(70, EnemyType.DURAHAN)
    defense = enemy.get_enemy_def_raw()
    print(defense)
    print("")