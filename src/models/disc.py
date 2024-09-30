from dataclasses import dataclass, field
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
    sets_buffs = []
    discs: list[Disc] = field(default_factory=list)

    def sum_stats(self) -> StatsBase:
        total_stats = StatsBase()
        for disc in self.discs:
            total_stats.incr_attr(disc.main_stats.id, disc.main_stats.value)
            for stat in disc.substats:
                total_stats.incr_attr(stat.id, stat.value)

        return total_stats
