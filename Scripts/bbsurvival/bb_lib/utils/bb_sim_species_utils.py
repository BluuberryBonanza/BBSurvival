"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from sims.sim_info import SimInfo
from sims.sim_info_types import SpeciesExtended


class BBSimSpeciesUtils:
    """Utilities for manipulating the Species of Sims."""
    @classmethod
    def is_human(cls, sim_info: SimInfo) -> bool:
        return cls.get_extended_species(sim_info) == SpeciesExtended.HUMAN

    @classmethod
    def is_large_dog(cls, sim_info: SimInfo) -> bool:
        return cls.get_extended_species(sim_info) == SpeciesExtended.DOG

    @classmethod
    def is_small_dog(cls, sim_info: SimInfo) -> bool:
        return cls.get_extended_species(sim_info) == SpeciesExtended.SMALLDOG

    @classmethod
    def is_horse(cls, sim_info: SimInfo) -> bool:
        return cls.get_extended_species(sim_info) == SpeciesExtended.HORSE

    @classmethod
    def is_fox(cls, sim_info: SimInfo) -> bool:
        return cls.get_extended_species(sim_info) == SpeciesExtended.FOX

    @classmethod
    def is_cat(cls, sim_info: SimInfo) -> bool:
        return cls.get_extended_species(sim_info) == SpeciesExtended.CAT

    @classmethod
    def get_extended_species(cls, sim_info: SimInfo) -> SpeciesExtended:
        return sim_info.extended_species
