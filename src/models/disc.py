from dataclasses import dataclass, field
from consts import HOYO_2P_DISCSET
from models.stats_base import StatsBase

@dataclass
class Stat:
    id: int = 0
    value: float = 0.0


@dataclass
class Disc:
    lvl: int = 15
    pos: int = 0
    equip_set: int = 0
    main_stats: Stat = field(default_factory=Stat)
    substats: list[Stat] = field(default_factory=list)


@dataclass
class DiscSet:
    disc_sets_count:dict[int,int] = field(default_factory=dict)
    discs: list[Disc] = field(default_factory=list)

    def sum_stats(self) -> StatsBase:
        total_stats = StatsBase()
        self.__reset_disc_sets_count()

        for disc in self.discs:
            total_stats.incr_attr(disc.main_stats.id, disc.main_stats.value)
            self.disc_sets_count[disc.equip_set] += 1

            if self.disc_sets_count[disc.equip_set] == 2:
                buff_set = HOYO_2P_DISCSET[disc.equip_set]
                total_stats.incr_attr(buff_set[0], buff_set[1])

            for stat in disc.substats:
                total_stats.incr_attr(stat.id, stat.value)

        return total_stats

    def __reset_disc_sets_count(self) -> None:
        for key in HOYO_2P_DISCSET:
            self.disc_sets_count[key] = 0
