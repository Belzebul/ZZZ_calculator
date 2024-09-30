from condicional_buff import ConditionalStats
from consts import CharacterId, CharacterNames

from models.character import StatsBase
from parsers.services_hakushin import CharacterBuilder
from parsers.services_hoyolab import ServiceCharacter

# carrega a url do hoyolab
URL = "hoyolab_data/nico_data.json"
serviceCharacter = ServiceCharacter(URL)
ben_bigger = serviceCharacter.build_character(CharacterId.BEN) # escolhe o boneco especifico da data

# tropical rain stats
wengine = StatsBase()
wengine.atk = 595
wengine.anomaly_prof = 75

#cria uma burnice base
burrice = CharacterBuilder(CharacterNames.BURNICE,60,9,9,9,9,9,6).build()
burrice.equip_wengine(wengine)
burrice.equip_disc_set(ben_bigger.disc_sets)
#burrice.sum_discs = ben_bigger.sum_discs

#burrice.sum_discs.atk_perc += 10.0 # hormone punk set hardcoded
burrice.sum_discs.anomaly_prof += 30.0 # Chaos Jazz 
burrice.sum_discs.energy_perc += 20.0 # Swing Jazz

# adiciona os buffs condicionais na burrice
burrice_buffs = ConditionalStats()
burrice_buffs.char = burrice

#rainforest R5 10 stacks
burrice_buffs.conditional_buffs.atk_perc = 4.0 * 10

burrice_buffs.print_stats()
pass